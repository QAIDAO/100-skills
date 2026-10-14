<!-- 由 release/tools/build_problems.py 自 campaign/bio/b12-followup/revision-6/FINAL-REPORT.md 生成，勿手改 -->

> B12 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B12 revision-6 最终报告

原36个剩余任务已结束：成功36、失败0。合并revision-5原12，实际量子核运行覆盖48/48个保留任务，剩余未核验0。这是原作者cap1000协议及新公平对照的执行覆盖，不是无cap全原分子、原运行exact split或原五模型完整复现。原应用目标仍incomplete。

long-job 20261003T203648Z-b12-rev6-author-cap36-7f706aca 已completed、exit0，主批次耗时2342.86秒(39.05分钟)，另有归入36的中型pilot14.39秒。新任务worker峰值RSS≤743.50MiB；单任务耗时范围13.85–343.91秒。资源冻结上限600秒/task、5400秒/主job、RSS4GiB、单CPU线程，未因score调参、改阈值、重分split或补跑失败。

独立审计新216个模型输出的AUROC/AP/Brier/accuracy/F1/kappa/confusion和grid选择；重新生成全部cap/outer/inner索引并核对holdout标签、源行。每任务2000次paired bootstrap完整置信区间独立重算，抽样hash和前25次direct resample验证通过。原21个首/中/末source行数值抽查及source/cache/split/driver hash通过，revision-5全部80哈希保持不变。全部新任务Qiskit三分子态交叉核验通过，最大振幅误差2.17e-14。resume跳过成功36项、零重训、全部record和training-log哈希不变。

合并48结果有6项被保守列为泄漏/表征碰撞预检：3项p53有canonical/完整特征跨train-test重复，3项insulin_receptor(5.62/7.0/7.47)各有1种完全相同2056维输入跨不同骨架边界。后者是表征碰撞，不等于已证明测试标签泄漏；具体源行/SMILES/不同pIC50见full_feature_overlap_details.json。其余42项outer canonical/scaffold/full-feature交集零，但inner随机split仍共享骨架。静态代码确认fit只用inner train或选择后outer train；未保存拟合预处理对象，因此不称独立重做UMAP验证。

合并29/48项量子模型在保存阈值下输出恒定类别，其中23项为holdout多数类、6项为少数类。这些任务的accuracy/F1不能作为有效分类证据；连续概率仍可产生非平凡AUROC排名，不能把恒定类别预测等同于恒定分数。未依据holdout改变阈值。量子相对内部验证选定经典模型的AUROC差在29/48项为正；原冻结门仅旧ACE2的2项通过，且二者均为恒定类别预测，新36项通过0。该门与2000次bootstrap CI未作多重比较校正，也仅条件于已冻结split；同靶点多阈值不独立，不推出总体优势。完整IDs见all48-threshold-ranking-diagnostics.json。

|模型|无外层输入重叠任务平均AUROC|
|---|---:|
|quantum_ZZ|0.527522|
|compressed_linear|0.505063|
|compressed_rbf|0.496454|
|full_linear|0.506428|
|full_rbf|0.523510|
|full_RF|0.562554|

全部预检task IDs：p53-5.5, p53-5.6, p53-5.8, insulin_receptor-5.62, insulin_receptor-7.0, insulin_receptor-7.47。
此表按任务描述均值，各阈值重用靶点数据；不把它们当独立dataset作显著性。逐靶点均值与每任务完整预测见all48-descriptive-summary.json/records。全部观察经典最高test表现只用于描述，不是test选部署模型，不推出全局量子优势。

protocol.json原冻结hash保留。scope/data_reuse/limitations继承旧rev4/5文本，与36实际运行清单有metadata冲突；逐字段errata见protocol-metadata-errata.json。操作性tasks/split/preprocessing/grid/budget/bootstrap在源码与独立审计中一致，但不能称冻结文档完全一致预注册。大型outer-val在六模型均不用，区别于作者大型经典train+val臂；版本差异和holdout公开已审计的retrospective边界均保留。

无finite shots、噪声、QPU、硬件加速或未降采样全数据泛化证据。费用包括实际CPU walltime/RSS以及每任务state准备、Gram entries和未优化H/P/CX计数，不能把理想态缓存成本换成真实QPU测量成本。

最终证据：results.json、manifest.json、completion_audit.json、independent_prediction_audit.json、resume_verification.json、all48-descriptive-summary.json、完整checkpoint/tasks。审计日志完整保留；NumPy macOS matmul警告出现，但全部finite指标/CI、独立代数复算与Qiskit检查通过，未隐去或借此更换模型。

未修改LATEST或共享summary/index；由父级验收后集成。
