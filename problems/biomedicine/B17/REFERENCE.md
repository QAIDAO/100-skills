<!-- 由 release/tools/build_problems.py 自 tasks/B17-sulfonyl-fluoride-dynamics/execution/cas8-sensitivity-r42/RESEARCH.md 生成，勿手改 -->

> B17 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# R42 B17 方法与来源

完整公开几何、参考HF与exact A2框架沿用R40/R41；本轮direct inactive-core JK与64×64 plain ERI变换，无SCF重启、DF或完整AO四指标缓存。CAS8与CAS6冻结核心还原比较保留常数和观测量。H arithmetic audit认证保存算术与输入，CAS8 fermion/operator action必须另验，不能由CAS6 pilot替代。

若执行动力学，参考为expm_multiply的经典指数作用数值方法，对照block Strang产品公式；不能称ED、量子优势或浮点全局严格证书。原文可核来源、冻结版本及实际输入见upstream-bindings.json（本地证据，未随题库发布）和results.json（本地证据，未随题库发布）；原作者labels/split缺失，原应用仍0完成。

历史量子组件证据指向R41真实细步长轨迹；独立端点只核实际端点，不冒称29点独立复现。原R40三项失败单列保留，不因新定义或大CAS追认。


## 条件性路线选择

本轮对当前可计算模型的推荐来自实际精度和成本。保留Strang作为量子动力学协议的受控数值基线；将它落到门级硬件还需要分解、编译、采样与读出成本，当前没有测量这些费用。不能把经典仿真中PF较慢直接推广为所有量子硬件都无优势，也不能从状态维数推断量子加速。

作者的[v4论文](https://arxiv.org/abs/2412.15804v4)研究以可观测量误差约束的哈密顿量项截断、Clifford分解/变换与硬件转译，并报告8比特实例的硬件子线路；它是门级后续方案的来源，不是本轮派生16自旋轨道模型已完成编译的证据。该论文的线路深度压缩与下游预测收益须分别验证。本轮未补入原标签或数据划分，不重现其机器学习结果。

[PySCF direct_spin1源码](https://pyscf.org/_modules/pyscf/fci/direct_spin1.html)与[SciPy expm_multiply文档](https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.sparse.linalg.expm_multiply.html)是API核对来源；实际运行绑定本地PySCF2.12.1、SciPy1.17.1和NumPy1.26.4。DOP853仅给独立数值交叉检查，不是严格区间误差证书。所有原始输入、源码与生产合同见当前包的upstream-bindings与各stage manifest。
