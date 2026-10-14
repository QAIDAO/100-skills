<!-- 由 release/tools/build_problems.py 自 tasks/B10-peptide-conformation/execution/RESEARCH.md 生成，勿手改 -->

> B10 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B10 独立深入研究（2026-10-04）

本轮对已发表 APRLRFY 固定序列的 9 比特教程哈密顿量运行真实 QAOA 状态演化和强经典参照，冻结的命中门槛未通过。没有设计或修改序列。此新协议不是原文硬件复现，也不代表天然构象预测。

## 输入身份与量子原语

输入为 qiskit-community/quantum-protein-folding 提交 73fb4500d6f21e2be496025bafae7222474ff53d 的教程打印 Hamiltonian：无侧链、惩罚参数均为 10，共 77 项 I/Z Pauli。解析出的 JSON、教程、转向解码器与 Miyazawa–Jernigan 矩阵均有执行前哈希。原文 2021 的 CVaR/evolution 变分训练与这里的均值能量 QAOA 不同，不混用成功率。

初态为 9 个 |+>；成本 C=(H−minH)/(maxH−minH)，每层 exp(−iγC/2) 后接 9 个 exp(−iβX/2)。深度 1、2、4，各三个独立初值，种子 20261004–20261006，COBYLA 每次至多 250 个理想期望值调用。优化器均达到调用上限，success=false 已保留。训练后抽取 256/4096 shots；训练过程没有有限 shot 或噪声。

量子态没有使用 ED 基态初始化。独立全 Kronecker 哈密顿量及稠密 X 张量线路重建最大态误差 1.28e−16、归一化误差 1.78e−15。经典参照枚举全部 512 字符串，并依据原解码器重建自回避四面体转向；另外运行同抽象成本调用数的 bit-flip 模拟退火。

## 验收与失败

精确最低能为 −1.425 模型单位，两个基态 010100101、011000101 均自回避。均匀采样基态率 0.00390625，合法率 0.4140625。深度 4 的三个基态概率为 0.004633、0.007555、0.008880，中位数 0.007555 低于预冻结 ≥0.1，故状态 quantum_experiment_gate_failed。其余数值正确性门槛通过。所有深度、种子与 shots 均留在 raw.json。

相同 250 次单点能量调用的退火在 9 次中 7 次找到精确基态。QAOA 的每个期望值调用需要全状态信息，退火只查一个构象；这只是抽象 cost-call 对照，不是相同物理测量预算。教程展示的 most-likely 字符串 101100011 能量为 −1.396，较精确基态高 0.029。这只说明此教程输出的最可能态不是其打印 H 的全局最低态，不据此否定论文硬件数据。

逻辑成本层有 76 次非恒等 Pauli 旋转、未合并奇偶网络 260 个 CNOT、混合层 9 个 RX；深度 4 每次制备为 304 次 Pauli 旋转、36 个 RX、1040 个未合并 CNOT。总训练调用 2250，总成功读出 39168 shots。没有编译拓扑成本或训练 shots，不能宣称真机资源优势。

## 物理边界与下一步

四面体接触势最低能不能验证溶液天然构象、RMSD或动力学。2023 的 20 比特丙氨酸四肽更完整势能研究报告浅层收益弱，不能与本 9 比特格点结果当作同一 Hamiltonian。其作者 40.9 MB Zenodo 数据包公开但本轮未下载；不能写成原始势能不存在。

后续若扩展计算，应先冻结该数据包内势能、侧链最小化与构象映射，比较枚举/退火/强经典采样，再评估原文 CVaR 路线。重试本实验须新 revision，不改 ≥0.1 门槛。真实结构用途仍缺模型验证、实验构象与映射、同预算独立测试。

来源：[2021 正例](https://www.nature.com/articles/s41534-021-00368-4)、[固定教程代码](https://github.com/qiskit-community/quantum-protein-folding/tree/73fb4500d6f21e2be496025bafae7222474ff53d)、[2023 负例全文](https://www.nature.com/articles/s41534-023-00733-5)、[负例数据](https://doi.org/10.5281/zenodo.6563433)。

## 可复核产物

当前数值：revision-2/results.json（本地证据，未随题库发布），协议与输入哈希：manifest.json（本地证据，未随题库发布），全部数据：raw.json（本地证据，未随题库发布）。历史初稿保留在 initial-RESEARCH.md（本地证据，未随题库发布） 和 initial-GOAL.md（本地证据，未随题库发布）；原 execution 根目录 manifest/results 未覆盖。共享来源和独立驱动位于 `tasks/_execution/2026-10-04/bio/subset-B09-B13/`。所有来源读取失败日志亦保留。
