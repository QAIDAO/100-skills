"""C11 入门：METABRIC 四维 UMAP 坐标上的 4 比特量子核分群，与 RBF、线性核比较。

问题：同一批乳腺癌样本，换一组重抽的样本再聚一次类，分群结果还稳不稳？
做法（与现有参照 R53 相同，可逐位复现其数字）：
1. 下载作者公开的 1980×4 UMAP 坐标（固定 commit），校验 SHA-256；不读取任何生物标签。
2. 固定随机切成开发 660 行 / 评价 1320 行；只用开发集拟合标准化参数和 RBF 带宽。
3. 每组抽 128 个共同 anchor，再给 A、B 两侧各配 128 个独有样本（每侧 256 行）。
   两侧分别用核矩阵的前 10 个正谱模式做 k=10 的 kmeans，比较 anchor 上两次分群的 AMI。
   AMI 越高，说明分群越不受其余样本影响，即越稳定。
4. 量子核：4 比特、两层数据重上传（每层 RY(αx_q)，再对相邻比特做 RZZ(αx_q x_{q+1})），
   K(x,y) = |⟨φ(x)|φ(y)⟩|²。这里用 16 维态矢精确计算；--shots 再模拟 8192 次测量的统计噪声。
5. 先在 8 组开发数据上选 α 与 RBF 带宽，锁定后在 24 组评价数据上报告平均 AMI。

运行：python starters/C11/run.py [--shots]    （约 30 秒；--shots 约 1 分钟）
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from sklearn.metrics import adjusted_mutual_info_score

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _common import check, fetch_inputs  # noqa: E402

# 以下常数与现有参照 R53 的冻结协议一致，改了就不能与参照逐位比较。
DEV_ROWS, DEV_PAIRS, EVAL_PAIRS = 660, 8, 24
ANCHOR, UNIQUE = 128, 128
CLUSTERS, MODES, RESTARTS, MAX_ITER, TOL = 10, 10, 10, 100, 1e-8
ALPHAS, RBF_MULTIPLIERS = (0.2, 1.0, 2.0), (0.25, 1.0, 4.0)
SHOTS = 8192
SPLIT_SEED, DEV_SEED, EVAL_SEED, CLUSTER_SEED, SHOT_SEED, BOOT_SEED = (
    2026105301, 202610531000, 202610532000, 202610533000, 202610534000, 202610535001)


def load() -> np.ndarray:
    rows = list(csv.reader(fetch_inputs(HERE)["C11-umap.csv"].open()))
    assert rows[0][1:5] == ["Component_1", "Component_2", "Component_3", "Component_4"]
    return np.array([[float(v) for v in row[1:5]] for row in rows[1:]])


def feature_states(x: np.ndarray, alpha: float) -> np.ndarray:
    """每行数据 → 4 比特态矢（16 维）。第 0 比特是最高位。"""
    psi = np.zeros((len(x), 16), complex)
    psi[:, 0] = 1
    idx = np.arange(16)
    for _layer in range(2):
        for q in range(4):  # RY(α x_q)
            bit = 1 << (3 - q)
            lo = idx[(idx & bit) == 0]
            hi = lo | bit
            c, s = np.cos(alpha * x[:, q] / 2)[:, None], np.sin(alpha * x[:, q] / 2)[:, None]
            a, b = psi[:, lo].copy(), psi[:, hi].copy()
            psi[:, lo], psi[:, hi] = c * a - s * b, s * a + c * b
        for q in range(3):  # RZZ(α x_q x_{q+1})，对角相位
            zz = (1 - 2 * ((idx >> (3 - q)) & 1)) * (1 - 2 * ((idx >> (2 - q)) & 1))
            psi *= np.exp(-0.5j * alpha * (x[:, q] * x[:, q + 1])[:, None] * zz)
    return psi


def kmeans(features: np.ndarray, seed: int) -> np.ndarray:
    """朴素 Lloyd kmeans，10 次随机初始化取惯量最小者。"""
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(RESTARTS):
        centers = features[rng.choice(len(features), CLUSTERS, replace=False)].copy()
        for _ in range(MAX_ITER):
            labels = ((features[:, None] - centers[None]) ** 2).sum(2).argmin(1)
            new = centers.copy()
            for j in range(CLUSTERS):
                if np.any(labels == j):
                    new[j] = features[labels == j].mean(0)
            done = np.max(abs(new - centers)) < TOL
            centers = new
            if done:
                break
        labels = ((features[:, None] - centers[None]) ** 2).sum(2).argmin(1)
        inertia = float(((features - centers[labels]) ** 2).sum())
        if best is None or inertia < best[0]:
            best = (inertia, labels)
    return best[1]


def spectral_kmeans(kernel: np.ndarray, seed: int) -> np.ndarray:
    """取核矩阵最大的 10 个正本征模，乘 √λ 作为特征，再 kmeans。"""
    ev, u = eigh(kernel, driver="evd")
    keep = np.flatnonzero(ev > 0)[-MODES:]
    feats = np.zeros((len(kernel), MODES))
    feats[:, : len(keep)] = u[:, keep] * np.sqrt(ev[keep])
    return kmeans(feats, seed)


def kernel(method: tuple, z: np.ndarray, median: float) -> np.ndarray:
    family, value = method
    if family == "quantum":
        psi = feature_states(z, value)
        return abs(psi.conj() @ psi.T) ** 2
    if family == "rbf":
        return np.exp(-((z[:, None] - z[None]) ** 2).sum(2) / (median * value))
    return z @ z.T


def sampled(k: np.ndarray, words: list[int]) -> np.ndarray:
    """模拟每个非对角元做 SHOTS 次 compute–uncompute 测量：计数 ~ Binomial(SHOTS, K_ij)。"""
    up = np.triu_indices(len(k), 1)
    counts = np.random.default_rng(np.random.SeedSequence(words)).binomial(SHOTS, np.clip(k[up], 0, 1))
    noisy = np.eye(len(k))
    noisy[up] = noisy[up[1], up[0]] = counts / SHOTS
    return noisy


def stability(phase: str, pair: int, pool: np.ndarray, xx: np.ndarray, median: float, methods: dict, shots: bool) -> dict:
    """一组：A、B 两侧各聚一次类，返回每种方法在共同 anchor 上的 AMI。"""
    seed_base = DEV_SEED if phase == "dev" else EVAL_SEED
    chosen = np.random.default_rng(seed_base + pair).choice(pool, ANCHOR + 2 * UNIQUE, replace=False)
    sides = [np.r_[chosen[:ANCHOR], chosen[ANCHOR:ANCHOR + UNIQUE]], np.r_[chosen[:ANCHOR], chosen[ANCHOR + UNIQUE:]]]
    labels: dict[str, list] = {}
    for side, rows in enumerate(sides):
        seed = CLUSTER_SEED + (0 if phase == "dev" else 1000) + 2 * pair + side
        for name, method in methods.items():
            k = kernel(method, xx[rows], median)
            labels.setdefault(name, []).append(spectral_kmeans(k, seed))
            if shots and method[0] == "quantum":
                reps = [spectral_kmeans(sampled(k, [SHOT_SEED, pair, side, SHOTS, r]), seed) for r in range(3)]
                for r, lab in enumerate(reps):
                    labels.setdefault(f"{name}@{SHOTS}#{r}", []).append(lab)
    return {name: adjusted_mutual_info_score(a[:ANCHOR], b[:ANCHOR], average_method="max") for name, (a, b) in labels.items()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", action="store_true", help=f"另外模拟每个核元素 {SHOTS} 次测量（3 次重复）")
    args = parser.parse_args()

    x = load()
    split = np.random.default_rng(SPLIT_SEED).permutation(len(x))
    dev, eva = split[:DEV_ROWS], split[DEV_ROWS:]
    xx = (x - x[dev].mean(0)) / x[dev].std(0)
    d2 = ((xx[dev, None] - xx[None, dev]) ** 2).sum(2)[np.triu_indices(DEV_ROWS, 1)]
    median = float(np.median(d2[d2 > 0]))

    candidates = {f"quantum α={a}": ("quantum", a) for a in ALPHAS}
    candidates |= {f"rbf ×{m}": ("rbf", m) for m in RBF_MULTIPLIERS}
    candidates["linear"] = ("linear", None)
    dev_ami = [stability("dev", p, dev, xx, median, candidates, False) for p in range(DEV_PAIRS)]
    dev_mean = {name: float(np.mean([r[name] for r in dev_ami])) for name in candidates}
    print("开发集平均 AMI（用来选参数）：")
    for name, value in dev_mean.items():
        print(f"  {name:<14} {value:.6f}")
    q = max((n for n in candidates if n.startswith("quantum")), key=dev_mean.get)
    r = max((n for n in candidates if n.startswith("rbf")), key=dev_mean.get)
    classical = r if dev_mean[r] >= dev_mean["linear"] else "linear"
    locked = {"quantum": candidates[q], "rbf": candidates[r], "linear": candidates["linear"]}
    print(f"锁定：{q}、{r}；最强经典对照为 {classical}\n")

    rows = [stability("eval", p, eva, xx, median, locked, args.shots) for p in range(EVAL_PAIRS)]
    results = {f"AMI[{name}]": float(np.mean([row[name] for row in rows])) for name in locked}
    print("评价集 24 组平均 AMI：")
    for name in locked:
        print(f"  {name:<8} {results[f'AMI[{name}]']:.6f}")
    if args.shots:
        cls = "rbf" if classical.startswith("rbf") else "linear"
        deltas = np.array([np.mean([row[f"quantum@{SHOTS}#{i}"] for i in range(3)]) - row[cls] for row in rows])
        boot = deltas[np.random.default_rng(BOOT_SEED).integers(0, len(deltas), size=(10000, len(deltas)), dtype=np.int32)].mean(1)
        lo, hi = np.quantile(boot, [0.025, 0.975])
        results[f"AMI[quantum@{SHOTS}]"] = float(np.mean([np.mean([row[f"quantum@{SHOTS}#{i}"] for i in range(3)]) for row in rows]))
        results["delta_AMI"] = float(deltas.mean())
        results["delta_AMI_lower95"], results["delta_AMI_upper95"] = float(lo), float(hi)
        print(f"  quantum@{SHOTS} {results[f'AMI[quantum@{SHOTS}]']:.6f}")
        print(f"\n量子（{SHOTS} shots）− {classical}：{deltas.mean():+.6f}，bootstrap 95% 区间 [{lo:.6f}, {hi:.6f}]")
        print("区间含零：在这个设定下，量子核没有显示出比 RBF 更稳定的分群。")

    (HERE / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    sys.exit(0 if check(results, HERE / "expected.json") else 1)


if __name__ == "__main__":
    main()
