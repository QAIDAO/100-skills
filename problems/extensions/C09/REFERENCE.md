<!-- 由 release/tools/build_problems.py 自 tasks/C09-crystal-annealing/execution/public-periodic-r63/RESULTS.md 生成，勿手改 -->

> C09 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# C09 R63：准确周期 Kr 小模型与完整松弛评分

原生表示通过，固定量子算法/有限读出联合门失败，本固定路线按负结果收束。细1600步 semantic 无条件 relaxedFCC 概率 0.20286222576117302；实际native概率 0.2028622257610588。8192量子模拟读出成功 1603 次，Wilson95 区间 [0.1872312577630794, 0.20441143993285196]。全部错误N和松弛失败留在分母。此结论只对应本 g2/8q/T40 固定协议，不推断所有量子材料方法无效。独立量子审计完整性通过且原门一致；正确审计不代表算法通过。

## 科学对象与模型身份

准确 OpenKIM `LJ_Shifted_Bernardes_1958LowCutoff_Kr__MO_995724792024_004` 和 driver `LJ_Shifted__MD_498634107543_004`；ε=.014 eV、σ=3.65 Å、rc=9.91 Å，胞边5.653 Å、三轴周期、g2全8占据位。全部256配置、N0..8保留，无mu、数目罚项或origin pin。来源明细见准确取源（本地证据，未随题库发布）与SHA清单（本地证据，未随题库发布）；[NIST官方条目](https://www.ctcms.nist.gov/potentials/entry/1958--Bernardes-N--Kr/LJ_Shifted_Bernardes_1958LowCutoff_Kr__MO_995724792024_004.html)确认准确low-cutoff ID。原文为[arXiv v2](https://arxiv.org/abs/2307.03123v2)/[PRA](https://doi.org/10.1103/PhysRevA.109.032416)，本地论文（本地证据，未随题库发布）。

原compute严格 r²<rc²，常数energy shift而非force shift；物理能保留self-image、ordered-pair一半与所有cutoff内镜像，不采用minimum-image代替能量。不同格点J先聚合镜像再上截1eV，self线性项保留；连续raw势不cap。QUBO→Ising/globalphase与梯度两FD步长独立资格。准确source-definedFCC参考 -0.431986694916221 eV/胞，论文−.431との差 -0.0009866949162209981 eV，超过事前±.0005窗，`paper_pointwise_energy_reproduction=false`。没有调ε/cutoff/零点追论文数字；这是来源定义的新缩小实验，未逐点复现论文。

## 经典强基准与连续结构身份

256离散枚举给raw/cap非空非满FCC4 ground证书；完整库对每mask固定一次，N0/N1直接解、247次BFGS、17376次objective物理能/梯度尝试、512次额外物理评分尝试。全部seed/失败/checkpoints已封存，无免费重启。完整库足以作为这个小问题的强经典离散→连续基准；不是连续全局最优或Hessian稳定性证明。所有库费用付费入账，量子只提案，库只在全部state保存后评分，不能用success masks制态或造phase。

70个N4起点仅67个通过 optimizer+finite+全原子force≤1e−6eV/Å+坐标RMS≤.001Å/max≤.002Å+sourceFCC能差≤1e−5eV 联合门。mask46/165优化器未成功且大force；mask78虽优化器success、低能近FCC，force为1.029656254053428e-06，超过冻结门，仍false。没有把67/70写成全N4收敛，也不删除三例或把失败硬改为FCC。

| N | attempts | optimizer_success | force_gate_count | FCC_qualified |
|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 0 |
| 1 | 8 | 8 | 8 | 0 |
| 2 | 28 | 28 | 28 | 0 |
| 3 | 56 | 56 | 53 | 0 |
| 4 | 70 | 68 | 67 | 67 |
| 5 | 56 | 56 | 55 | 0 |
| 6 | 28 | 28 | 27 | 0 |
| 7 | 8 | 8 | 6 | 0 |
| 8 | 1 | 1 | 1 | 0 |


| mask | optimizer_success | final_energy_eV | max_force_eV_per_A | force_gate | FCC_qualified |
|---|---|---|---|---|---|
| 46 | False | 3.7340929723807172 | 1.4958950219599985 | False | False |
| 78 | True | -0.4319866949136111 | 1.029656254053428e-06 | False | False |
| 165 | False | 1.9678392988896074 | 5.13389802154598 | False | False |


完整每N CSV（本地证据，未随题库发布）、失败N4 CSV（本地证据，未随题库发布）保存status/message/源recordSHA；全部原始coords、optimizer status、次数、witness在完整库（本地证据，未随题库发布）和松弛结果（本地证据，未随题库发布），独立库审计（本地证据，未随题库发布）核原始初态及最终端点能/梯度与身份，不重跑BFGS。扰动起点仅核seed坐标，未另算jitter起点物理；有限96个坐标witness不是任意连续平移/Hessian证明，见审计范围澄清（本地证据，未随题库发布）。

## 量子提案、读出与公平比较

|+>8由真实RY(pi/2)制备。H(s)=−(1−s)ΣX+s Esearch/S，S来自h/Jcap绝对值和，完整常数I/Z/ZZ由系数生成。固定T40、800/1600 midpoint Strang；细线路逐条RY/RZ/CX+GP实际replay，全256 complex state保留，无phase alignment/real投影/后选制态。局部门全basis/全部角、完整指定输入态native误差、粗细分布与norm门已独立核。这不是全256×256unitary资格或连续时间严格误差证书。

| method | P_N4 | unconditional_relaxed_FCC_probability | P_relaxed_FCC_given_N4 | successes | draws | Wilson95_lower | Wilson95_upper |
|---|---|---|---|---|---|---|---|
| quantum | 0.21127750222059735 | 0.2028622257610588 | 0.9601695572359046 | 1603 | 8192 | 0.1872312577630794 | 0.20441143993285196 |
| uniform_bits | 0.2734375 | 0.26171875 | 0.9571428571428572 | 2201 | 8192 | 0.2591878875763717 | 0.2783824742903712 |
| uniform_N4 | 0.9999999999999998 | 0.9571428571428571 | 0.9571428571428573 | 7821 | 8192 | 0.9499920142792336 | 0.9590055593600185 |


全bits uniform 的exact概率 0.26171875；N4 uniform 的exact概率 0.9571428571428571（额外N4信息、不同空间，不能与未限制N量子分母宣称同协议优势）。三条各8192独立PCG64流，baseline seed事前域分离；量子draw用实际fine-native概率，微小FP归一调整单列。P(N4)/条件比与无条件均报告，主门只用无条件。全库失败按false评分，库lookup不是新松弛计算。

| gate | observed | threshold | direction | passed |
|---|---|---|---|---|
| native_state_maxabs | 3.392727896801892e-14 | 1e-10 | <= | True |
| native_probability_maxabs | 8.449838051483027e-15 | 1e-10 | <= | True |
| coarse_fine_TV | 1.0899752704394492e-06 | 0.01 | <= | True |
| coarse_fine_relaxed_FCC_delta | 4.6687074090057123e-07 | 0.005 | <= | True |
| fine_semantic_unconditional_relaxed_FCC | 0.20286222576117302 | 0.5 | >= | False |
| Wilson95_lower | 0.1872312577630794 | 0.5 | >= | False |


经典完整枚举+逐配置付费局部松弛是必要强参考；uniform仅提案分布参照。没有扫描T/seed/能标追门，没有量子优势结论。量子primitive/编译/IR/传播/真实native replay/readout/lookup组件费用完整保存，狭窄draw wall不是公平TTS。全量库先解出小问题不能被当成免费success oracle。此固定小模型的推荐路线是完整256枚举与已付费松弛库；量子P(N4)低于全bits uniform，条件成功率较高仍不能补偿无条件失败。

（图：周期FCC模板与库，本地证据，未随题库发布）

（图：概率与误差，本地证据，未随题库发布）

## 完整费用与失败边界

| stage | CPU_s | wall_s | RSS_bytes | output_bytes |
|---|---|---|---|---|
| input-production | 0.8999999999999999 | 0.92 | 71254016 | 86750 |
| input-audit | 0.55 | 0.52 | 69238784 | 447714 |
| input-audit-r2 | 0.55 | 0.53 | 68239360 | 448661 |
| relax-production | 98.46 | 78.63000000000001 | 109985792 | 16102778 |
| basin-audit | 1.3900000000000001 | 1.22 | 104579072 | 2140346 |
| quantum-production | 4.56 | 4.01 | 113262592 | 7622454 |
| quantum-audit | 6.859999999999999 | 6.47 | 122224640 | 1784152 |


七stage合计CPU113.27s、累计wall92.30s、峰RSS122224640bytes、输出28632855bytes、scratch0bytes。CPU/累计wall求和，RSS峰值max；累计wall不是端到端并行延时。首次input audit完整运行但margin口径错误，完整性false，其0.55CPU/0.52wall仍计一次；修正版另stage封存、未变科学势/门。见修复记录（本地证据，未随题库发布）与资源总账（本地证据，未随题库发布）及独立核账（本地证据，未随题库发布）。monitor时间已包含，不二次相加；组件wall已包含parent stage。工程render/打包另列receipt，未冒充科学stage或记为0；完整历史生命周期未知。

| gate | fine_actual_once | conditional8192_physical_plan | actual_QPU_gate_executions |
|---|---|---|---|
| RY | 12808 | 104923136 | 0 |
| RZ | 140800 | 1153433600 | 0 |
| CX | 179200 | 1468006400 | 0 |


GP保存但无物理门；coarse原生计划未执行，fine实际一次native replay与8192假想曝光严格分开。实际QPU调用/物理shots=0。硬件连接/routing/noise/门时间/校准/容错unknown，T40无量纲不能换算20µs。该新周期小模型没有闭合原g4/g6、MoS2三体、实验晶相或工业CSP。原应用仍incomplete。

## 验收范围与可重建入口

旧结果（本地证据，未随题库发布）仍`algorithm_pass`，只支持非周期empty/full编码传播；本轮不反转旧门。当前真实周期/非平凡竞争/全库结构身份/固定量子实验和全部误差成本若经独立交付核验齐备，可按事前R52范围复核（本地证据，未随题库发布）限定支持R4/R6 proven_scoped；不等于算法成功、论文逐点复现或原应用完成。LATEST/global由父线程另行核验晋升，本builder不修改。

固定source与seed/门/失败政策见方法（本地证据，未随题库发布）、松弛设计（本地证据，未随题库发布）、量子设计（本地证据，未随题库发布）和ROOT（本地证据，未随题库发布）。全部七stage结果/合同/worker/manifest/receipt与源SHA由展示manifest递归绑定。重建命令见 REPRODUCE.md，属于未来有预算的独立复建，不指示原目录免费重跑。图仅依据保存JSON/CSV；两张PNG已经父级及独立实际目视通过并绑定精确SHA；PDF仅导出未目视。

图中“Uniform all 256 bits”指8位占据变量的全部256个位串构型，并非256量子比特。

渲染工程另列 CPU2.3400000000000003s、wall2.1799999999999997s、RSS220037120bytes、输出824428bytes、scratch0bytes，不并入七个科学stage。见工程receipt（本地证据，未随题库发布）与工程seal（本地证据，未随题库发布）。authoring/资料获取/打包完整生命周期未测。

R1–R8按独立范围复核（本地证据，未随题库发布）记限定proven_scoped；R4/R6证据包括真实非平凡周期/连续结构竞争、完整量子演化和误差/读出/付费成本，结果为科学负例，原应用仍incomplete。本固定路线closed_negative_result；晋升须最后独立delivery准入，未晋升LATEST/global。
