<!-- 由 release/tools/build_problems.py 自 tasks/M06-lfp-annealing/execution/cost-qualification-r66/RESEARCH.md 生成，勿手改 -->

> M06 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M06 R66：原32变量成本资格完成，完整N8表示在预算前停止

**本轮完成原32变量输入/成本闭包、一次真实21q Dicke原生制备、原32相位与N8地址分块资格、完整线路门账和独立审计；没有执行完整32变量优化。** 原应用仍incomplete。资格生产 86/86、独审 1346/1346，当前完整经典成本独审 147/147。全部数值来自封存JSON，构包不新算能量、传播、拟合或draw。

## 原模型与选择

[作者公开数据](https://doi.org/10.26165/JUELICH-DATA/VEHDXR) CC0、2025-09-10版本的1×2×2和1×4×1两超胞，全部16Li+16Fe-redox占据变量及交叉项保留，单位eV/16FU。FeII/FeIII是同一位点的标签，不是另外32个Fe位点。原十进制系数、CIF顺序及输入SHA见输入审查（本地证据，未随题库发布）。没有加入chemical potential、软约束罚项或周期绑定位点；主sector NLi=Ne=8。

选择原32固定数exact-sector路线，成本归一化只用原系数 `D=(E-c)/S, S=Σ|a|+Σ|B|`。mixer保持完整两物种240pair `−Σ(XX+YY)/2`，未另除128；D范数上界1而N8 mixer尺度128，固定T8/64与128步计划不宣称保证搜索成功。成本和替代路线的一级资料见冻结设计（本地证据，未随题库发布）、公开算法阅读（本地证据，未随题库发布）。更好的无anc制备、complex64、streaming/MPS尚未在本实例资格；不能据本停止宣布所有32q方法不可行。

## 实际量子组件和容量停止

一次完整16data+5count=21q线路从全0逐RY/RZ/CX/GP实际回放，保留全部2²¹幅度和全部65536理想数据幅度，包括微小非法空间；maxabs=5.23027564704e-16、norm=1、count leakage=6.13748441932e-30、错误填充质量=1.61369910361e-30。实际单物种门记录为 {'RY': 641, 'CX': 6928, 'RZ': 1985, 'GP': 193}。第二物种是数学重标资格复用，**不是第二次21q实跑**；硬件制备计划付两倍门费，32data+5复用workspace临时37q，末count清零，不免费reset或inject Dicke答案。

原32能量的0/32single/496pair及1024固定random位串、真实小原生全列模板、12个XY块和6个energy/phase块各1warmup+3timed均实际执行。地址是原N8 lex-combinations固定8×12870工作tile，不是新8q子模型；probe使用完整sector均匀幅度1/sqrt165636900，tile质量不是1。全21q准备、每cell首个完整XY块与所有固定witness/byteSHA保存于生产seal（本地证据，未随题库发布）；其它完整tile没有重复存档。独审从原系数/独立模板/保存幅度与地址核验，不导入producer，不再执行完整21q制备，也不传播不存在的N8全态。

N8维数12870²=**165636900**，一个complex128态payload **2650190400bytes**，已超本轮hardRSS **2147483648bytes**；并存计划还含第二态及energy数组，总payload **6625476000bytes**。本候选要求完整可写resident态、不用swap/out-of-core，故在任何全sector分配之前写capacity guard（本地证据，未随题库发布）并停止。实际前缀peakRSS 263421952bytes单列；payload不是RSS测量，OS paging/compression可改变RSS，**这不是实际OOM、全机内存不足或所有量子算法不可行的证明**。

`full_sector_allocation_actual=false`、`full_N8_steps_actual=0`、`finite_draws_actual=0`、真实QPU/physical shots均0。full32成功率、coarse/fine TV、有限读出门均未执行/null，不能记算法科学失败，也不能记算法通过。实际native preparation qualification runs=1；new_quantum_runs=1仅定义为包含这次制备的受监控资格stage，**new_full32_quantum_optimization_runs=0**。

## 完整原生计划及成本

完整coarse/fine计划真实逐条生成指令，按37q依赖时钟计算depth/count/globalphase并记录full byteSHA；保存recipe+schedule+源生成器和摘要，可恢复展开流，不重复存巨型展开文件。它是已生成的线路计划，**不是已执行完整N8线路**。cost半层发射全部32个线性RZ（含零角不省略），另存actual_nonzero_h_count；二次非零项按原系数统计。GP是全局相位记录，不是backend physical gate时长。以下含两物种制备：

|cell|steps|RY planned|RZ planned|CX planned|GP records|native dependency depth|
|---|---:|---:|---:|---:|---:|---:|
|LFP_1x2x2|64|247042|501634|263712|123394|90110|
|LFP_1x2x2|128|492802|999298|513568|246402|162110|
|LFP_1x4x1|64|247042|501634|263712|123394|90110|
|LFP_1x4x1|128|492802|999298|513568|246402|162110|

summary.csv（本地证据，未随题库发布）直接复制保存计划字段；profile-summary.csv（本地证据，未随题库发布）保存实际tile narrow median。这些median排除共享setup、索引、phase准备、warmup及序列化，warmup仍计stage总成本。不能将小块median乘165M动作冒充全态实测，更不能与完整经典端到端成本相除称speedup。未来8192独立读出必须每shot重新制备/推进，曝光计划已列但实际draw为0。硬件路由/连接、门时长、噪声、纠错、QPU等待/价格unknown。

## 强经典参考、旧负结果与全部已测费用

原完整经典算法已经穷尽两cell×N4/N8/N12六扇区**344523400**配置并审查**1006**历史批次。因旧全进程CPU/RSS无法恢复，父级事前批准一次必要同范围成本复测例外：原算法/原128行块/原输入，新out写入；39项检查通过；4份结果JSON除wall_seconds外逐值一致，旧结果未覆写，不算新的最优发现。新受监控完整成本见baseline seal（本地证据，未随题库发布）和独立成本核（本地证据，未随题库发布）。旧约20.72s枚举/历史审核与5.29s整数审计只是历史wall，旧CPU/peakRSS仍unknown，不能被新147636224bytes追认。

六扇区原能量（本地证据，未随题库发布）与旧完整经典报告（本地证据，未随题库发布）保持原样；独立逐行最优证书证明ground energy/简并，next-distinct gap仅为旧producer报告值，未冒称本轮独立第一激发证明。1×2×2 N8 periodic restriction损失**26.03meV/FU**仍成立。旧8q量子22.8125% versus SA43.75%（matched1280读出）与粗步长失败保持历史，是受限36态比较，**不是本原32N8的算法性能对照**。见原8q结果（本地证据，未随题库发布）。

作者历史2444500 reads×100μs=244.45s只是配置的anneal-duration乘积，不是实测QPU access/生命周期/paid费用；embedding、programming、readout、校准与完整费用未存，保持unknown。软约束样本的feasible-conditional成功率不能等同守sector全部读出的成功率。本轮hardware0不表示作者历史hardware0。

|stage|worker completed|CPU s|wall s|peakRSS bytes|retained output bytes|
|---|---|---:|---:|---:|---:|
|baseline-cost|True|18.15|15.83|147636224|1101163|
|cost-audit|True|9.29|8.41|148406272|330180|
|cost-qualification|True|33.49|28.76|287571968|22158539|

全部封存attempt合CPU **60.93s**、累计stage wall **53.0s**、peakRSS **287571968bytes**、output **23589882bytes**、scratch **0bytes**。失败attempt若有同样保留；worker+monitor已在receipt合计，内部phase计时不再次相加。wall和不是端到端历时，RSS取max。资源汇总（本地证据，未随题库发布）/review（本地证据，未随题库发布）与stage CSV（本地证据，未随题库发布）均绑定；构包/审阅等完整工程生命周期没有监控，不填0。

静态准入的旧身份拒绝记录保留，是授权metadata编辑并发读取旧expectedhash，v2正式准入后才启动；不是生产科学失败或额外科学run。监控receipt通用new_quantum_results=0不是科学计数，实际component类别以生产进度为准。

## 关闭范围与复建

本固定路线收束为资源准入停止，算法full32科学门未执行；原8q负例和完整32经典强参考不变。只有最终独立case delivery通过后，才建议R6由not_verified补为**本原32候选当前成本/误差及停止证据proven_scoped**；R1–R5/R7/R8原scoped边界保留，不把R4升级成完整32搜索成功。原应用incomplete、总84 Goal active、原有64量子任务计数不递增。本builder不晋升全局/LATEST。

GOAL（本地证据，未随题库发布）、机器结果（本地证据，未随题库发布）、证据SHA（本地证据，未随题库发布）、原命令与版本（本地证据，未随题库发布）。live LATEST/EXECUTION-STATUS不绑定，输入时指针原字节另存LATEST-at-intake.json（本地证据，未随题库发布）。本路线停止后不自动改dtype/MPS/N4追成功，新的完整32方案需另冻精度、成本和停止条件。
