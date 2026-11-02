"""B16 入门示例：两比特 VQE 的能量要测多少次才能达到化学精度？

在 starters/B16 的基础上加一步：不再直接读态矢的期望值，而是把 4×4 哈密顿量拆成 Pauli 串，
按逐比特对易分组测量，用有限 shots 估计能量，统计误差随 shots 怎么变。

运行（仓库根目录）：python solutions/B16/qaidao-vqe-shot-budget/code/shot_budget.py [--out 路径] [--check]
--check 把本次结果与 data/shot_budget.json 按事先声明的判据比较（见 ACCEPT），不满足时退出码为 1；
统计判据按抽样误差设容差，不要求不同平台逐位一致。CI 用 --check 并把结果写到临时目录。
"""

from __future__ import annotations

import argparse
import itertools
import math
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "starters" / "B16"))
sys.path.insert(0, str(ROOT / "starters"))
import run as starter  # noqa: E402  starters/B16/run.py

CHEM_ACC = 1.6e-3  # Ha，约 1 kcal/mol
SHOTS = (256, 1024, 4096, 8192, 32768)
REPEATS = 2000
SEED = 20261028
COMMITTED = HERE.parent / "data" / "shot_budget.json"
# 验收判据（事先声明，改动须在 SOLUTION.md 说明理由）：
#   CASCI 绝对差 ≤ 1e-6 Ha；单次测量 σ 相对差 ≤ rel_tol：VQE 能量误差约 1e-12 Ha 时态误差约 1e-6，
#   σ 对态误差是一阶的，跨平台实测相对差约 4e-5（macOS arm64 与 Ubuntu x86_64），故取 1e-3；
#   95% 预算每个基允许 ±1 次（向上取整的边界）；
#   σ 实测/解析 偏离 1 不超过 5 个抽样标准误 1/√(2(R−1))；
#   落在化学精度内的比例与正态预测 2Φ(ε/σ)−1 之差不超过 5 个二项标准误（下限 0.01）；
#   均值偏差不超过 5σ/√R。
ACCEPT = {"vqe_minus_casci_abs": 1e-8, "rel_tol": 1e-3, "n_se": 5.0}

PAULI = {
    "I": np.eye(2),
    "X": np.array([[0, 1], [1, 0]]),
    "Y": np.array([[0, -1j], [1j, 0]]),
    "Z": np.diag([1.0, -1.0]),
}
# 把单比特 Pauli 的本征基转到 Z 基的旋转：X 用 H，Y 用 H·S†
ROTATE = {
    "Z": np.eye(2),
    "X": np.array([[1, 1], [1, -1]]) / np.sqrt(2),
    "Y": np.array([[1, 1], [1, -1]]) / np.sqrt(2) @ np.diag([1, -1j]),
}


def pauli_terms(h: np.ndarray) -> dict[str, float]:
    """H = Σ c_P P，c_P = Tr(P H)/4。只保留非零项。"""
    terms = {}
    for a, b in itertools.product("IXYZ", repeat=2):
        c = np.trace(np.kron(PAULI[a], PAULI[b]) @ h).real / 4
        if abs(c) > 1e-12:
            terms[a + b] = c
    return terms


def groups(terms: dict[str, float]) -> dict[str, list[str]]:
    """每个测量基（两比特各取 X/Y/Z）对应一组可以同时测的 Pauli 串；按项的顺序贪心归组。"""
    out: dict[str, list[str]] = {}
    for p in terms:
        if p == "II":
            continue
        for basis, members in out.items():
            if all(q == "I" or q == s for q, s in zip(p, basis)):
                members.append(p)
                break
        else:
            out["".join(q if q != "I" else "Z" for q in p)] = [p]
    return out


def outcome_probs(psi: np.ndarray, basis: str) -> np.ndarray:
    u = np.kron(ROTATE[basis[0]], ROTATE[basis[1]])
    return np.abs(u @ psi) ** 2


def eigenvalue(p: str) -> np.ndarray:
    """Pauli 串在 4 个测量结果 |b0 b1⟩ 上的取值 ±1。"""
    return np.array([np.prod([1 if q == "I" else (-1) ** bit for q, bit in zip(p, bits)])
                     for bits in itertools.product((0, 1), repeat=2)])


def estimate(psi, terms, grp, shots, rng, repeats):
    """每个测量基各测 shots 次，重复 repeats 次，返回能量估计的样本。"""
    energy = np.full(repeats, terms.get("II", 0.0))
    for basis, members in grp.items():
        counts = rng.multinomial(shots, outcome_probs(psi, basis), size=repeats)
        values = sum(terms[p] * eigenvalue(p) for p in members)
        energy += counts @ values / shots
    return energy


def analytic_sigma(psi, terms, grp, shots) -> float:
    var = 0.0
    for basis, members in grp.items():
        probs = outcome_probs(psi, basis)
        values = sum(terms[p] * eigenvalue(p) for p in members)
        var += (probs @ values**2 - (probs @ values) ** 2) / shots
    return float(np.sqrt(var))


def acceptance(report: dict, committed: dict) -> list[str]:
    """按 ACCEPT 比较本次结果与已提交结果，返回不满足的判据。"""
    fails = []
    n_se = ACCEPT["n_se"]
    for name, ref in committed["species"].items():
        got = report.get(name)
        if got is None:
            fails.append(f"{name}：本次缺失")
            continue
        if abs(got["vqe_minus_casci"]) > ACCEPT["vqe_minus_casci_abs"]:
            fails.append(f"{name}：VQE−CASCI = {got['vqe_minus_casci']:.2e} Ha")
        if abs(got["E_CASCI"] - ref["E_CASCI"]) > 1e-6:
            fails.append(f"{name}：CASCI 与已提交结果差 {got['E_CASCI'] - ref['E_CASCI']:.2e} Ha")
        if got["bases"] != ref["bases"]:
            fails.append(f"{name}：测量分组与已提交结果不同")
        if abs(got["sigma_single_shot"] / ref["sigma_single_shot"] - 1) > ACCEPT["rel_tol"]:
            fails.append(f"{name}：单次测量 σ {got['sigma_single_shot']:.8g}，已提交 {ref['sigma_single_shot']:.8g}")
        if abs(got["shots_per_basis_for_95pct_chem_acc"] - ref["shots_per_basis_for_95pct_chem_acc"]) > 1:
            fails.append(f"{name}：95% 预算每个基 {got['shots_per_basis_for_95pct_chem_acc']} 次，"
                         f"已提交 {ref['shots_per_basis_for_95pct_chem_acc']}")
        for row in got["scan"]:
            sig, emp = row["sigma_analytic"], row["sigma_empirical"]
            se = 1 / math.sqrt(2 * (REPEATS - 1))
            if abs(emp / sig - 1) > n_se * se:
                fails.append(f"{name} M={row['shots_per_basis']}：σ 实测/解析 = {emp / sig:.3f}")
            p = math.erf(CHEM_ACC / (sig * math.sqrt(2)))
            tol = max(n_se * math.sqrt(p * (1 - p) / REPEATS), 0.01)
            if abs(row["fraction_within_chem_acc"] - p) > tol:
                fails.append(f"{name} M={row['shots_per_basis']}：化学精度内比例 {row['fraction_within_chem_acc']:.3f}，"
                             f"正态预测 {p:.3f}")
            if abs(row["bias"]) > n_se * sig / math.sqrt(REPEATS):
                fails.append(f"{name} M={row['shots_per_basis']}：均值偏差 {row['bias']:.2e} Ha")
    return fails


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=COMMITTED, help="结果写到哪里（缺省覆盖 data/shot_budget.json）")
    parser.add_argument("--check", action="store_true", help="按 ACCEPT 与已提交结果比较，不满足时退出码为 1")
    args = parser.parse_args()
    geoms = starter.load_geometries()
    rng = np.random.default_rng(SEED)
    report = {}
    for name in starter.QUICK:
        h, _, e_casci = starter.cas_hamiltonian(geoms[name])
        best = None
        for seed in (0, 1, 2):
            x0 = np.random.default_rng(seed).uniform(-np.pi, np.pi, 4)
            res = starter.minimize(lambda t: starter.ansatz(t) @ h @ starter.ansatz(t), x0, method="BFGS",
                                   options={"gtol": 1e-10})
            best = res if best is None or res.fun < best.fun else best
        psi = starter.ansatz(best.x)
        terms = pauli_terms(h)
        grp = groups(terms)
        print(f"\n{name}：CASCI {e_casci:.10f} Ha，理想 VQE 误差 {best.fun - e_casci:.1e} Ha")
        print("  Pauli 项：" + "，".join(f"{p} {c:+.6f}" for p, c in terms.items() if p != "II"))
        print("  测量基：" + "，".join(f"{b}[{' '.join(m)}]" for b, m in grp.items()))
        rows = []
        for shots in SHOTS:
            e = estimate(psi, terms, grp, shots, rng, REPEATS)
            sigma = analytic_sigma(psi, terms, grp, shots)
            within = float(np.mean(np.abs(e - e_casci) <= CHEM_ACC))
            rows.append({"shots_per_basis": shots, "total_shots": shots * len(grp), "sigma_analytic": sigma,
                         "sigma_empirical": float(e.std(ddof=1)), "bias": float(e.mean() - e_casci),
                         "fraction_within_chem_acc": within})
            print(f"  每个基 {shots:>6} 次（共 {shots * len(grp):>6}）：σ 解析 {sigma:.2e}，σ 实测 {e.std(ddof=1):.2e} Ha，"
                  f"{within:6.1%} 的重复落在化学精度内")
        # σ ∝ 1/√shots：σ(M) = σ(1)/√M，要 1.96σ ≤ 化学精度
        sigma1 = analytic_sigma(psi, terms, grp, 1)
        need = int(np.ceil((1.96 * sigma1 / CHEM_ACC) ** 2))
        print(f"  95% 置信落在化学精度内：每个基约需 {need} 次，共 {need * len(grp)} 次")
        report[name] = {"E_CASCI": e_casci, "vqe_minus_casci": float(best.fun - e_casci),
                        "pauli_terms": terms, "bases": grp, "sigma_single_shot": sigma1,
                        "shots_per_basis_for_95pct_chem_acc": need, "total_shots_for_95pct_chem_acc": need * len(grp),
                        "scan": rows}
    out = args.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"seed": SEED, "repeats": REPEATS, "chem_acc_Ha": CHEM_ACC, "species": report},
                              indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n结果已写入 {out}")
    if args.check:
        fails = acceptance(report, json.loads(COMMITTED.read_text(encoding="utf-8")))
        for f in fails:
            print(f"  ✗ {f}")
        print("验收判据全部满足。" if not fails else f"{len(fails)} 项验收判据未满足。")
        sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
