#!/usr/bin/env python3
"""从仓库内的公开源确定性地生成题库的说明页与索引。只读本仓库，不读私有目录、不读时钟、不联网。

每题目录 problems/<领域>/<题号>/ 里：
  源（可以直接改，改动走 PR）：problem.json、BACKGROUND.md、REFERENCE.md（有参照的题）、*.svg
  生成物（勿手改）：PROBLEM.md
另生成 problems/INDEX.md、problems/<领域>/INDEX.md 与 release/stats.json。

用法：
  python3 -I release/tools/build_problems.py           # 校验源并更新生成物，只写有变化的文件
  python3 -I release/tools/build_problems.py --check   # 只校验：源不合规或生成物过期时退出码为 1
改了一道题的源要把 problem.json 的 version 加 1，CI 会对照 PR 的基线检查（--base）。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DOMAINS = {
    "biomedicine": ("B", "生物医药"),
    "applied-materials": ("M", "应用材料"),
    "model-dynamics": ("F", "材料模型与动力学"),
    "extensions": ("C", "交叉方向与算法"),
}
STATEMENT = (
    ("system", "研究体系"),
    ("observable", "可观测量"),
    ("classical_baseline", "经典基线"),
    ("quantum_role", "量子方法的角色"),
    ("decision", "研发决策"),
)
REQUIRED = ("id", "version", "title", "domain", "subdomain", *(k for k, _ in STATEMENT), "track", "area", "has_reference")
LEVELS = ("热身", "进阶", "前沿")
BACKGROUNDS = ("量子化学", "凝聚态与动力学", "优化与算法")
SOURCE_FILES = ("problem.json", "BACKGROUND.md", "REFERENCE.md")
STATUS_LABEL = {"incomplete": "未完成（incomplete）"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)[^)]*\)")
HEADING_RE = re.compile(r"^(#{1,4}) ", re.MULTILINE)
FORBIDDEN = ("本地证据，未随题库发布",)
TO_ROOT = "../../.."
INPUT_LEAD = {
    "public": "解法默认使用下列输入，以便与现有参照和其他解法直接比较；改用其他输入时请说明理由。",
    "substitute": "原文输入没有完全公开。下表是参照运行实际使用的替代输入，解法可以沿用以便直接比较；"
    "取得原文输入或改用其他输入时请说明理由。",
    "self_build": "原文输入没有公开，也没有可直接运行的替代输入，解法需要自建模型并写明来源与哈希。"
    "下表只列出已知的公开材料。",
}


class SourceError(Exception):
    pass


def cell(text: object) -> str:
    return str(text or "").replace("|", "\\|").replace("\n", " ")


def dump_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def demote(text: str) -> str:
    """原案例说明并入「现有参照」节，标题整体降两级。"""
    return HEADING_RE.sub(lambda m: "#" * min(len(m.group(1)) + 2, 6) + " ", text)


def reference_input(case: dict) -> list[str]:
    spec = case.get("reference_input")
    if not spec:
        return [
            "本题尚未指定基准输入。请在「模型对应」中写明所用结构、参数或数据的来源与哈希；"
            "如能找到权威的公开输入，欢迎在 issue 中提出，采纳后写入后续版本。",
        ]
    rows = ["| 项目 | 内容 | 出处 |", "|---|---|---|"]
    for item in spec["items"]:
        where = f"[{item['origin']}]({item['url']})" if item.get("url") else item["origin"]
        rows.append(f"| {cell(item['label'])} | {cell(item['value'])} | {where} |")
    lead = INPUT_LEAD[spec.get("kind", "public")]
    lines = [lead + "「原文」指作者或原论文公开的材料，「参照」指本项目参照运行自行冻结的选择。", "", *rows]
    if spec.get("gaps"):
        lines += ["", f"**尚未公开或需注意：**{spec['gaps']}"]
    return lines


def acceptance(case: dict) -> list[str]:
    return [
        "一份解法满足以下五点即可提交审核。负结果同样接受，只要过程可复现、结论有依据。",
        "",
        f"1. **模型对应**：说明所用模型或数据如何对应「{case['system']}」，列出简化与近似。",
        f"2. **可观测量**：报告「{case['observable']}」，附单位与不确定度。",
        f"3. **经典对照**：在同一模型或数据上，与「{case['classical_baseline']}」中至少一种方法比较。",
        "4. **可复现**：提供代码、环境、随机种子、输入来源与哈希，以及计算资源和成本；用到 QPU 时注明设备与 shots。",
        f"5. **研发决策**：说明结果能否支撑「{case['decision']}」，以及还缺什么证据。",
        "",
        "本题的细化标准欢迎在 issue 中讨论；被采纳的讨论结论会写入后续版本。",
    ]


def start_here(case: dict, track: dict) -> list[str]:
    """热身题在题面之前给出入门入口：有 starter 的给命令，没有的邀请认领。"""
    if track["level"] != "热身":
        return []
    starter = track.get("starter")
    if starter is None:
        return [
            "## 从这里开始",
            "",
            "这是一道热身题：输入公开，笔记本能跑，参照里有可以直接对照的数字。它还没有 starter，"
            f"为它写一个本身就是一份很好的第一份贡献，做法见 [入门轨道]({TO_ROOT}/starters/README.md)。",
            "",
        ]
    return [
        "## 从这里开始",
        "",
        f"这是一道热身题。装好 [入门轨道]({TO_ROOT}/starters/README.md) 的环境后运行：",
        "",
        "```bash",
        f"python {starter['path']}/run.py",
        "```",
        "",
        f"{starter['runtime']}。复现的内容：{starter['reproduces']}。"
        f"脚本逐项对照参照数字并打印 ✓ 或 ✗；之后可以从 [{starter['path']}/README.md]({TO_ROOT}/{starter['path']}/README.md) 里的「下一步」挑一个方向往下做。",
        "",
    ]


def check_links(path: Path, root: Path) -> list[str]:
    """源 Markdown 里的相对链接必须指向仓库中存在的文件，不能指向未公开的东西。"""
    text = path.read_text(encoding="utf-8")
    errors = [f"{path.relative_to(root)}：含「{word}」，未公开的内容请直接删去或改写" for word in FORBIDDEN if word in text]
    for target in LINK_RE.findall(text):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        resolved = (path.parent / target.partition("#")[0]).resolve()
        if root.resolve() not in resolved.parents or not resolved.exists():
            errors.append(f"{path.relative_to(root)}：链接 {target} 指向的文件不存在")
    return errors


def load_case(pdir: Path, domain: str, prefix: str, root: Path) -> tuple[dict, list[str]]:
    errors: list[str] = []
    where = pdir.relative_to(root).as_posix()
    try:
        case = json.loads((pdir / "problem.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SourceError(f"{where}/problem.json 读不了：{exc}") from exc
    missing = [k for k in REQUIRED if case.get(k) in (None, "", [])]
    if missing:
        errors.append(f"{where}/problem.json 缺少或为空：{missing}")
    if case.get("id") != pdir.name or not pdir.name.startswith(prefix):
        errors.append(f"{where}/problem.json 的 id 应为目录名 {pdir.name}，且以 {prefix} 开头")
    if case.get("area") != domain:
        errors.append(f"{where}/problem.json 的 area 应为 {domain}")
    if not isinstance(case.get("version"), int) or isinstance(case.get("version"), bool) or case["version"] < 1:
        errors.append(f"{where}/problem.json 的 version 须为正整数")
    track = case.get("track") or {}
    if track.get("level") not in LEVELS or track.get("background") not in BACKGROUNDS:
        errors.append(f"{where}/problem.json 的 track 须含 level（{LEVELS}）与 background（{BACKGROUNDS}）")
    starter = track.get("starter")
    if starter and not (root / starter.get("path", "") / "run.py").is_file():
        errors.append(f"{where}/problem.json 的 track.starter.path 下没有 run.py")
    if case.get("has_reference") != (pdir / "REFERENCE.md").is_file():
        errors.append(f"{where}：has_reference 与 REFERENCE.md 是否存在不一致")
    if not (pdir / "BACKGROUND.md").is_file():
        errors.append(f"{where}：缺少 BACKGROUND.md")
    for name in ("BACKGROUND.md", "REFERENCE.md"):
        if (pdir / name).is_file():
            errors += check_links(pdir / name, root)
    return case, errors


def problem_md(case: dict, label: str, background: str, has_reference: bool) -> str:
    track = case["track"]
    statement = ["| 环节 | 内容 |", "|---|---|"] + [f"| {name} | {cell(case.get(key))} |" for key, name in STATEMENT]
    if not case["has_reference"]:
        status = ["本题暂无本项目的数值执行记录，下面只有文献整理。"]
    else:
        value = case.get("original_target_status")
        status = [
            "本项目已有数值执行记录（经典计算机上的计算与模拟），供对照与复用，不代表最优解。",
            "",
            f"- 原应用目标：{STATUS_LABEL.get(value, value) if value else '状态未记录'}",
        ]
        if has_reference:
            status.append("- 最新研究报告：[REFERENCE.md](REFERENCE.md)")
    lines = [
        "<!-- 由 release/tools/build_problems.py 自同目录的 problem.json 与 BACKGROUND.md 生成，勿手改；改题请改这两个文件 -->",
        "",
        f"# {case['id']} · {case['title']}",
        "",
        f"> 开放题 · {label} · {case.get('subdomain', '')} · 题面版本 v{case['version']}",
        f"> 难度：{track['level']}（[分级说明]({TO_ROOT}/starters/README.md#难度分级)） · 背景：{track['background']}",
        "",
        *start_here(case, track),
        "## 题面",
        "",
        *statement,
        "",
        "## 基准输入",
        "",
        *reference_input(case),
        "",
        "## 什么算解",
        "",
        *acceptance(case),
        "",
        "## 现有参照",
        "",
        *status,
        "",
        "### 原案例说明",
        "",
        demote(background).strip(),
        "",
        "## 如何提交",
        "",
        f"按 [CONTRIBUTING.md]({TO_ROOT}/CONTRIBUTING.md) 把解法放在 `solutions/{case['id']}/<你的名字>-<短名>/`，"
        f"格式见 [解法模板]({TO_ROOT}/solutions/_template/SOLUTION.md)。被采纳的解法会按 "
        f"[沉淀规则]({TO_ROOT}/skills/README.md) 提炼为可复用的 skill。",
    ]
    return "\n".join(lines) + "\n"


def domain_index(label: str, cases: list[dict]) -> str:
    out = [
        f"# {label} · 开放题",
        "",
        f"共 {len(cases)} 题。每题有题面、验收标准和现有参照；提交方式见 [CONTRIBUTING.md](../../CONTRIBUTING.md)。"
        "第一次参与建议从「热身」题开始，见 [入门轨道](../../starters/README.md)。",
        "",
        "| 题号 | 题目 | 难度 | 背景 | 子领域 | 现有参照 |",
        "|---|---|---|---|---|---|",
    ]
    for case in cases:
        if case["has_reference"]:
            value = case.get("original_target_status")
            ref = f"有执行记录；原应用目标{STATUS_LABEL.get(value, value) if value else '状态未记录'}"
        else:
            ref = "仅文献整理"
        track = case["track"]
        out.append(
            f"| [{case['id']}]({case['id']}/PROBLEM.md) | {cell(case['title'])} | {track['level']} | {track['background']} "
            f"| {cell(case.get('subdomain'))} | {ref} |"
        )
    return "\n".join(out) + "\n"


def render(root: Path) -> dict[Path, str]:
    """读全部公开源，返回 生成物路径 → 内容。源不合规时抛 SourceError，列出全部问题。"""
    problems = root / "problems"
    if not problems.is_dir():
        raise SourceError(f"找不到 {problems}")
    outputs: dict[Path, str] = {}
    errors: list[str] = []
    by_domain: dict[str, list[dict]] = {}
    for domain, (prefix, label) in DOMAINS.items():
        cases = []
        for pdir in sorted(p for p in (problems / domain).iterdir() if p.is_dir()) if (problems / domain).is_dir() else []:
            case, found = load_case(pdir, domain, prefix, root)
            errors += found
            if found:
                continue
            background = (pdir / "BACKGROUND.md").read_text(encoding="utf-8")
            outputs[pdir / "PROBLEM.md"] = problem_md(case, label, background, (pdir / "REFERENCE.md").is_file())
            cases.append(case)
        by_domain[domain] = cases
    stray = [p.name for p in problems.iterdir() if p.is_dir() and p.name not in DOMAINS]
    if stray:
        errors.append(f"problems/ 下有未知领域目录：{stray}")
    if errors:
        raise SourceError("\n".join(errors))

    every = [c for cases in by_domain.values() for c in cases]
    stats: dict = {"total_problems": len(every), "with_reference": 0, "levels": {}, "domains": {}}
    for case in every:
        level = case["track"]["level"]
        stats["levels"][level] = stats["levels"].get(level, 0) + 1
    overview = [
        "# 开放题总索引",
        "",
        f"{len(every)} 道量子计算与科学计算研究问题，分 4 个领域。提交方式见 [CONTRIBUTING.md](../CONTRIBUTING.md)。",
        "",
        "| 领域 | 目录 | 题数 | 有执行记录 |",
        "|---|---|---|---|",
    ]
    for domain, (_, label) in DOMAINS.items():
        cases = by_domain[domain]
        outputs[problems / domain / "INDEX.md"] = domain_index(label, cases)
        statuses: dict[str, int] = {}
        for case in cases:
            if case["has_reference"]:
                key = case.get("original_target_status") or "未记录"
                statuses[key] = statuses.get(key, 0) + 1
        with_ref = sum(c["has_reference"] for c in cases)
        stats["domains"][domain] = {"problems": len(cases), "with_reference": with_ref, "original_target_status": statuses}
        stats["with_reference"] += with_ref
        overview.append(f"| {label} | [{domain}]({domain}/INDEX.md) | {len(cases)} | {with_ref} |")
    overview += [
        "",
        "## 第一次参与：热身题",
        "",
        "难度分三级：热身、进阶、前沿（[分级说明](../starters/README.md#难度分级)）。"
        f"现有 {stats['levels'].get('热身', 0)} 道热身题，输入公开、笔记本能跑；带 starter 的题一条命令就能复现参照数字。",
        "",
        "| 题号 | 题目 | 背景 | starter |",
        "|---|---|---|---|",
    ]
    for case in sorted((c for c in every if c["track"]["level"] == "热身"), key=lambda c: c["id"]):
        t = case["track"]
        starter = f"[{t['starter']['path']}](../{t['starter']['path']}/README.md)" if "starter" in t else "欢迎认领"
        overview.append(f"| [{case['id']}]({case['area']}/{case['id']}/PROBLEM.md) | {cell(case['title'])} | {t['background']} | {starter} |")
    outputs[problems / "INDEX.md"] = "\n".join(overview) + "\n"
    outputs[root / "release" / "stats.json"] = dump_json(stats)
    return outputs


def stale_outputs(root: Path, outputs: dict[Path, str]) -> tuple[list[Path], list[Path]]:
    """返回（内容过期或缺失的生成物，没有对应源的多余 PROBLEM.md）。"""
    changed = [p for p, text in outputs.items() if not p.is_file() or p.read_text(encoding="utf-8") != text]
    orphans = [p for p in (root / "problems").glob("*/*/PROBLEM.md") if p not in outputs]
    return changed, orphans


def version_errors(root: Path, base: str) -> list[str]:
    """与基线提交相比，源有改动的题 version 必须变大；新题从 1 开始。"""
    out = subprocess.run(["git", "-C", str(root), "diff", "--name-only", base, "--", "problems"],
                         capture_output=True, text=True, check=True).stdout.split()
    touched = sorted({Path(p).parent for p in out if Path(p).name in SOURCE_FILES or p.endswith(".svg")})
    errors = []
    for pdir in touched:
        meta = root / pdir / "problem.json"
        if not meta.is_file():
            continue
        now = json.loads(meta.read_text(encoding="utf-8")).get("version")
        old = subprocess.run(["git", "-C", str(root), "show", f"{base}:{pdir.as_posix()}/problem.json"],
                             capture_output=True, text=True)
        before = json.loads(old.stdout).get("version") if old.returncode == 0 else 0
        if not isinstance(now, int) or now <= (before or 0):
            errors.append(f"{pdir.as_posix()} 的源有改动，problem.json 的 version 应从 {before} 加 1（现为 {now}）")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[2]), help="仓库根目录（测试用）")
    parser.add_argument("--check", action="store_true", help="只校验，不写文件")
    parser.add_argument("--base", help="对照这个提交检查改过的题是否升了 version（CI 用 PR 的基线）")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        outputs = render(root)
    except SourceError as exc:
        print(f"题库源不合规，未写任何文件：\n{exc}", file=sys.stderr)
        return 1
    errors = version_errors(root, args.base) if args.base else []
    changed, orphans = stale_outputs(root, outputs)
    if args.check:
        errors += [f"{p.relative_to(root)} 与源不同步，请运行 build_problems.py 并提交结果" for p in changed]
        errors += [f"{p.relative_to(root)} 没有对应的 problem.json" for p in orphans]
        for error in errors:
            print(error, file=sys.stderr)
        print("题库源合规，生成物与源一致。" if not errors else f"\n{len(errors)} 处问题。")
        return 1 if errors else 0
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    for path in changed:  # 全部渲染成功后才写，且只写有变化的文件
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(outputs[path], encoding="utf-8")
    for path in orphans:
        path.unlink()
    print(f"共 {len(outputs)} 个生成物，更新 {len(changed)} 个，删除 {len(orphans)} 个多余 PROBLEM.md。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
