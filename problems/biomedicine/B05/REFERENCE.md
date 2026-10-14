<!-- 由 release/tools/build_problems.py 自 tasks/B05-carbonic-anhydrase/execution/jk-pilot-cost-screen-r44/RESEARCH.md 生成，勿手改 -->

> B05 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B05：局部收缩正确，但当前完整 R 成本路线未准入

原公开frame05的178原子、1627 AO、648电子、8013辅助行保持；原3021 MINAO因子中保留全部508严格正占据，未截断小值。依据原研究来源及量子路线（本地证据，未随题库发布）、[PySCF官方DF JK实现](https://pyscf.org/_modules/pyscf/df/df_jk.html)和冻结的本机outcore源码，按数字数据集拼接下三角列，自写NumPy收缩，不调用旧producer/get_jk。

对L_P，rho=Tr(L_P D0)，J=Σrho L_P，X=C_positive sqrt(occ)，K=Σ(L_P X)(L_P X)^T。局部独立读回改用右乘密度 D0 L_j 与math.fsum二次型。它共享原D0和producer提取的选定L行，只验证指定算术；不独立认证缓存packing、积分或全部J/K。

三个固定8行区间只覆盖24/8013≈0.2995%的辅助行。实际读取254280576缓存逻辑字节，两NPZ前后hash累计205805072字节。所请求的BLAS线程环境设为1，保存build配置；没有独立观测BLAS运行线程数。预冻结3AO夹具只验证实现，未计为B05科学结果。

当前推荐保留合格缓存和局部正确性证据，关闭当前batch8/1200CPU-1800wall完整R路线。不得把成本预测超额外推到所有收缩实现。B05的量子方案仍有条件：取得收敛参考及IBO/投影/FNO、同轨道顺序h1/ERI/offset后，以CAS(6e,6o)同H经典CASCI作基线，再比较12自旋轨道FAST-VQE；现阶段缺H，不能启动假设H上的通用水链或小酶proxy。QPE属于资源更远的替代路线，不因本pilot通过而获得可行性证明。

本轮完整R、XC、SCF、VQE/QPE均未运行；原PES未复现。下一公开输入工作转向M09官方数据传输闭包（本地证据，未随题库发布），只允许可信CA官方链修复后正常证书/hostname验证；缺数据时保持未闭合，不降级验证。
