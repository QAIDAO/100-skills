<!-- 由 release/tools/build_problems.py 自 tasks/C05-warm-dense-stopping/execution/coupled-r65/RESEARCH.md 生成，勿手改 -->

> C05 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# C05 R65：有限耦合量子动力学完成，连续波包与边界资格失败

**真正三维电子—质子联合演化、同模型强经典参考与独立审计已完成；这是有限模型的量子算法实验，原温稠密物质 stopping 应用仍未完成。** 生产 273/278 检查通过，五个 continuum 门失败；独审 18102/18102 完整性通过并确认原科学布尔。正的 S_proxy 不能覆盖截断失败。

初态 σ5 的保留概率只有 **0.388142%**（门≥99%），最大边界人口约 **96–98%**（门≤1%）。这是小动量基组与宽波包不相容的负结果；没有缩σ、扩基、重选速度/时间窗或调整门。没有通过连续极限、定位路径或 bulk 稳态停止资格。

## 做了什么、为什么选这条路线

采用 [arXiv:2308.12352v1](https://arxiv.org/abs/2308.12352v1) 的第一量子化非 Born–Oppenheimer kinetic/电子—投射体 Coulomb 结构。原子单位，η=Zp=1、质子质量1836、无固定核中性周期盒；零 Fourier 模删除。Ω861.328194bohr³只借用论文TableII体积数值，实际电子密度 **0.00116099763942 bohr⁻³**，不是391电子碳或10g/cm³。温度1eV是自由电子canonical模型参数，不能从公开 EIGENVAL 认证作者KS热态。

G=Gtilde={−1,0,1}³：729物理态，compact10q完整1024地址。全部6130有向/3065无向Coulomb转移都按合法输入/输出保留，没有FFT模回绕。Pp=kq+κ，论文变量kproj=−κ；κ²常数/交叉项与global phase保留。所有27个thermal分支、slow/fast/reverse/zero四对照、固定T8au、80/160步、17个时间点都实际完成，reverse同时翻转boost与R0。

量子路线是系数生成的二阶对称乘积公式：27个不相交转移层的forward/reverse half steps及kinetic半步。以CNOT地址桥+9控制RX的RY/RZ/CX模板资格为基础，**实际动力学采用全10q、27分支的数学两态/层缓存作用**；没有逐时间步重放全部scalar primitive，没有免费dense exactU或eigenstate制态。所有3065条桥图覆盖1024地址，代表mask全部实际角族的逐门列资格与全mask整数Walsh证书分开披露。详见冻结设计（本地证据，未随题库发布）、原生证据（本地证据，未随题库发布）及门账（本地证据，未随题库发布）。

同模型强经典参考利用125个总整数动量sector、最大27维，独立装配矩阵元后精确eigh传播相同初态/热权重/全phase/17节点；独审另建H、重演粗细缓存/原生模板和全部保存状态。这个小模型自然推荐经典分块谱传播；没有量子加速、全球最优线路或硬件可用性声明。作者目标规模的PF8/QSP条件取舍见路线决策（本地证据，未随题库发布），本PF2不是作者优化八阶算法复制。TableIV碳条目QSP2.225×10¹⁸与PF1.074×10¹⁶ Toffoli是作者条件估算，非本轮独立复算或硬件运行。

## 结果：正代理量与严重物理截断相邻解释

固定S=−full-window OLS[Kp versus x_kin]，x_kin为directed velocity的梯形积分，不能用t·v或周期位置中心替代。全部窗口/负值/零耦合结果保留。以下单位S均为Ha/bohr，速度为au；reverse物理vx为负，但沿初始方向的积分x为正。**这些S只属于上述quench有限模型；σ保留0.388%、边界96–98%，不能称原材料稳态stopping。**

|case|初始物理vx|fine S|同模型精确S|8192/node finite S|delta-normal95区间|最大边界人口|
|---|---:|---:|---:|---:|---|---:|
|slow|0.503553562404|0.00759770981062|0.00759791247613|0.0070726696519|[0.00591903782724, 0.00822630147656]|0.980131730305|
|fast|1.00710712481|0.00488445355423|0.00488442261977|0.00492043739401|[0.00376563549526, 0.00607523929277]|0.974719207631|
|reverse|-0.503553562404|0.00759771325762|0.00759791247611|0.00802373604146|[0.00686874777089, 0.00917872431202]|0.980131742138|
|zero|0.503553562404|-2.08891758826e-13|2.76677826259e-16|0.000677310199116|[-0.000477085522163, 0.00183170592039]|0.962905024556|

slow从t0到8：Kp 232.773999446→232.741924346Ha；Ke 0.00344808156281→0.0793031795224Ha；Vep -3.60136374768e-18→-0.0437795909912Ha。近似Ke升.07586、V降.04378、Kp降.03208，是关联形成/势能交换账，**不是把电子全部升能都算成质子损失，也不是稳态摩擦**。独立判断不需强迫S为正；zero exactS约−2.09×10⁻¹³，finite区间跨0，正有限估计可由测量噪声出现。两个速度的proxy不同，但没有冻结“两速度差值显著性”检验，不能补作材料速度趋势结论。

（图：封存数据的四面板观测，本地证据，未随题库发布）

PNG已由父线程实际目视通过，精确SHA绑定PLOT-PROVENANCE（本地证据，未随题库发布）；PDF导出（本地证据，未随题库发布）未目视。图只读取封存JSON，没有新传播、拟合或draw。细/粗/经典曲线重叠并不能把相同严重basis截断变成收敛。

## 精度、读出与费用

实现/native template、finite model dynamics、finite readout均true；continuum false、joint_quantum_science_qualified false。Norm/illegal、残余动量和boost×合法质量账均保留；局部native error乘线路edge数量只是启发式累计指标，不是allmask/global floating bound，`native_global_scalar_roundoff_bound_qualified=false`。门账中的GP是全局相位记录，serial-depth只计RY/RZ/CX，不能把GP换算成未知backend门时长。完整精度见四case保存结果（本地证据，未随题库发布）与独立审计（本地证据，未随题库发布），全部五个失败另存failed-gates.json（本地证据，未随题库发布）。

|case|fine–exact最大state L2|fine–exact Kp(Ha)|coarse–fine Kp(Ha)|H drift(Ha)|细步速度积分–.5节点积分(bohr)|
|---|---:|---:|---:|---:|---:|
|slow|7.76162684729e-06|7.40686061818e-07|2.22231511771e-06|4.39235776639e-07|2.2151479051e-07|
|fast|9.29509678023e-06|7.1049817052e-07|2.13274029193e-06|5.82541133554e-07|8.72055609946e-08|
|reverse|7.64893653074e-06|7.27054469962e-07|2.18142130848e-06|4.37517570617e-07|2.21514848242e-07|
|zero|2.07852888646e-13|8.52651282912e-13|2.27373675443e-13|8.81072992343e-13|1.24344978758e-14|

每case每节点8192 joint(thermal label,basis)独立重制备，合557056实际模拟draw；QPU调用/physical shots为0。读出同时从同一bitstring计算Kp/v，保存Cov(meanK,meanv)，包括cross term及噪声velocity积分给x带来的相关性。S区间是预冻结局部delta-normal近似，**不是精确覆盖或完整非线性统计保证**；V/H是state expectation，不冒称有限shot读出。独审重放原draw，0新shots。每节点重新制备并付j×10 fine步骤，17节点prefix合1360步/sample；全部Gaussian/thermal X/RY/RZ/CX/GP门曝光计划见门账，不是实际硬件门数。

三个monitored科学/独审stage（包含失败独审v1）的保守receipt只各加一次（monitor成本已合并）：

|stage|CPU s|wall s|peak RSS bytes|retained output bytes|
|---|---:|---:|---:|---:|
|quantum-production|13.28|11.52|287408128|117682009|
|quantum-audit|7.6|6.7|172589056|9589274|
|quantum-audit-v2|10.83|9.49|173473792|32495442|

合计CPU **31.71s**、累计stage wall **27.71s**、peak RSS **287408128bytes**、output **159766725bytes**、scratch **0bytes**。wall和不是端到端历时，RSS取max；资源汇总（本地证据，未随题库发布）、独立资源review（本地证据，未随题库发布）。R64输入历史费用与工程费用单列，不用这三个已计费stage冒充完整生命周期。generic receipt的new_quantum_results=0只是封存器metadata，实际科学result明确new_coupled_quantum_component_executed=true；C05本来已有Gaussian量子组件，任务总量64不因四case或coarse/fine增加。

生产内部相位计时只作收费范围诊断，**不能再次加进stage总CPU/wall**；经典构建/谱传播、原生资格、缓存演化、readout/输出和共享setup各自可见，没有从部分CPU推出公平hardware TTS或量子优势：

|phase|CPU s|wall s|
|---|---:|---:|
|Hamiltonian_transfer_and_layer_construction|0.029339|0.0297117|
|native_9control_template_actual_elementary_replay|2.47876|2.49325|
|slow:coarse_cached_native_action|0.330454|0.332343|
|slow:fine_cached_native_action|0.707996|0.712139|
|slow:strong_classical_sector_eigh|0.061405|0.0640447|
|slow:coarse_observables|0.015136|0.0157127|
|slow:fine_observables|0.008065|0.00806304|
|slow:classical_observables|0.007894|0.00790012|
|slow:finite_readout_all_17_nodes|0.066938|0.0686137|
|fast:coarse_cached_native_action|0.36453|0.366868|
|fast:fine_cached_native_action|0.805195|0.811048|
|fast:strong_classical_sector_eigh|0.109282|0.110209|
|fast:coarse_observables|0.009757|0.00980008|
|fast:fine_observables|0.008447|0.00861246|
|fast:classical_observables|0.008675|0.00878217|
|fast:finite_readout_all_17_nodes|0.086254|0.0869969|
|reverse:coarse_cached_native_action|0.409714|0.412712|
|reverse:fine_cached_native_action|0.906108|0.91233|
|reverse:strong_classical_sector_eigh|0.153186|0.154222|
|reverse:coarse_observables|0.008149|0.00822754|
|reverse:fine_observables|0.00805|0.00805613|
|reverse:classical_observables|0.008006|0.00800583|
|reverse:finite_readout_all_17_nodes|0.104574|0.105473|
|zero:coarse_cached_native_action|0.109191|0.109855|
|zero:fine_cached_native_action|0.337454|0.340074|
|zero:strong_classical_sector_eigh|0.199546|0.200774|
|zero:coarse_observables|0.008214|0.00825467|
|zero:fine_observables|0.008389|0.00847058|
|zero:classical_observables|0.00839|0.00845546|
|zero:finite_readout_all_17_nodes|0.122983|0.124017|

首AUDIT-STATIC-REVIEW为699/701假，冻结器正确拒绝且0审计科学执行；两项是独立静态检验器对等价CX代码拼写和父准入文件归属的误判。原negative记录保留（本地证据，未随题库发布），正确AST/逐byte复核新版704/704（本地证据，未随题库发布）后启动实际独审v1。v1在16316/16316检查通过后，因局部momentum bound数组覆盖输入SHA字典而发生IndexError，audit_completed=false，不能充当完整审计。失败stage与7.60CPU/6.70wall保留；最小v2修复（本地证据，未随题库发布）仅三处局部变量更名，生产没有重跑，科学参数/门不变。v2的完整通过证据与旧失败同时绑定。首静态拒绝没有科学运行，不另造第四stage；完整工程生命周期成本未测。

## 复核、来源与停止范围

summary.csv（本地证据，未随题库发布）直接抄录生产保存field，无新fit/propagation；results.json（本地证据，未随题库发布）保留producer+audit完整字段、读出raw links和门成本；manifest.json（本地证据，未随题库发布）以绝对path→SHA绑定全部原始科学证据及新交付。原作者public source commit为acd92bae93287bacefcb0e2b3175885b892d644b，见源清单（本地证据，未随题库发布）；原公开TDDFT轨迹仅为R64经典来源参考（本地证据，未随题库发布），没有用于本轮制态/phase/答案。旧Gaussian algorithm_pass（本地证据，未随题库发布）保持历史，不能替代coupled stopping。输入时的指针原字节另存LATEST-at-intake.json（本地证据，未随题库发布），live LATEST与会更新的EXECUTIONSTATUS不进入本case hash清单。

若独立科学审计、资源和本case最终delivery准入均实际通过，依限定充分性（本地证据，未随题库发布）建议R2/R4/R6/R8补为**有限模型proven_scoped**；本builder不晋升全局或LATEST。它们对应同模型强经典比较、真实任务映射的coupled量子负例、分层误差/完整已测成本、独立数值核验与可用交付；**不意味着continuous门通过或原应用完成**。本固定路线closed_negative_result，总84 Goal仍active。

原应用还缺391电子KS/赝势身份、多电子热态/交换、真实材料速度/温度/密度、近碰撞/局域化/连续基组和尺寸时间收敛，以及目标fault-tolerant硬件资格。下一动作由父线程NEXT确定；本报告不自动启用扩大basis或替代算法扫描。复建方式见REPRODUCE（本地证据，未随题库发布）。
