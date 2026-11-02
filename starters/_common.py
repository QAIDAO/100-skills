"""入门轨道的共用小工具：下载并校验公开输入、对照 expected.json 打分。"""

from __future__ import annotations

import hashlib
import json
import math
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


def check(results: dict, expected_path: Path, profile: str = "quick") -> bool:
    """逐项对照 expected.json，全部必需指标在容差内才返回 True。

    每项的 profiles 列出它在哪些运行模式下必须出现（缺省为 quick 与 full）。
    当前模式必需的指标缺失、不是有限实数或超差都算失败；其他模式的指标只标为跳过。
    """
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    ok, checked = True, 0
    print(f"\n对照现有参照（{profile} 模式）：")
    for key, spec in expected["values"].items():
        required = profile in spec.get("profiles", ("quick", "full"))
        got, want, tol = results.get(key), spec["value"], spec["tol"]
        if got is None:
            if required:
                ok = False
                print(f"  ✗ {key}：缺失（{profile} 模式必需）")
            else:
                print(f"  ·  {key}：跳过（{spec.get('note', '其他模式才计算')}）")
            continue
        if isinstance(got, bool) or not isinstance(got, (int, float)) or not math.isfinite(got):
            ok = False
            print(f"  ✗ {key} = {got!r}：不是有限实数")
            continue
        good = abs(got - want) <= tol
        ok &= good
        checked += 1
        mark = "✓" if good else "✗"
        print(f"  {mark} {key} = {got:.10g}（参照 {want:.10g}，容差 {tol:g} {spec.get('unit', '')}）")
    if checked == 0:
        ok = False
    print("\n全部必需指标落在容差内：你已经复现了现有参照。" if ok else "\n有必需指标缺失或超出容差，先检查环境版本和输入哈希。")
    return ok
