<!-- 由 release/tools/build_problems.py 自 tasks/M20-confined-cyclic-ozone/execution/public-cage-pair-v3/RESEARCH.md 生成，勿手改 -->

> M20 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M20 原公开 C60-O3 笼：18e12o 量子组件，冻结精度门失败

真实输入已闭合到原作者公开的单个 cyclic O3@C60 坐标，完成同 Hamiltonian 的 full singlet CASCI、paired-CI、24-qubit pair-UCC/VQE 及有限 shot 验证。原应用仍未完成：没有同笼内 bent/TS 配对驻点，也未计算相对稳定性、势垒或寿命。

## 原输入与新模型边界

来源是 [arXiv v2](https://arxiv.org/html/2408.13244v2)（2026-08-17）和官方 [pyLIQTR v1.1.1 固定 commit](https://github.com/isi-usc-edu/pyLIQTR/tree/fdf2a62ac11527bb19687aa2c20405277ec6ef42)。原 case 的 v1 已有后续版本。`data/geometries/c60-o3-opt.xyz` 是完整60C+3O原坐标；三个O与`o3-opt.xyz`逐数值相同，O-O距离1.30855–1.30903Å。本实验未替换分子、未优化几何、未裁掉笼，未推断坐标的原优化方法。

采用论文混合基组 C/STO-3G、O/cc-pVDZ，342AO、384电子，登记中性 singlet。新模型使用 weigend 辅助基组 density fitting 的 RHF及全部CAS积分。这里的 **density fitting** 与原资源论文 **double factorization** 缩写DF不同；未重现原 qubitized-QPE 或容错资源估计。作者 Gaussian积分/AVAS数值阈值没有公开闭合。

固定规则：MINAO O2s/2p投影取最大9个occupied和3个virtual特征向量，分别在选定occupied/virtual块准正则化；剩余183occupied冻结、147virtual排除。保留所有12个选定活性轨道和18个电子，未依据FCI/VQE能量挑选轨道。选中occupied权重.97819–.99960、virtual .98165–.99298；下一未选权重.01776/.02152，投影选择有明显间隔。此规则是可复现派生AVAS，不能宣称已恢复作者未知阈值/轨道。

## 同模型强经典对照和负结果

| 项目 | 总电子能量 / Ha | 相对 full singlet CASCI / Ha |
|---|---:|---:|
| DF-RHF | -2468.159730298572 | 0.145305904 |
| full singlet CASCI (18e12o, Ms0维48400) | -2468.305036202208 | 0 |
| paired-CI (同18e12o, seniority-zero维220) | -2468.209924097428 | 0.095112105 |
| pair-UCC/VQE 最佳seed41 | -2468.209919217451 | 0.095116985 |

3个固定seed41/42/43均比paired-CI高约4.880×10⁻⁶Ha，通过预冻结 paired-optimization 1mHa门；均比full CASCI高约.095117Ha，**full-model 1mHa门失败**。最优paired-CI本身遗漏.0951121Ha（59.684kcal/mol），即使当前优化器达到paired全局最优，也不能消除此误差。不能将失败一概归给优化器，也不能据此泛化到其他轨道/ansatz。

BFGS三个seed都返回precision-loss状态而非success；分别27/26/31次迭代、1260/1148/1568次能量调用。接受的是观察到的对paired精确参考能量误差，不是optimizer success标记。优化期间使用无shot的精确状态传播，未执行硬件优化。

full CASCI能量收敛1e-10，S²约8.08e-12，独立H作用残差9.38e-6Ha。原DF-RHF收敛46.19s、gradient6.40e-7、overlap condition200.34。独立冻结Hamiltonian的HF行恢复全DF-RHF至2.32e-11Ha；paired闭壳层矩阵与fullFCI contraction一致至7.11e-14Ha。RHF内部稳定性/其他spin分支未测试，不能主张整个原体系的物理全局基态。

固定密度非DF诊断给出 −2468.164391597327Ha；DF高+.004661298755Ha（2.925kcal/mol），该密度在exact Fock下gradient.00335360。因此DF模型差异本身不能忽略；此项不是单独收敛的非DFHF，也没有将DF结果包装为原非DFHamiltonian。事后完整FCI在paired子空间投影权重.950179，仅诊断表示限制，不用于更新候选。

## 实际线路、shot与验收

初态为9个alpha/beta电子对。一个固定顺序layer含9occupied×3virtual=27个电子对双激发 `exp(theta(A-A†))`。原24qubit Jordan–Wigner double-excitation generator的8个Pauli项两两对易，按精确Pauli旋转实现。量子优化通过220个seniority-zero态严格传播；原线路与压缩表示的等价性独立核验。

完整native QASM包含5616CX、1728H、432S、432Sdg、216Rz、18X，all-to-all depth6538。24是算法数据qubit数，不是容错physical-qubit估计；未映射连接拓扑、噪声或误差校正。driver核验所有27生成器在全部220个paired ket的作用，并对3种native门核验12个basis输入。独立审查另对**整条实际24qubit native线路**逐门计算基稀疏模拟，不在门后投影，最大2800个非零振幅、最后220个态；对压缩ansatz振幅残差1.28e-13、N18/seniority leakage0。未运行dense2²⁴态矢；稀疏阈值1e-14明确记录。

测量使用211个Pauli项的paired-observable lift；在登记ansatz上的期望与完整H完全一致。该observable的单个XX/YY项可离开N18，期望按扇区外0处理，其±1方差仍保留。此预算是该lift的逐项独立测量，**不是完整原H所有Pauli项的shot成本**，也未实施对易项分组。所有系数显式构造/1e-12截断，未使用`from_operator`默认rtol；lift与原paired矩阵逐元素核验。

| shots/term | 每个能量估计shots | 解析单能量SE / Ha | 9批样本相对状态能量误差范围 / Ha |
|---|---:|---:|---:|
|8192|1,728,512|约.019843|−.044377至+.008397|
|32768|6,914,048|约.009922|−.011220至+.022644|

3optimizer seeds×2shot levels×3replicates=18条独立随机流；精确保存`plus1_counts`（+1本征值计数，不是计算基bit1），总 **77,783,040** simulated term shots。32768shots/term的预冻结解析SE≤1mHa门失败。样本误差与解析SE分别保留，不以偶然样本命中替代精度门。测量流由四元SeedSequence生成，独立审查逐count重放。QPU调用0；不主张quantum advantage。

## 协议失败保留与可复现性

v2于23:30:40Z冻结，作业总298.305s、未超过300s硬预算；原H/FCI已经完成，但错误地要求每个Pauli项保持N18，assert导致exit1，尚无VQE。原driver/manifest/失败门完整保留。v3于23:38:16Z另冻，仅修复此实现假设，复用完成的相同H/FCI，无SCF重跑/空间或参数追调。v3作业2.076s（科学driver1.152s）；独立核验3.676s。两个budget分别登记，不合并宣称一次从头完整运行。未记录实测peak RSS；PySCF配置上限2200MB，线程变量均1，OpenMP不可用。

来源静态审查22checks、独立数值/线路/shot审查138checks全pass。arXiv源码端点HTTP406已记录并停止，官方HTML/GitHub API/raw成功下载；没有绕过访问限制，没有执行作者下载代码。源码DPW最低0.5Ry文件是64个spinless modes，不能容纳中性384e；其他原文件1–20Ry与论文40Ry/10Å假设不同。PEST单位常数Julia .529117 vs Python .529177、padding文档与代码加单次7.5Å等差异原样归档，不据此作原DPW物理求解。M30备用分支因M20真输入闭合而未新增运行。

最小后续输入是同笼内bent/TS驻点坐标、共同电子态与原AVAS/积分定义，才可形成任务所需相对能量。当前停止：有限shots门和paired-full模型门均失败，进一步优化当前paired参数不能修复后者。旧LATEST/shared/旧冻结文件未修改。
