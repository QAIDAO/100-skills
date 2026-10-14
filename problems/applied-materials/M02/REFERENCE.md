<!-- 由 release/tools/build_problems.py 自 tasks/M02-diels-alder-barrier/execution/public-coordinate-v2/RESEARCH.md 生成，勿手改 -->

> M02 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M02：真实原反应几何上的量子候选负结果

本轮从原方法明确引用的坐标论文官方 SI 取得乙烯、环戊二烯和其 TS1A，完成原 aug-cc-pVTZ 基组下的真实反应子实验。冻结 EF/QSE 候选的精度门均失败：同模型 CASCI 势垒 45.522554 kcal/mol，EF 为 64.367448，QSE 为 47.023255；误差分别为 18.844894 和 1.500701 kcal/mol，均超过事前 1 kcal/mol 门。真实输入已推进到量子线路和数值，不意味着原材料应用完成。QPU 调用为 0。

## 输入和模型

[原研究](https://arxiv.org/html/2403.08107v1)及[正式出版页](https://doi.org/10.1039/D4CP01314J)使用 Levandowski/Houk 的[2015 坐标来源](https://doi.org/10.1021/acs.joc.5b00174)。本轮通过[ACS 官方 Figshare SI](https://acs.figshare.com/articles/journal_contribution/Theoretical_Analysis_of_Reactivity_Patterns_in_Diels_Alder_Reactions_of_Cyclopentadiene_Cyclohexadiene_and_Cycloheptadiene_with_Symmetrical_and_Unsymmetrical_Dienophiles/2180551)的公共 API article 2180551/file 3814474 下载原 PDF，MD5 `28ab3a5d52b6ff5cf0f90d4eae213989` 与 metadata 一致。几何为原 SI 的 Ethylene、Cyclopentadiene、TS1A-Cyclopentadiene+Ethylene，未优化、未替换体系；product 坐标保留但不执行。RSC 直接网页访问拒绝已记录，没有绕过。源文件、元数据、公开下载日志与哈希均保留。

单 CPU 预处理采用 DF-RHF (`aug-cc-pvtz-jkfit`) 和 native DF-MP2 (`aug-cc-pvtz-ri`)。未松弛 MP2 1-RDM 的默认表示经本地 PySCF 原生实现核查为 MO；本轮的 `C_RHF @ eigenvectors` 与原生 `make_natorbs` 相同，按自然占据降序排序。选取 HONO/LUNO 周围的乙烯 CAS(2e,2o)、环戊二烯 CAS(4e,4o)、TS CAS(6e,6o)，零基索引分别 [7,8]、[16,17,18,19]、[23,24,25,26,27,28]。低占据虚轨道舍弃、低索引核心轨道冻结双占据。原文较大 AS(8,8) 按 HONO/LUNO 前沿选取，较小 AS(6,6) 强调 π/π* 子集。本轮明确冻结为相应电子数的连续前沿 NO 小空间，未逐个核对原文图1的 π 轨道身份或作者 MO 系数；不得据接近原文45.7 kcal/mol宣称原活性轨道完全一致。三个几何独立排序，没有跨几何最大重叠跟踪。自然占据 trace 分别为 16、36、52，NO 的 S 正交误差小于 3e-11。

CASCI 使用密度拟合后的积分，属于明确定义的近似模型；未证明与原作者未拟合积分等价。52=16+36 个总电子、6=2+4 个活性电子和23=7+16 个冻结核心轨道均相加一致。势垒明确是 `E(TS)-E(ethylene)-E(cyclopentadiene)`；无零点、热力学、熵或 BSSE 修正。未执行原更大 CAS(8,8)、PT2、furan 环境分支或强经典全基组关联法。因此下面的求解器误差只针对同一已冻结小空间 Hamiltonian。

## 实际线路与基准

冻结候选是 rank-2 EF 变体：相同的 α/β 邻接 Givens 守粒子数线路，2 层、`2(n-1)+1` 个参数，两项参考分别为 HF 和 HONO→LUNO 激发；未用 FCI 支持挑选参考。三个固定种子 61/62/63 用状态向量能量优化，保留全部参数和结果。全部 9 次 BFGS `success=False`（precision loss），没有掩盖优化器退出状态。独立 Qiskit 线路幅度核对通过；每分支 n=2/4/6 量子比特、通用编译 CX=4/12/20、深度11/26/36。该浅层变体与论文旧硬件 Ansatz 不相同，不能视为对原协议的逐门复现。

同模型 CASCI/完整固定 Nα=Nβ 扇区对角化是强经典基准，维度为 4/36/400。QSE 用 EF 态的 occupied→virtual 同自旋单/双激发向量，通过**精确经典矩阵元**构建 Gram/Hamiltonian 并白化，不是有限 shots 下的 QSE 测量实验。矩阵量子测量组数、执行次数与采样噪声未实现，成本未知。Gram 阈值1e-9，秩4/27/118，保留条件数1.457/1.446/1.353；独立重建最低根、能量与投影残差（最大4e-14 Ha）通过。FCI、EF 和 QSE 态的 N/Sz、归一化、S² 以及父级独立 fermionic ladder 核查通过，S²约0。QSE 降低误差但仍不是完整 CASCI 基态。

| 点 | CASCI / Ha | EF 对 CASCI 误差 / Ha | QSE 对 CASCI 误差 / Ha |
|---|---:|---:|---:|
| 乙烯 | -78.0894212863944 | <1e-12 | <1e-12 |
| 环戊二烯 | -192.9060489331100 | 0.024951126 | 0.000141349 |
| TS | -270.9229254156215 | 0.054982375 | 0.002532868 |

TS 的 QSE 单点误差超过冻结 1e-3 Ha 门；EF 在环戊二烯和 TS 也失败。QSE 势垒误差1.500701超过冻结1 kcal/mol门，不因接近阈值而追调轨道或改门。

父级事后 Schmidt 诊断（本地证据，未随题库发布）使用精确 FCI 态，前两项权重分别为环戊二烯0.967827、TS0.942100；范数最佳 rank-2 截断能量误差0.023454/0.036716 Ha。这提示表达能力限制，不能一概将冻结 EF 失败归因于优化器。此诊断含 oracle 信息，不是独立可制备候选，也不是变分最优 rank-2 能量下界；截断态未额外核查自旋。

## 有限读取与成本

分支线路不足以提供联合 αβ 读取分布。本轮有限读取使用明确冻结的 **2n 比特 coherent 变体**：将经典重构 EF 纯态用 Qiskit `initialize` 制备，再模拟计算基测量。三个点为4/8/12量子比特，通用编译 CX=11/247/4083、深度24/496/8168，此外有15/255/4095个 U 和4/8/12个 reset。这是指数成本的经典状态装载，不是论文6比特 EF 硬件测量协议，也不支持量子优势主张。门数没有特定硬件路由或噪声，不能当物理运行成本。

每点 64/256/1024 shots、三个种子，同预算 uniform fixed-N 对照，合计54组、24,192 shots；每组 SeedSequence 含种子、几何、shots、候选标签，彼此独立随机流。读取支持上的精确投影对角化是经典后处理。本轮 1024 shots 的 TS EF 支持仅16–21/400，能量误差0.0410–0.0506 Ha；uniform 支持358–372，误差0.00145–0.01265 Ha。该 EF 分布在此预算劣于 uniform，完整400维 CASCI依然是更强对照。投影支持保留N/Sz但会破坏S²；原始计数和逐组S²全部保存，不能把采样可行率1称为自旋可行率1。

计算作业单 CPU 运行153秒，乙烯/环戊二烯/TS分别约4.60/21.56/124.81秒。保留 SCF 检查点和作业退出日志，exit0。这是模拟器和经典预处理耗时，QPU耗时、QSE物理测量、误差纠正资源未知。完整资源字段见 resource-ledger.json。

## 物理模型敏感性与 SCF 警告

**额外事后诊断**：同批点的 DF-RHF、DF-MP2 总能量、CASCI 势垒为43.124185、3.463968、45.522554 kcal/mol，差异很大。DF-MP2不是精确真值，这些方法差异也不是新冻结验收门。原任务需要动态关联和更大活性空间等验证；QSE相对小模型的1.5 kcal/mol差异不能掩盖这一模型不确定性。

SCF 均达到1e-10能量收敛设置，但 AO 重叠矩阵条件数约2.20e6/4.91e6/1.10e7。TS 日志和stderr的近线性相关警告保留；其最后常规迭代 ΔE=-7.97e-11 Ha、梯度3.46e-6，extra cycle进一步收敛。NO正交、Hermitian Hamiltonian、CASCI根残差等数值核验通过，仅支持本次有限精度内部一致性。**未做 RHF Hessian 稳定性、diffuse basis/线性相关阈值或 DF→常规积分收敛检查**，不能把 SCF converged 等同于物理稳定或完备基组可信。

停止条件已经到达：真实输入已闭合到这一原反应小空间，冻结候选明确失败，所有失败和未验证项保留。后续若推进原应用，应先验证轨道/基组与动态关联模型，或事前冻结表达能力更强的候选；不通过追调当前阈值或使用其他分子替代。

冻结 manifest（本地证据，未随题库发布） · results（本地证据，未随题库发布） · 独立 validation（本地证据，未随题库发布） · source/provenance（本地证据，未随题库发布） · summary（本地证据，未随题库发布） · 父级态核查（本地证据，未随题库发布）
