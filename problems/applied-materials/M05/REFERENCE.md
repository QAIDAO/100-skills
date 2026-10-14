<!-- 由 release/tools/build_problems.py 自 tasks/M05-battery-eels/execution/public-input-audit-v2/RESEARCH.md 生成，勿手改 -->

> M05 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M05 原公开输入闭包复查

审计完成，原 EELS 数值实验仍缺输入，未运行量子线路、SCF、谱计算或 shots。本次把候选缩小到原文真实 CAS(8e,7o)，而非从泛两能级谱或别的分子补实验数量。

## 已闭合的定义与可行规模

原晶体是 Materials Project mp-18988、C2/m。作者实际提取并封端的模型是 Li4Mn2O19H26（51 原子），不是 XAS 的裸 Li4Mn2O。轨道来自 unrestricted PBE0/ANO-RCC-VDZP，broken-symmetry 初猜 Sz=0，AVAS 选中心 O 1s/2p，阈值 0.09。Sz=0 不等于已验证总自旋 S=0。[原文 IV](https://arxiv.org/html/2508.15935v1)

原 Fig.4 小模型为 CAS(8e,7o)，CDF L=7，q=(1,1,1)，按全篇原子单位约定 q 单位为 Bohr^-1，eta=0.06 Ha，Delta 谱窗口=3.28 Ha，nmax=87。固定 Nalpha=Nbeta=4 的精确经典空间只有 C(7,4)^2=1225 个行列式，量子映射为 14 系统比特+1 Hadamard 辅助比特。这是有根据的下一候选规模，未据此声称原输入已闭合或本机实验已通过。作者 Fig.4 的灰色谱才是该同 CAS 精确对照；CAS(14,14) DMRG 制备及 18+ 轨道容错估算不能混作该小实例结果。

原协议采用 dipole approximation，用三个 Cartesian 偶极矩阵组合六个对称相关函数。完整有限 q 的密度算符 exp(i q·r) 是更广理论对象，但不是执行这份原小实例的必需输入。电子入射能和收集角对实验绝对截面有意义，不能把它们误列为原固定 q DSF 算法组件的缺口。

## 源参数冲突与真正缺口

预印本 Fig.4 明写 tau=0.096；相邻主文定义 tau=pi/Delta，代入 Delta=3.28 得 0.957802638 Ha^-1。用正文 nmax≈5/(eta*tau) 得 87.005，而用图注 tau 得 868.056。约十倍冲突已保存成输入一致性诊断，未静默改成 0.96。正式 JCP 163,244110(2025), DOI 10.1063/5.0300557 已核实，但官方正文 GET 403，无法判断正式版本是否修正。[正式 DOI](https://doi.org/10.1063/5.0300557)

还缺 51 原子实际坐标（尤其 26 H 封端位置）、总电荷/晶体快照/截取定义、broken-symmetry 初猜与 ANO/AVAS 详细设置；或者直接提供原 CAS h1/eri/ecore、三个 mu 矩阵、轨道/core 索引和准确 CVS mask，即可绕过重新猜簇的路线。基态可在同一 H 的 1225 维扇区精确求得，作者态矢不是独立强制缺口；匹配原 CDF 算法还需 numeric U/Z 或可复现分解实现参数。

有原张量后，最小下一实验是冻结该原 CAS(8,7)/q 实例，对 15 比特真实 Hadamard 时间演化与同 H 全谱比较，分别报告 CVS/CDF/Trotter/有限 shot 误差、粒子数/自旋、资源及 q 投影强度。应先解决 tau 原文冲突或另冻明确的新时间网格，且在真实系数上测量成本后才承诺 ≤300 秒。此为条件建议，本轮未冻结或执行量子协议，不能计入量子模拟数量。

## 共享来源审计

两案共享 Li2MnO3 氧 K 边的物理主题，但不能假定共用同一个电子哈密顿量。2024/2025 XAS 是裸 Li4Mn2O/cc-pVDZ；2025 EELS 是 H 封端 Li4Mn2O19H26/PBE0/ANO-RCC-VDZP。图形示意与晶体编号不足以恢复这两种簇的原数值输入。

本轮取得 arXiv:2506.15784v2 官方完整源包，13 项为 README、TeX、参考文献、图形及目录，没有 XYZ、FCIDUMP、数组文件或运行代码。另取得官方 PennyLane XAS demo 并只做静态检查：它是 N2/STO-3G、1.0 Å、CAS(4e,5o)，不能代替材料任务。精确题名/论文编号/正式 DOI 的已记录 GitHub、Figshare、Zenodo 查询未找到输入；这是查询范围内的结果，不证明作者数据在全网不存在。宽泛 eels/DOI 片段查询确实有大量无关记录，不能记成零结果。

材料数据库两个公开页均返回 403，2024/EELS PDF 和部分 arXiv 源请求返回 406，AIP 正式 EELS 文本返回 403，均记录后停止，不绕过。EELS 正式发表为 JCP 163, 244110 (2025)，DOI 10.1063/5.0300557；Crossref 元数据可得，但正式正文、数据可用性声明和 SI 未核实。可读预印本文本未给可直接执行的原积分/偶极矩阵下载入口。

完整请求见 source-index.json（本地证据，未随题库发布），哈希见 post-run-provenance.json（本地证据，未随题库发布），参数复算见 m05-time-step-consistency.json（本地证据，未随题库发布）。静态源内容和逐项检查见共享 followup 目录。未修改任何 LATEST 或共享汇总。
