<!-- 由 release/tools/build_problems.py 自 tasks/B04-iron-sulfur-sqd/execution/original40q-MPS-SQD-v4/RESEARCH.md 生成，勿手改 -->

> B04 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B04 原40q LUCJ 的截断MPS量子组件与采样修补

已在作者公开[2Fe–2S]原30e20o、40qubit空间执行固定优化LUCJ的近似MPS门传播，随后验证保存截断态的有限采样与固定支持SCI。状态为 `normalized_saved_truncated_MPS_sampling_validated_precision_failed`，原目标 `incomplete`。本轮可归档为组件负结果；没有通过1mHa、自旋及整体残差/收敛门，不构成量子优势或电子转移目标完成。

（图：独立验收科研图，本地证据，未随题库发布）

图A展示原Aer采样失败与完整环境修补的统计门；图B为同谱外部近似DMRG参考差，不是严格误差下界；图C/D保留修补后各支持的自旋与投影残差失败。PNG和PDF均由已冻结JSON生成，未重新执行传播或SCI。

## 来源与真实模型

作者仓库 [jrm874/sqd_data_repository](https://github.com/jrm874/sqd_data_repository/tree/865bd762d3f96ee79bb362eb3dd46951b48b426e) 固定commit `865bd762d3f96ee79bb362eb3dd46951b48b426e`，关联[原论文](https://arxiv.org/abs/2405.05068)。读取公开numeric目录内原QPY和配套MO h1/ERI；不执行下载作者脚本。25项sourcehash审计通过，QPY数据与nativeQASM/角度审计吻合。历史硬件ZIP只静态核其NPY头，未运行objectpickle或用于本轮新采样。

原空间为20空间轨道、15alpha+15beta电子，ecore=0；作者固定HF+UCJSpinBalancedJW，有三次轨道旋转和一次对角Coulomb作用。完整active空间未缩成小CAS或toy。固定总N维847660528，固定(15,15)维240374016，singlet维52581816。共享alpha/beta支持、Ms0和spin balance均不保证S0。

localized、experimentalMO与numericMO输入先前逐项不相同；新增完整20×20轨道变换证书已联合重构h和ERI。独立纯文本FCIDUMP解析及顺序四轴收缩再次核实h最大差1.95e−14、ERI9.63e−14、正交误差<2e−15。因此原DMRG−116.6056091 Eh可作同谱外部近似参考，仍未独立重算，也不能当严格下界。旧peer-review的未闭合记录不改，本轮peer-repair-review记录新证据。

## 冻结方案与原失败

原协议规定Aer0.17.2 MPS bond8/16/32、truncation1e−12、单线程、无noise/fusion、各4096shots；全原线路原生基门cx/rz/sx/x，opt0。逻辑门2366CX、20769Rz、6840Sx、30X，depth1039，没有实际coupling map/routing成本验证。

只保留Nalpha=Nbeta=15采样用于SCI，不恢复invalid outcomes。alpha/beta halfstrings合并频率，top24/48并强制HF，共同支持形成576/2304维Cartesian子空间。对照为同支持规模的uniform固定粒子随机提案与确定性HF一阶SlaterCondon/能量分母提案；不称它为优化HCI或总CPU公平对照。文献RHF/CISD/CCSD/HCI/DMRG作为强经典参考，但预算不同。

原Aer `mps_apply_measure` counts与全张量规范化占据最大偏差12.60σ/11.50σ/5.15σ，前两项超过冻结6σ门。全局范数平方实际为1.092875558/1.060877029/1.039121525，不是小于1。旧norm-assumption-failure.json把abs(norm²−1)误加负号，原错误记录完整保留，独立 `validation/norm-sign-erratum.json` 给出校正与原hash。每站点局部lambda-Gamma两结果范数和约1，却不等同完整环境规范概率；这支持测量canonical假设不一致的机制，但没有隔离唯一上游缺陷。

保存排序直接改变原qreg，并会执行swap/SVD；后续采样复制同一个已排序qreg，不是测量独立未排序原态。Aer静态累计日志按每2366事件分段；logged discard sum13.18/6.11/3.12不是总infidelity，仅包含超过日志chop1e−8的项；原1e−6门仍失败。原joint(15,15)无效counts达41.50%/9.57%/2.22%，总N无效39.23%/9.40%/2.22%。这些是模拟/采样近似问题，不是源线路粒子不守恒或硬件噪声。

## 单独冻结的技术修补

修补从原保存Gamma/Lambda构造A=Gamma×右Lambda与完整right environments。对每个前缀计算w0/w1，用w_s/(w0+w1)条件Born采样；不假定局部canonical规范。它只采样规范化后的保存截断MPS（包括snapshot排序近似），没有恢复精确40q量子态，也没有重新传播或优化。新种子9926100404+bond，各4096shots、同支持规则和原验收门。

第一次修补仅在第一份SCI保存后numpy.bool_ JSON序列化失败。v2修正输出并复用原bond8 counts/D24 SCI，未重新抽样；两对文件逐字节hash一致。cached D24 solver_converged=null保留，独立残差审计不冒充求解器历史。v2 bond8 max_imaginary_probability=0为跳过抽样的占位，原v1实测6.947567521287112e−16；不能把零当新测量。v2冻结输入清单没列这两个缓存依赖，peer-repair-review和最终manifest已补其路径/hash。

新counts的占据最大偏差2.0087σ/2.4378σ/2.3001σ，全部过6σ门。完整联合粒子分布与独立density-transfer收缩比较TV=.01442/.00608/.00128；bulk类别（期望计数≥5）的最大偏差2.8865σ/.7019σ/.5733σ。原independent-audit=False完整保留，修补independent-audit32项allpass；正审计验证数值一致性，不表示精度通过。

## 科学验收仍未通过

修补后6行SCI中，norm6/6通过，投影残差≤1e−5为1/6，自旋S²≤1e−6为0/6，同谱DMRG差≤1mHa为0/6。最小外部参考差约393mHa；不能把投影残差当全H残差。D48的bond32−16能量差+.00222519 Ha超过.001门，counts占据最大差.0874023超过.01门；保存态独立占据差本身.0930011。

D48修补后bond8/16/32能量分别−116.2058410513/−116.2121643306/−116.2099391419 Eh。确定性一阶D48为−116.2747588543 Eh，比三组MPS支持都低；uniformD48为−116.2059744667 Eh。该结果仅表明本轮很小支持预算未表现出量子提案优势，不能外推精确LUCJ、原大shots自洽SQD或量子算法一般有效性。全部分支与失败门保留在results.json及原campaign，不用solver_converged标志覆盖独立残差失败。

## 时间、shots与资源

原作业27.477656CPU秒、27.88548wall秒（含经典提案和SCI后处理）。修补v2为14.698095CPU秒；两完成作业已知CPU合计42.175751秒，但v1失败CPU未知（wall4.326537秒），独立审计也有额外成本，不能宣称42.18为完整总CPU。

原12288distinct draws加修补12288，共24576；修补4096draws复用v1，v2只新增8192，没有双计或重抽。新门传播0、QPU调用0。真实QPU反事实每shot重制备成本：原29073408逻辑CX，两版本58146816逻辑CX；这不是保存MPS上经典重采样实际执行的门成本，也不含hardware routing/noise。

## 可执行交付与结束边界

`results.json` 含统一id/status/target_status/experiment_kind/metrics/limitations及正负分支；`GOAL.md` 冻结完成与未完成条件，`NEXT.md` 禁止重复运行与无量子优势边界。完整manifest覆盖campaign原source、QPY/H、协议、drivers、原和修补counts/SCI、v1缓存、失败jobs、正负审查、旋转证书、独立勘误、图表和本revision；只排除非证据pyc缓存及manifest自身。没有修改LATEST/shared。

要推进原决策，需要另冻能控制bond逼近误差、singlet和全H低能准确度的原空间方案，复现论文configuration recovery并提供预算匹配强经典提案。本轮不自动重试、更大bond/shot、改门槛或重优化。基态能组件不等于电子转移速率或完整蛋白应用。
