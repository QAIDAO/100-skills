<!-- 由 release/tools/build_problems.py 自 tasks/M17-mof-carbon-capture/execution/public-input-quantum-v2/RESEARCH.md 生成，勿手改 -->

> M17 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M17 原完整缩小模型：输入已闭合、线路已执行、物理目标仍有限

本轮取得了作者公开的三套原 reduced Hamiltonian、周期配对结构及原固定 QNP 参数，实际执行8/20/28q完整缩小模型。没有投影4q子问题，没有替换MOF、猜几何或重优化源参数。28q使用完整 (N_\alpha=N_\beta=7\) 扇区，包含11,778,624个振幅；原QNP线路和同H FCI都已计算完毕。

原阶段2 job 仍是 **failed / exit1**：同H FCI比源存储参考低3.87338872e−8 Ha，未通过driver的1e−8源参考一致性门。它自身converged=true、残差7.858786e−6、S²≈0，均通过冻结的强经典检查。我们保留失败job、原driver、post-FCI检查点与初始采样非收敛行；后处理没有重跑QNP/FCI，也没有退回较差的参考以取得PASS。最终结果明确 `all_original_driver_checks_pass=false`。

| 原体系 | 原CAS / qubits | Ms0维数 | layers / params | CX / depth | QNP energy (Ha) | 同H独立FCI (Ha) | QNP−FCI (kJ/mol) |
|---|---:|---:|---:|---:|---:|---:|---:|
| CO2 | 4e4o / 8 | 36 | 4 / 24 | 204 / 319 | −25.7620386729331 | −25.7620386729406 | ≈0 |
| Fe-MOF-74 | 10e10o / 20 | 63,504 | 10 / 180 | 1530 / 798 | −55.2732781635470 | −55.2745218646023 | 3.26534 |
| Fe-MOF-74+CO2 | 14e14o / 28 | 11,778,624 | 18 / 468 | 3978 / 1436 | −74.7046917248712 | −74.7059865649926 | 3.39960 |

门数来自原完整线路在rz/sx/cx、all-to-all逻辑连接、optimization3、seed1704上的实际编译，不能当作有真实硬件路由/噪声的成本。8/20q native statevector与完整守扇区结果fidelity分别0.9999999999999978和0.9999999999998894。28q没有构造全Fock native statevector；逐局部原PX/OR的量子门序与独立16×16作用定义已在冻结角度0、0.37、−1.2核验，最大误差<7e−16，再在完整扇区执行其全部468参数。原态、编译门数和完整扇区能量均已持久化。父级从保存态直接检查QNP对新FCI的overlap²：CO2 0.9999999999888669、MOF0.9987522298476035、ads0.9987317364998035，无拟合。

Ordering是源blocked-JW的量子wire重标号到每轨道alpha/beta交错，而不是随意进行费米模式重新排序。CO2另有从原FCIDUMP独立构造完整256×256二次量子化Hamiltonian的审计：反对易关系、Hermiticity、Ms0无泄漏、native态能量及基态均一致，producer能量差6.75e−14 Ha。独立验证只在建H后才读取producer结果比较。20/28q源Qiskit打印能量也吻合；ads差2.53e−11 Ha。原QNP三个S²数值均在1.1e−11以内，不把Ms0自动叫作singlet。

原paired周期HF正值结合基线是17.9899246337 kJ/mol。每个相关能必须用同一reduced H的原固定占据HF相减，再组装

\[
D = D_{\rm HF,periodic}+[E_{\rm corr,MOF}+E_{\rm corr,CO2}-E_{\rm corr,ads}].
\]

新独立FCI给相关结合项25.4443436387 kJ/mol，HF嵌入的原缩小singlet模型电子结合能43.4342682724 kJ/mol。原QNP给43.3000026926 kJ/mol，相差−0.1342655798 kJ/mol。这个小差主要来自MOF与ads各约3.3 kJ/mol误差的抵消，不是三者绝对能量均精确到0.1343 kJ/mol。不能直接相减三个Ecore0的电子总能，也不能加上不同原NO空间的MP2修正。

有限采样冻结为每体系1024/4096/16384 shots、每项3次，共27行、193536 distinct logical samples。如果在硬件每shot重备原native线路，需要368492544 CX×shots；本轮没有实际重放这么多门，而是从三个已模拟的原理想态概率分布抽数值样本，QPU调用0。重构相同原样本与SCI修复不增加distinct shots，但额外经典CPU均计入。采样后取alpha/beta string union的笛卡尔积做经典SCI，此步骤会加入并未直接抽到的determinants；它不是原论文的完整SQD流程复现，也不是单纯Pauli能量测量。CO2的子空间立即覆盖全部36态，因此其接近零误差是完整经典对角化的结果。

初始MOF9行SCI80cycle全部未收敛，已保留；同初始RNG/源态恢复整数draws，验证determinant和union数量后只提高max_cycle到500、同样默认初猜重新求解SCI（没有80cycleCI检查点续接），9行converged=true。其1024/4096/16384 shots平均误差为0.0419142/0.0121513/0.00366476 Ha；16384的S²仍0.00418–0.03666。对ads也保存原80cycle全部未收敛的9行和原始整数draws，另做同样固定draws的500cycle诊断，4/9收敛、5/9仍未收敛；16384的S²为0.04398–0.06242。16384shots/system的三个结合能诊断比FCI低22.26–23.06 kJ/mol，其中一行仍未收敛，均未通过纯spin/准确结合能门。未收敛数值只作失败诊断，不能称已量化的测量误差。父级独立重播27组RNG，与保存整数draws逐元素、hash、unique及union维数全部相同。完整终态与每行残差、S²、CPU时间见results.json；不能因SCI solver旗标收敛而声称纯singlet。子空间不对S²封闭，有限shots结合能只能作为诊断，不能通过准确吸附能的门槛。

同H强经典FCI CPU：CO2约0.00145 s、MOF0.5423 s、ads217.8113 s；单root Davidson由原QNP态作初猜，不能当作独立从头、最优经典性能比赛。原adsQNP扇区传播22.8591 s，H期望4.0487 s；这不包括完整源VQE优化或上游VASP。阶段1总9.676 CPU秒、MOF采样修复16.191秒、ads初始采样后处理77.219秒、ads500cycle修复431.697秒（全部有终态job，未超600秒止损）。原阶段2已记录到FCI结束的CPU至少270.397秒；包括它的可核对分段CPU合计至少805.180秒，额外保存/最终检查开销不冒充已测总数。CO2/MOF全Fock native态分别4096 B/16.78 MB；ads扇区94.23 MB而全Fock complex128态4.30 GB，FCI max_space12资源估算约1.8 GB。精确扇区模拟、编译和SCI都依赖经典计算；结果不支持量子速度优势。后续应优先同H Krylov/FCI、spin-adapted方法与源物理模型收敛。

公开输入版本固定在作者repo commit `ad3c6658f3d32167b6c0462af2451e5b0e062c2a`。49源文件均与Git blob或API元数据匹配并SHA256封存，旧case15文件哈希保持。原完整NO parent空间远大于当前reduced CAS；真实Fe高自旋与全晶格磁序、扩大空间/基底、实验热效应和等温线仍未闭合。SI S2公开triplet相对S0的MOF/ads偏移5.53/2.81 kJ/mol，quintet26.8/124 kJ/mol，不能把这些spin模型混进singlet结果。ads(9,5)quintet扇区4,008,004维不能为节省内存替换原QNP模型；若未来用真正S0-adapted表示，代数维数2,760,615，不等同本轮实际Ms0实现。本轮证明的是原缩小模型的完整三体系组件及有证据的负面采样诊断，原碳捕获业务目标未完成。

campaign：`tasks/_execution/2026-10-04/materials/m17-followup/`；入口 `NEXT.md`、`SOURCES.md`、`source-ledger.json`、`quantum-protocol.json`、`results/final-results.json`。所有协议/原失败job/后处理job和检查点保留。LATEST/shared没有由本单元修改。
