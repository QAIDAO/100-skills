<!-- 由 release/tools/build_problems.py 自 tasks/M22-cavity-polaritonic-states/execution/native-three-state-v2/RESEARCH.md 生成，勿手改 -->

> M22 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M22 三低态 SA-VQE：经终审的拒绝终态

**严格协议 rejected；原目标 incomplete；独立数值终审通过。** 本轮完成固定8点、16个seed，资源与源码入口核验通过。每点所选候选的全部数值门均通过，但16次 SLSQP 都在150迭代上限退出，`Iteration limit reached`，优化器成功数0/16。事前协议要求每点两个seed都成功；因此不能因数值误差小而改判 accepted，也未重试、延长预算或调整阈值。

## 模型、初态与执行边界

本轮是原 LIAC 模型族的新预注册实验：H₂/STO-3G，中心对称z轴，λ=.1，ω=1Ha，one-hot photon0..3，r=[.4,.5,.6,.7,.74,.8,.9,1]Å。8wire，三层24参数；每层先 spinfree single，再pair，再同空间轨道、同photon邻接连续成对的α/β controlled-Givens。训练使用完整对称门块的12维限制；每个有限seed候选最终在全256维逐原生门重放。

原§IV.1明确的三参考为HF×0、归一化HOMO-LUMO singlet-excited HF×0、HF×1，均literal native preparation，没有QED-FCI向量初始化。Round27的HF×0/1/2猜测已纠正。Eq20与Eq21标准Pauli符号不一致，本轮冻结Eq21显式动作，并披露独立Pauli-string原生分解。积分采用PySCF，原文为Psi4/QuantNBody；不是作者完整driver、角度或精确网格逐点复现。

PF保留核排斥、total signed dipole、−√(ω/2)λD(b+b†)、.5λ²D²，无ω/2零点。D16@D16先平方再投影，保留完整有限MO自能；它不同于连续空间Pr²P，STO-3G电子basis误差未评估。旧λ=.08 ground-only结果未用于本次初始化或对照。

## 保存数值的汇总

以下源于保存的raw JSON，并经独立终审对完整门重放、保存的哈密顿量组装、Ritz谱、态子空间及组成复算。所选候选三态最大能误差 **9.6402387159688629e-06 Ha**（R=.9Å，E₀；约.00964024mHa），最大E₂−E₁误差 **2.3206701780797978e-06 Ha**（R=.8Å），cutoff3→5/5→7三态最大差 **1.1153273606068215e-06 Ha**（R=1Å）。对应门为1.6mHa、1e−4Ha、1e−4Ha。

三态平均projector leakage最大7.5795176806003894e-06，最差principal sin² 2.2209155651320422e-05，cluster sin²最大2.2034557159322787e-05；门分别1e−3、1e−2、1e−2。低三态外边界gap最小0.10234884553519302Ha，超过1e−4Ha。norm/Gram、N、S²、one-hot/singlet、native读回综合误差最大1.5898393712632242e-13；native与restricted重放差最大7.8271066410870366e-14，均低于1e−10。

| R / Å | SA Ritz E₂−E₁ / Ha | 三能max误差 / Ha | gap误差 / Ha | cutoff max差 / Ha | 两seed均能spread / Ha |
|---|---:|---:|---:|---:|---:|
| 0.4 | 0.553530198 | 7.58285e-07 | 8.33188e-08 | 7.08309e-08 | 3.66832e-07 |
| 0.5 | 0.363515606 | 2.18085e-06 | 1.95391e-06 | 1.15434e-07 | 1.72447e-07 |
| 0.6 | 0.225082576 | 2.30238e-06 | 1.19607e-06 | 1.73657e-07 | 2.58844e-06 |
| 0.7 | 0.163386778 | 5.56868e-06 | 7.55128e-07 | 1.92096e-07 | 2.72218e-06 |
| 0.74 | 0.164619730 | 7.37177e-06 | 2.41474e-08 | 2.30553e-07 | 3.64348e-06 |
| 0.8 | 0.185698950 | 6.66729e-06 | 2.32067e-06 | 3.88294e-07 | 4.19837e-06 |
| 0.9 | 0.240370750 | 9.64024e-06 | 1.64481e-06 | 7.05068e-07 | 2.71028e-05 |
| 1 | 0.295383131 | 2.49842e-06 | 1.59791e-06 | 1.11533e-06 | 8.46438e-08 |

最低**已采样网格**gap在R=.7Å：SA Ritz=0.1633867776939614Ha，FCI=0.16338602256546408Ha。固定8点不能精确定位连续minimum，不能由连接折线建立连续PES或LICI。相邻reference gap≤1e−4Ha时按cluster比较projector；本轮低三态均分离。

已排序E₁/E₂的组成显示交换：R=.4Å时两态平均photon数为.98408935/.01891751，singlet-single电子边际权重为.01920158/.98112750；R=.7Å时photon数为.58401435/.42266630；R=.74Å为.44280686/.56455814；R=1Å为.10546991/.90789363，single权重为.89596912/.10070836。它支持该有限模型的态混合与组成迁移；边际组成不能直接替代完整product-state联合权重或实验观测。

## 优化、成本与推荐

两固定seed 2026100401/2026100402各点独立uniform[-.2,.2]起点，等权Trace(W†HW)/3、SLSQP、ftol1e−10、bounds±π。总目标调用**60638**，每seed 3783–3794，均低于硬6000上限；实际限制来自maxiter150。选择按最低均能再seed固定，所选值仍有完整失败身份。两seed均能spread最大2.7102803982215207e-05Ha（R=.9Å，约.0271028mHa）；这里只比较两个均能，不能证明统计稳健性、单态误差或全局最优。

生产入口记录总42.07CPU秒、37.02wall秒、采样RSS119046144bytes（113.53125MiB）、输出3169480bytes，低于300CPU/600wall/1GiB/128MiB。固定monitor本身终态为42.045268CPU秒、36.9504975wall秒、3031597bytes；入口总量包含外围与后续metadata，输出口径不同需保留。monitor采样间隔.05s，有采样及终止延迟边界。源码hash通过，worker exit0是正常交付终态，不代表科学accepted。

每态一次U为H816/RZ588/CX624；60638目标调用对应181914次native-equivalent U，最终16候选×3参考共48次full256重放。记录8次3×3Ritz解和24次12/18/24维reference解。全部实际经典积分、优化、原生重放、cutoff/FCI、Ritz、I/O/monitor时间都在资源止损内。这个账不包括硬件Pauli能量shots、噪声重复、Ritz测量或容错；QPU调用0，finite shots0。

推荐关闭本冻结协议为rejected，保留所选候选的有限模型数值质量与原生门实现证据。线路表达力值得保留，但优化成功条件没有满足，不能作为稳定收敛方法交付。后续若改变优化或收敛合同，应先提出独立预注册版本与相应问题，不能用本轮好误差事后取消optimizer门；本报告不启动新运行。只有one-hot qubit编码，尚不能推荐其优于qudit/qumode或硬件路线。原目标所需编码比较、noise/shots、basis依赖、连续物性及实际腔催化仍未完成。

## 可执行证据入口

- 科学生产目录：m22-three-state-v2（本地证据，未随题库发布），含冻结protocol、raw-results、逐点/seed checkpoint、资源ledger和原生源码。
- 生产入口：m22-round28-production-intake.json（本地证据，未随题库发布）；protocol SHA256 `dab752c4b107e6b95ce24cbefc8703b390c7b24f3e709e135dc4bdf1756cae8e`。
- 本报告精确数值、逐点数据及输入hash：results-draft.json（本地证据，未随题库发布）。
- 保存数据图：saved-summary.png（本地证据，未随题库发布） / PDF（本地证据，未随题库发布）；plot.py（本地证据，未随题库发布）仅读取JSON，不计算模型。

独立终审144项检查通过，科学协议仍rejected。审计费用15.040 CPU秒，原始记录、数组、协议和资源均封存。

公开原始来源：[Ab Initio Polaritonic Chemistry on Diverse Quantum Computing Platforms, v2](https://arxiv.org/abs/2506.12504v2)。

终审独立性边界：独立门作用重放共享已通过全basis夹具的生产电路生成器；用保存的电子积分与D16重建有限模型，未重新生成AO积分或偶极矩。没有重新优化、调种子或读入精确本征态训练。

独立终审结果（本地证据，未随题库发布） · 父级终验（本地证据，未随题库发布）
