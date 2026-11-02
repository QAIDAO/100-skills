#!/usr/bin/env python3
"""新建一份解法目录：复制模板，填好题号、作者和标题；有 starter 的题顺带填入公开输入及其 SHA-256。

用法：python3 -I release/tools/new_solution.py <题号> <名字>-<短名> [--author 署名] [--title 标题]
例如：python3 -I release/tools/new_solution.py B16 alice-shot-budget --author "Alice Wang"
目录名只用 ASCII 字母、数字、点、下划线和连字符；中文署名放在 --author。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "solutions" / "_template"
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.]*-[A-Za-z0-9][A-Za-z0-9_.-]*$")


def problem_title(pid: str) -> str | None:
    for path in (ROOT / "problems").glob(f"*/{pid}/problem.json"):
        return json.loads(path.read_text(encoding="utf-8"))["title"]
    return None


def head_commit() -> str | None:
    """当前检出的提交，作为 problem_revision（所依据的题面版本）。"""
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short=12", "HEAD"], capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout.strip() or None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("problem", help="题号，如 B16")
    parser.add_argument("name", help="目录名 <你的名字>-<短名>，只用 ASCII，如 alice-shot-budget")
    parser.add_argument("--author", default=None, help="署名，可以是中文；缺省取目录名第一段")
    parser.add_argument("--title", default=None, help="解法标题，可以之后再改")
    args = parser.parse_args()

    pid = args.problem.upper()
    title = problem_title(pid)
    if title is None:
        print(f"找不到题号 {pid}，题号列表见 problems/INDEX.md", file=sys.stderr)
        return 1
    if not NAME_RE.match(args.name):
        print("目录名须为 <你的名字>-<短名>，只用字母、数字、点、下划线和连字符，例如 alice-shot-budget；中文署名请用 --author", file=sys.stderr)
        return 1
    dest = ROOT / "solutions" / pid / args.name
    if dest.exists():
        print(f"{dest.relative_to(ROOT)} 已存在，换一个短名", file=sys.stderr)
        return 1

    author = args.author or args.name.split("-", 1)[0]
    sol_title = args.title or "<解法标题>"
    dest.mkdir(parents=True)
    md = (TEMPLATE / "SOLUTION.md").read_text(encoding="utf-8")
    md = md.replace("<题号>", pid, 1).replace("<解法标题>", sol_title, 1).replace("<你的名字>", author, 1)
    (dest / "SOLUTION.md").write_text(md, encoding="utf-8")

    data = json.loads((TEMPLATE / "solution.json").read_text(encoding="utf-8"))
    data["problem"] = pid
    data["title"] = sol_title
    data["authors"] = [author]
    revision = head_commit()
    if revision:
        data["problem_revision"] = revision
    inputs = ROOT / "starters" / pid / "inputs.json"
    if inputs.is_file():
        data["reproducibility"]["inputs"] = [
            {"name": s["name"], "url": s["url"], "sha256": s["sha256"]}
            for s in json.loads(inputs.read_text(encoding="utf-8"))
        ]
    (dest / "solution.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rel = dest.relative_to(ROOT)
    print(f"已建好 {rel}/（{pid} · {title}）")
    print("接下来：")
    print(f"  1. 把代码和小型结果文件放进 {rel}/")
    print("  2. 填写 SOLUTION.md 的五节，替换 solution.json 里所有 <...> 占位符（不填完校验不会通过）")
    print("  3. python3 -I release/tools/check_submissions.py --root .")
    print("  4. git commit -s（DCO 签名，CI 会检查），然后开 PR")
    print("通过校验只说明格式与证据齐全；独立复现与采纳由审核者另开 PR 写入 review.json。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
