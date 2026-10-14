<!-- 由 release/tools/build_problems.py 自 tasks/B03-p450nor-electrostatics/execution/revision-5-input-closure/RESEARCH.md 生成，勿手改 -->

> B03 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B03 revision5：原P450nor输入闭包

本轮完成公开输入深入审计，原静电量子目标仍incomplete。没有取得原4e4o Hamiltonian、广义静电J数值或经过验证的原态输入；量子线路执行0、模拟shots0、科学CPU0。旧public-si-audit-v4的SI表格/误差/门成本审计保留，未重复计算。

## 官方原输入与新增检查

已重读case、README、LATEST指向的v4及原来源。原论文为[arXiv2312.14739v1](https://arxiv.org/abs/2312.14739v1)，关联[ACS DOI10.1021/acscentsci.4c00058](https://doi.org/10.1021/acscentsci.4c00058)。本轮保存官方HTML，SHA256 `9936621e5d80d9313ae7f731512430f844dadf0e1cb85a180e4a8d54a2b887e4`。标准src和e-print入口均HTTP406，日志保留；未得到源包，不能宣称检查过其附件。ACS直接正文403、PMC浏览器挑战均未绕过，未联系作者。

[ACS Figshare25483061](https://acs.figshare.com/articles/journal_contribution/25483061)当前与version API仍只有version1、单个SI文件45286631。名称、大小和md5均与既有下载相同；复用3,751,590字节12页原PDF，SHA256 `ac65241398b0a7b47db423326da85642a0fe7993d1e7a523c0163b6d930eb56c`，没有重新下载或重复表格审计。SI提供算法/建模/图与汇总结果，已读的机器可执行H/J或原counts缺口未被新版本补上。原文仍将实测数据置于合理请求范围，当前授权不包括联系作者。

正文链接[Zenodo2573505](https://doi.org/10.5281/zenodo.2573505)解析到8190968，是Qiskit metapackage软件归档，不是原P450nor数据。未下载或运行该软件。

新增公开仓库审查：QCWare组织列出11库；选读[Quasar](https://github.com/qcware/quasar)、[Promethium示例](https://github.com/qcware/promethium-examples)、[qcscore基准](https://github.com/qcware/qcscore-benchmarks)完整未截断树，分别60/189/188条。固定树标识分别`a40f747e9231ee693bf8805097631286b1cdc66f`、`519977fd29316f208f6b18914accd7719c407758`、`5e10ed3abb9fe54b75443a15fa0a378436f70a1d`。未找到P450/P450nor、1CL6/1XQD、原paper/DOI或FCIDUMP的路径命中。这是文件树及选定静态文本边界，不是所有源文件语义扫描。

Promethium有公开FSAPT文件，因此额外静态读取该示例输入/坐标排除混淆：名为water_dimer的29原子示例实为C8H19NO，无Fe/S，不是原P450nor。没有调用Promethium服务或用其模型替代本案。GitHub P450nor/paper-ID/SAPT-VQE库查询、Zenodo精确原题名/P450nor查询均0条；DataCite精确题名仅原arXiv DOI。只据本轮保存的索引响应陈述这些负结果，不泛称数据不存在。

## 真实起始晶体与不可替代边界

已取得原SI指定的[RCSB1CL6](https://www.rcsb.org/structure/1CL6)和[1XQD](https://www.rcsb.org/structure/1XQD)。PDB SHA分别`ff372ae747fd31f8c4f0c06161f74d2447785989ee401950adbe7b79741b9e81`、`5764ece945de9c7f69b5b1087e2e6818ab8ed618fe8f4271117b0ca402e9f407`。1CL6包含HEM与NO；1XQD包含HEM与DND前驱。SI建模还包括截断/封端、NADH前驱修改、手工放置NO、MOE准备及约束DFT优化。这些操作后的原笛卡尔坐标、确切原子分割与轨道文件未取得。PDB不是最终优化模型；不自动裁簇、赋电荷或重算一个替代H。

这里“中间体A/B”是两个反应模型，“单体A/B”是每个模型内的活性中心与环境分割，两组字母不能混同。每个反应模型各需对应的单体H、环境密度及静电算符。

## 输入闭包与资源

原广义J包括环境电子密度、核—电子和单体间核项。MO活性表示可写成`E_elst = c_elst + Tr(J_act gamma_act)`，其中原core贡献与核项归属必须明确，不能另外重复加入一个猜测核常数。只知道公开平均能量或输出概率不能唯一恢复原J；本轮没有反拟合文献数字。

同H求解/态误差判别仍缺h1/h2、完整offset、单位/积分约定、轨道顺序、最终CASSCF变换、charge/MS2及单体分割。原20e20o SHCI→4e4o CASSCF的图和选取说明不等于数值轨道。SI给出A线路图及架构、B资源计数，未核验完整可靠的两套优化角度/机器线路；不能把图片识别或近似读数称原线路复现。raw counts/端序/布局/独立运行与后选记录也缺。

若真实4e4o singlet输入取得，8逻辑JW位全complex128态矢4096字节，256×256复H约1MiB；固定Na=Nb=2的Ms0扇区36维，矩阵20736字节。这包括其他总自旋，不等于20维自旋适配单重态子空间。4×4实J仅128字节。这些只是容量算术，不是H构造或态运行；工作算符等额外开销另计，规模明显低于2GiB。可在600单线程CPU秒限额内设计完整模型组件，无需裁小；当前不冻结虚假的实验协议，因为输入门blocked。

## 最小可执行输入与下一步

对任一原中间体，最小固定H包为：4e4o完整h1/h2/offset、原Na/Nb/MS2和约定、原轨道与环境定义、`J_act+c_elst`；另给原初态/优化角度/完整旋转线路和布局（或原可验证态文件），以经典同态1-RDM/直接算符期望和同H精确CASCI分开审查。只有J本征值时还需要原旋转矩阵/线路或明确已在该本征基的态，并保持core常数归属。

若只提供原counts和测量本征值/core项，可重放有限shot静电估计、后选保留率与协方差，但无法据此独立核验原基态制备/H。完整重放需raw counts、每运行shots/seed或运行标识、端序/αβ位顺序、bitflip/缓解数据和后选规则。原v4发现随机参考也能通过单一1kcal差值门，因此新组件不能只用该宽门；需态/密度判别及H与observable误差分离。不得从静电正确升格为整体相互作用、自由能或量子优势。

本次没有新科学失败或模型重试。全部31个旧受保护文件hash不变；新设置仅静态来源获取与标准库审计。证据入口：`tasks/_execution/2026-10-04/bio/b03-followup/revision-5/input-closure-audit.json`、`validation.json`、`fetch-log.json`及`FINAL-MANIFEST.json`。未改LATEST/shared，无B03科学job在运行。
