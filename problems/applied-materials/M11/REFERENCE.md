<!-- 由 release/tools/build_problems.py 自 tasks/M11-flibe-tritium/execution/public-source-v2/RESEARCH.md 生成，勿手改 -->

> M11 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M11 FLiBe 氚结合公开输入闭包复查（source-v2）

已取得原论文官方 PDF、完整源包与同包 SI(S1–S7)，并静态检查作者关联代码的新公开入口。电荷、计量、电子数、自旋与浴构造规则已核实；原坐标和 Hamiltonian 输入未闭合。本轮完成来源审计，原应用保持 incomplete，SCF/FCI/VQE/量子线路/shot/QPU 执行均为0。文献数值没有登记为新模拟。

官方源包有20个目录条目、19个文件：ms.tex、ms.bib、00README.json和16张图。包中没有XYZ/CIF/HDF5/FCIDUMP；S1“Geometries”只描述构型生成与球棍图，没有Cartesian表。S4.2说明Vayesta会写自包含片段HDF5，但没有随包发布或给出存储地址。具体包清单、内容hash及来源获取日志已保存。[原文与SI](https://arxiv.org/html/2606.30402v1)，[官方源包](https://arxiv.org/src/2606.30402v1)

|原物种|原子数|电荷|总电子|Nα=Nβ|基组AO数|
|---|---:|---:|---:|---:|---:|
|Li6Be3F12|21|0|138|69|378|
|Li6Be3F13T|23|0|148|74|398|
|[Li6Be3F13]−|22|−1|148|74|396|

这三组均是原文气相闭壳单重态。电子数是核电荷减总电荷的独立算术核验；6-31+G(d)的原子基组metadata独立给出Li/Be/F各18、H为2个球谐AO，与SI计数逐项一致，没有构造假坐标或做原子电子能计算。T的Z=1；电子Hamiltonian的同位素质量不改变固定核势，ZPE、核量子效应和自由能仍不在本任务结论内。

原结合差为 E(Li6Be3F13T,148e,0,R)−E([Li6Be3F13]−,148e,−1,R去T)。阴离子保留其他原子的完全相同坐标，移除的是裸T+核，不是中性T原子，也不重新优化参考。两边电子数相同，不能误设为147e或扣掉中性氚原子能。原AO398/396说明两边basis数量不同；本文未见counterpoise/BSSE规定，未来不能静默加ghost-T并仍称原协议。[定义见SI S1/S7](https://arxiv.org/html/2606.30402v1#S1)

原embedding已明确到规则层：6-31+G(d) RHF→每原子IAO片段→RHF Schmidt DMET bath→MP2占据与虚BNO扩展，η=1e−5；保留虚占据>η、占据BNO<2−η。实际各fragment电子扇区、局域轨道、积分与投影系数仍缺。全簇能量是 E_RHF + Tr[FΣΔγ(i)] + Σe2c(i) 的民主分区cumulant重构，绝不能把片段本征能直接相加或相减作为氚结合能。仅有一段H可以核验局部solver，却不能恢复整簇结合或bath误差。

新入口复查：作者共同维护的Quantum-Fragment-Methods主分支固定commit `dc43754a7d69ffe5261b267efff49375a60087e0`，完整tree未截断。示例为H2/N2/alanine；静态读取其EWF实现显示HDF5读取`eris`、`c_frag`、`c_cluster`及global overlap/Fock，说明重构需要投影与环境数据。main的extSQD是NotImplemented stub；这不能代表作者实际私有/其他版本流程不存在。[作者关联公开代码](https://github.com/qiskit-community/quantum-fragment-methods/tree/dc43754a7d69ffe5261b267efff49375a60087e0)

官方QCE教程新增的直接链接指向IEEE_QW_2026分支，固定commit `b66585dbb7358c7c181869375a3c709f550111b2`。其HDF5和notebook明确是glycine/STO-3G，另有alanine/proteasome输入，没有本案FLiBe。只读取notebook JSON/cells，不执行安装命令、代码或pickle；未下载并求解无关HDF5。[官方教程](https://qiskit-community.github.io/qce26-tut-deploying-fermionic/)，[固定示例](https://github.com/qiskit-community/quantum-fragment-methods/blob/b66585dbb7358c7c181869375a3c709f550111b2/examples/notebook_demos/ewf_sqd_demo/ewf_sqd.ipynb)

三次recursive API响应的`sha`等于所选commit，而与commit metadata的`commit.tree.sha`不同；本次没有把两值并列记录当作整棵树与commit一致性已通过。请求URL与差异保存在validation。实际取得的6个固定commit文件均独立计算Git blob SHA1并与其所列path/blob值一致；只支持这些具体文件的内容身份，整棵tree绑定未独立建立，目录缺失结论应限于实际响应及取得的数据包。

原arxiv ID和原题名的Zenodo查询均0；Figshare原arxiv DOI查询为空，GitHub原ID查询0。IBM原研究博客只有原文/方法及展望链接，没有输入数据链接。以上只约束当前明确来源与查询范围，不证明公开资料绝对不存在，也不能靠图中布局反推三维坐标。[IBM原研究说明](https://www.ibm.com/quantum/blog/molten-salts-fusion-quantum)

最小可执行输入是一个真实FLiBe原片段的普通HDF5/FCIDUMP，附nα/nβ、h1/ERI张量顺序、轨道身份、核/冻结常数及来源版本。优先原T中心或其他实际小片段，以同H FCI/强选定CI验收实际线路及有限shot，并明确局部结果与全结合的边界。若评估结合/η收敛，还必须取得至少一组原23/22配对坐标及完整片段系数/global Fock/overlap/RDM重构定义。缺这些输入时不冻结任意模型，不把其他分子数据作为本案量子组件。

未来真实组件仍须先冻结单线程≤600CPU秒、设计≤2GB内存、强经典同H参考、物理模型/求解/测量误差拆分和线路成本；实际peakRSS需独立记录，不能把设计值充当实测。当前没有科学solver作业和peakRSS，因此不声称预算内完成量子算法或有效结合计算。

独立来源hash/物种/原文接口/仓库身份核验54项全通过。一次自写文本文字断言的格式错误已修复，失败脚本和原因保留；它不涉及SCF或科学结果。新manifest是获取来源后的audit清单，不是假称量子预冻结。旧文件、LATEST与共享表未改。
