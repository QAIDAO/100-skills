#!/usr/bin/env python3
"""从 tasks/ 的现有研究结果确定性地生成开放题库 problems/。

用法：python3 -I release/tools/build_problems.py --out <dir>
写出 <dir>/problems/... 与 <dir>/stats.json。只读源文件，不读时钟、不联网、不计算。
题面五段取自 tasks/catalog.json 原文；背景与参照取自源 README 和最新研究报告，
只做链接改写与本机路径脱敏，不改写结论。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASKS = ROOT / "tasks"

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
PROBLEM_FIELDS = (
    "id", "title", "domain", "subdomain", "system", "observable", "classical_baseline",
    "quantum_role", "decision", "scale", "tags", "sources",
)
MAX_SVG = 1_000_000
MAX_REPORT = 65_536
OMITTED = "本地证据，未随题库发布"
STATUS_LABEL = {"incomplete": "未完成（incomplete）"}
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)([^)]*)\)")
FOREIGN_PATH_RE = re.compile(r"/Users/[^\s)\]\"'`<>，。；]*")
HEADING_RE = re.compile(r"^(#{1,4}) ", re.MULTILINE)
TO_ROOT = "../../.."


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def scrub(text: str) -> str:
    """去掉本机绝对路径：仓内路径改为相对路径，仓外路径替换为占位。"""
    text = text.replace(f"{ROOT}/", "").replace(str(ROOT), ".")
    return FOREIGN_PATH_RE.sub("<本机路径>", text).replace("file://", "")


def scrub_json(value: object) -> object:
    return json.loads(scrub(json.dumps(value, ensure_ascii=False, sort_keys=True)))


def rewrite_links(text: str, base: Path, shipped: dict[Path, str], omitted: set[str]) -> str:
    """题目目录内有的文件改指向副本；嵌入的 png 有同名 svg 时改用 svg；其余本地链接降为纯文本。"""

    def replace(match: re.Match[str]) -> str:
        bang, label, target, _title = match.groups()
        if re.match(r"^(https?:|mailto:|#)", target):
            return match.group(0)
        path_part, _, fragment = target.partition("#")
        candidate = Path(path_part)
        resolved = candidate.resolve() if candidate.is_absolute() else (base / candidate).resolve()
        name = shipped.get(resolved)
        if name is None and bang and resolved.suffix.lower() == ".png":
            name = shipped.get(resolved.with_suffix(".svg"))
        if name is not None:
            return f"{bang}[{label}]({name}{'#' + fragment if fragment else ''})"
        try:
            omitted.add(rel(resolved))
        except ValueError:
            omitted.add("<仓外路径>")
        if bang:
            return f"（图：{label or resolved.name}，{OMITTED}）"
        return f"{label}（{OMITTED}）"

    return LINK_RE.sub(replace, text)


def demote(text: str) -> str:
    """原案例说明并入「现有参照」节，标题整体降两级。"""
    return HEADING_RE.sub(lambda m: "#" * min(len(m.group(1)) + 2, 6) + " ", text)


def cell(text: object) -> str:
    return str(text or "—").replace("|", "／").replace("\n", " ")


def dump_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


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


def build_problem(case: dict, domain: str, label: str, dest: Path) -> dict:
    src = TASKS / case["folder"]
    dest.mkdir(parents=True)
    sources = [src / "README.md"]
    omitted: set[str] = set()

    shipped: dict[Path, str] = {}
    for svg in sorted(src.glob("*.svg")):
        if svg.stat().st_size <= MAX_SVG:
            shutil.copyfile(svg, dest / svg.name)
            shipped[svg.resolve()] = svg.name
            sources.append(svg)

    latest_path = src / "execution" / "LATEST.json"
    latest = None
    reference = None
    if latest_path.is_file():
        sources.append(latest_path)
        raw = json.loads(latest_path.read_text(encoding="utf-8"))
        report = latest_path.parent / raw["research"] if isinstance(raw.get("research"), str) else None
        if report is not None and report.is_file() and report.stat().st_size <= MAX_REPORT:
            sources.append(report)
            reference = "REFERENCE.md"
            body = rewrite_links(report.read_text(encoding="utf-8"), report.parent, {}, omitted)
            header = (
                f"<!-- 由 release/tools/build_problems.py 自 {rel(report)} 生成，勿手改 -->\n\n"
                f"> {case['id']} 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。\n\n"
            )
            (dest / reference).write_text(header + scrub(body), encoding="utf-8")
        latest = {
            "original_target_status": raw.get("original_target_status"),
            "pointers": scrub_json(raw),
            "reference": reference,
        }

    statement = ["| 环节 | 内容 |", "|---|---|"] + [f"| {name} | {cell(case.get(key))} |" for key, name in STATEMENT]
    if latest is None:
        status = ["本题暂无本项目的数值执行记录，下面只有文献整理。"]
    else:
        value = latest["original_target_status"]
        status = [
            "本项目已有数值执行记录（经典计算机上的计算与模拟），供对照与复用，不代表最优解。",
            "",
            f"- 原应用目标：{STATUS_LABEL.get(value, value) if value else '状态未记录'}",
        ]
        if reference:
            status.append(f"- 最新研究报告：[{reference}]({reference})")
        status.append(f"- 其余证据指针见 evidence.json（{OMITTED}）")
    readme = rewrite_links((src / "README.md").read_text(encoding="utf-8"), src, shipped, omitted)
    lines = [
        f"<!-- 由 release/tools/build_problems.py 自 {rel(src / 'README.md')} 与 tasks/catalog.json 生成，勿手改 -->",
        "",
        f"# {case['id']} · {case['title']}",
        "",
        f"> 开放题 · {label} · {case.get('subdomain', '')}",
        "",
        "## 题面",
        "",
        *statement,
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
        demote(scrub(readme)).strip(),
        "",
        "## 如何提交",
        "",
        f"按 [CONTRIBUTING.md]({TO_ROOT}/CONTRIBUTING.md) 把解法放在 `solutions/{case['id']}/<你的名字>-<短名>/`，"
        f"格式见 [解法模板]({TO_ROOT}/solutions/_template/SOLUTION.md)。被采纳的解法会按 "
        f"[沉淀规则]({TO_ROOT}/skills/README.md) 提炼为可复用的 skill。",
    ]
    (dest / "PROBLEM.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    problem = {key: case.get(key) for key in PROBLEM_FIELDS}
    problem["area"] = domain
    problem["has_reference"] = latest is not None
    dump_json(dest / "problem.json", scrub_json(problem))
    dump_json(dest / "evidence.json", {
        "id": case["id"],
        "latest": latest,
        "sources": [{"path": rel(p), "sha256": sha256(p)} for p in [TASKS / "catalog.json", *sources]],
        "omitted": sorted(omitted),
    })
    return {"has_latest": latest is not None, "status": latest and latest["original_target_status"]}


def domain_index(label: str, rows: list[tuple[dict, dict]]) -> str:
    out = [
        f"# {label} · 开放题",
        "",
        f"共 {len(rows)} 题。每题有题面、验收标准和现有参照；提交方式见 [CONTRIBUTING.md](../../CONTRIBUTING.md)。",
        "",
        "| 题号 | 题目 | 子领域 | 现有参照 |",
        "|---|---|---|---|",
    ]
    for case, info in rows:
        if info["has_latest"]:
            value = info["status"]
            ref = f"有执行记录；原应用目标{STATUS_LABEL.get(value, value) if value else '状态未记录'}"
        else:
            ref = "仅文献整理"
        out.append(f"| [{case['id']}]({case['id']}/PROBLEM.md) | {cell(case['title'])} | {cell(case.get('subdomain'))} | {ref} |")
    return "\n".join(out) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    out = Path(parser.parse_args().out).resolve()
    problems_dir = out / "problems"
    if problems_dir.exists():
        shutil.rmtree(problems_dir)
    catalog = json.loads((TASKS / "catalog.json").read_text(encoding="utf-8"))

    stats: dict = {"total_problems": 0, "with_reference": 0, "domains": {}}
    overview = [
        "# 开放题总索引",
        "",
        "84 道量子计算与科学计算研究问题，分 4 个领域。提交方式见 [CONTRIBUTING.md](../CONTRIBUTING.md)。",
        "",
        "| 领域 | 目录 | 题数 | 有执行记录 |",
        "|---|---|---|---|",
    ]
    for domain, (prefix, label) in DOMAINS.items():
        cases = sorted((c for c in catalog if c["id"].startswith(prefix)), key=lambda c: c["id"])
        rows = [(c, build_problem(c, domain, label, problems_dir / domain / c["id"])) for c in cases]
        (problems_dir / domain / "INDEX.md").write_text(domain_index(label, rows), encoding="utf-8")
        statuses: dict[str, int] = {}
        for _, info in rows:
            if info["has_latest"]:
                key = info["status"] or "未记录"
                statuses[key] = statuses.get(key, 0) + 1
        with_ref = sum(info["has_latest"] for _, info in rows)
        stats["domains"][domain] = {"problems": len(rows), "with_reference": with_ref, "original_target_status": statuses}
        stats["total_problems"] += len(rows)
        stats["with_reference"] += with_ref
        overview.append(f"| {label} | [{domain}]({domain}/INDEX.md) | {len(rows)} | {with_ref} |")
    (problems_dir / "INDEX.md").write_text("\n".join(overview) + "\n", encoding="utf-8")
    dump_json(out / "stats.json", stats)


if __name__ == "__main__":
    main()
