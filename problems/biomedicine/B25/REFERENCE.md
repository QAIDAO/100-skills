<!-- 由 release/tools/build_problems.py 自 tasks/B25-fe-hydrogenase-embedding/execution/revision-3-input-closure/RESEARCH.md 生成，勿手改 -->

> B25 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B25 revision3：原五驻点输入闭包与版本审计

本轮完成公开来源审计，原目标仍未完成：**没有取得可执行的原 RE、TS1、IS、TS2、PR 五套几何或哈密顿量，量子任务0项**。取得两个完整作者PDF（2022全文49页含6页SI；2014接受稿34页含16页SI），前驱的部分电荷/模型准备信息确实公开，但不能闭合后文的五驻点嵌入输入。

## 来源与访问边界

2022作者全文 [arXiv2202.04460v2](https://arxiv.org/pdf/2202.04460v2) 已保存4903983字节，SHA256 `59cad01df35e5a62804e840b333f8ae287d957ad3dfaa244a523dd2d8e549858`，43页正文后接6页补充：封面、F2重复shot图、炔烃曲线及一二阶导数。完整PDF无附加嵌入文件，未见氢化酶Cartesian表/积分。官方期刊 [DOI页](https://onlinelibrary.wiley.com/doi/10.1002/jcc.26958) 数据声明为 “The data that support the findings of this study are available from the corresponding author upon reasonable request.” 官方SI列表 jcc26958-sup-0001-supinfo.pdf/214.8KB；本地HTTP403，未绕过。我们阅读的是不同公开作者版本的SI，不声称它与正式SI字节或内容完全相同。arXiv源包406，未检查其成员，不能声称源包无数据。

2014前驱作者机构公开 [接受稿](https://eprints.gla.ac.uk/95072/1/95072.pdf) 已保存5203381字节，SHA256 `25f82375fb8eb4e51b07ac710bd7ebaf37ad7efa747f78ee9d088114b05a4bac`，18页正文+16页SI。SI含FeGP/底物部分电荷表、His14电荷与质子化、PDB模型构建、MM与QM/MM设置、MD阶段及PES扫描。它提供真实模型数值资料，却没有2022五驻点坐标/轨道/积分。其PDF亦无附加嵌入文件。RSC候选suppdata路径403，不重复尝试；该候选路径来自出版商常见命名，未作为已读取/确切唯一官方文件。已读接受稿中的SI是独立作者机构公开来源。

GitHub原arXiv编号repo检索0项；Zenodo正式DOI检索0项；Riverlane公开13repo元数据已保存。两候选README分别是2019量子hackathon与另一H2/QEC编译研究，不是该酶原输入；其余仓库只审名称/描述，没有搜索所有文件。这是有限定向检索，**不证明数据不存在**；期刊明示数据可向作者申请，本任务禁止联系作者，因此该途径未执行。全部请求与失败均见 fetch-log.json（本地证据，未随题库发布）。

## 为何前驱不能替代后文

| 项目 | 2014前驱 | 2022嵌入VQE | 下一步影响 |
|---|---|---|---|
| 路径 | 闭/开构象snapshot；无稳定hydride；相关扫描未定位两个TS | 自行NEB得到两步RE/TS1/IS/TS2/PR与IS | 不能重标记前驱结构当原五点 |
| 软件/几何 | ChemShell/Turbomole、HDLC微迭代 | development ORCA、NEB-CI/NEB-TS | 必须取得原优化坐标/态身份 |
| 几何基组 | Fe TZVP、其他SVP；另有全TZVP检查 | QM部分TZVP | 不是相同几何输入 |
| 高层电子能 | DFT QM/MM | DLPNO-CCSD/TZVPP+CAS4e4o替换 | 需要真实积分及减法基线 |
| 环境 | ff03/GAFF/TIP3P、作者给部分电荷和准备协议 | AMBER转ORCA prms、电嵌入/charge shift/H links | 前驱表格不能代替原五点完整电荷坐标场 |
| 起始结构 | 改造3H65、对齐3F47与2B0J后MD | Reiher组提供起始蛋白/forcefield后新路径 | 公开晶体PDB也不能作为后文终点 |

仅有PDB编号或参数表，仍缺原结构修改、快照、完整电荷坐标与边界映射。本轮没有重新做上述模型构建、截取簇、用图像反推三维坐标或用旧结构生成新积分。2022正文一处称配位Cys175、活动区清单又称CYS176，而2014为Cys176；需原子映射才能判断是重编号或排版问题，不能自行“修正”。

## 输入证据矩阵

| 需要 | 读到的证据 | 门状态 |
|---|---|---|
| 五点Cartesian/原子顺序/质子化 | 五个标签、路径与轨道图 | blocked |
| QM/MM选择与link-H原子图 | 片段化学描述和charge-shift方法 | blocked |
| 原五点完整MM电荷坐标/topology/prms | 前驱部分电荷和后文“私下提供”初始文件 | blocked |
| 每点完整h1/h2/标量核与inactive常数 | ORCA导出FCIDUMP/JW的说明；无实际Fe积分文件 | blocked |
| 原MO/IAO及两occupied/two virtual顺序、连续性 | 化学识别与MP2密度选择规则；无数值轨道 | blocked |
| core/inactive分区及有效一体势 | 总能表不能确定core常数或冻结轨道 | blocked |
| DMET bath | 原实现明确不采用所讨论DMET bath构造 | not_applicable，不能自造bath |
| charge/multiplicity/Nalpha/Nbeta/MS2/态根 | 4活性电子明确；原五点spin元数据未取回 | blocked |
| 同积分CCSD/完整DLPNO减法与收敛日志 | 旧rev2仅算术核对打印表 | blocked |
| TS/Hessian/NEB对应关系 | 方法描述，无原checkpoint/虚频记录 | blocked |

完整结构化required/missing/evidence见 input-closure-audit.json（本地证据，未随题库发布）。通用DMET介绍不能被解释为该CAS带有bath；其他示例的singlet激发态也不能移用为氢化酶spin证据。表格能量不能唯一反推哈密顿量，也不能替代missing scalar energy。

## 最小可执行缺口与预算

最小求解器入口是**原五点各自完整FCIDUMP或JW列表**，携带4轨道/4电子、spin sector、单位、轨道顺序、core/MM/核标量与Table1身份，以及同积分activeCCSD/完整DLPNO参照。即使完整MM文件暂不可公开，原作者已生成的有效积分可以支持固定Hamiltonian求解器组件；报告必须说明这还不能重建完整QM/MM路径。全应用闭包另需原五点完整几何、电荷场、topology/prms、link原子与NEB/TS/Hessian身份。

4空间轨道对应8个自旋轨道/最多8个JW qubits，完整Fock空间256维，固定4电子70个determinants；若Nalpha=Nbeta=2得到原证据确认，则对应36维sector。这里是组合规模估计，**没有创造或求解模型**。输入齐全后可先用同积分精确对角化检查能量、S²和常数，再冻结单CPU≤300秒的VQE-UCCSD/强经典对照、误差与终止预算；本轮输入门未通过，不先编造spin、截簇、训练预算或数值结果。

旧五驻点路径相对能/嵌入增量目标及1kJ/mol误差意图保留。先判定输入/轨道误差是否已大于原微hartree量子增量，再谈扩大空间；不存在由小空间通过自动支持QPU或量子优势的门。静态电子势垒、自由能及物理速率仍分开。本轮没有重算无关表格参数以增加实验计数。

## 交付与复核

GOAL.md（本地证据，未随题库发布）保留原五驻点目标；results.json（本地证据，未随题库发布）、summary.json（本地证据，未随题库发布）、版本对照（本地证据，未随题库发布）、来源审计（本地证据，未随题库发布）与hash清单已归档。qmmm-evidence-audit的选择文件inventory冻结8件实际源文件；通过verify-against只表示哈希/文件身份一致，不表示科学闭包。旧case、execution/LATEST与旧成果全部保护hash不变，共享索引未改。
