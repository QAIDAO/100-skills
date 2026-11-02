# B32 · 血蓝蛋白 Cu₂O₂：双铜氧桥的超交换与杂质模型求解

> 2026-10-30 新增：替换移出的量子机器学习题，仅文献整理的开放题，本项目没有对本题执行任何计算。

## 研发决策与价值

判断双铜—氧桥超交换中的多体关联是否改变氧合血蓝蛋白的磁结构与单重/三重态排序，从而决定含双铜氧桥的金属蛋白何时必须用多位点杂质求解器，而不能只靠 DFT(+U) 或单位点 DMFT。

## 模型与可观测量

- 研究体系：氧合血蓝蛋白（oxyHc）58 原子模型的 Cu₂O₂ 核：两个 Cu 为杂质位点，过氧桥与咪唑配体为浴；6、8、14 比特的 Anderson 杂质模型哈密顿量
- 可观测量：杂质模型基态能、杂质间自旋—自旋关联 ⟨Sz·Sz⟩、改变 U 时的单重—三重态交叉
- 规模：硬件运行限于 6 比特（Quantinuum H 系列与 IBM 设备），14 比特只在模拟器上；完整蛋白环境、DMFT 自洽与有限温度都没有进入量子部分

## 量子—经典工作流（建议，未运行）

DFT 加簇 DMFT 给出双杂质 Anderson 模型参数→VQE（广义 UCCSD 等拟设）求杂质加浴的基态与杂质间自旋关联→结果回到 DMFT 自洽（原文只做了单次杂质求解，自洽未闭合）

## 强经典基线

同一哈密顿量的精确对角化与 Lanczos 杂质求解器（原文 DMFT 所用）、DMRG 或选态 CI；化学侧对照 NEVPT2/CASPT2 QM/MM 与 broken-symmetry DFT

## 已有文献与证据边界

2024 年研究沿用 al Badri 等的 oxyHc DFT+DMFT 模型，把双杂质 Anderson 模型写成 6–16 比特哈密顿量并用 VQE 求解：Quantinuum 真机上 6 比特、广义 UCCSD 加 SPSA 收敛到精确值 0.485% 以内；IBM 真机的 6 比特运行陷入平台，带同设备噪声模型的模拟器也不收敛。6 比特杂质自旋关联精确值 −0.307，自旋守恒 UCCSD 得 −0.314，广义 UCCSD 在三种比特排布下分别为 −0.169、−0.018、−0.078；全局去极化噪声下，5% 的能量误差可对应高达 80% 的关联误差。

局限：6 比特规模可以精确对角化，不构成量子优势。论文摘要外的报道称用了零噪声外推，但正文没有给出相应结果；代码仓库只写「GitHub Repository」，没有链接；IBM 硬件运行在图 6 图注里是陷入平台，在讨论部分却写成明显收敛，两处不一致。只做了单次杂质求解，没有闭合 DMFT 自洽。

## 与已有题目的区别

最接近的现有题目：B31、F11、F13。B31 是细胞色素 c 氧化酶 Fe–Cu 双核中心的 O₂ 还原与质子泵；F11、F13 是晶格材料的 DMFT 杂质求解。这里是生物双铜氧桥的超交换与自旋关联。

## 可执行试点（建议，未运行）

用附录公开的 6、8、14 比特 Pauli 哈密顿量做精确对角化，作为能量与 ⟨Sz·Sz⟩ 的基准；在同一哈密顿量上比较能量与自旋关联对噪声和比特排布的敏感度，再估算把杂质求解接回 DMFT 自洽的成本。

## 文献与读取范围

- Q1 [Quantum Embedding of Non-local Quantum Many-body Interactions in Prototypal Anti-tumor Vaccine Metalloprotein on Near Term Quantum Computing Hardware](https://arxiv.org/abs/2410.12733)（2024），预印本；期刊版 Int. J. Mol. Sci. 26(4), 1550 (2025)；读取范围：full_text。oxyHc 双杂质 Anderson 模型（U=0.2934 Eh、J_Hund=0.02939）的 6–16 比特 VQE；Quantinuum 6 比特收敛到精确值 0.485% 以内，IBM 真机陷入平台；表 II 自旋关联精确值 −0.307 与各拟设、排布结果；附录给出 6、8、14 比特 Pauli 哈密顿量；代码链接缺失。
- R1 [Revisiting Oxygen Transport Features of Hemocyanin with NEVPT2 Level QM/MM Calculations](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11866748/)（2025），期刊论文；读取范围：search_excerpt。QM[NEVPT2]/MM 给出过氧到双(μ-氧)异构化势垒低于 DFT 的预测，蛋白环境中过氧式仍更稳定；作为化学侧经典对照。

读取范围：full_text 表示已取得全文并逐条核对本题引用的论断；abstract 表示只读到摘要或仓库页；search_excerpt 表示只读到检索摘录（付费、人机验证或无法连接）。2026-10-30 完成全文核对。
