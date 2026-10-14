<!-- 由 release/tools/build_problems.py 自 tasks/B07-protein-ligand-embedding/execution/public-source-v4/RESEARCH.md 生成，勿手改 -->

> B07 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B07 原输入闭包审计 v4

本轮完成来源审计，新增量子模拟 **0**，原蛋白结合能目标 **incomplete**。主 EWF-TrimSQD 原 Hamiltonian 未闭合。凝血酶官方 SI 可提供五套真实配体坐标及各 4023 个 ESP 点电荷，但其与 B15 已执行的输入逐行完全相同；不重复 B15 的派生 CAS，也不给 B07 新量子完成计数。

## 取得的真实输入

[arXiv 2605.01138v2](https://arxiv.org/html/2605.01138v2) 的 HTML、PDF及[源包](https://arxiv.org/src/2605.01138v2) 已原样保存。源包严格只有 main.tex、00README.json 和7幅 PDF图，共9个regular文件，没有原含水结构、积分、样本或投影矩阵。PDF文本转换有字体/字典警告，方法核实以原 main.tex 与 HTML 为准。

原文给出初始 [3PTB](https://files.rcsb.org/download/3PTB.pdb) 和 [4W57](https://files.rcsb.org/download/4W57.pdb)，本轮取得原PDB。分别只有1701/1597条坐标记录，4W57含264条altloc记录。它们是最初晶体，不能替代作者12635/11608原模型；需要原MD/水分子保留、手动His/Lys质子化修正及最终坐标。没有由PDB另制含水结构。

凝血酶[官方全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC13418096/)与 [ACS Figshare ZIP](https://ndownloader.figshare.com/files/66481841)、[SI PDF](https://ndownloader.figshare.com/files/66481844)均公开取得。官方API元数据的文件大小与MD5通过。ZIP/PDF SHA256与 B15 保存件相同。五个ZIP成员解析后全部坐标、ESP行和member哈希也与B15输入一致：

| 原配体 | 原子数 | 配体+1电子数 | STO-3G AO计数 | ESP点数 | 实际ESP电荷和/e |
|---|---:|---:|---:|---:|---:|
| 2zc9 | 52 | 204 | 164 | 4023 | 0.03598600 |
| 2zfp | 45 | 172 | 137 | 4023 | 0.18377700 |
| 2zgb | 51 | 188 | 151 | 4023 | -0.03507300 |
| 3dhk | 62 | 244 | 198 | 4023 | -0.16427200 |
| 3dux | 58 | 210 | 170 | 4023 | -0.04179400 |

AO计数由原元素/STO-3G壳层计量得到，不是新SCF。原文formal protein−1与实际拟合ESP电荷和不同，本轮保留每个原值。XYZ+ESP文本未显式标记单位和自旋；原B15在Å/闭壳层约定下9套RHF落入SI舍入窗，为该使用口径提供旁证，此处不重跑。B15原600CPU止损、第五配体环境未完成和派生CAS范围均保留，见原B15报告（本地证据，未随题库发布）。

## 原模型与能量组装边界

主论文采用ORCA HF，原EWF为原子中心fragment+bath；MP2局部半径7Å、ERI额外缓冲3Å，基础bath η为蛋白/配体1e−5、水1e−7。改良T4模型按距配体3Å内残基选择3-21G、其余STO-3G，并在结合区加严η至1e−8。实际局域轨道、bath eigenvectors、保留AO/ERI列表与mixed-basis残基表没有公开实例文件。

EWF总能由分区1-RDM及2-body cumulant重构，原结合定义为 E(bound)−E(unbound)−E(ligand)。trypsin bound0/unbound−1，移除的是benzamidinium+1；正文另对unbound及孤立ligand的一体相关能施加 Q·Δq/r 修正。实际fragment电荷变化、质心距离和投影/常数缺失。片段本征值相加或相减无法替代此原组装。

凝血酶R2是不同模型：完整原配体在4023点电荷场中做meta-Löwdin DMET，原fragment2有24 localized+24 bath轨道，原VQE截断2e2o/4e4o及8e6o。原fragment atom/AO映射、bath、收敛势/μ和嵌入h1/ERI/ecore尚缺。原结合差 E(ligand-in-protein)−E(ligand-in-vacuum)要求收敛的分区DMET总能。该ESP模型没有溶剂、色散和温度贡献。论文明示Tangelo0.4.0到Qulacs/shot/hardware的作者transpiler为trade secret，公开通用Tangelo不是整套原实例。

原文报道基础EWF结合能偏正、T4换基组/加严bath及trypsin增加静电修正才改变预测符号，说明模型误差不能由fragment solver精度替代。此处模型输入仍未闭合；solver和measurement均没有新实验误差；global assembly缺失另列，不以已刊数字充当新模拟。

## 仓库核验与可执行性

原文所引[SBD](https://github.com/r-ccs-cms/sbd)本轮固定commit `ee9d33e62cf8483754504de513e8307426e5198e`、root tree `a694fc79b3b84b00fa4e7d6c09cdbd72275cc611`。请求真实tree SHA，完整递归API response与commit元数据一致，选定raw文件Git blob SHA1通过；不是将commitSHA误当treeSHA。314条目录中数据为H2O/N2/NH3/C2H2/C4H4/Fe4S4及测试模型，没有命名为原蛋白的输入。未下载运行这些替代模型。该排查仅支持已核目录/源码未提供目标，不声称全球不存在数据。

Tangelo本轮main固定commit `4b478a101cba28a58cc0ba17ad5ef110a737fce3`，468条目录也未见目标实例。原v0.4.0固定commit `2b0c04b4fb4cd18d2474b9606ada34691567c564`的DMET/bath静态源复用B15，不执行。代码明确按fragment切片与1-/2-RDM做能量contraction并加全局项，足以防止用solver本征值冒充总能，仍不足以从通用算法恢复作者数值bath与投影。最新main不是原paper版本。

原Table I列示的最大fragment为66e45o、36e35o、34e42o，直接未taper量子规模90/70/84q。若Ms=0，full sector维数分别是 827,138,850,772,872,845,025、20,589,520,178,326,522,500、64,852,697,142,807,850,248,336；这些是计量条件值，不是取得sector文件的证据。小原fragment或原CAS4e4o可在600单线程CPU秒/设计2GiB内形成同H强经典对照，但当前缺其真实积分，没有据此造模型。

## 核验与最小下一步

自写 audit_inputs.py（本地证据，未随题库发布） 97项通过：源包完整目录、静态TeX一致性、SI大小/MD5、五个真实输入逐行与B15一致、粒子计量、PDB有限坐标、正确commit→treeAPI绑定、实际raw blob身份及旧文件未改。未执行作者源码、pickle、SCF或量子线路。部分网页工具返回PMC挑战页，未交互挑战；普通未认证公开获取取得完整PMC正文。旧ACS拒绝没有绕过，官方SI从独立公开Figshare API取得。

最小可量子执行单元是作者实际单fragment的 h1/ERI/ecore、Nα/Nβ、orbital order、fragment/bath/frozen projector与同H经典参考。原CAS4e4o为8q、Ms0维36，取得这些后可另冻守粒子数线路、3seed、有限shot和资源协议，分别验收solver误差与分区RDM误差。完整binding还要配对原结构的全部分区能量张量、HF/常数及电荷修正；单片段通过不证明蛋白结合能准确。此处不发起后续后台任务，不改LATEST或共享汇总。
