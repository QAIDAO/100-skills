"""入门轨道的共用小工具：下载并校验公开输入、对照 expected.json 打分。"""

from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

CACHE = Path(__file__).resolve().parent / ".cache"


def fetch_inputs(starter_dir: Path) -> dict[str, Path]:
    """按 <starter>/inputs.json 下载全部公开输入，返回 名字 → 本地路径。"""
    specs = json.loads((starter_dir / "inputs.json").read_text(encoding="utf-8"))
    return {s["name"]: fetch(s["url"], s["sha256"], s["name"]) for s in specs}


def fetch(url: str, sha256: str, name: str) -> Path:
    """下载公开输入到 starters/.cache/，校验 SHA-256；已下载且哈希一致时直接复用。"""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / name
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != sha256:
        print(f"下载 {url}")
        with urllib.request.urlopen(url, timeout=120) as resp:
            data = resp.read()
        digest = hashlib.sha256(data).hexdigest()
        if digest != sha256:
            raise SystemExit(f"{name} 的 SHA-256 不符：期望 {sha256}，实际 {digest}。上游文件可能变了，请开 issue。")
        path.write_bytes(data)
    return path


def check(results: dict, expected_path: Path) -> bool:
    """逐项对照 expected.json，打印每一项是否落在容差内，全部通过返回 True。"""
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    ok = True
    print("\n对照现有参照：")
    for key, spec in expected["values"].items():
        if key not in results:
            print(f"  ·  {key}：本次未计算（{spec.get('note', '可加参数运行')}）")
            continue
        got, want, tol = results[key], spec["value"], spec["tol"]
        good = abs(got - want) <= tol
        ok &= good
        mark = "✓" if good else "✗"
        print(f"  {mark} {key} = {got:.10g}（参照 {want:.10g}，容差 {tol:g} {spec.get('unit', '')}）")
    print("\n全部落在容差内：你已经复现了现有参照。" if ok else "\n有数字超出容差，先检查环境版本和输入哈希。")
    return ok
