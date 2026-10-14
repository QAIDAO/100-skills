<!-- 由 release/tools/build_problems.py 自 tasks/M15-electrolyte-fault-tolerant/execution/public-salt-qpe-v2/report.md 生成，勿手改 -->

> M15 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M15：原公开盐分子输入与 QPE 组件验证

作者七种分子的完整几何已经取得，原记录中“作者几何缺失”的缺口可修正。本轮实际完成原 LiPF₆、PF₆⁻ 几何与派生 Li⁺ 原子上的小活性空间 QPE；所有预冻结的最终精度门通过。**原还原稳定性、断键势垒、SEI 科学目标仍未完成。** 派生气相离子解离能只是模型诊断，不是还原电势、含溶剂解离自由能或原论文发表的反应预测。

## 原公开输入与边界

[arXiv v2 正文](https://arxiv.org/html/2104.10653v2#S2.T1) Tables 1/2 给出 EC、LEC、LREC、FEC、LFEC、PF₆⁻、LiPF₆ 的四位小数 Å 坐标。原文 II.2/II.3 指定 PF₆⁻ 为 −1、其他分子中性，并列 STO-3G、DZ、6-311G、cc-pVDZ、cc-pVTZ。优化采用 PBE/VASP，520 eV 与固定 15 Å 空胞；这些是来源描述，本轮没有重复几何优化。原论文保留全部电子；本轮活性空间是另定的缩小模型。[官方出版全文](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevResearch.4.023019/fulltext) 已下载，独立解析 PDF 与 HTML 的全部 67 原子行数值完全相同。

作者的数据可用性段将支持资源结论的数据置于正文；额外数据需要联系作者。本轮检查原 arXiv、APS 入口及题名/编号公开检索，没有找到版本化原积分、原 MO、原 DF 张量归档或还原态/断键 TS 数据，未联系作者。官方页面没有列出 Supplemental 链接。这是检索范围内的缺口，不能推断公开仓库不存在。[出版页面](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.4.023019)

本轮定义 **LiPF₆ → PF₆⁻ + Li⁺ 的孤立气相电子端点能差**。两种多原子结构均取作者原坐标，Li⁺ 坐标复制原 LiPF₆ 的 Li 行；单原子的平移不改变孤立电子 Hamiltonian。Li⁺ 电荷 +1、三个端点 singlet RHF 是本协议的明确状态选择，不能称原作者独立发布了这个反应计算。电子数为 72 → 70+2，电荷为 0 → −1+1，均守恒。

## 冻结协议与实际量子线路

manifest（本地证据，未随题库发布） 在成功作业开始前冻结模型、轨道规则、1 mHa 能量门与 1 kcal/mol 派生能差门。基组采用论文列出的 STO-3G，常规 RHF 使用精确 Gaussian 积分，无 SCF density fitting。LiPF₆/PF₆⁻/Li⁺ 全空间分别 44/39/5 空间轨道、72/70/2 电子，固定 Mₛ=0 determinant 数分别约 3.14×10¹⁶、6.77×10⁹、25；没有进行前两者全电子 FCI。

量子模型统一为 canonical HOMO/LUMO CAS(2,2)：4 系统量子位、Nα=Nβ=1 的 4 维经典精确参考。其他占据轨道作为 inactive core，跨几何独立 canonical 排序；没有最大重叠轨道跟踪、FCI 选轨道或改几何。Li⁺ 的 HOMO 是 1s，两个分子与原子的冻结核芯处理不形成共享一致的解离轨道流形，这进一步限制化学解释。

初态是 RHF determinant，无精确基态制备。实际标准 QPE 电路含 8/11/14 位相位寄存器，受控 U^(2ʲ)、inverse QFT 与相位读出，最多 18 量子位。U=exp[+2πi(H_active−lower I)/width] 由经典精确矩阵指数构造；相位范围使用固定电子扇区 Gershgorin 界加两端各 0.125 Ha，不用 FCI 根选能窗。估计量是完整 histogram 的全局众数；没有按精确根过滤、选最低 shot 或 ground-state postselection。经典 FCI 只用于最终同模型验收和分布独立核验。

九个完整 Qiskit 线路均执行态矢模拟，终态已保存；54 组理想有限 shot 读出来自这些线路分布。三个 seed 标签 101/202/303、1024/8192 shots，端点/精度/shot/seed 的 SeedSequence entropy 均不同，不复用随机流。最终粒子数为 2，自旋 S²≈0，扇区泄漏为 0；与独立谱分布的最大偏差 4.78×10⁻¹²。两级 active ERI 分解仅做经典重构诊断，**没有构造 DF-QROM/PREPARE/SELECT 或 qubitization 线路**。

## 数值与验收

| 端点 | RHF / Ha | CAS(2,2) / Ha | 较大经典空间 / Ha | RHF overlap with CAS2 ground | 14 位众数误差 / mHa |
|---|---:|---:|---:|---:|---:|
| LiPF₆ | −932.384456400 | −932.384456918 | −932.384458150，CAS(4,4) | 0.99999951 | −0.033031 |
| PF₆⁻ | −924.940319985 | −924.943667329 | −924.949379773，CAS(4,4) | 0.99730067 | −0.021589 |
| Li⁺ | −7.135447629 | −7.135608077 | −7.135654284，full STO-3G FCI(2,5) | 0.99997046 | −0.136397 |

三种端点 14 位单 shot 在 CAS2 基态能量 ±1 mHa 范围的概率分别为 0.98496、0.98989、0.94470。最终 8192 shots、三个 seed 的九个众数全部通过 1 mHa 门。派生气相离子解离能的同模型 CAS2 参照为 **191.504290 kcal/mol**；14 位所有有限 seed 众数得到 **191.425880 kcal/mol**，偏差 **−0.078411 kcal/mol**，通过预冻结 1 kcal/mol 门。1024 shots 的观测众数也相同；相同众数不等于相同随机计数，也不保证未执行 seed 全部成功。

低相位精度控制保留：8 位派生能差偏差 −8.233744 kcal/mol，11 位为 −0.819113 kcal/mol。这些是预设精度扫描输出，8 位没有通过事后套用的 1 kcal 诊断；冻结的最终验收针对 14 位。

模型敏感性更大：同一原几何/基组下 RHF 的派生能差为 **193.705138 kcal/mol**；CAS2 为 **191.504290**；两种分子 CAS(4,4) 加 Li⁺ full FCI 为 **187.891455**。CAS2 相比 RHF 改变 −2.200848 kcal/mol，较大空间再改变 **−3.612835 kcal/mol**。RHF 是全轨道平均场，不是全空间相关真值；较大 CAS 也不是物理真值。该诊断不能被 QPE 同模型精度通过所替代。

PF₆⁻ 的 canonical HOMO 与前一个轨道能差仅 1.12×10⁻¹⁴ Ha，CAS2 切开简并占据空间；较大空间的虚轨道边界也涉及简并组。我们保留冻结 canonical 规则及数值，没有据结果重选轨道。此模型不满足轨道旋转/基组/活性空间收敛。STO-3G 缺少阴离子 diffuse 描述，没有溶剂、counterpoise、振动、热修正、电位、相对论校验或动力学路径；191.5 kcal/mol 不能作为实验盐解离值或材料推荐依据。

三个 RHF 均收敛，gradient norm 为 3.88×10⁻⁸、5.27×10⁻⁹、3.08×10⁻⁹；内部 RHF stability 检查均通过，外部/自旋破缺 stability 未测。overlap condition 为 6.07、5.22、1.64。CAS2 与较大空间的最低根 S²≈0，显式 N/S² Hamiltonian commutator、PySCF Hamiltonian 重构与 QPE 态核验通过。日志保留 OpenMP 未编译警告、stability 起始向量数量警告；单线程环境控制已记录。

## 成本、失败记录与交付

成功主作业 wall 为 **15.37 s**，单 CPU，QPU 调用 0。首次作业在 LiPF₆ RHF 已收敛后因 PySCF `get_grad` API 缺显式 MO 参数退出 1；保留 attempt-1（本地证据，未随题库发布） 的 driver、manifest、原 SCF 日志与外部 job 记录，修复 API 后重新冻结相同科学协议，恢复完成 checkpoint，未重跑该 SCF。没有为通过门增加参数或放宽预算。

最终每次 14 位电路为 18 量子位、6419 CX；LiPF₆/PF₆⁻ 为 12959 u、depth 14231，Li⁺ 为 12953 u、depth 14225。raw driver counts 把初态 H/X 保留为 primitive；事后纯编译资源审计将这些也变成 u，CX/depth 不变，原结果与 driver 不修改。resource-ledger（本地证据，未随题库发布） 保存修正及完整 native QPY。完整量子态模拟针对 dense 受控 U；native 等价性在每端点首/末两个 5q 控制块做矩阵核验，未直接模拟全部 native CX 线路。

读出总计 **248832 shots**，若每次执行 native 线路，对应约 **1.248×10⁹ CX、2.523×10⁹ u** 和 2737152 相位位测量。这是理想逻辑门预算，未发生硬件执行。每 14 位 QPE 使用 14 个经典构造的受控矩阵，等效基础 U 调用和为 16383；大幂矩阵被直接生成，不能把矩阵预言机当零成本可扩展实现。无硬件路由、噪声、Clifford+T 旋转合成、容错编码、光子资源或 magic-state factory 实测成本。这个组件不替代原作者全电子容错资源估计。

同模型强基线是 4×4 精确经典对角化，算法验证没有量子优势结论。父级独立核验涵盖全部原坐标、PySCF 四根、九个完整终态/谱分布与 54 组计数随机流，见 m15-parent-audit（本地证据，未随题库发布）。运行和来源哈希、原始矩阵、轨道、SCF checkpoint、54 组计数、QPY、冻结失败与环境均归档；旧结果、LATEST 与共享汇总未修改。

可执行下一步应先闭合目标还原态/断键端点、电荷/多重度、溶剂及电位条件，并检验包含整个简并轨道组的一致相关空间与基组收敛；随后才比较 scalable DF-qubitization。当前原公开几何已闭合，不应继续把“所有几何缺失”当下一步理由。

完整结果（本地证据，未随题库发布） · 输入几何（本地证据，未随题库发布） · GOAL（本地证据，未随题库发布） · 来源输入审计（本地证据，未随题库发布） · 归档核验（本地证据，未随题库发布） · 来源与执行哈希（本地证据，未随题库发布）
