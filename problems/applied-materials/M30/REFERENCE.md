<!-- 由 release/tools/build_problems.py 自 tasks/M30-cgc-polymerization-resources/execution/public-cgc-fno-v2/RESEARCH.md 生成，勿手改 -->

> M30 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M30 公开输入与实验边界


已取得原文所引 CGC(1) 的真实公开 CIF，并完成四个有来源的量子组件；模型与完整 CASCI 精度门均失败。原应用尚未完成。本次没有修改 LATEST、共享表或旧 revision。

原资源工作指向 Arriola 的 CGC(1)，固定最高三个占据轨道估算 FNO 宽度，未扫描全部增量。其数据声明指向文内数据；公开原稿没有可直接执行的 CGC 分子输入或积分。[原论文 v2](https://arxiv.org/abs/2002.07901v2)

沿原参考文献取得 ACS 官方 Figshare 的 `ja070061y_si_002.cif`，`data_1` 对应 C17H33NSiTi；配套 SI Table19(S73)给出化合物1的正交 Pnma 晶体。两文件均通过官方 metadata 的 MD5 和本地 SHA256 校验。[原晶体 CIF](https://doi.org/10.1021/ja070061y.s002)，[原 SI](https://doi.org/10.1021/ja070061y.s001)

本次输入不是作者原分子处理的精确复现。完整占据位点按原镜面 y=.5−y 展开并去掉特殊位置重复；半占据 Si/tBu 采用 CIF 所列一个方向，未覆盖镜像无序。H10 group2 为预冻结主分支 A2，group3 为敏感性 A3；选择不依据能量，没有优化几何。两个分支均53原子/178电子，全部位点是 Ti 中心的最近镜像，分数位移小于半晶格；连接图完整，所有H连C，最短接触0.978955Å。作者的无序/氢/晶体到孤立分子处理仍未知。

冻结使用中性单重态完整分子 cc-pVDZ(478AO)，RHF/CAS/MP2 均采用 weigend 辅助基的 Gaussian density fitting。保留 canonical HOMO、HOMO−1、HOMO−2（zero-based86–88）；冻结其余86个占据轨道。由该3占据轨道的 restricted DFMP2 全389虚轨道 MO 一阶密度生成 FNO，按占据数降序固定取 top3/top6，所选虚轨道子空间单独半正则化。所选三个占据轨道均保留，没有按答案调整空间。

冻结时间 2026-10-04T00:03:05.976426Z，作业开始00:03:06Z。预算600CPU秒与600wall秒双硬限，无重试或延长。A2两个点全部结束后才运行A3。每点为6e6o/6e9o，完整 Ms=0 CASCI 维数400/7056，精确配对参考20/84。量子算法为一层有序 pair-UCC，3个初始占据轨道依次到所有选定虚轨道，9/18参数、固定seed41/42/43，BFGS最多80次迭代。实际12/18q Jordan–Wigner 双激发以8个对易 Pauli 旋转实现；不是精确求解器输出冒充线路。

冻结门分别为：所有seed对pairedCI及fullCASCI误差≤1mHa；粒子数6/单重态/归一误差≤1e−10；32768shot/term单能量解析SE≤1mHa；FNO占据权重≥99%、截断/全虚轨道restrictedMP2差≤1mHa。99%失败仍执行小空间组件作为截断诊断。8192与32768shot/term各3次重复，优化使用精确模拟，最终测量独立模拟；真值没有参与轨道筛选。

|分支/虚轨道|FNO权重|MP2遗漏(mHa)|fullCASCI(Ha)|VQE−fullFCI(mHa，最大seed)|VQE−pairedCI(μHa，最大seed)|32768 SE(mHa，最大seed)|
|---|---:|---:|---:|---:|---:|---:|
|A2/top3|54.415%|37.171|-1849.272250319|6.968|0.814|1.226|
|A2/top6|77.319%|23.073|-1849.290719922|21.585|1.259|2.526|
|A3/top3|54.409%|37.389|-1849.277027506|7.373|0.813|1.214|
|A3/top6|77.392%|23.125|-1849.295708698|22.351|1.213|2.486|

所有四点：输入/SCF/fullCASCI/粒子数/自旋/线路核验通过，pairedCI误差门通过；fullCASCI误差、32768单能量SE、FNO99%及MP2截断门失败。三seed均返回优化器 precision-loss，不能称梯度收敛；不过与同空间精确配对解仅差0.8–1.3μHa。因此7–22mHa的完整CAS误差主要是seniority-zero表达限制，不宜归咎优化器。完整FCI在配对子空间的权重为99.109/97.414/99.055/97.303%；这项使用精确参考的事后诊断没有参与优化，也不是新候选。

A2/A3 完整DF-RHF能量分别−1849.249399136/−1849.254105737Ha，最终梯度约4.99e−7；重叠矩阵条件数1.82e5，保存了Fock/密度/轨道/checkpoint，未做RHF稳定性或其他电荷/自旋态扫描。独立核验确认CAS冻结常数使HF determinant恢复完整DF-RHF，残差≤2.51e−12Ha。完整CASCI收敛，独立N/S²和Hamiltonian作用核验通过。A3相对A2的fullCAS总能差top3/top6约−4.78/−4.99mHa，仅是H10无序分支敏感性，不能当反应能。

同一新DF模型达到99%需要A2 62/A3 61虚轨道，即130/128q；原文126q对应60虚轨道，未精确复现。原因可能包括未知几何/无序/氢处理、density fitting及软件约定，当前不能分配因果。本次top3/6仅54.4%/77.3%，全389虚轨道restrictedDFMP2相关能−.05436/−.05463Ha，而遗漏23–37mHa；MP2只作扰动诊断，不是精确完整虚空间真值。原文小分子MI-FNO还使用MBPT2补偿缺失相关能；当前冻结测试是raw截断H能量与同H完整CASCI，不把MP2补偿加到量子能量门，也不据此推断全虚空间高阶准确度。更大的top6空间有更多broken-pair相关，配对误差随之增加，不能据小空间pairedCI拟合良好称空间受控。

12/18q主线路分别1008/2880 CX、深度1318/3505，均未含连接路由、纠错或硬件噪声；测量observable分别52/118项。独立完整逐门 sparse computational-basis 模拟（没有每门投影到配对空间）与保存压缩态最大残差8.86e−14，粒子数/配对泄漏0；最大中间support224/1008，没有分配完整2^18 dense向量。原始结果继承字段名`full_original_24q_statevector_simulated`和`all_generator_220ket_JW_residual`只是旧标签，实际宽度与维数由`algorithm_data_qubits`/`paired_propagation_dimension`给出，本次均为12/18q与20/84。

测量使用配对期望等价的物理Pauli lift，而非完整H在所有破对态上的相同算符；噪声泄漏时不能保证等价。observable系数绝对截断显式1e−12，JW生成器simplify显式atol1e−12/rtol0；某些单独XX/YY项离开粒子扇区，均值为0但方差保留。`plus1_counts`确为Pauli +1结果，不是计算基bit1。72个全局唯一SeedSequence随机流、125337600 term-shots均独立复现；QPU调用0。单能量SE是冻结门，未新增反应/差值SE验收，也无优化过程shot开销。

科学driver CPU101.220秒，watchdog wall103.665秒，单线程。peak RSS实测5.342GB；配置的PySCF max_memory2400MB是软内存估计，本次实际超出，不能宣称2.4GB硬限。独立saved-data核验另用3.57秒，796项全通过，没有重跑SCF或优化器。

完成的是原CGC1真实来源分子的HOMO3原始相关电子子问题。没有一/二占据子问题的inclusion–exclusion，故不是不可约三体Δε；没有117569项的总MI组合，没有原99%空间量子结果，没有反应物/TS/聚合势垒，也没有量子优势证据。本次明确采用Gaussian density fitting；原作者的积分与DF处理约定未完整公开，不能称原Hamiltonian精确复现。

原输入最小缺口是作者公开的CGC1孤立分子几何/无序处理与对应轨道/FNO/积分；原应用另缺反应路径和完整增量构造。下一合理实验需新冻结预算，优先给99%空间强经典基线并检验破对相关及MP2截断校正，再评估量子接口。当前负结果不支持直接升级到整套聚合催化任务。

来源访问：AIP与ACS原期刊页403、arXiv源包406均停止；合法公开作者PDF、arXiv HTML与官方ACS Figshare取得。Tangelo两个固定commit仅静态检查，现有公开示例未见CGC输入；空的DOI Figshare查询/1QBit public repo查询不是“数据不存在”证明。全部入口、版本、响应和hash见sourceledger。没有联系人、认证服务、付费QPU或执行下载的作者代码。

可复核交付：

- 冻结manifest（本地证据，未随题库发布）
- 原始结果（本地证据，未随题库发布）
- 精简结果表（本地证据，未随题库发布）
- 输入闭包与缺口（本地证据，未随题库发布）
- 来源访问台账（本地证据，未随题库发布）
- 独立复算脚本（本地证据，未随题库发布）
- 796项核验证据（本地证据，未随题库发布）
- 最终SHA256归档（本地证据，未随题库发布）
