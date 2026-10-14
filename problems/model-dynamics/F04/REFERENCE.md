<!-- 由 release/tools/build_problems.py 自 tasks/F04-frustrated-spin-liquid/execution/native-dynamics-r67/RESEARCH.md 生成，勿手改 -->

> F04 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# F04 R67：18自旋原生动力学与固定有限读出

**完成18q圆柱几何/初态资格、真实逐门动力学、同模型独立参考、两固定读出预算和独立审计；原应用仍incomplete。** 实现资格、科学响应门与有限读出门分别报告：native=True，精度=True，全部精确响应/对照=False，全部有限CI=False，joint=False。最终独审已完成，但audit integrity=False、independent native qualification=False：四个固定zero支路逆回门失败，**严格独立原生验收没有通过**。科学false与独审false均原样保留，交付真实性不等于算法或独审资格通过。

## 模型、初态和观测

[原论文v2](https://arxiv.org/html/2501.18554v2)研究中性原子Kitaev模型；本轮不是作者72data+32anc硬件反馈复现，也不是指定材料。3×3单元、18自旋，x周期/y开放，24条bond、6个指定hexface，H=−ΣXX−ΣYY−JzΣZZ，Jz∈{1,8}，单位采用Jx=Jy=1与ℏ=1。几何、signed Pauli和补全见冻结源设计（本地证据，未随题库发布）。9ZZ+6W秩15，加circumference C0和两个边界Dpair得到完整18稳定子；边界补全定义初态，不宣称全部与H对易。

Qiskit从完整signed稳定子生成Clifford，真实从0制备并降为RY/RZ/CX与GP相位记录，未注入ED答案或免费投影。资格native准备单次RY43/RZ72/CX119/GP72，depth120。动态每case/grid重新制备，实际初态与资格保存全幅在1e−12门下比较，不归一化或投影。纯target、zero、Z0target三支路；partial_dephase仅target与Z0target等权的**单点部分去相干**，不是全Z去相干。Majorana物理投影/Gaussian参考仍未资格。

全部42条长度2不同端点开放串与9个n=(1−ZZ)/2密度、全部三时点都事前冻结，不选最强路径。W/C0守恒只作实现检查，各branch用自己的t0值。12条near-loop W×ZZ只作静态coherence见证，在flux+扇区等于ZZ，不能当独立动态相关。长度2串响应和对照差也不构成Chern数、长程拓扑序、任意子交换或真实材料QSL证据。

## 实际动力学及强经典参考

固定T=.5、t=.125/.25/.5、coarse32/fine64，Strang X半/Y半/Z整/Y半/X半。两J×三pure×两grid共12条轨迹，576实际steps、36完整节点全幅；每步完整18q scalar RY/RZ/CX实际回放，GP累计相位仅按协议施加一次，无cached macro替代主线路。动态physical preparation 1876、physical evolution 233280，GP记录97348；GP不计硬件门时长。

独立同H spin matrix-free expm_multiply采用资格actualnative全幅，另以固定Taylor24阶/32segments、不同tensor算符实现核误差；自己的128orbit只核初态身份，不作为免费量子准备。Taylor截断界只覆盖精确算术尾，整体FP严格证明未知。coarse/fine与参考对照固定maxobservable≤.002、L2≤.01。实际coarse/fine最大L2=0.00483083144857、观测差=0.0010075674273；fine对reference最大L2=0.00160351784251、观测差=0.000334748666029。reference两独立方法最大L2=1.46474077746e-12、观测差=4.20607992884e-13。数值直接取封存checks，完整状态/误差/范数见量子seal（本地证据，未随题库发布）与reference seal（本地证据，未随题库发布）。同模型精度不能证明物理材料模型正确。

|Jz|开放串响应RMS|密度响应RMS|与zero差RMS|与partial差RMS|
|---|---:|---:|---:|---:|
|1|0.175424210402|0.165923715885|0.0817381399457|0.0522757276208|
|8|0.0336366507294|0.00786859486005|0.014176932136|0.00894361984295|

精确科学门依次为.05/.01/.05/.05；Jz=8四项全部未达门，不能把静态各向异性直接解释为拓扑相证实。Jz=1限定响应与对照区分必须与下面有限CI能力一起判断。exact-response.csv（本地证据，未随题库发布）直接来自保存字段，全部51观测见observables.csv（本地证据，未随题库发布）。

## 固定预算的真实模拟读出

两预算N=1024/8192使用独立PCG64域、seed20261004；42Pauli native基旋转setting+一个Zsetting共享九密度。partial每setting总N，从branch+bit联合分布抽样，不冒称两branch各N仍同预算。所有262144输出保留，仅全pure/jointflat一次FP概率归一，不按branch后选。实际7133184draws、1548 raw记录、774完整硬件program；独审逐原draw重放，**0新shots**。这全部是本地模拟抽样，真实QPU=0。

全18q实际native基旋转与独立H/Sdg全幅核精度；每setting保存全state/prob byteSHA和资格数值，只有事前指定J1/t.125/setting0三pure旋转全幅存为raw witness，其余是哈希/资格与可由原state+IR复建，不能声称全部旋转全幅已存档。完整硬件计划逐项包含重新准备、fine prefix、基旋转、18测量/reset，partial按实际branch draws计费；共享模拟state不是免费硬件制备。

95% simultaneous family M=1836包含两预算/两J/三时间/三condition/51均值。Pauli±1用span2 Hoeffding，密度span1；Zsetting九维sample covariance保留，union bound不要求均值独立。所有42×3固定RMS差的下界同时传播，t0是qualified exact expectation并加1e−10数值allowance，不额外伪造抽样CI。有限门：signal/zero/partial lower≥.01，density lower≥.002；两N及两J全部通过才joint，不能用8192掩盖1024负门。

|Jz|N|metric|estimate|simultaneous lower|simultaneous upper|required lower|
|---|---:|---|---:|---:|---:|---:|
|1|1024|signal|0.17573956461196347|0.06074112394888958|0.3119717699397623|0.01|
|1|1024|density|0.1611359909549026|0.10125289325914716|0.22867392626454328|0.002|
|1|1024|zero|0.09188917493282367|0.0|0.37087088195075435|0.01|
|1|1024|partial_dephase|0.06995528507853975|0.0|0.3502917432998881|0.01|
|1|8192|signal|0.17590240931759044|0.1330909696613014|0.22188633937606783|0.01|
|1|8192|density|0.16643814142158495|0.14397055698129435|0.18985123571045517|0.002|
|1|8192|zero|0.08299996475179583|0.030163519167662647|0.17185033852714857|0.01|
|1|8192|partial_dephase|0.05426497516092435|0.017928590585328707|0.1432311327265411|0.01|
|8|1024|signal|0.048757078769264134|0.0|0.19030637743473264|0.01|
|8|1024|density|0.00845519085884448|0.0|0.08190669039982393|0.002|
|8|1024|zero|0.045177252446445555|0.0|0.3335248334908407|0.01|
|8|1024|partial_dephase|0.04310838434094615|0.0|0.33149855018162216|0.01|
|8|8192|signal|0.035223739673518696|0.002457773786868292|0.08505169125679352|0.01|
|8|8192|density|0.008179217017665203|0.0|0.0341463682935681|0.002|
|8|8192|zero|0.023353132148931782|0.0|0.12383158465049711|0.01|
|8|8192|partial_dephase|0.018172532942225216|0.0|0.11956863714699789|0.01|

finite-CI.csv（本地证据，未随题库发布）逐值来自sealed JSON。实际有限负门共10项：J1/N1024两个对照区分门失败；J1/N8192四项通过，不能覆盖联合失败；J8两预算各四项失败。图中interval是上述共同family置信区间，不是标准差或postselected区间。

（图：固定读出与响应比较，本地证据，未随题库发布）

PNG已真实目视；PDF（本地证据，未随题库发布）仅导出，未目视。绘图仅读sealed JSON，不新传播/抽样，全部来源见plot manifest（本地证据，未随题库发布）。

## 独立核验、全部费用与范围

资格生产 171/171、资格独审 480/480；动态 189/193、读出 2366/2376、独立动态审计 19070/19074。审计从独立Pauli/Strang重建动力学、核完整IR与小原生全列、全部幅度/参考/CI/原draw/费用；没有再逐235156个18q scalar门重跑，也不把只重算数组称独立完整native重演。audit integrity=False与joint science=False是不同结论。

|stage|worker complete|CPU s|wall s|peakRSS bytes|output bytes|
|---|---|---:|---:|---:|---:|
|qualification-production|True|2.02|2.03|165363712|21183000|
|qualification-audit|True|1.75|1.74|141639680|96144|
|dynamic-production|True|232.01|202.47|119160832|165530596|
|reference-production|True|367.26|331.71999999999997|245940224|164088860|
|finite-readout|True|83.50999999999999|61.3|196100096|54610276|
|dynamic-audit-v3|True|149.52|132.81|274923520|4178279|
|dynamic-audit|False|81.01|71.49000000000001|227016704|1439521|

首dynamic-audit尝试的工程失败原样保留：旧审计result（本地证据，未随题库发布）及seal/source/receipt均绑定。它完成576 semantic steps、407checks中402通过，但5项initial byte identity检查false并遇到int(complex sign)异常，0draw replay；这不是J8或有限统计科学负门。诊断（本地证据，未随题库发布）明确：生产仅保存前三个共用初态payload，12run各有SHA记录，协议没有要求每次重新制备byteequal；五个差异原样留痕，缺失的重复幅度不被追认为逐字资格。最终V3显式核signed Pauli实部/虚部类型，前三payload严格身份保持，再从各case最早节点t=.125逆semantic推进144steps/5616pair，与资格actual初态比较combined maxabs≤1e−12。这个误差包含原native传播和逆回roundoff，**不是纯制备误差界，也不能证明未保存的各run初态幅度逐字一致**。最终V3完成19070/19074检查；J1/J8×32/64的四个zero支路逆回combinedmaxabs约2.88e−12至5.76e−12，超过固定1e−12，不能放宽或重跑V4。其余19070项通过，576forward/144reverse/7133184原draw replay完整完成；audit_integrity_passed=false、independent_native_dynamics_qualified=false，参考/读出精度true和科学负门分别保存。最终证据仅取dynamic-audit-v3（本地证据，未随题库发布）独立完成证据，不覆盖旧失败、也不把工程修订snapshot计新科学run。

最终负审计收束（本地证据，未随题库发布）说明四zero combined失败不能归因于纯制备错误，也不能证实仅有全局相位误差；未保存逆回arrays/overlap，不能声称相位对齐后会通过。保持原1e−12门，不phase-align、不重跑。

所有受监控科学attempt CPU **917.08s**、累计stage wall **803.56s**、peakRSS **274923520bytes**、output **411126676bytes**、scratch **0bytes**。worker+monitor只计一次，phase/call计时不再相加；wall求和不是端到端历时，RSS取max。图/构包/审阅等工程生命周期不在科学总账，不填0。资源汇总（本地证据，未随题库发布）、资源review（本地证据，未随题库发布）、stage CSV（本地证据，未随题库发布）与完整per-draw exposure见readout result（本地证据，未随题库发布）。不同workload本地CPU不可相除称量子speedup；硬件连接/路由、门时长、纠错、噪声和价格unknown。

旧6自旋结果（本地证据，未随题库发布）finest string error门passed原样保留，只验证单hexagon守恒弦代数；原旧scoped pass没有反转，本轮补充真正动态观测与对照。限定推荐见路线比较（本地证据，未随题库发布）：当前完整spin参考可用，Majorana路线仍未资格且未被排除；未做Floquet/Chern协议，不声称数字路线全球最优或实验优势。

原R52 R6=incomplete（全进程/完整测量成本缺口）、R8=not_verified（独立科学重建缺口）。根据R6/R8独立范围决定（本地证据，未随题库发布），本轮只提出这两项在**该18q有限模型**的成本/误差、独立重建与有效负证据范围proven_scoped，须最终case review与父级晋升；这不把audit/native false升级为true；不把原应用完成等同八项scoped证据。材料有效交换、作者二维阵列反馈数据和拓扑完整观测仍缺，original_application_completed=false、总84 Goal active。live LATEST/EXECUTION-STATUS不绑定，输入时指针另存LATEST-at-intake.json（本地证据，未随题库发布）。

GOAL（本地证据，未随题库发布）、机器结果（本地证据，未随题库发布）、全部SHA（本地证据，未随题库发布）、封存命令（本地证据，未随题库发布）。固定负门之后不调J/时间/路径/steps/shots追pass；下一科学问题需另冻输入与门。
