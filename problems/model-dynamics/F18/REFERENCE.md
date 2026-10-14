<!-- 由 release/tools/build_problems.py 自 tasks/F18-nonlinear-multidimensional-spectroscopy/execution/full-response-reference-v3/RESEARCH.md 生成，勿手改 -->

> F18 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# F18 v3 研究证据边界

目标是完整可审计强经典参考和物理bath cutoff评估。结果层次见 RESULTS（本地证据，未随题库发布）；numerical_qualification_complete与physical_cutoff_pass分别报告，不混为同一门。

采用锁定公开source二聚体、正文Γ/4 Markov与物理finite-memory bath，occupation/稀疏Lindblad及普通转置L.T线性读出，不对光学非Hermitian operator施加density正性/trace门。实际raw密度无repair。

源参数为ε1=1.55、ε2=1.46、J=−0.01、Γ=0.05908、Ω=0.1 eV，ω0=0，g=√(ΓΩ/2)。finite-memory jump为√(2Ω)a；Markov无mode，物理维4、Liouville维16，d2/4/8仅属于finite-memory。ħ取0.6582119569 eV·fs，与作者代码0.658212的舍入差异明示，不称逐点一致。旋转参考1.505 eV；二维变换t1用FFT、t3用IFFT，保留原36×36窗与1/144归一化。

public固定机器工作精度减少局部截断误差，旧strict对照和独立模型/actions/DFT/prefix/选定forwardpath终审仍可证伪；同Taylor族共用degree/scaling工具的限制保留，抽样forward审计不声称全部路径重新传播。

Markov/d2旧strict仅按独立证书复用，旧failed-density全run不被追认。新增量子0，原量子组件历史和本次经典资格分开；原应用仍incomplete。

数值问题已与物理截断问题分离：全部416solver行通过，而三对24cutoff联合门失败（24响应失败、16谱失败）。4→8的谱相对L2最大0.00351355838通过谱门，但全响应绝对误差最大0.00490240978失败；2→8最大响应0.373992112、最大谱相对L2 0.194921749说明d2在该完整窗下不足。不能因为图谱接近或solver高度一致而忽略响应门。

该完整二维非线性谱协议不等于原论文IV.1.2所用dynamics convergence逐点复现。当前负结果只拒绝本协议范围下的截断资格，不能反证论文；公开source方法匹配与作者原图/原数据复现仍需区分。

当前两二能级site与至多两个小模式的模型优先使用强经典occupation/稀疏Lindblad。量子collision+LCU只在物理cutoff先合格、量子门/采样/成本独立验收之后有比较意义；本轮既不证明量子优势，也不以经典数值恢复作为量子完成。本轮不提高cutoff或重试。

累计CPU/wall/RSS和实际文件字节以最终父级ledger为准；真实复制计字节，绝对只读引用保留既有字节一次。物理失败阻native，不缩窗、换主参考、改门或自动重启。
