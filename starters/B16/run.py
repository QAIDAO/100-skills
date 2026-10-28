"""B16 入门：β-拉帕醌前药断键体系的 CAS(2e,2o) 两比特 VQE。

做三件事，全部在笔记本 CPU 上完成：
1. 从作者公开仓库（固定 commit）下载几何并校验哈希；
2. 经典端：真空 RHF/6-311G(d,p)，HOMO–LUMO 的 CAS(2e,2o) 精确对角化（CASCI）；
3. 量子端：把 Nα=Nβ=1 的四维扇区写成 2 个量子比特，用 4 个 RY + 1 个 CX 的线路做 VQE，
   在态矢模拟器上优化，和 CASCI 比较。

默认只算 H2O 和产物 5（约半分钟）。加 --all 再算 6、4、TS（大体系，各需数十分钟到数小时）。
运行：python starters/B16/run.py [--all]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
from pyscf import fci, gto, mcscf, scf
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _common import check, fetch_inputs  # noqa: E402

# 物种名 → 作者 qc.py 里的变量名（作者 Gaussian 优化坐标）
SPECIES = {"H2O": "geom_h2o", "5": "geom_gaussian5", "6": "geom_gaussian6", "4": "geom_gaussian4", "TS": "geom_ts"}
QUICK = ("H2O", "5")


def load_geometries() -> dict[str, str]:
    text = fetch_inputs(HERE)["B16-qc.py"].read_text(encoding="utf-8")
    blocks = dict(re.findall(r'^(geom_\w+)\s*=\s*"""(.*?)"""', text, re.MULTILINE | re.DOTALL))
    return {name: blocks[var] for name, var in SPECIES.items()}


def cas_hamiltonian(atom: str) -> tuple[np.ndarray, float, float]:
    """返回 CAS(2e,2o) 在 Nα=Nβ=1 扇区的 4×4 哈密顿量、RHF 能量和 CASCI 能量（Ha）。"""
    mol = gto.M(atom=atom, basis="6-311g(d,p)", verbose=0)
    mf = scf.RHF(mol).run(conv_tol=1e-10)
    cas = mcscf.CASCI(mf, 2, 2)
    e_casci = cas.kernel()[0]
    h1, ecore = cas.get_h1eff()
    eri = cas.get_h2eff()
    # 基矢 |a,b⟩：a 是 α 电子所在的活性轨道（0=HOMO，1=LUMO），b 是 β 电子的。
    # 这正好是两个量子比特的计算基：第 0 比特记 α，第 1 比特记 β。
    h2 = fci.direct_spin1.absorb_h1e(h1, eri, 2, (1, 1), 0.5)
    cols = []
    for i in range(4):
        e = np.zeros(4)
        e[i] = 1.0
        cols.append(fci.direct_spin1.contract_2e(h2, e.reshape(2, 2), 2, (1, 1)).ravel())
    return np.array(cols).T + ecore * np.eye(4), mf.e_tot, e_casci


def ry(theta: float) -> np.ndarray:
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return np.array([[c, -s], [s, c]])


CX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=float)


def ansatz(theta: np.ndarray) -> np.ndarray:
    """RY⊗RY → CX(0→1) → RY⊗RY，作用在 |00⟩ 上。实数线路，4 个参数。"""
    psi = np.zeros(4)
    psi[0] = 1.0
    psi = np.kron(ry(theta[0]), ry(theta[1])) @ psi
    psi = CX @ psi
    return np.kron(ry(theta[2]), ry(theta[3])) @ psi


def vqe(h: np.ndarray, seeds=(0, 1, 2)) -> float:
    best = np.inf
    for seed in seeds:
        x0 = np.random.default_rng(seed).uniform(-np.pi, np.pi, 4)
        res = minimize(lambda t: ansatz(t) @ h @ ansatz(t), x0, method="BFGS", options={"gtol": 1e-10})
        best = min(best, res.fun)
    return float(best)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="也算 6、4、TS（慢）")
    args = parser.parse_args()
    geoms = load_geometries()
    names = list(SPECIES) if args.all else list(QUICK)

    results: dict[str, float] = {}
    print(f"{'物种':>4} {'RHF/Ha':>18} {'CASCI/Ha':>18} {'VQE−CASCI/Ha':>14} {'耗时/s':>8}")
    for name in names:
        t0 = time.time()
        h, e_hf, e_casci = cas_hamiltonian(geoms[name])
        e_ed = float(np.linalg.eigvalsh(h)[0])
        e_vqe = vqe(h)
        assert abs(e_ed - e_casci) < 1e-8, "4×4 哈密顿量的最低本征值应等于 CASCI 能量"
        print(f"{name:>4} {e_hf:18.10f} {e_casci:18.10f} {e_vqe - e_casci:14.2e} {time.time() - t0:8.1f}")
        results[f"E_CAS2[{name}]"] = e_casci
        results[f"E_VQE[{name}]"] = e_vqe
    if "E_CAS2[4]" in results and "E_CAS2[TS]" in results:
        results["barrier_CAS2"] = (results["E_CAS2[TS]"] - results["E_CAS2[4]"]) * 627.5094740631
        print(f"\n电子能垒 E(TS) − E(4) = {results['barrier_CAS2']:.3f} kcal/mol（真空、CAS(2e,2o)，不含溶剂与热校正）")

    (HERE / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    sys.exit(0 if check(results, HERE / "expected.json") else 1)


if __name__ == "__main__":
    main()
