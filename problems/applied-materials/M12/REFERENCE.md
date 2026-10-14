<!-- 由 release/tools/build_problems.py 自 tasks/M12-half-mobius-molecule/execution/public-derived-cas-v3/RESEARCH.md 生成，勿手改 -->

> M12 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M12：真实公开几何上的 8 比特派生实验

当前推荐：对本次36/24维固定扇区，优先使用精确经典FCI。SqDRIFT实现核验通过，但六个量子投影态均未通过自旋纯度门，未观察到量子优势。原72比特表面分子模型和拓扑目标仍未完成。

## 公开证据与模型身份

[原论文v4](https://arxiv.org/pdf/2507.03516v4)含完整SI，Fig3D对应表面优化几何。[Zenodo15495263](https://zenodo.org/records/15495263)的真空与表面XYZ已核验：两个表面文件均305坐标，前15个为C13Cl2，后290个为145Na+145Cl点位，不能全当AO分子。singlet-surface注释误写triplet，文件名/官方MD5及异常均保留。表面点电荷大小和72q基组/活性轨道扩张规则、MO/积分仍未闭合。SI几何优化用CASPT2(12,12)/cc-pVDZ；这不足以唯一指定量子36轨道模型。ANO-RCC-VTZP出现于电子态/SOC计算，不能静默当作72q基组。

作者24轨道TB也未作为数值替代：Eq6印刷两个cross项同号；改成正交旋转块会改变单键谱。S2已确定七键段从7–8弱键开始，bending项为kbend sin²θ；NNN端点signed angle与全局局部轨道约定仍不够明确。无分子TB数值完成声明。

## 本次新派生模型与算法

使用作者singlet-vacuum.xyz的完整15原子几何，不改变元素/结构。112电子、83AO、STO-3G，conventional RHF无DF；25周期收敛。固定冻结54个双占轨道，保留canonical MO54..57（零基）。CAS中性4电子、阴离子5电子，共享中性MO，分别固定Ms=0和1/2。四轨道不保证完整π空间，RHF稳定性未测。最小基组无diffuse，不能由本次附着能判断真实阴离子是否束缚。

自写Jordan–Wigner full-H实现，198个厄米fermionic monomial组，λ=12.885720405 Ha；包含对角项，按组范数抽样并归一演化，无噪声、无配置恢复。times=0.5/1 au、steps=16/64、每格8 randomizations、每电路128 shots、种子20261004/5/6。每sector/seed32电路和4096 shots，总192电路、24576模拟shots。所有proposal先完成，再求FCI目标；未用FCI本征向量准备量子初态。

两个首条16步电路经Qiskit8q UnitaryGate Statevector与独立SciPy expm重放验证；门没有分解成硬件native gates，未报告虚构CX成本。所有采样CI结果使用完整相同H投影。逐组Nα/Nβ守恒不代表逐组S²守恒；选取的determinant子空间也不必自旋完备。

## 实际数值

| 状态 / seed | 唯一行列式 | 能量误差 (mHa) | S² | 1 mHa | 自旋门 |
|---|---:|---:|---:|---|---|
| neutral / 20261004 | 22 | 1.022101 | 0.006107865 | 失败 | 失败 |
| neutral / 20261005 | 16 | 1.177009 | 0.003406838 | 失败 | 失败 |
| neutral / 20261006 | 27 | 0.049163 | 0.000192291 | 通过 | 失败 |
| anion / 20261004 | 15 | 0.258802 | 0.750217682 | 通过 | 失败 |
| anion / 20261005 | 12 | 0.814322 | 0.753428891 | 通过 | 失败 |
| anion / 20261006 | 19 | 0.351960 | 0.753358582 | 通过 | 失败 |

经典HF+uniform legal以相同4096次draw覆盖全部36/24行列式，六组均精确FCI且自旋正确。HF+uniform singles/doubles给中性0.288163 mHa、阴离子0.192393 mHa误差；后者也未过自旋门。该比较仅匹配抽样次数，不能视为端到端成本等价，更不能外推大体系。

同H精确中性/阴离子能量为−1394.757946753204 / −1394.725741167648 Ha。本派生模型E_anion−E_neutral=0.032205585556 Ha，约0.876359 eV；它不是原分子实验电子亲和能预测。

| seed | 附着能误差 (mHa) | Dyson L2误差 | 属性+自旋联合门 |
|---|---:|---:|---|
| 20261004 | -0.763299 | 0.006992 | 失败 |
| 20261005 | -0.362687 | 0.057570 | 失败 |
| 20261006 | 0.302797 | 0.003466 | 失败 |

Dyson为保存的CI波函数在共享正交MO中的经典后处理，未在量子硬件测量。三个量子seed的附着能均满足2 mHa，但seed20261005的Dyson L2=0.057570超过0.05，全部seed的联合属性+自旋门失败。即使能量差碰巧很准，也不应把这些Ms态当纯singlet/doublet。

## 验证、资源与复现

来源父级155项检查通过；独立full256 H误差3.33e−15 Ha，PySCF扇区误差≤6.67e−16 Ha，FCIDUMP/MO/各态及属性已读回复核。Qiskit/独立expm误差≤2.49e−16。化学CPU6.48s、wall7.30s、峰值262MB；量子及经典控制合并阶段post-import CPU0.7144s、job wall2.21s、峰值389MB。量子全过程CPU未记录，不用wall代替。

属性协议文件02:20:13Z写入，量子作业02:21:13Z开始；hash登记02:21:45Z晚于结果02:21:15Z。首次属性脚本因登记flag失败，尚未计算属性；原版与失败记录保留。仅修正时间核对方式，科学阈值未改。这里是本地文件和工具记录，不是独立签名预登记。

输入/运行入口：`tasks/_execution/2026-10-04/materials/m12-derived-cas-v1/run_chemistry.py`、`tasks/_execution/2026-10-04/materials/m12-derived-quantum-v1/run_quantum.py --input tasks/_execution/2026-10-04/materials/m12-derived-cas-v1/hamiltonian.npz`。已有terminal输出，正常审阅无需重跑。验证入口：`tasks/_execution/2026-10-04/materials/m12-derived-independent`、`tasks/_execution/2026-10-04/validation/derive_m12_attachment.py`。所有依赖于现有PySCF2.12.1/Qiskit1.4.5环境，不执行下载的作者代码。

图表：m12-derived-evidence.png（本地证据，未随题库发布）。全文对应源文件与hash在manifest.json。旧public-geometry-input-v2保持不变。

## 后续判断

原目标优先恢复32e36o表面H、基组/轨道索引、点电荷和state-specific MO overlaps，再比较同H HCI/SHCI或DMRG。SqDRIFT/ExtSqDRIFT只作有明确误差/成本门的候选，经典selection与同样SD扩展应配对控制。删除对角项或拒绝trivial抽样改变演化，不能直接援用full-H收敛保证。四轨道实验未证明原分子的半Möbius拓扑；不因本轮失败自动加shots或更换模型。
