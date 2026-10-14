<!-- 由 release/tools/build_problems.py 自 tasks/F15-skqd-impurity-greens-functions/execution/orbital-response-r47/RESEARCH.md 生成，勿手改 -->

> F15 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# R47 来源与适用边界

[固定原文v1](https://arxiv.org/html/2609.09147v1)；详细公式、Table1与引用绑定见 source protocol（本地证据，未随题库发布） 与 citations/schema（本地证据，未随题库发布）。


HF rotation可由公开Eq4–10重建；原缺作者旋转假设不再成立。HF传播保留物理counterterm htilde=diag(eHF)−2P，并加完整U Nup Ndown。Bare是非相互作用orbital basis，不是旧site-product。

本轮K36、dtπ/8、一阶Gaussian/impurity Trotter、eta.1，双方自身low4参考；旧K17/times0..8/eta.15/addition-only和旧失败完整保留。两流程同时改变basis与physicalreference，不作单因素归因。

各slice保留全部测中bitstrings与c0± mandatorychildren；SCI依据自身Hamiltonian残差，不读ED真值选择。同D容不下mandatorychildren即not_evaluable，未删slice或权重。3seed median/range不是置信区间。

完整addition/removal GF的原χnorm是1−n与n，总权重1；未反射/归一化谱代替removal。Ritz有限Lanczos poles不称完整3920 ED谱；独立只在6频点directsolve。单起点投影eigsh仅给返回Ritz对残差，不证明全对称sector最低根。

本轮是source-defined功能模拟，不是作者未舍入数据逐bit复现、native编译、噪声/QPU或DMFT自洽。保留所有技术/精度负门；没有量子优势结论。

结果（本地证据，未随题库发布） · 全部切片（本地证据，未随题库发布） · 统计（本地证据，未随题库发布） · 全部门（本地证据，未随题库发布） · 四阶段原JSON（本地证据，未随题库发布） · 成本（本地证据，未随题库发布） · 旧失败（本地证据，未随题库发布）
