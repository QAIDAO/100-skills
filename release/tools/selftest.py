#!/usr/bin/env python3
"""校验工具自身的回归测试：坏样例必须被拒绝，好样例必须通过。只用标准库，不跑科学计算。

用法：python3 -I release/tools/selftest.py
覆盖 check_submissions（证据完整性与审核状态）、starters/_common.check（必需指标）、
build_problems（只用公开文件重建、确定性、只改动相关文件、版本号）。全部通过时退出码为 0。
"""

from __future__ import annotations

import copy
import io
import json
import shutil
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "release" / "tools"))
sys.path.insert(0, str(ROOT / "starters"))
import check_submissions as cs  # noqa: E402
from _common import check  # noqa: E402

GOOD = ROOT / "solutions" / "B16" / "qaidao-vqe-shot-budget"
failures: list[str] = []


def expect(name: str, ok: bool) -> None:
    print(f"  {'✓' if ok else '✗'} {name}")
    if not ok:
        failures.append(name)


def solution_cases() -> None:
    print("check_submissions：")
    base = json.loads((GOOD / "solution.json").read_text(encoding="utf-8"))
    problems = cs.known_problems(ROOT)

    def errors(mutate) -> list[str]:
        data = copy.deepcopy(base)
        mutate(data)
        return cs.check_json(data, "B16", problems, ROOT)

    expect("现有 B16 示例通过", errors(lambda d: None) == [])
    expect("缺 inputs 被拒绝", bool(errors(lambda d: d["reproducibility"].pop("inputs"))))
    expect("输入哈希格式错被拒绝", bool(errors(lambda d: d["reproducibility"]["inputs"][0].update(sha256="abc"))))
    expect("缺 wall_time 被拒绝", bool(errors(lambda d: d["compute"].pop("wall_time"))))
    expect("缺 command 被拒绝", bool(errors(lambda d: d["reproducibility"].pop("command"))))
    expect("代码路径不存在被拒绝", bool(errors(lambda d: d["reproducibility"].update(code=["missing-file.py"]))))
    expect("无种子且无说明被拒绝", bool(errors(lambda d: d["reproducibility"].update(seeds=[]))))
    expect("无误差且无说明被拒绝", bool(errors(lambda d: d["reproducibility"].pop("uncertainty_note"))))
    expect("results.value 为 null 且无原因被拒绝", bool(errors(lambda d: d["results"][0].update(value=None))))
    expect("null 带 status 与 reason 可通过", errors(
        lambda d: d["results"].append({"observable": "x", "value": None, "unit": "Ha", "status": "not_evaluable", "reason": "大体系未运行"})
    ) == [])
    expect("基线 value 为对象被拒绝", bool(errors(lambda d: d["baseline_comparison"][0].update(value={"a": 1}))))
    expect("复数与向量可通过", errors(lambda d: d["results"].append({"observable": "z", "value": [{"re": 1.0, "im": -0.5}], "unit": "a.u."})) == [])
    expect("NaN 被拒绝", bool(errors(lambda d: d["results"][0].update(value=float("nan")))))
    expect("solution.json 自填审核状态被拒绝", bool(errors(lambda d: d.update(review_status="accepted"))))
    expect("旧 self_assessment 被拒绝", bool(errors(lambda d: d.update(self_assessment="pass"))))
    expect("文献类贡献可没有数值结果", errors(lambda d: d.update(contribution_type="literature", results=[], baseline_comparison=[])) == [])
    expect("复现类贡献不能没有结果", bool(errors(lambda d: d.update(results=[]))))

    authors = base["authors"]
    repro = {
        "reviewer": "bob", "kind": "reproduction", "date": "2026-11-03", "solution_commit": "d0540d2",
        "environment": "Python 3.12.13; numpy 1.26.4", "command": "python run.py",
        "results": [{"observable": "E", "tolerance": "1e-6 Ha", "within_tolerance": True}],
    }
    review = {"schema_version": 1, "status": "unreviewed", "application_status": "open", "accepted_claims": [], "reviews": []}
    expect("unreviewed 记录通过", cs.check_review(review, authors) == [])
    expect("无复现记录却标 independently_reproduced 被拒绝", bool(cs.check_review({**review, "status": "independently_reproduced"}, authors)))
    self_rep = {**repro, "reviewer": authors[0]}
    expect("作者自己复现不能升级状态", bool(cs.check_review({**review, "status": "independently_reproduced", "reviews": [self_rep]}, authors)))
    expect("非作者复现可升级为 independently_reproduced", cs.check_review({**review, "status": "independently_reproduced", "reviews": [repro]}, authors) == [])
    expect("accepted 缺 accepted_claims 被拒绝", bool(cs.check_review({**review, "status": "accepted", "reviews": [repro]}, authors)))
    expect("未采纳时不能标原题完成", bool(cs.check_review({**review, "status": "reviewed", "application_status": "completed",
                                                    "reviews": [{**repro, "kind": "format"}]}, authors)))


def starter_cases() -> None:
    print("starters/_common.check：")
    path = ROOT / "starters" / "B16" / "expected.json"
    values = {k: v["value"] for k, v in json.loads(path.read_text(encoding="utf-8"))["values"].items()}
    quick = {k: values[k] for k in ("E_CAS2[H2O]", "E_CAS2[5]", "E_VQE[H2O]", "E_VQE[5]")}

    def run(results: dict, profile: str = "quick") -> bool:
        with redirect_stdout(io.StringIO()):
            return check(results, path, profile)

    expect("空结果失败", not run({}))
    expect("quick 四项齐全通过", run(quick))
    expect("缺一项必需指标失败", not run({k: v for k, v in quick.items() if k != "E_VQE[5]"}))
    expect("NaN 失败", not run({**quick, "E_VQE[5]": float("nan")}))
    expect("Infinity 失败", not run({**quick, "E_VQE[5]": float("inf")}))
    expect("超差失败", not run({**quick, "E_VQE[5]": quick["E_VQE[5]"] + 1e-5}))
    expect("full 模式缺额外指标失败", not run(quick, "full"))
    expect("full 模式齐全通过", run(values, "full"))


def build_cases() -> None:
    print("build_problems：")
    with tempfile.TemporaryDirectory() as tmp:
        # 只复制公开仓库里的东西：题库、生成器与 starter；没有任何私有目录
        fake = Path(tmp)
        shutil.copytree(ROOT / "problems", fake / "problems")
        shutil.copytree(ROOT / "starters", fake / "starters", ignore=shutil.ignore_patterns(".cache"))
        (fake / "release" / "tools").mkdir(parents=True)
        shutil.copy(ROOT / "release" / "stats.json", fake / "release")
        tool = fake / "release" / "tools" / "build_problems.py"
        shutil.copy(ROOT / "release" / "tools" / "build_problems.py", tool)

        def build(*extra: str) -> int:
            return subprocess.run([sys.executable, "-I", str(tool), "--root", str(fake), *extra],
                                  capture_output=True, cwd=fake).returncode

        def snapshot() -> dict[str, bytes]:
            return {p.relative_to(fake).as_posix(): p.read_bytes() for p in fake.rglob("*") if p.is_file() and ".git" not in p.parts}

        expect("仅凭公开文件即可重建且与已提交生成物一致", build("--check") == 0)
        before = snapshot()
        build()
        build()
        expect("连续两次构建结果逐字节一致", snapshot() == before)

        bg = fake / "problems" / "biomedicine" / "B16" / "BACKGROUND.md"
        bg.write_text(bg.read_text(encoding="utf-8") + "\n补充一句背景。\n", encoding="utf-8")
        build()
        after = snapshot()
        changed = sorted(k for k in after if after[k] != before.get(k))
        expect("改一道题只改该题源与它的 PROBLEM.md",
               changed == ["problems/biomedicine/B16/BACKGROUND.md", "problems/biomedicine/B16/PROBLEM.md"])

        meta = fake / "problems" / "biomedicine" / "B14" / "problem.json"
        good = meta.read_text(encoding="utf-8")
        data = json.loads(good)
        data.pop("system")
        meta.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        frozen = snapshot()
        expect("源不合规时非零退出", build() != 0)
        expect("源不合规时不写任何生成物", snapshot() == frozen)
        meta.write_text(good, encoding="utf-8")

        bg14 = fake / "problems" / "biomedicine" / "B14" / "BACKGROUND.md"
        original = bg14.read_text(encoding="utf-8")
        bg14.write_text(original + "\n见 [原始结果](results/raw.json)。\n", encoding="utf-8")
        expect("指向不存在文件的链接被拒绝", build("--check") != 0)
        bg14.write_text(original, encoding="utf-8")

        git = ["git", "-C", str(fake), "-c", "user.name=t", "-c", "user.email=t@example.com"]
        subprocess.run([*git, "init", "-q"], check=True)
        subprocess.run([*git, "add", "-A"], check=True)
        subprocess.run([*git, "commit", "-qm", "base"], check=True)
        bg14.write_text(original + "\n改了一句。\n", encoding="utf-8")
        build()
        expect("改了源却没升 version 被拒绝", build("--check", "--base", "HEAD") != 0)
        data = json.loads(good)
        data["version"] += 1
        meta.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        build()
        expect("升 version 后通过", build("--check", "--base", "HEAD") == 0)


def main() -> int:
    solution_cases()
    starter_cases()
    build_cases()
    if failures:
        print(f"\n{len(failures)} 项失败：{failures}")
        return 1
    print("\n全部通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
