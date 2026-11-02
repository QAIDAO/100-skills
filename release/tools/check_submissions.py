"""校验 solutions/ 下的解法提交：结构、类型与证据完整性。不运行任何计算。

用法：python3 -I release/tools/check_submissions.py --root <仓库根>
全部合规时退出码为 0；否则逐条列出错误，退出码为 1。

通过只说明元数据齐全、类型正确、本地代码路径存在；不说明科学结论成立，
也不说明已经被独立复现。审核与采纳状态记在各解法的 review.json 里。
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

SCHEMA_VERSION = 2
SECTIONS = ("## 方法", "## 结果", "## 经典对照", "## 复现", "## 局限")
LICENSES = {"Apache-2.0", "MIT", "BSD-3-Clause"}
CONTRIBUTIONS = {
    "reproduction", "baseline", "method-comparison", "failure-analysis",
    "hardware-validation", "input-curation", "literature",
}
NON_NUMERIC = {"input-curation", "literature"}  # 这两类可以没有数值结果，不必为模板编数字
CONCLUSIONS = {"supported", "refuted", "inconclusive", "not_applicable"}
MILESTONES = {"completed", "partial", "not_completed"}
MISSING_STATUS = {"not_evaluable", "skipped"}
REVIEW_STATUSES = {"unreviewed", "needs_changes", "reviewed", "independently_reproduced", "accepted"}
REVIEW_KINDS = {"format", "evidence", "reproduction", "scientific"}
APPLICATION = {"open", "completed"}
MAX_FILE = 5_000_000
PLACEHOLDER_RE = re.compile(r"<[^<>\n]{1,60}>")
DIR_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*-[A-Za-z0-9_.-]+$")
COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SKIP = {"_template", "README.md", ".DS_Store"}


def known_problems(root: Path) -> set[str]:
    problems = root / "problems"
    if not problems.is_dir():
        return set()
    return {p.name for domain in problems.iterdir() if domain.is_dir() for p in domain.iterdir() if p.is_dir()}


def non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def strings(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def finite(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def typed_value(value: object) -> bool:
    """实数、复数 {"re","im"}，或由它们组成的非空（可嵌套）列表，用于向量、谱和表格。"""
    if finite(value):
        return True
    if isinstance(value, dict):
        return set(value) == {"re", "im"} and finite(value["re"]) and finite(value["im"])
    if isinstance(value, list):
        return bool(value) and all(typed_value(v) for v in value)
    return False


def check_values(items: object, field: str, label_key: str, need_unit: bool) -> tuple[list[str], int]:
    """返回错误与带数值的条目数。value 为 null 时须给 status 与 reason。"""
    errors, numeric = [], 0
    for i, item in enumerate(items):
        where = f"{field}[{i}]"
        if not isinstance(item, dict) or not non_empty_str(item.get(label_key)):
            errors.append(f"{where} 须包含非空的 {label_key}")
            continue
        if need_unit and not non_empty_str(item.get("unit")):
            errors.append(f"{where} 须包含非空的 unit")
        if "value" not in item:
            errors.append(f"{where} 缺少 value")
        elif item["value"] is None:
            if item.get("status") not in MISSING_STATUS or not non_empty_str(item.get("reason")):
                errors.append(f"{where}.value 为 null 时须给 status（{sorted(MISSING_STATUS)}）与 reason")
        elif not typed_value(item["value"]):
            errors.append(f"{where}.value 须为有限实数、{{re, im}} 复数或它们的列表")
        else:
            numeric += 1
            if "uncertainty" in item and not typed_value(item["uncertainty"]):
                errors.append(f"{where}.uncertainty 须为有限数值或数值列表")
    return errors, numeric


def check_code(code: object, root: Path) -> list[str]:
    """code 是列表：仓库内相对路径（必须存在），或 {"repository": URL, "commit": 哈希}。"""
    if not isinstance(code, list) or not code:
        return ["reproducibility.code 须为非空列表（仓库内路径，或 {repository, commit}）"]
    errors = []
    for i, entry in enumerate(code):
        where = f"reproducibility.code[{i}]"
        if isinstance(entry, dict):
            if not non_empty_str(entry.get("repository")) or not COMMIT_RE.match(str(entry.get("commit", ""))):
                errors.append(f"{where} 外部代码须给 repository 与 7–40 位小写十六进制 commit")
        elif not non_empty_str(entry):
            errors.append(f"{where} 不能为空")
        elif "://" in entry or entry.startswith("/") or ".." in Path(entry).parts:
            errors.append(f"{where} 须为仓库内相对路径；外部代码用 {{repository, commit}}")
        elif not (root / entry).exists():
            errors.append(f"{where} 指向的 {entry} 不存在")
    return errors


def check_inputs(inputs: object) -> list[str]:
    if not isinstance(inputs, list) or not inputs:
        return ["reproducibility.inputs 须为非空列表；每项给 name，以及 sha256 或 git_commit"]
    errors = []
    for i, item in enumerate(inputs):
        where = f"reproducibility.inputs[{i}]"
        if not isinstance(item, dict) or not non_empty_str(item.get("name")):
            errors.append(f"{where} 须包含非空的 name")
        elif "sha256" in item:
            if not SHA256_RE.match(str(item["sha256"])):
                errors.append(f"{where}.sha256 须为 64 位小写十六进制")
        elif not COMMIT_RE.match(str(item.get("git_commit", ""))):
            errors.append(f"{where} 须给 sha256，或整目录输入时给 git_commit")
    return errors


def check_json(data: object, problem_dir: str, problems: set[str], root: Path | None = None) -> list[str]:
    if not isinstance(data, dict):
        return ["solution.json 顶层必须是对象"]
    root = root or Path(".")
    errors = []
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version 须为 {SCHEMA_VERSION}（旧格式的迁移见 solutions/README.md）")
    if data.get("problem") != problem_dir:
        errors.append(f"problem 应为所在目录的题号 {problem_dir}")
    if data.get("problem") not in problems:
        errors.append(f"题号 {data.get('problem')!r} 不在 problems/ 中")
    if not COMMIT_RE.match(str(data.get("problem_revision", ""))):
        errors.append("problem_revision 须为所依据题面版本的本仓库提交哈希（7–40 位小写十六进制）")
    for key in ("title", "scope"):
        if not non_empty_str(data.get(key)):
            errors.append(f"{key} 不能为空")
    authors = data.get("authors")
    if not isinstance(authors, list) or not authors or not all(non_empty_str(a) for a in authors):
        errors.append("authors 必须是非空的字符串列表")
    if data.get("license") not in LICENSES:
        errors.append(f"license 须为 {sorted(LICENSES)} 之一")
    kind = data.get("contribution_type")
    if kind not in CONTRIBUTIONS:
        errors.append(f"contribution_type 须为 {sorted(CONTRIBUTIONS)} 之一")
    method = data.get("method")
    if not isinstance(method, dict) or not all(non_empty_str(method.get(k)) for k in ("family", "quantum_component")):
        errors.append("method 须包含非空的 family 与 quantum_component")

    numeric_needed = kind not in NON_NUMERIC
    results = data.get("results")
    numeric = 0
    if not isinstance(results, list) or (numeric_needed and not results):
        errors.append("results 必须是列表；除 input-curation、literature 外不能为空")
    else:
        found, numeric = check_values(results, "results", "observable", need_unit=True)
        errors += found
        if numeric_needed and results and numeric == 0:
            errors.append("results 中至少要有一项带数值的结果")
    baseline = data.get("baseline_comparison")
    if not isinstance(baseline, list) or (numeric_needed and not baseline):
        errors.append("baseline_comparison 必须是列表；除 input-curation、literature 外不能为空")
    else:
        errors += check_values(baseline, "baseline_comparison", "method", need_unit=False)[0]

    repro = data.get("reproducibility")
    if not isinstance(repro, dict):
        errors.append("reproducibility 须为对象")
    else:
        for key in ("command", "environment"):
            if not non_empty_str(repro.get(key)):
                errors.append(f"reproducibility.{key} 不能为空")
        errors += check_code(repro.get("code"), root)
        errors += check_inputs(repro.get("inputs"))
        seeds = repro.get("seeds")
        if not isinstance(seeds, list):
            errors.append("reproducibility.seeds 须为列表")
        elif not seeds and not non_empty_str(repro.get("seeds_note")):
            errors.append("没有随机种子时须在 reproducibility.seeds_note 说明为何是确定性的")
        has_unc = isinstance(results, list) and any(isinstance(r, dict) and "uncertainty" in r for r in results)
        if numeric and not has_unc and not non_empty_str(repro.get("uncertainty_note")):
            errors.append("结果都没有 uncertainty 时须在 reproducibility.uncertainty_note 说明误差如何估计或为何不适用")
    compute = data.get("compute")
    if (not isinstance(compute, dict) or not non_empty_str(compute.get("hardware"))
            or not isinstance(compute.get("qpu"), bool) or not non_empty_str(compute.get("wall_time"))):
        errors.append("compute 须包含非空的 hardware、wall_time 与布尔值 qpu")
    claims = data.get("claims")
    if not isinstance(claims, dict) or claims.get("conclusion") not in CONCLUSIONS or claims.get("milestone_status") not in MILESTONES:
        errors.append(f"claims 须包含 conclusion（{sorted(CONCLUSIONS)}）与 milestone_status（{sorted(MILESTONES)}）")
    for key in ("self_assessment", "review_status", "application_status"):
        if key in data:
            errors.append(f"solution.json 不能含 {key}：作者自评写在 claims，审核与原题完成状态只记在 review.json")
    if any(PLACEHOLDER_RE.search(s) for s in strings(data)):
        errors.append("solution.json 中仍有 <...> 占位符")
    return errors


def check_review(data: object, authors: list[str]) -> list[str]:
    """review.json 由审核者写。复现/采纳状态必须能追溯到非作者的复现记录。"""
    if not isinstance(data, dict):
        return ["review.json 顶层必须是对象"]
    errors = []
    status = data.get("status")
    if status not in REVIEW_STATUSES:
        errors.append(f"review.json status 须为 {sorted(REVIEW_STATUSES)} 之一")
    if data.get("application_status") not in APPLICATION:
        errors.append(f"review.json application_status 须为 {sorted(APPLICATION)} 之一")
    elif data["application_status"] == "completed" and status != "accepted":
        errors.append("原题完成（application_status=completed）只能在 status=accepted 时记录")
    reviews = data.get("reviews")
    if not isinstance(reviews, list):
        errors.append("review.json reviews 须为列表")
        reviews = []
    if status != "unreviewed" and not reviews:
        errors.append(f"status={status} 须至少有一条 reviews 记录")
    reproduced = False
    for i, r in enumerate(reviews):
        where = f"reviews[{i}]"
        if not isinstance(r, dict) or not non_empty_str(r.get("reviewer")) or r.get("kind") not in REVIEW_KINDS:
            errors.append(f"{where} 须包含 reviewer 与 kind（{sorted(REVIEW_KINDS)}）")
            continue
        if not non_empty_str(r.get("date")) or not COMMIT_RE.match(str(r.get("solution_commit", ""))):
            errors.append(f"{where} 须包含 date 与被审核的 solution_commit")
        if r["kind"] != "reproduction":
            continue
        rows = r.get("results")
        if not all(non_empty_str(r.get(k)) for k in ("environment", "command")) or not isinstance(rows, list) or not rows:
            errors.append(f"{where} 复现记录须包含 environment、command 与非空 results")
            continue
        ok_rows = all(
            isinstance(x, dict) and non_empty_str(x.get("observable")) and isinstance(x.get("within_tolerance"), bool)
            and non_empty_str(str(x.get("tolerance", ""))) for x in rows
        )
        if not ok_rows:
            errors.append(f"{where}.results 每项须包含 observable、tolerance 与布尔值 within_tolerance")
        elif r["reviewer"] not in authors and all(x["within_tolerance"] for x in rows):
            reproduced = True
    if status in {"independently_reproduced", "accepted"} and not reproduced:
        errors.append(f"status={status} 须有一条非作者、全部结果在容差内的 reproduction 记录")
    claims = data.get("accepted_claims")
    if status == "accepted" and (not isinstance(claims, list) or not claims or not all(non_empty_str(c) for c in claims)):
        errors.append("status=accepted 须在 accepted_claims 写明采纳的具体命题")
    return errors


def check_solution(path: Path, problems: set[str], root: Path) -> list[str]:
    errors = []
    if not DIR_RE.match(path.name):
        errors.append("目录名须为 <名字>-<短名>")
    for file in path.rglob("*"):
        if file.is_file() and file.stat().st_size > MAX_FILE:
            errors.append(f"{file.relative_to(path)} 超过 5MB，大型数据请给下载地址与 SHA-256")
    md = path / "SOLUTION.md"
    if not md.is_file():
        errors.append("缺少 SOLUTION.md")
    else:
        text = md.read_text(encoding="utf-8", errors="replace")
        missing = [s for s in SECTIONS if s not in text]
        if missing:
            errors.append(f"SOLUTION.md 缺少章节 {missing}")
        if PLACEHOLDER_RE.search(text):
            errors.append("SOLUTION.md 中仍有 <...> 占位符")
    meta = path / "solution.json"
    if not meta.is_file():
        errors.append("缺少 solution.json")
    else:
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"solution.json 不是合法 JSON：{exc}")
        else:
            errors += check_json(data, path.parent.name, problems, root)
            review = path / "review.json"
            if review.is_file():
                authors = data.get("authors") if isinstance(data, dict) and isinstance(data.get("authors"), list) else []
                try:
                    errors += check_review(json.loads(review.read_text(encoding="utf-8")), authors)
                except json.JSONDecodeError as exc:
                    errors.append(f"review.json 不是合法 JSON：{exc}")
                if not (path / "REVIEW.md").is_file():
                    errors.append("有 review.json 时须附 REVIEW.md（人读的审核记录）")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    root = Path(parser.parse_args().root).resolve()
    solutions = root / "solutions"
    problems = known_problems(root)
    report: dict[str, list[str]] = {}
    count = 0
    if solutions.is_dir():
        for problem_dir in sorted(solutions.iterdir()):
            if problem_dir.name in SKIP:
                continue
            if not problem_dir.is_dir():
                report[problem_dir.name] = ["solutions/ 下只能放 <题号>/ 目录"]
                continue
            if problem_dir.name not in problems:
                report[problem_dir.name] = [f"题号 {problem_dir.name} 不在 problems/ 中"]
            for entry in sorted(problem_dir.iterdir()):
                if entry.name in SKIP:
                    continue
                key = f"{problem_dir.name}/{entry.name}"
                if not entry.is_dir():
                    report[key] = ["每份解法须是一个目录"]
                    continue
                count += 1
                errors = check_solution(entry, problems, root)
                if errors:
                    report[key] = errors
    for key, errors in report.items():
        for error in errors:
            print(f"solutions/{key}: {error}")
    if report:
        print(f"\n{len(report)} 处不合规，共检查 {count} 份解法。")
        return 1
    print(f"全部合规，共检查 {count} 份解法。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
