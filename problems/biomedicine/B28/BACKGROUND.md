# B28 · 维生素 B12 与自由基 SAM 酶：Co–C 断键与自由基态序

> 第三轮补题（2026-10-14）：仅文献整理的开放题，本项目没有对本题执行任何计算。来自原问题单 B06。

## 研发决策与价值

判断甲基钴胺素与腺苷钴胺素断键差异、以及自由基 SAM 断键选择性，是否来自强相关电子结构，从而决定是否值得投入高精度计算。

## 模型与可观测量

- 研究体系：甲基钴胺素与腺苷钴胺素的 Co–C 键均裂，以及自由基 SAM 酶中 [4Fe–4S] 簇驱动的 S–C 断键
- 可观测量：Co–C 与 S–C 断键能垒、键离解能差、自由基产物的自旋态序
- 规模：Co 卟啉类咕啉环加轴向配体的截断模型；Fe–S 簇为多金属中心，活性空间预计远超精确对角化范围

## 量子—经典工作流（建议，未运行）

对 Co 中心或 Fe–S 簇的断键活性空间做嵌入，再用 QPE/qubitization（远期）或小规模 VQE/SQD（近期）求势垒电子能；构象门控与反应网络留在经典端（提案）

## 强经典基线

DFT（BP86 与 B3LYP 对 Co–C 键强的系统偏差）、IMOMM/QM/MM 加溶剂模型；CASSCF/CASPT2、NEVPT2、DMRG、选定 CI

## 已有文献与证据边界

经典侧：甲基钴胺素 Co–C 键离解能实验值 155 ± 13 kJ/mol，B3LYP 只给 91–117 kJ/mol；基组、相对论、溶剂、零点能与热校正都解释不了这一差距，BP86 与 MP2 给出 135–139 kJ/mol，两类泛函相差约 55 kJ/mol，且这一偏差在四吡咯类金属–碳键中普遍存在；腺苷钴胺素键能更低的实验趋势计算未能重现。IMOMM 研究指出溶液中的趋势需要溶剂效应。量子侧仅有同类金属酶活性空间的资源估计先例（P450）。2026-10-14 检索未见针对该具体体系的量子计算研究（检索不穷尽）。

局限：不同泛函给出的 Co–C 键能相差可达约 55 kJ/mol，经典参照本身需要先收敛；完整反应网络和构象门控仍须经典计算。

## 与已有题目的区别

最接近的现有题目：B04、B01、B25。核心是 Co–C 与 S–C 断键及自由基态序；B04 是铁硫簇电子传递，B01 是固氮酶，B25 是单铁氢化酶。

## 可执行试点（建议，未运行）

先在同一截断模型上比较 DFT、NEVPT2 与 DMRG 的 Co–C 离解能，确认多参考特征的强弱，再划定量子求解的活性空间。

## 文献与读取范围

- R1 [Theoretical prediction of the Co–C bond strength in cobalamins](https://lup.lub.lu.se/record/128729)（2003），期刊论文；J Phys Chem A 107, 7539；Lund 大学仓库 post-print；读取范围：full_text。MeCbl Co–C 键能实验 155±13 kJ/mol，B3LYP 91–117，各项校正都解释不了；BP86/MP2 给 135–139；B3LYP 比 BP86 低约 55 kJ/mol，归因于 HF 交换与 LYP，对 Co/Fe/Ni 四吡咯普遍成立。
- R2 [Computational study on the difference between the Co–C bond dissociation energy in methylcobalamin and adenosylcobalamin](https://iciq.org/research/publication/computational-study-on-the-difference-between-the-co-c-bond-dissociation-energy-in-methylcobalamin-and-adenosylcobalamin)（2005），期刊论文；J Biol Inorg Chem 10, 509；读取范围：search_excerpt。IMOMM 计算两种钴胺素的 Co–C 键离解能，指出需要溶剂效应才能重现溶液中的趋势（无开放全文）。
- Q1 [Reliably assessing the electronic structure of cytochrome P450 on today's classical computers and tomorrow's quantum computers](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9499570/)（2022），期刊论文；PNAS 119(38) e2203533119；读取 arXiv 2202.01244 全文；读取范围：full_text。CYP3A4 衍生模型：41 轨道 DMRG 给出 Cpd I 二重态比四重态仅低 0.02 kcal/mol，CCSD(T) 在多参考特征强的二重态上偏离 DMRG；最大 58 轨道活性空间的相位估计在 0.1% 物理错误率下约需 460 万物理比特、73 小时。方法先例，不是本题体系。

读取范围：full_text 表示已取得全文并逐条核对本题引用的论断；abstract 表示只读到摘要或仓库页；search_excerpt 表示只读到检索摘录（付费、人机验证或无法连接）。2026-10-14 完成全文核对，修正记录见题目说明。
