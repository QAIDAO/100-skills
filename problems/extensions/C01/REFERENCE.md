<!-- 由 release/tools/build_problems.py 自 tasks/C01-lithium-superoxide/execution/public-geometry-v2/RESEARCH.md 生成，勿手改 -->

> C01 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# C01 public-geometry-v2 — 原几何端点电子子问题

R/P 端点电子子实验已完成。使用官方 SI 原坐标、6-311++G(d,p) 基组、作者指定的两个活性空间；CASCI 能量与 SI 表格相差小于1 microHa，实际 UCC-VQE 与各自 CASCI 一致。原重排应用仍未完成：TS 的 O2/O3 原坐标完全重合，未修正、未计算势垒。

## 输入与边界

[出版论文](https://doi.org/10.1021/acs.jpca.0c09530)与[官方 SI 元数据](https://api.figshare.com/v2/articles/14128697)已取得；原 PDF、提取文本及下载hash在 `tasks/_execution/2026-10-04/cross/c01-followup/`。SI PDF SHA-256为 `6932e45a1f9eea8ed0cf43129da3d3b3c4cedff6b5f0525f7dfdeb23b597b6d4`。坐标由 SI “Cartesian coordinates of the stationary points”逐行提取至 `geometries.json`，没有重新优化几何。TS重复的两个氧核在原PDF已视觉核对；原样保留为invalid source。

模型为气相中性 Li₂O₄，38电子，单重态canonical RHF，132 AO。R/P RHF分别约5.3/4.6秒收敛，日志、checkpoint和MO文件保留。没有几何优化、溶剂、热自由能、振动或速率计算。

CAS(2,2)用HOMO/LUMO，CAS(4,3)用HOMO−6/HOMO/LUMO。38电子的HOMO zero-based index为18，选取[18,19]及[12,18,19]，其余已占据轨道进入冻结core。两个端点分别按canonical MO能量排序；没有maximum-overlap跨几何轨道跟踪，不能将轨道标签的一致性当作轨道态连续性的验证。

## 量子与强经典验收

同模型CASCI作为精确基线。独立从h1、二电子积分构建完整Jordan-Wigner Hamiltonian，并与PySCF逐列生成的FCI矩阵比对，最大元素差≤4.00×10⁻¹⁵ Ha。CASCI与显式矩阵最低本征值相差在浮点误差内。

VQE采用实际spin-adapted UCCSD：同自旋成对求和的singles，以及α/β交换对称的doubles；一个pool指数 U(θ)=exp[Σθ(A−A†)]。CAS(2,2)/CAS(4,3)分别2/5个参数、4/6个spin-orbital比特，固定Nα=Nβ。初态为对应HF determinant，没有从精确解制备初态。生成元与S²的commutator数值为零。3个固定随机种子41/42/43，每点以精确statevector期望值BFGS优化。

| 几何 | 活性空间 | CASCI / Ha | 最佳VQE / Ha |
|---|---|---:|---:|
|R|CAS(2,2)|−314.270196930109|−314.270196930109|
|P|CAS(2,2)|−314.212670270186|−314.212670270186|
|R|CAS(4,3)|−314.270892994462|−314.270892994462|
|P|CAS(4,3)|−314.271925099590|−314.271925099590|

全部12个优化种子通过预设≤10⁻⁶ Ha同空间能量误差、粒子数及单重态S²门槛。BFGS有10/12次返回precision-loss的`success=false`，原消息完整保留；独立能量与态身份验收通过不代表optimizer成功标志改变为true。

把最佳UCC参数构建为完整Fock-space Qiskit unitary电路，再独立验证完整statevector能量、N均值/方差、Sz和S²，均通过。generic cx/u全连接分解需CAS(2,2)100 CX、CAS(4,3)1868 CX，深度约213–216/4257–4258。此数目是显式pool unitary的generic分解；不是旧Aqua中的短qUCCSD线路，没有物理拓扑路由、噪声、误差缓解或容错资源，QPU调用为0。

## 活性空间影响及有限shots失败

相同端点几何的P−R电子反应能：

| 活性空间 | P−R / Ha | P−R / kcal mol⁻¹ | 假设独立物理测量的解析反应能1σ / kcal mol⁻¹ |
|---|---:|---:|---:|
|CAS(2,2)|+0.057526659923|+36.098526|1.727081|
|CAS(4,3)|−0.001032105127|−0.647656|4.496556|

加入HOMO−6使反应能变号。VQE与同空间经典参考一致证明这个小空间求解器成功，不能证明HOMO/LUMO足以保留反应化学；两个空间均不足以作为完整电子结构的收敛证据。

对每个优化末态的每个Pauli项取8192 shots，3个固定测量种子，记录所有项计数、能量估计与解析统计标准差。原driver在不同几何及优化种子间复用了shotseed 41/42/43，因此保存的R/P Monte Carlo计数使用共同随机流；它们不是独立端点采样。`ones_per_term`实际保存Pauli +1结果的binomial计数，不是计算基bit1计数。表中的反应能σ来自假设独立物理测量的解析sqrt(varR+varP)预算，并非已执行独立R/P采样的经验标准差。优化阶段使用精确期望值，未声称finite-shot VQE训练。展开项数R/P分别为CAS(2,2)27/27项，CAS(4,3)114/62项；每次能量估计模拟了221,184/221,184/933,888/507,904个项shots，含无需实际硬件测量的identity项，其贡献零方差。实际非identity测量预算可各减8192；尚未测量分组压缩。

当前8192 shots/项没有达到原应用1 kcal/mol的反应能精度；CAS(4,3)约−0.65 kcal/mol信号远小于假设独立物理测量时约4.50 kcal/mol的解析反应能σ，不能在此预算下可靠确定该微小反应能符号。该精度检查为运行后对原应用目标的审计，未伪称为冻结manifest中的事前shot门槛。

## 交付与下一步

`manifest.json` 在SCF前冻结sourcehash、原basis/坐标/轨道规则、种子和验收门槛；`results.json`/`results-points.json`保留所有点、所有优化和finite-shot结果；Hamiltonian/MO/checkpoint为复算输入。`validation.json`保存独立full-circuit身份、SI能量对照和失败。环境及交付hash见 `post-run-provenance.json`。

从仓库根目录复算（会更新此revision输出，审计时先保留原文件）：

```sh
<本机路径> tasks/_execution/2026-10-04/cross/c01-followup/freeze_inputs.py
OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 <本机路径> tasks/_execution/2026-10-04/cross/c01-followup/run_endpoints.py
<本机路径> tasks/_execution/2026-10-04/cross/c01-followup/verify_delivery.py
```

下一步的最小缺口是作者更正或可靠补充的TS坐标，并核验它确为连接R/P的驻点；取得后才可做同空间势垒与跨几何轨道跟踪。未经授权发送作者消息，本轮没有对外联系。全部旧执行和原SI文件保留，没有修改共享汇总。
