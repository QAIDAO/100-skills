<!-- 由 release/tools/build_problems.py 自 tasks/F10-vibronic-boson-sampling/execution/real-molecules-v2/RESEARCH.md 生成，勿手改 -->

> F10 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# F10：四真实分子双模振电子谱的闭包与判定

本轮把旧 F10 的 synthetic Gaussian 控制换成四种真实分子跃迁的公开双模参数，检验省略模式混合或压缩是否仍能保留完整光子分布与指定分辨率光谱。两种独立算法通过全部 3312 项检查，支持这个名义模型中的数值结论。应用上应优先用已验证的经典确定性积分；完整 Gaussian 变换的重要性不等于必须采用量子采样。

## 源输入及实验身份

[2020 PRX 论文](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.10.021060) 的表 II/III 对应 [作者 v2 完整 PDF](https://arxiv.org/pdf/1908.03598v2) 的 SI 表 I/II。作者 PDF 已实取，SHA256为 `dda8fc98cb6d17447590f2f89414546a3c0f5a87eb9de9362c2072d47d1e9c2c`。本轮主输入取已舍入硬件 Gaussian 参数，包含两套频率、旋转、位移及八初态。输入身份为 SHA256 `14fa31d128ede42074b893f82c3917588c895adb9b239a50db7e9df35af2cef6`。

| 分子跃迁 | 初始 Fock 态 |
|---|---|
| H₂O → H₂O⁺(B̃²B₂)+e⁻ | (0,0) |
| O₃⁻ → O₃+e⁻ | (0,0)、(1,0)、(1,2) |
| NO₂⁻ → NO₂+e⁻ | (0,0)、(1,0) |
| SO₂ → SO₂⁺+e⁻ | (0,0)、(0,1) |

这里始终保留两个选定振动模式，不代表分子全部 3N−6 核自由度。它是 **source-derived nominal harmonic model 的 method-matched new experiment**，不是原硬件实验的逐点复现，也不是整分子的谱预测。

源文存在两处必须公开的冲突：物理参数表把 θ 标为 degree，但四分子 K→d→α 静态闭包只有 rad 解释与硬件表位移一致；源 A7/S7 和 A8/S8 的旋转生成元又相反。本轮在计算前明确选择 rad 和 A7 主动输出约定，没有拟合 FCF：

`R=exp[θ(a₁a₂†−a₁†a₂)]`，`R†aR=Ua`，`U=[[cosθ,−sinθ],[sinθ,cosθ]]`。

完整变换为 `D(α) S†(ζ′) R(θ) S(ζ)`，右至左施加；`S(r)=exp[r(a²−a†²)/2]`。坐标法独立使用 `L=diag(expζ′) U diag(exp−ζ)` 与 `d=√2α`，从初态 Hermite 波函数求 overlap，而不复用 Fock 生成元代码。

## 同输入计算与应用控制

量子方法分支是软件中的理想 bosonic 门模拟，使用 sparse `expm_multiply`。每模维度 N=16、24、32、40，索引为 0…N−1；保存 32 个 NPZ、96 份 full/parallel/linear 复振幅态与未经重新归一化的概率。独立经典参照为二维 Cartesian Gaussian–Hermite 积分，分别使用 48/64 节点，输出每模40维，并检查尾质量及解析均能。

parallel 保留位移和两组压缩、省去 R；linear 在相同初 Fock 态上仅施加 D。四个真空块可按 Gaussian 简化层级解释；四个激发块只称为算符删减控制，不能套用 2026 论文的真空 Gaussian 层级结论。[层级近似的原始研究](https://www.nature.com/articles/s41534-026-01250-x)。

光谱横轴为 `E/(hc)=n′·ν′−n·ν`，单位 cm⁻¹；忽略电子 0–0 常数和零点能常数。固定 100 cm⁻¹ bins 使用 `floor(E/100)`，保留激发初态导致的负能量偏移。光子分布和分桶谱采用同一先验 TV 容许量 0.02；TV 指两概率分布绝对差之和的一半。该容许量是本实验的应用标准，不能视为普遍化学精度。

finite shots 仅对 full N40 抽样：256/4096 shots、各30固定 seed 重复，总硬件等效 shots为1,044,480；软件用 aggregate multinomial，不实际反复执行电路，也没有设备损耗、脉冲误差或实测 counts。图中的 q05/median/q95 是30次理想抽样的经验分位数，**不是置信区间**。

## 验收与停止条件

数值门在计算前冻结：norm误差≤1e−10；N32→40 TV≤.002；GH48→64振幅/概率差≤1e−10；N40参照尾质量≤1e−7；N40门法对 GH 的TV≤1e−7。保存输出身份、counts整数/合计、负 bins、能量和参数绑定均由独立审计检查。全部3312项通过后才解释简化分支；简化超门本身是科学结果，不调整输入、容许量或分桶去追求通过。

作者 FCF 表的本地初步抽取出现跨页重复状态、表块归属不确定，已从生产和审计排除；保留原 PDF 和拒绝记录，不去重选值、归一化截断表或拟合参数。两方法一致性验证不依赖这份抽取，也不能把一致性误当作者表格或硬件测量复现。

## 可用结论及成本边界

只在 O₃(0,0)、SO₂(0,0) 中，parallel 同时满足 photon/spectrum TV≤.02；linear 八块均超标。其余块提示在该模型和分辨率下需要保留完整变换才能达到容许量，**并不意味着需要量子硬件**。经典积分已直接给出同一完整分布；应先使用它，量子采样的应用优势仍无证据。

生产 job intake 为 CPU2.76s、wall3.074s、RSS79,790,080bytes、outputs1,685,206bytes；独立参考及审计为 CPU0.80s、wall0.750s、相同报告峰值RSS、outputs1,894,472bytes。两个科学作业合计 CPU3.56s、输出约3.58MB。二者包含的 workload 不同，不能据这些时间作速度比或优势比较；下载、人工源审查、fixtures和交付绘图也不包含在该作业计量中。

完整量子分支记7 Gaussian gates、一次 ideal PNR 测量 setting；初 Fock 制备的真实硬件成本未知，PNR读出 N40与源硬件至15光子的范围不同。测量预算、态制备、设备实现和强经典求解均不能省略成一个 gate 数。此次完成了有实质新输入的应用组件，`original_application_complete=false`：未重建原硬件counts与完整噪声/读出标定链，未复现作者所有实验谱。

审计证据：独立结果（本地证据，未随题库发布）、生产输出索引（本地证据，未随题库发布）、源筛选（本地证据，未随题库发布）。终态进程与资源证据位于 producer intake（本地证据，未随题库发布） 和 audit intake（本地证据，未随题库发布）；这些 intake 的 scope 文本保留“审计待定”旧阶段，最终科学结论以独立 results 的 `status=passed` 与3312门为准。


数值结果与图（本地证据，未随题库发布） · 完整指标CSV（本地证据，未随题库发布） · 冻结协议（本地证据，未随题库发布） · 终态复核（本地证据，未随题库发布）。
