<!-- 由 release/tools/build_problems.py 自 tasks/B01-femoco-nitrogenase/execution/revision-4-original-input/RESEARCH.md 生成，勿手改 -->

> B01 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B01 原完整Reiher输入与有界量子验证

本轮取得官方保存的完整54e54o哈密顿量，并执行同源派生CAS8e8o的真实量子门数值组件。**量子精度门和缩减模型门均失败；原FeMoco低能自旋与固氮机理目标未完成。** LATEST、共享表、旧冻结成果未修改。

## 原始输入闭包

[官方固定commit数据](https://github.com/quantumlib/OpenFermion/blob/60a6e1ab3362b6e580a3a96ebf24e42680c78799/src/openfermion/resource_estimates/integrals/eri_reiher.h5)共68,049,832字节，SHA256 `82406a5209a6915844f2bd63041377ac7466677e6c1260dfb448ae3ca8772a2f`，Git blob `1af236091aef3060084657e5948588e71b7e3c22`与官方树一致。安全HDF5只读包含h0(54,54)、chemist ERI(54,54,54,54)、ecore=-13212.970326Ha。官方loader及测试静态核验h0=h1eff、ecore=冻结芯电子能+核排斥能，Na=Nb=27；文件本身无电子数/自旋attrs。所有积分保留，没有化学阈值删项，也未使用SparsePauliOp.from_operator默认容差。作者代码未执行、未读取pickle。

[2017原研究](https://arxiv.org/abs/1605.03590)结构1为54e54o、S=0、charge+3；[2019原文](https://arxiv.org/abs/1809.10307)指出该空间缺少FeMoco代表性开壳层。不能与113e76o输入混用，更不能由该闭壳单结构推广真实氮化酶。2026原作者[公开仓库](https://github.com/hczhai/femoco-scripts-2026/tree/master/00-Integrals)的FEMOCO.FCIDUMP明确为113e76o，也不是本H的替代。原DMRG图缺同版本数据checksum/offset，未将图值或近似图读数用作验收。

## 冻结模型与科学判别

协议SHA256 `c91eed5dd64c2d302b33b1d8825e275657caed5b9443c76acc23ca802e55268f`。全54o/108自旋轨道Ms0空间维3.79057e30，complex128全态矢需约5.19e33字节，未尝试全态矢。按全H RHF-MP2未松弛1RDM，分别对占据/虚轨道块对角化，占据按占据数升序、虚轨道按降序取k/2+k/2，固定CAS6/8/10。MP2仅选轨道规则，不是强关联真值。对剩余轨道固定双占/空，构造准确PHP、冻结offset与全C变换，不更换分子/删ERI。CAS8排除MP2占据消耗0.301675、虚轨道占据0.266996电子，原始完整占据和被排除值见selection.json。

完整同H RHF=-13481.668509395327、MP2=-13482.045039290349、CCSD=-13482.154678533310、CCSD(T)=-13482.175402301702Ha。CCSD33步收敛，但T1=0.03890185；CCSD(T)仅近似诊断，不是严格本征能控制。

| 同H精确singlet控制 | 总电子能/Ha | 相对全RHF相关能/Ha | Ms0维数 |
|---|---:|---:|---:|
| CAS6e6o | -13481.879163667940 | -0.210654273 | 400 |
| CAS8e8o | -13481.977248631398 | -0.308739236 | 4900 |
| CAS10e10o | -13481.983731357099 | -0.315221962 | 63504 |

CAS8独立CSR H有1,768,900非零，三随机向量作用与PySCF最大误差1.11e-15Ha。精化singlet参考总能-13481.977248631407Ha，本征残差4.7657e-12Ha，旧CAS8原FCI输出完整保留，精化能量仅改变9.11e-12Ha。CAS8→CAS10变化**6.482726mHa>1mHa**。对保存的CAS10态作明确S0投影而不重求解，得到同全H的singlet试探态；由嵌套空间变分原理，CAS8相对完整54o S0基态模型损失至少6.482726mHa（限数值精度），已经排除1mHa收敛。CAS8对完整CCSD(T)差**198.153670mHa**是更大的近似诊断差，不能当精确损失界。

## 实际量子组件与失败

固定CAS8、HF初态、单层28个spin-free single与28个singlet pair-hop，56参数，精确费米二能级门与336个互相可交换组内JW Pauli旋转等价，保持N和总S。三个seed2026100101/02/03、角域[-π,π]、初角std=.03、L-BFGS-B解析反向梯度、每seed最多150iter/250eval。全局量子CPU限180秒，未按能量增加迭代或改门。每seed均达到150iter，调用157/154/155次，共466次实际门态传播。

最佳总能**-13481.904790086224Ha**，相对同CAS8精确singlet能误差**72.458545mHa**，远高于冻结1e-5Ha门；三个seed全部失败。最佳fidelity=0.898275125、variance=0.056432958Ha²；此高重叠不代表能量精度。S²、归一与固定N/Ms通过。保存所有seed原角/最优角/trace/态，不补跑、不挑不同模型包装成功。

独立Qiskit1.4.5的16q完整statevector与own sector门模拟逐幅相位对齐差1.56e-13，归一误差3.97e-13、sector leakage1.11e-16；归一后独立能量复算差2.66e-14Ha。16q线路7512指令、3808 CX、336 RZ、深度4356。原108q线路含全部旁观轨道JW字符串和1431个实Givens的原轨道反变换：272226指令、228408 CX、6060 RZ、深度123833。QPY逐门名称/wire/浮点角度精确读回；没有QASM舍入或小角删项。奇数占据旁观轨道独立CAR wedge与8q Qiskit算法测试差5.55e-16，说明不能只做naive wire组成。**108q仅验证形式嵌入/基旋转和线路资源，没有108q完整态传播**；此算法小测试不计FeMoco应用模型。

## 技术attempt、预算与边界

原协议/源码保留。attempt1为PySCF2.7与NumPy2.5 einsum路径tuple兼容失败；attempt2标准einsum默认未优化导致54⁸AO2MO，诊断后自有PID92643 SIGTERM并确认终止，70.44wall秒成本保留；attempt3恢复原optimize=True并只在进程中替换lib.einsum，原环境未修改。CAS控制首次preflight能量容差不等于本征态残差；attempt4过严PySCF精化未返回converged，未延长；attempt5独立eigsh默认LM选到高自旋、S²门失败；attempt6明确SA才完成目标singlet控制并首次开始量子训练。所有失败驱动、协议amendment和8个作业记录保留；不称与最初冻结源码完全一致。另原108wirecompose草案未执行，full JW修补有独立嵌入验证，未重跑量子优化。

科学作业均单线程，RLIMIT_CPU硬限，总预算600CPU秒。完整准备实测4.878982CPU、量子+参考4.583456CPU、Qiskit6.239039CPU；原CAS6/8/10控制0.302792CPU在先前preflight，已复用、未重复求解。原量子raw的baseline_CPU_seconds引用这笔历史控制成本，不能再加算一次。失败进程没有最终CPU计数，8个job单CPUwall合计94.642077秒，再保守计互动诊断和终审，**总数值CPU上界约100.445秒**，非声称精确失败CPU。最高RSS未实测，2GiB仅内存设计估计。466次forward模拟加解析梯度有完整经典处理成本，无加速比。finite shots=0，QPU调用=0，无硬件噪声/QPE/制备重叠成功率或容错全成本复现。

## 交接

本轮可计一个真实来源派生H量子数值组件，不能称54o原应用完成。下一步优先原54o H的高质量同S0多参考经典收敛及来源一致性，再评估直接原H稀疏/selected-support量子路线；CAS8扩迭代不会修复已证明的模型门失败。不要复用无cap声称或追加任意CAS2。

入口：本目录results.json/GOAL.md；证据目录 `tasks/_execution/2026-10-04/bio/b01-followup`；冻结manifest包含源、协议、全部attempt、原始数据、QPY与终审。旧17个受保护文件hash无变化，全部作业终态，无后台计算。LATEST由父级独立验收后决定。
