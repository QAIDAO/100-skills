<!-- 由 release/tools/build_problems.py 自 tasks/M08-nv-sic-multiplets/execution/symmetry-native-r60/RESULTS.md 生成，勿手改 -->

> M08 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M08 R60：身份资格通过，原生表示失败，联合QPE按门停止

固定公开NV四轨道模型的自旋与候选有效群身份通过，但第二个受控幂 C(U²) 的原生表示误差超过事前门。独立审计确认该负结果；原应用仍未完成。未运行新的四初态32768次联合读出，未更改门、编译器、H或预算追通过。

身份生产（本地证据，未随题库发布）结构39/39、科学10/10通过。signed spin对易残差0；五joint块最坏对易残差.000383701550802056eV <= .001，四目标最低mean purity .9999998616482102 >= .99。独立身份审计（本地证据，未随题库发布）结构220/220、科学10/10通过，采用PySCF contract_ss全16列与显式群表示∧³/minors/class-average，未导入producer候选来复核自身。

[WEST官方2026教程](https://west-code.org/doc/West/latest/tutorials/APS_Short_Course_2026/aps_001.html)给出轨道426/430/431/432的A1/A1/E/E标签。多E副本标签不保证两个活性E轨道物理闭包；本结果仅资格有来源支持的有效实2A1+E表示，H对易通过不能反证明波函数群作用。真实irrep闭包与E空间轴/δ仍未验证，先能量后身份的测量也不宣称QND。

|证据|power00 C(U)|power01 C(U²)|
|---|---:|---:|
|原producer manual最大绝对误差|1.7628474883638588e-10|3.266449200286506e-9|
|固定严格门 <1e-9|通过|失败并停止|
|独立audit manual误差|1.762847381606963e-10|3.2664488014028715e-9|
|独立audit SDK误差|1.7628429527814754e-10|3.2664495388747755e-9|
|native RY/RZ/CX|818/1636/524（原保存）|844/1688/526（独立一次复现）|
|depth|1979|2047（独立一次复现）|

原生生产（本地证据，未随题库发布）20结构检查19通过/1失败，exit2、completed=false、完整cost_ledger=null。power00全32列manual/SDK/QPY已保存；power01在首manual gate拒绝时尚未保存原失败IR/QPY，原SDK误差没有结果。表中power01 SDK、门数、depth来自后来**一次有界独立审计复现**，不能追写为原producer证据。原生负结果审计（本地证据，未随题库发布）108/108检查通过，audit integrity和negative confirmation为true，native科学资格与joint native资格仍false。未编译power02..13或B†/IQFT/完整18q计划。

（图：五joint块、四目标泄漏与原生停止门，本地证据，未随题库发布）

图CSV（本地证据，未随题库发布）直接来自保存JSON，PDF（本地证据，未随题库发布）只导出未实际查看；PNG已由父线程实际查看，独立交付目视另行审核。图是模型资格与编译停止证据，没有新联合QPE counts。左侧群残差单位eV、中侧mean leakage=1−purity、右侧native条目最大误差；门与数据不跨单位比较。

只读诊断（本地证据，未随题库发布）发现安装QSD存在默认allclose、近Hermitian与小旋转省略等候选误差机制。关闭opt_a1/opt_a2不关闭所有内部阈值；但当前未插桩定位哪个分支触发。独立audit只确认同版流水线可重现失败，没有证明allclose是唯一原因，也不普遍否证QPE算法、多重态可辨认性或未执行的统计CI。

未执行主草案记录（本地证据，未随题库发布）：new joint draws=0、完整18q主线路=0，无main合同/freeze/job。解析B不含H本征矢，其实际native measurement尚未资格。原14clock/4×8192/seed20261004预算未变；主统计E/W与能量Hoeffding只是未执行草案，没有四目标coverage/identityCI/gap结论。

旧QPE原始结果（本地证据，未随题库发布）按普通prior reference保存：四峰对应根3/0/7/11不等于四目标全覆盖；峰最大误差.00034982759537258374eV、norm约5.02e-12。旧active/full最大gap误差.21767333945311007eV > .05仍失败，不能用精确线路或模型身份修补。旧32768次仅能量读出不冒充本轮joint draws，旧WEST parser后来补核的chronology不追认预冻。

资源汇总（本地证据，未随题库发布）与独立只读资源复核（本地证据，未随题库发布）核4个terminal stage的receipt、monitor/root-time、source/manifest SHA与文件字节：包括native失败，共5.30CPU/5.73累计wall秒，RSS峰181846016B、output累计1457321B、scratch0。monitor CPU已包含，未双加；累计wall不是并行端到端延迟。旧生命周期与文档/展示工程成本unknown，不能称全部生命周期费用。完整native cost不可用；7715CX/draw及252805120全计划界仅条件理论事前界，536838144 base-U等价查询不是本轮实际调用。

R1/R2/R4/R5/R7/R8保持原proven_scoped边界，R3/R6仍incomplete；全672要求计数550/91/31/0不增。四目标实际联合读出/量子gap、完整14power/measurement成本、物理irrep闭包、E轴/SiC/光学与量子优势均未资格。19轨道两洞FCI仍优先。独立交付通过后本固定路线可closed_negative_result，原应用incomplete、总84Goalactive；不自动启动编译器改写、参数搜索或新shots。

来源与复核入口：执行scope（本地证据，未随题库发布）、量子替代路线与选择依据（本地证据，未随题库发布）、官方网页保存（本地证据，未随题库发布）、逐轨道来源身份（本地证据，未随题库发布）、独立设计与来源（本地证据，未随题库发布）、要求收束建议（本地证据，未随题库发布）。所有实际科学原始数据由本包manifest哈希绑定，打包没有重算科学或更新LATEST。
