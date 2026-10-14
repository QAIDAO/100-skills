<!-- 由 release/tools/build_problems.py 自 tasks/F17-electron-molecule-rmatrix/execution/RESEARCH.md 生成，勿手改 -->

> F17 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# F17 原始来源研究与条件性推荐

来源核验

2507.05514v2明确H2 STO3G、GTO continuum、radius10a0、5dim扇区；SSO只用H和92Pauli，作者强调noiseless statevector。全文无完整数值一/二电子积分及boundary函数可在此直接运行。

条件性推荐

若拿到真实UKRmol内区积分与channel basis，优先SO(k) SSO以保证所有roots正交并输出boundary；现实碰撞数据仍由成熟UKRmol/CCC承担基线。

候选方法及经典基线比较

foldedH和variance cost需H²且容易漏root；SSO较少distinct terms但门深和cost calls不可免；容错多rootQPE可能更稳，需要初态overlap和目标能窗。

本轮实验

SO(5) Givens sequential-subspace VQE and controlled boundary-amplitude measurement。冻结输入：explicit synthetic radial inner-region:radius10a0,V=-.5exp(-(r/1.4)^2)Ha;5 sin((n+.5)pi r/a)basis;not H2。真实本地功能模拟量子态准备/门/受控读出，ED或ODE只作独立真值或明确标记的理想基态输入。实现细节、环境、随机种子和源码hash在manifest；raw.json保留全响应或计数，raw.csv提供可读指标。

验收与全成本

{"max_eigenvalue_error": 1e-06, "orthogonality_error": 1e-10} 为预注册最大误差。审查全部参数切片，有限step/shot/depth/cutoff曲线分别解释。理想statevector时间不是QPU时间；后选成功率、优化调用、Krylov采样、response路径和经典投影成本不能忽略。模拟硬件噪声或编译之外的成本不能由小尺寸外推。

范围限制
- 五维径向SSO为task-specific synthetic接口验证，不是H2内区谱
- boundary/R矩阵只对该径向模型有效，未输出电子分子截面

未完成输入
- H2有限体积one/twoelectron integral tensor
- retained target/channel basis 与bound配置矩阵
- continuum boundary uij(a)
- outer-region传播和实验截面数据

下一步：向作者或UKRmol流程获取实际积分/边界文件，逐root验能量、残量、正交，再连outerregion。

原始来源

- [Electron–molecule scattering via R-matrix variational algorithms on a quantum computer](https://arxiv.org/html/2507.05514v2)
- [Complete Solution of Electronic Excitation and Ionization in Electron-Hydrogen Molecule Scattering](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.116.233201)

本轮source快照见 `tasks/_execution/2026-10-04/frontier/sources/F17-primary.txt`（其HTML/补充截取若存在一并保留）。本地实验结论在results.json，不能倒写成文献结论。


执行后证据审查

- v1真实执行但用synthetic径向模型；后发现Zenodo真实输入，需以public-input-v3另案结果审查，不能倒改v1manifest。

原作者公开Zenodo代码/积分已经取得，冻结v1缺口为当时状态；新的实际输入结果见public-input-v3，两个optimizer均未过门。当前发布次序与归档NPZ不一致，不声称原论文实验复现。
完整数值与cost边界见 RESULTS.md（本地证据，未随题库发布）。


## 主代理新增：门序与后选的独立诊断（v4）

此前v3归档复现失败保留。新协议与原门序在同一公开积分/同一五态子空间、相同SLSQP预算和两个初始化下比较。先用Qiskit的基本CX/Ry构造NC矩阵，再独立传播完整12比特线路，与五维表示比较40组随机态；最大差5.63e-16。

原j-major前乘门序在逐根优化时扰动已优化列，列变化范数最大2.036，最终多根误差1.359 Ha。新i-major右乘（实际线路逆序施门）让后续门只作用于尚未锁定的输入列，旧列变化为0；五根最大误差2.043e-14 Ha。新协议所有预冻结门槛通过，但不能据此称原归档线路已复现或证明量子优势。

原“ancilla求和”必须有物理解释：五个ancilla在Hadamard基测量并全后选，成功概率1/32。当前完整12比特态核验确认这一概率；每个被接受的能量样本期望约32次制备，尚需乘以能量测量分组、训练评估和有限shot预算。不存在免费trace-out得到相干和。

证据：v4 manifest（本地证据，未随题库发布）、results（本地证据，未随题库发布）、raw（本地证据，未随题库发布）。源码为tasks/_execution/2026-10-04/frontier/f17_order_diagnostic.py。原任务仍缺连续谱边界振幅与外区匹配，尚无分子散射截面。

### 独立复核补充

独立Qiskit复核已确认锁列、全部最终态和显式五Hadamard后选；不能用partial trace替代相干投影（最低根能量会改变约0.260 Ha）。五个参考根来自B†HB，不是完整H的五个精确根。两个优化臂仅具有相同迭代上限与初始化数，实际理想能量调用分别562和331次，不能称等测量预算优势。详见总执行目录validation/frontier-f17-audit.md。
