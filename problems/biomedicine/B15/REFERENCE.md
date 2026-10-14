<!-- 由 release/tools/build_problems.py 自 tasks/B15-thrombin-dmet-binding/execution/public-coordinate-quantum-v3/RESEARCH.md 生成，勿手改 -->

> B15 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B15 原坐标派生量子电子子问题，原 DMET 目标仍开放

本轮新取得官方原五配体坐标与 ESP 点电荷，执行了 9 个完整8比特主组件和两个4比特预检。四个配体完成真空/原ESP配对。第五个3dhk的真空已完成，原ESP的RHF触及600CPU秒硬止损；原作业failed/exit−24，未重启。原DMET fragment2输入仍未闭合，不能称原结合能目标完成。

## 来源与选择

[作者论文](https://pubs.acs.org/doi/10.1021/acs.jcim.6c00544) 的数据声明指向几何/点电荷 SI 与公开 Tangelo，同时将其 shot-based 转译器列为商业秘密。此次通过官方 [Figshare 32952515](https://api.figshare.com/v2/articles/32952515) / [32952518](https://api.figshare.com/v2/articles/32952518) 取得原ZIP与PDF，并核验大小和原MD5。完整五配体为2zfp、2zgb、2zc9、3dux、3dhk，45–62原子、172–244电子、STO-3G 137–198AO；各环境原ESP点数4023。按原子数递增执行，未按计算结果挑选对象。

实际 ESP 总和依次为+0.183777、−0.035073、+0.035986、−0.041794、−0.164272e，与正文formal protein−1不一致。本轮原样使用；最初以−1为条件的输入预检失败与脚本保留。已完成的9套HF全部落入原SI TableS4三位小数的±0.0005Ha舍入窗。这个数值吻合支持原输入/静电能定义的一致性，不能消除formal/fitted charge定义缺口。

官方Tangelo v0.4.0固定commit 2b0c04b4fb4cd18d2474b9606ada34691567c564 的完整tree与DMET/bath源码仅作静态规范。未取得作者原fragment2 atom/AO map、bath、收敛correlation/chemical potential或嵌入h1/ERI/ecore。B05最新官方SI仍只有已知完整酶坐标；补取arXiv2408.11091v3源码archive只有TeX/bibliography/图，无qm_models.xyz、projector或积分。它是后加入的研究源，未进入已冻结B15数值输入；未构造猜测的B05酶片段。

## 冻结模型与实际量子线路

原完整配体几何、原ESP、电荷+1、spin0、STO-3G保持不变。direct RHF tol1e−10/max100；环境势和核—点电荷项由同一PySCF qmmm对象进入电子Hamiltonian与constant。主空间固定为canonical HOMO−1/HOMO/LUMO/LUMO+1、CAS4e4o，core=nocc−2；2zfp另取HOMO/LUMO CAS2预检。两环境canonical轨道独立选择，未用共同跟踪projector；不是原48轨道localized fragment+bath，也不是原片段的主动空间。

保存完整CAS h1、四指标ERI、ecore、MO指标/向量。精确强基线为同积分PySCF FCI，并以独立full-Fock creation/annihilation矩阵、Nα/Nβ、S²与singlet投影精确谱核对。8比特full Fock维256，Ms0维36，S0维20；它是强经典易解的电子组件，不能据此推断原大DMET模型的量子优势。

守粒子/自旋PX/OR brickwork四层24参数；同一zero及seed1504 Gaussian两初猜，BFGS解析梯度/max500/gtol1e−8，取固定两次中更低能量。参考FCI只作验收，不拟合参数。优化器在36维Ms0内用同一QNP门的精确作用与解析梯度做经典优化；随后实际传播最终Qiskit原生线路并与该态交叉核验。没有硬件优化或shot-based训练。实际Qiskit线路用blocked JW：alpha0..3/beta4..7，门作用[p,p+4,p+1,p+5]；原生rz/sx/cx、opt3、seed1504、逻辑all-to-all，无硬件路由。主组件CX132–204，depth192–319。保存原生态与dense H；独立bitwise费米/Pauli审计对全部11组件通过。

SparsePauliOp.from_operator显式atol1e−12、rtol0，并独立完整矩阵读回；没有默认1e−5删项。原生能量、sector probability、S²、独立same-H FCI均闭合。

## 数值与未通过门槛

9个主CAS4中3个通过冻结1e−6Ha理想求解门，6个失败；误差范围5.6843e−12至5.2773e−6Ha。两CAS2预检通过1e−7Ha门。小误差不能抹去预设失败；没有加层、重设初猜、优化active space或修改电荷追pass。

下表仅为此派生静态模型的E(原ESP)−E(真空)，单位kcal/mol；不作原论文DMET排序、ITC焓或自由能结论。

| 原配体 | QNP派生电子响应 | 同H FCI响应 | QNP−FCI响应(Ha) |
|---|---:|---:|---:|
| 2zfp | −70.384070 | −70.386173 | 3.3517e−6 |
| 2zgb | −86.076561 | −86.077769 | 1.9249e−6 |
| 2zc9 | −72.859549 | −72.859549 | −3.7926e−10 |
| 3dux | −81.366486 | −81.367393 | 1.4453e−6 |
| 3dhk | 缺原ESP终态 | 缺原ESP终态 | 不组装 |

2zfp从CAS2扩大到CAS4的FCI降低：真空0.01006368Ha，原ESP0.01194107Ha；其环境响应改变约−0.00187739Ha（−1.1781kcal/mol），远大于求解器微Hartree误差。这个原坐标派生空间敏感性说明缩小空间与原目标之间仍有物理模型误差；不能用高精度小H求解替代embedding完整性。

## 有限测量、成本与止损

按每个nonidentity Pauli项1024/4096/16384 shots×3重复，identity解析。8q每组件360项，4q26项；独立PCG64种子由固定component_prefix SHA256生成，无重用或事后选择。使用最终实际线路的精确Pauli概率作独立±1计数仿真，保存逐项plus_counts；不是QPU或逐shot门噪声仿真。独立复播全部99组counts与能量/标准误吻合。

9主+2预检共212,373,504逻辑测量shots；源态制备CX×shots的假设账本为39,617,851,392。它不代表本机实际执行了这些门；且不含额外测量基旋转/路由。均匀非分组分配不是最优测量方案。16384shots/项时四个配对的独立标准误分别为0.6267、0.6563、0.1354、0.6360kcal/mol，明显超过理想求解器误差。没有保证化学精度或设备可用性。

原job handle：20261003T233351Z-b15-five-original-coordinate-CAS4-QNP-547b6b38。registry/log/checkpoints保留。600CPU秒为冻结硬上限；末次完整组件checkpoint CPU570.572374，随后3dhk原ESP在RHF中SIGXCPU。9个主组件、两个预检与9套HF已持久化；未完成RHF仅有检查点，不误标converged。观察RSS快照1,959,168KiB（约1.87GiB），高于原1200MB PySCF工作区估计；该参数不是进程内存硬上限。3dhk真空RHF286.06CPU秒、积分/FCI阶段82.04秒，完整配体轨道生成占主要成本。没有经典/量子端到端速度收益证据。

## 交付与最小缺口

results.json具有统一id/status/target_status/experiment_kind/metrics/limitations，status为original_coordinate_derived_quantum_executed_budget_and_solver_gates_failed，target_status=incomplete。all_completed_same_H_source_and_native_checks_pass=true；all_original_driver_checks_pass=false、all_requested_components_complete=false、all_frozen_solver_accuracy_gates_pass=false并列，不混淆组件与原目标。

campaign：tasks/_execution/2026-10-04/bio/b05-b15-followup；原11组件的integrals.npz/dense-H.npy/native-state.npy/result.json可供外部独立审查。validation/delivery-independent-audit.json不导入执行driver，逐项标明独立方法、旧42文件hash和成本。初始预检失败、原协议历史、终态失败与原优化失败均保留。manifest封存campaign与本revision，LATEST/shared留给父级。

下一科学最小输入：作者原每环境、每片段数值h1/ERI/ecore及粒子数/spin/orbital ordering/三片段能量定义，或可完全复建的bath/投影器与收敛embedding参数。只补最后3dhk原ESP可完成派生五配对，但不关闭原DMET目标；本轮明确不续跑。
