#!/usr/bin/env python3
"""校验 solutions/ 下的解法提交格式。只检查结构，不运行任何计算。

用法：python3 -I release/tools/check_submissions.py --root <仓库根>
全部合规时退出码为 0；否则逐条列出错误，退出码为 1。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SECTIONS = ("## 方法", "## 结果", "## 经典对照", "## 复现", "## 局限")
LICENSES = {"Apache-2.0", "MIT", "BSD-3-Clause"}
ASSESSMENTS = {"pass", "fail", "inconclusive"}
MAX_FILE = 5_000_000
PLACEHOLDER_RE = re.compile(r"<[^<>\n]{1,60}>")
DIR_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*-[A-Za-z0-9_.-]+$")
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


def check_json(data: object, problem_dir: str, problems: set[str]) -> list[str]:
    if not isinstance(data, dict):
        return ["solution.json 顶层必须是对象"]
    errors = []
    if data.get("problem") != problem_dir:
        errors.append(f"problem 应为所在目录的题号 {problem_dir}")
    if data.get("problem") not in problems:
        errors.append(f"题号 {data.get('problem')!r} 不在 problems/ 中")
    if not non_empty_str(data.get("title")):
        errors.append("title 不能为空")
    authors = data.get("authors")
    if not isinstance(authors, list) or not authors or not all(non_empty_str(a) for a in authors):
        errors.append("authors 必须是非空的字符串列表")
    if data.get("license") not in LICENSES:
        errors.append(f"license 须为 {sorted(LICENSES)} 之一")
    method = data.get("method")
    if not isinstance(method, dict) or not all(non_empty_str(method.get(k)) for k in ("family", "quantum_component")):
        errors.append("method 须包含非空的 family 与 quantum_component")
    results = data.get("results")
    if not isinstance(results, list) or not results:
        errors.append("results 必须是非空列表")
    else:
        for i, item in enumerate(results):
            if not isinstance(item, dict) or not non_empty_str(item.get("observable")) or "value" not in item or not non_empty_str(item.get("unit")):
                errors.append(f"results[{i}] 须包含 observable、value、unit")
    baseline = data.get("baseline_comparison")
    if not isinstance(baseline, list) or not baseline:
        errors.append("baseline_comparison 必须是非空列表")
    else:
        for i, item in enumerate(baseline):
            if not isinstance(item, dict) or not non_empty_str(item.get("method")) or "value" not in item:
                errors.append(f"baseline_comparison[{i}] 须包含 method 与 value")
    repro = data.get("reproducibility")
    if not isinstance(repro, dict) or not all(non_empty_str(repro.get(k)) for k in ("code", "environment")):
        errors.append("reproducibility 须包含非空的 code 与 environment")
    compute = data.get("compute")
    if not isinstance(compute, dict) or not non_empty_str(compute.get("hardware")) or not isinstance(compute.get("qpu"), bool):
        errors.append("compute 须包含非空的 hardware 与布尔值 qpu")
    if data.get("self_assessment") not in ASSESSMENTS:
        errors.append(f"self_assessment 须为 {sorted(ASSESSMENTS)} 之一")
    if any(PLACEHOLDER_RE.search(s) for s in strings(data)):
        errors.append("solution.json 中仍有 <...> 占位符")
    return errors


def check_solution(path: Path, problems: set[str]) -> list[str]:
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
            errors += check_json(data, path.parent.name, problems)
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
                errors = check_solution(entry, problems)
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
