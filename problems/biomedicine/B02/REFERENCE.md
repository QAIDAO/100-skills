<!-- 由 release/tools/build_problems.py 自 tasks/B02-p450-spin-metabolism/execution/highest-spin-completion-r46/RESEARCH.md 生成，勿手改 -->

> B02 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B02：补齐原模型自旋范围后的方案判断

[原作者公开积分](https://zenodo.org/records/5941130)提供spin-free共同ROHF轨道模型。原A/B参考研究（本地证据，未随题库发布）已解S=1/2、3/2、5/2；本轮解剩余原B最高S，保留原h1/chemistERI/ecore与轨道，不从结构重建替代模型。

对于N电子M空间轨道，Smax=min(N,2M−N)/2。本轮9e8o和11e9o的Smax=7/2，固定最高Ms的维数C(M,Nα)C(M,Nβ)为8、8、36。先用PySCF完整矩阵作用构造H与S²；独立程序从原积分的 c†iσ c†kτ c_lτ c_jσ、1/2系数与带符号bitstring、两条S±路径重建矩阵。两实现均校验原Hermiticity后求全谱；保留原H残差，未平均对称化。共享NumPy eigensolver，不夸大为所有软件层独立。

结果支持已解低能排序，在相同原模型内无需担心遗漏S7/2翻转最低自旋。它不解决共同ROHF轨道之外的状态弛豫、动态相关、更大C–X、SOC或蛋白环境，也不预测代谢速率。当前最佳有证据路线仍为同S经典FCI；完整B的量子自旋保持VQE或QPE只能作为另有资源与精度门的候选，当前没有量子优势证据。旧oxoA VQE未能解析微哈特里尺度自旋隙，不能增加seed/迭代来追认旧协议。

本批B02有限自旋覆盖问题收束。下一全局工作按F15候选（本地证据，未随题库发布）先冻结原L8模型的同H基底变换与双响应资格，再决定量子采样协议；该候选未执行，不能计为新增量子结果。
