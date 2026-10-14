<!-- 由 release/tools/build_problems.py 自 tasks/B28-cobalamin-radical-sam/README.md 与 tasks/catalog.json 生成，勿手改 -->

# B28 · 维生素 B12 与自由基 SAM 酶：Co–C 断键与自由基态序

> 开放题 · 生物医药 · 金属辅因子 / 自由基酶

## 题面

| 环节 | 内容 |
|---|---|
| 研究体系 | 甲基钴胺素与腺苷钴胺素的 Co–C 键均裂，以及自由基 SAM 酶中 [4Fe–4S] 簇驱动的 S–C 断键 |
| 可观测量 | Co–C 与 S–C 断键能垒、键离解能差、自由基产物的自旋态序 |
| 经典基线 | DFT（BP86 与 B3LYP 对 Co–C 键强的系统偏差）、IMOMM/QM/MM 加溶剂模型；CASSCF/CASPT2、NEVPT2、DMRG、选定 CI |
| 量子方法的角色 | 对 Co 中心或 Fe–S 簇的断键活性空间做嵌入，再用 QPE/qubitization（远期）或小规模 VQE/SQD（近期）求势垒电子能；构象门控与反应网络留在经典端（提案） |
| 研发决策 | 判断甲基钴胺素与腺苷钴胺素断键差异、以及自由基 SAM 断键选择性，是否来自强相关电子结构，从而决定是否值得投入高精度计算。 |

## 什么算解

一份解法满足以下五点即可提交审核。负结果同样接受，只要过程可复现、结论有依据。

1. **模型对应**：说明所用模型或数据如何对应「甲基钴胺素与腺苷钴胺素的 Co–C 键均裂，以及自由基 SAM 酶中 [4Fe–4S] 簇驱动的 S–C 断键」，列出简化与近似。
2. **可观测量**：报告「Co–C 与 S–C 断键能垒、键离解能差、自由基产物的自旋态序」，附单位与不确定度。
3. **经典对照**：在同一模型或数据上，与「DFT（BP86 与 B3LYP 对 Co–C 键强的系统偏差）、IMOMM/QM/MM 加溶剂模型；CASSCF/CASPT2、NEVPT2、DMRG、选定 CI」中至少一种方法比较。
4. **可复现**：提供代码、环境、随机种子、输入来源与哈希，以及计算资源和成本；用到 QPU 时注明设备与 shots。
5. **研发决策**：说明结果能否支撑「判断甲基钴胺素与腺苷钴胺素断键差异、以及自由基 SAM 断键选择性，是否来自强相关电子结构，从而决定是否值得投入高精度计算。」，以及还缺什么证据。

本题的细化标准欢迎在 issue 中讨论；被采纳的讨论结论会写入后续版本。

## 现有参照

本题暂无本项目的数值执行记录，下面只有文献整理。

### 原案例说明

### B28 · 维生素 B12 与自由基 SAM 酶：Co–C 断键与自由基态序

> 第三轮补题（2026-10-14）：仅文献整理的开放题，本项目没有对本题执行任何计算。来自原问题单 B06。

#### 研发决策与价值

判断甲基钴胺素与腺苷钴胺素断键差异、以及自由基 SAM 断键选择性，是否来自强相关电子结构，从而决定是否值得投入高精度计算。

#### 模型与可观测量

- 研究体系：甲基钴胺素与腺苷钴胺素的 Co–C 键均裂，以及自由基 SAM 酶中 [4Fe–4S] 簇驱动的 S–C 断键
- 可观测量：Co–C 与 S–C 断键能垒、键离解能差、自由基产物的自旋态序
- 规模：Co 卟啉类咕啉环加轴向配体的截断模型；Fe–S 簇为多金属中心，活性空间预计远超精确对角化范围

#### 量子—经典工作流（建议，未运行）

对 Co 中心或 Fe–S 簇的断键活性空间做嵌入，再用 QPE/qubitization（远期）或小规模 VQE/SQD（近期）求势垒电子能；构象门控与反应网络留在经典端（提案）

#### 强经典基线

DFT（BP86 与 B3LYP 对 Co–C 键强的系统偏差）、IMOMM/QM/MM 加溶剂模型；CASSCF/CASPT2、NEVPT2、DMRG、选定 CI

#### 已有文献与证据边界

经典侧：IMOMM 计算比较了两种钴胺素的 Co–C 键离解能并指出溶剂效应必要；多参考方法对断键势垒的描述仍有争议。量子侧仅有同类金属酶活性空间的资源估计先例。2026-10-14 检索未见针对该具体体系的量子计算研究（检索不穷尽）。

局限：不同泛函对 Co–C 键强给出相反趋势，经典参照本身需先收敛；完整反应网络和构象门控仍须经典计算。

#### 与已有题目的区别

最接近的现有题目：B04、B01、B25。核心是 Co–C 与 S–C 断键及自由基态序；B04 是铁硫簇电子传递，B01 是固氮酶，B25 是单铁氢化酶。

#### 可执行试点（建议，未运行）

先在同一截断模型上比较 DFT、NEVPT2 与 DMRG 的 Co–C 离解能，确认多参考特征的强弱，再划定量子求解的活性空间。

#### 文献与读取范围

- R1 [Computational study on the difference between the Co–C bond dissociation energy in methylcobalamin and adenosylcobalamin](https://iciq.org/research/publication/computational-study-on-the-difference-between-the-co-c-bond-dissociation-energy-in-methylcobalamin-and-adenosylcobalamin)（2005），期刊论文；J Biol Inorg Chem 10, 509；读取范围：search_excerpt。IMOMM 计算两种钴胺素的 Co–C 键离解能，指出需要溶剂效应才能重现溶液中的趋势。
- R2 [Challenges in the simulation of enzymatic transition states with emerging multireference character](https://arxiv.org/abs/2607.09769)（2026），预印本；读取范围：search_excerpt。讨论酶过渡态中出现的多参考特征及其模拟难点。
- Q1 [Reliably assessing the electronic structure of cytochrome P450 on today's classical computers and tomorrow's quantum computers](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9499570/)（2022），期刊论文；PNAS 119(38) e2203533119；读取范围：abstract。同类金属酶活性空间的 DMRG+NEVPT2/CCSD(T) 对照与 qubitization 相位估计资源估计；作为量子路线的方法先例，不是本题体系。

读取范围中 search_excerpt 表示只读到检索摘录，abstract 表示读到摘要页；均未读全文。

## 如何提交

按 [CONTRIBUTING.md](../../../CONTRIBUTING.md) 把解法放在 `solutions/B28/<你的名字>-<短名>/`，格式见 [解法模板](../../../solutions/_template/SOLUTION.md)。被采纳的解法会按 [沉淀规则](../../../skills/README.md) 提炼为可复用的 skill。
