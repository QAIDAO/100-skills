<!-- 由 release/tools/build_problems.py 自 tasks/M04-battery-xas/execution/public-input-audit-v2/RESEARCH.md 生成，勿手改 -->

> M04 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M04 原公开输入闭包复查

审计完成，原材料谱实验仍缺输入，未运行量子线路、SCF、谱计算或 shots。本次结果改变了下一步：M04 不应直接借用 M05 的 51 原子封端模型；也不应把 N2 官方示例作为 Li2MnO3 复现。

## 已闭合的定义

2024 原文指定 Materials Project mp-1173926、数据库 v2023.11.1，提取裸 Li4Mn2O（7 原子），使用 cc-pVDZ/HF 和 PySCF AVAS。资源目标为 CAS(22e,18o)，AVAS 包含 Mn 3d、Li 2s、O 1s/2p，阈值调整到该空间但未报告数值。[2024 原文](https://arxiv.org/html/2405.11015v1)

2025 原文真正的材料谱模拟是更小的 CAS(14e,11o)，10 个 Mn 3d 加 O 1s，22 系统比特和 1 Hadamard 辅助比特；jmax=50，S=5000，谱窗口 2 Ha，tau=pi/4 Ha^-1，二阶 Trotter、Delta=tau。作者用延长演化时间检查材料谱收敛，未给此材料谱的完整经典精确参考。N2/STO-3G 1.077 Å、CAS(14e,10o) 的 250 根 FCI 谱比较是另一体系；附录也有较小 LiMnO 活性空间的积分近似误差诊断，但均未导出数值 H。[2025 源版本](https://arxiv.org/abs/2506.15784v2)

v2 PDF 与本轮取得的 TeX 摘要/正文统一写 Toffoli 成本；arXiv 摘要页元数据仍写 T gates。保留差异，以 PDF/TeX 为本版本资源计数来源，不把两种门数当成等价量。

## 原输入缺口与停止边界

原 7 原子 XYZ、晶体提取位点/去锂选择、簇电荷/自旋、AVAS 阈值和轨道排序未闭合。也未取得同一轨道序下 h1/eri/常数项、三个偶极矩阵、O 1s 索引、准确 CVS mask、基态及 CDF 数值耦合/旋转。正文的“去掉小 core-valence 积分”不能替代数值 mask，不能自行删所有含核/价指标的积分。

原任务还要求区分两个结构/机制；单一作者簇即便输入闭合，也只支持单结构的谱算法组件，不足以证明氧空穴、O-O 成键或结构退化的判别。下一最小输入是作者原 CAS(14e,11o) 张量和偶极/CVS bundle，或完整簇 XYZ+电子态/AVAS 定义；若要机制判断，还需第二个真实结构与同口径参数。11 轨道的完整固定自旋精确参考比 M05 CAS(8,7) 更大，本轮不承诺未测量的 300 秒预算。

## 共享来源审计

两案共享 Li2MnO3 氧 K 边的物理主题，但不能假定共用同一个电子哈密顿量。2024/2025 XAS 是裸 Li4Mn2O/cc-pVDZ；2025 EELS 是 H 封端 Li4Mn2O19H26/PBE0/ANO-RCC-VDZP。图形示意与晶体编号不足以恢复这两种簇的原数值输入。

本轮取得 arXiv:2506.15784v2 官方完整源包，13 项为 README、TeX、参考文献、图形及目录，没有 XYZ、FCIDUMP、数组文件或运行代码。另取得官方 PennyLane XAS demo 并只做静态检查：它是 N2/STO-3G、1.0 Å、CAS(4e,5o)，不能代替材料任务。精确题名/论文编号/正式 DOI 的已记录 GitHub、Figshare、Zenodo 查询未找到输入；这是查询范围内的结果，不证明作者数据在全网不存在。宽泛 eels/DOI 片段查询确实有大量无关记录，不能记成零结果。

材料数据库两个公开页均返回 403，2024/EELS PDF 和部分 arXiv 源请求返回 406，AIP 正式 EELS 文本返回 403，均记录后停止，不绕过。EELS 正式发表为 JCP 163, 244110 (2025)，DOI 10.1063/5.0300557；Crossref 元数据可得，但正式正文、数据可用性声明和 SI 未核实。可读预印本文本未给可直接执行的原积分/偶极矩阵下载入口。

完整请求见 source-index.json（本地证据，未随题库发布），哈希见 post-run-provenance.json（本地证据，未随题库发布），参数复算见 m05-time-step-consistency.json（本地证据，未随题库发布）。静态源内容和逐项检查见共享 followup 目录。未修改任何 LATEST 或共享汇总。
