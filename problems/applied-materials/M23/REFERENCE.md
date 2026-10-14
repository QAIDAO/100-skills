<!-- 由 release/tools/build_problems.py 自 tasks/M23-lithium-sulfur-dissociation/execution/delivery-clarification-r52/RESEARCH.md 生成，勿手改 -->

> M23 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M23：三点LiH证据清单澄清

本案已有LiH/STO-3G CAS(2e,3o)激发酉VQE及同模型CASCI/FCI、1RDM偶极比较。冻结键长只有1.45、2、3 Å三点；最大能量误差2.664535e-15 Ha，偶极误差1.660149e-6 D。它是方法接口验证，不能代替原LiSH/Li₂S或真实锂硫电化学应用。

历史raw_evidence多列了point-1.npz。实际读取其xyz为1.45 Å；h1、eri、H、vqe、reference、mo_coeff、xyz七个数组与point-1.45.npz逐元素完全相同。它是保留的旧命名文件，不是第四个1 Å样本；没有据此声称数据污染。

当前摘要（本地证据，未随题库发布）仅列三个正式坐标文件，旧文件在legacy_files中以SHA保留。别名检查（本地证据，未随题库发布）记录逐字段证据。原数值、门、源码与文件不改；本次不新增量子模拟。完整方案/来源/限制见原研究（本地证据，未随题库发布），原实验Goal见原Goal（本地证据，未随题库发布）。

下一步应取得原含硫分子的几何/活性空间/积分及物种身份后再做相应模型；不得把LiH数值通过当作含硫应用通过。
