<!-- 由 release/tools/build_problems.py 自 tasks/B23-therapeutic-sequence-design/execution/public-input-v3.1/RESEARCH.md 生成，勿手改 -->

> B23 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B23 public-input-v3：公开模型闭包推进

2026-10-04。本轮为原公开输入身份审计，原目标仍 incomplete。没有训练、预测、解码、新序列、新结合候选或量子模拟。

## 已闭合的部分

论文 R1 数据可用性入口 nanobody_MOQA 正式重定向至 [WS-MOQA](https://github.com/tucs7/WS-MOQA)。锁定 commit `ed013d4b5b61589178bc7dd62c40f9effbcaf0f3`。下载 35 个非 pycache 原文件；逐文件 SHA256 及 Git blob SHA1 校验记录于 `tasks/_execution/2026-10-04/bio/b23-followup/input-audit.json`，全部身份一致。

五个已训练 PARROT 分类器 `.pt` 每个 11964 bytes；五个 classifier dataset 每个2462行；原始已发表CSV及bVAE训练文本均冻结。二元自动编码器 TensorFlow checkpoint data/index/meta 已冻结；配置 latent_size=64，已有 vectors.txt 为2000行×64位，全部为二进制。模型只按原始字节存储，不 import、反序列化、pickle load。

原来的“未冻结预测器 checkpoint”缺口已有实质推进：公开模型字节身份现已冻结。尚不能声称模型运行与论文输出一致，因为不执行作者代码且缺模型格式/预处理/外部NetSolP权重的完整闭包。

## 数学与采样路径的静态核对

`sampler.py` 将五分类器均值、负标准差、NetSolP溶解度作为三个最大化目标。超体积参考点是 (0,-1,0)。非支配层分数 1/(层号+1)，不入前20层者为-10；FM拟合负层分数。模型是 `fmqa.FMBQM.from_data(vectors_all,scores)`，随后随每轮新增数据重训练，不是一个固定QUBO。配置64位意味着最多64线性项与2016两体项，不等于原实例系数已公开。

代码默认 `dimod.samplers.SimulatedAnnealingSampler()`；循环200轮，每轮num_reads=10，即每运行2000个采样读数。README提供切换D-Wave Advantage_system4.1的操作说明。代码默认状态不能识别论文Fig3的实际采样资源，不能将2000 reads认定为QPU记录。

静态发现 `NSPareto` 用 `np.where(i == classifiers_solubility_original)` 回查行，采用逐元素相等而非全行相等，可能把拥有某个相同目标值的其他行误认成对应行。此处是潜在偏差，需要已发表数值目标矩阵才能量化；不在本轮修复/重跑作者优化。

## 原H与固定非敏感基准为何仍未闭合

原树只有初始化vectors和训练指标，无FM的线性/二次权重、拟合标签、逐轮三目标数值、res.record的样本/energy/num_occurrences、作者十次运行seed和QPU元数据。现有64位文件README明确描述为随机初始化；没有依据当作论文采样分布。不能用它反推H，也不以通用toy H替代。

最小可执行输入：作者任意一轮已发表运行的64位QUBO稀疏系数+offset+变量映射、同一轮既有二进制样本/能量/频次与采样参数/solver ID。可完全停留在匿名二元变量，不加载生物模型、不解码；自实现校验能量并与既有记录比对。若要同输入经典基线再需预先冻结允许采样预算、seed、温度schedule和指标。当前这些前提未满足，不启动采样。

更大的端到端缺口：冻结NetSolP原权重/版本、fmqa精确版本、PARROT版本与拆分索引、每轮目标值/随机种子及QPU/SA实际运行身份。公开训练集存在不等于这些均已闭合。

## 其他正式路线

R2 论文PMC链接本轮返回reCAPTCHA，不绕过。作者[MOQA仓库](https://github.com/tucs7/MOQA)树锁定`f278fa09da6aba638de3478cbd5e177d0810b2e4`，同样仅见bVAE checkpoint、初始化vectors和训练指标，未见原QUBO/采样record。README示例为电荷密度、稳定性与Boman指标，并说明用SA，不能替代R1实例。

R3 [arXiv正式全文](https://arxiv.org/html/2503.05458v1)可读，现已关联JCTC 2025,21(19),9993–10005，DOI 10.1021/acs.jctc.5c00768。它是物理模型同时优化序列/构象的独立路线，不能当作WS-MOQA既有H。仅核对资源身份，不生成目标结合候选。

R1 SI PMC下载响应为HTML（21318 bytes）而非PDF；Springer CDN DNS失败。响应保留于sources/SI-response.bin并明确未读SI，不把HTML当补充材料。

## independent audit

自编 `audit_inputs.py` 仅使用标准库，计算文件哈希、对照Git tree blob身份、数已有二元向量形状、JSON配置与TSV行数，AST静态读取第三方采样器。35/35 blob身份通过。另读公开README与代码核对模型存在、SA默认路径、缺失输出和运行识别边界。没有执行第三方代码，没有数值预测与新生物序列产物。

## 下一步

仅申请上述“一轮匿名64位QUBO+既有采样record”即可开启原H能源复核；未取得前停止数值采样，不重复1/5统计审计。旧文件与LATEST不修改。


# B23 identity-v2：commit→tree 独立绑定

保留REPORT.md、manifest.json及全部旧冻结文件。上一版直接取递归trees/main响应sha作为commit，证据链不充分。本次通过`/repos/tucs7/WS-MOQA/commits/main`独立确认commit确为`ed013d4b5b61589178bc7dd62c40f9effbcaf0f3`；commit对象明确root tree为`0c0103e3492c4bbacf9638d4ca7a1742e44cdb21`。

随后以真实root tree身份读取非递归tree，按Git排序与二进制格式重建：`mode SP filename NUL raw-20-byte-SHA1`，拼接后加`tree SP payload-length NUL`头计算SHA1。得到`0c0103e3492c4bbacf9638d4ca7a1742e44cdb21`，与commit绑定和root-tree API身份三方一致。旧递归响应的全部root直系条目与新root条目一致。

因此原commit标签值正确，原推导方法不足，已补齐；旧递归响应sha本身不是root-tree身份，不能据其字段名独立推定对象类型。公开35文件blob校验仍有效。原目标incomplete，量子/经典采样/模型预测0；科学结论未改变。

证据：campaign sources/commit-main.json、sources/root-tree.json、audit_git_binding_v2.py与git-binding-v2.json。新版完整性清单为manifest.identity-v2.json，包含旧manifest与新增证据。未覆盖冻结旧版，也未晋升LATEST。


## 父级独立检查

105项文件/对象/路径检查通过。另用不含生物输入的两行三目标匿名数组验证了索引风险：两行共享一个目标值时，逐元素回查会把第二行指向第一行。该验证仅证明代码机制，原论文目标矩阵缺失，不能断言其发表结果已受影响。基于此，后续获得原H/采样记录前还需先验证目标行与样本ID的对应关系。完整检查见campaign validation/b23-parent-audit.json与b23-indexing-counterexample.json。
