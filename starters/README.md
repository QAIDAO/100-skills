# 入门轨道

第一次参与，建议走这条路：先挑一道热身题，用一条命令复现现有参照的数字，再在这个基础上往前走一小步，最后写成一份解法提交。不需要集群，不需要 QPU，笔记本就够。

## 1. 装环境（一次）

需要 Python 3.10 及以上。推荐用 [uv](https://docs.astral.sh/uv/)：

```bash
uv venv .venv
```

```bash
source .venv/bin/activate
```

```bash
uv pip install -r starters/requirements.txt
```

不用 uv 时，`python3 -m venv .venv` 加 `pip install -r starters/requirements.txt` 也可以。依赖只有 numpy、scipy、pyscf，版本已固定，以保证数字能逐位对上。Windows 用户若装 pyscf 失败，可以用 WSL。

## 2. 复现一道题

```bash
python starters/B16/run.py
```

脚本会下载该题的公开输入（固定版本，校验 SHA-256，缓存到 `starters/.cache/`），跑完经典基线和量子方法，最后逐项对照现有参照：

```text
对照现有参照：
  ✓ E_CAS2[H2O] = -76.04512813（参照 -76.04512813，容差 1e-06 Ha）
  ...
全部落在容差内：你已经复现了现有参照。
```

全部打 ✓，说明你的环境和参照一致，可以开始做自己的东西了。有 ✗ 时先核对依赖版本；还对不上，请开 issue 并贴出输出。

## 3. 往前走一小步

每个 starter 的 README 末尾都有「下一步」，列出几个半天到几天能做完的方向，例如加入测量噪声、换一种线路、扩大活性空间。挑一个做，结果不论好坏都可以提交：负结果同样被接受。

## 4. 提交

```bash
python3 -I release/tools/new_solution.py B16 你的名字-短名
```

脚手架会建好 `solutions/B16/你的名字-短名/`，填好题号，并把公开输入的 SHA-256 写进 `solution.json`。照着 `SOLUTION.md` 里的提示填写五节，然后运行校验、开 PR，流程见 [CONTRIBUTING.md](../CONTRIBUTING.md)。写法可以参考 [B16 入门示例解法](../solutions/B16/qaidao-vqe-shot-budget/SOLUTION.md)。

## 热身题与 starter

| 题号 | 背景 | starter | 运行时间 |
|---|---|---|---|
| [B16 β-拉帕醌前药断键](../problems/biomedicine/B16/PROBLEM.md) | 量子化学 | [starters/B16](B16/README.md)：CAS(2e,2o) 两比特 VQE | 约 40 秒 |
| [B14 光合能量传递](../problems/biomedicine/B14/PROBLEM.md) | 凝聚态与动力学 | 欢迎认领 | — |
| [B22 BODIPY 光敏剂](../problems/biomedicine/B22/PROBLEM.md) | 量子化学 | 欢迎认领 | — |
| [C07 自由基对自旋化学](../problems/extensions/C07/PROBLEM.md) | 凝聚态与动力学 | 欢迎认领 | — |
| [F16 H＋H₂ 反应散射](../problems/model-dynamics/F16/PROBLEM.md) | 凝聚态与动力学 | 欢迎认领 | — |

## 写一个 starter

给标着「欢迎认领」的热身题写 starter，是一份很好的第一份贡献。先开一个「题目讨论」issue 认领，避免撞车。一个 starter 包含：

- `inputs.json`：公开输入的名字、说明、固定版本的下载地址和 SHA-256；
- `run.py`：用 `_common.fetch_inputs` 下载并校验这些输入，跑通题面列出的一种经典基线和一个最小的量子方法，结果写进 `results.json`，最后调用 `_common.check` 对照参照；
- `expected.json`：从该题 `REFERENCE.md` 摘出的参照数字和容差，每个数字都要能在 `REFERENCE.md` 里找到；
- `README.md`：这道题在问什么、脚本做了什么、怎么读输出，以及三到五个「下一步」。

要求：只用 `requirements.txt` 里的依赖（确需新依赖请在 PR 里说明）；默认运行在笔记本上几分钟内结束，慢的部分放在参数开关后面；不把第三方数据提交进仓库。合并后维护者会把这道题的 starter 写进 `release/tracks.json`。

## 难度分级

每道题的 `PROBLEM.md` 开头都标了难度和背景，分级标准如下。分级由维护者按现有参照判断，觉得不准欢迎开 issue。

| 难度 | 含义 | 题数 |
|---|---|---|
| 热身 | 输入公开，笔记本能跑，参照里有可以直接对照的数字。 | 5 |
| 进阶 | 已有参照运行，但需要较多领域知识、工作站级算力，或要用替代输入、自建输入。 | 60 |
| 前沿 | 还没有参照运行，或者目标规模属于容错量子计算，需要先做资源估算。 | 35 |

背景分三类：量子化学、凝聚态与动力学、优化与算法。完整标签见 [release/tracks.json](../release/tracks.json)，各领域索引里也有对应列。
