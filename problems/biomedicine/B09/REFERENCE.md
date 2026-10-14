<!-- 由 release/tools/build_problems.py 自 tasks/B09-kras-generative/execution/public-input-v3/RESEARCH.md 生成，勿手改 -->

> B09 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B09 公开输入后续闭包审计

本轮完成公开发布状态复核，原任务仍 incomplete；没有新复现输入，因此没有量子分布诊断、模型训练或分子生成。旧百万行 CSV 未重复计数。

## 新证据

作者仓库原 URL 自动迁移到 `the-matter-lab/quantum-generative-models`。公开 main 是 `20cb407b228735dc479737cf765448e9c7d5a9cc`，与 revision-2 的归档相同；API 返回 5 条提交、一个 main 分支、一个 `1.0.0-beta.1` 标签和 release。release 没有附件 assets，最近代码提交为 2024-05-08。仓库 updated_at 是平台元数据，不能解释为代码更新。

完整递归 tree 有 108 个条目，truncated=false；模型目录是源码，未发现训练权重、冻结划分索引、按模型归属的生成样本、原量子参数快照或硬件 counts 文件。该结论限于本次公开主分支树及唯一 release；不代表所有潜在第三方副本均不存在。

Zenodo latest API 仍解析到 record 11137638；versions API 只有该记录，版本 1.0.0-beta.1，唯一文件仍为已审查作者 zip。没有重复下载旧 zip。

正式出版页 Data/Code availability 仍引用同一 DOI。正式出版 SI 下载 SHA256 为 `b276bedd400ffcda1fc22c451a4f7e8303f4f15597b3c730d2255e3ece69e363`，与 revision-2 已审查 SI 完全相同，故没有重复审查其数值。出版页的 16q 实验与四比特示意线路描述提供方法轮廓，不能替代原训练角度和样本。

## 最小缺口

量子分布诊断需要原 16q 拟合参数、精确门序列/拓扑及 bit order；或原硬件 counts、shots、bit order、任务与运行身份。单有配置和训练代码不能构成原分布。原混合模型复核另需 checkpoints、tokenizer/预处理快照、按模型分组的已有样本和冻结划分。当前公开发布没有新增这些输入，故依赖步骤停止，不造 toy。

## 证据与范围

获取日志、原始公开 API 响应和正式 SI 均在 `tasks/_execution/2026-10-04/bio/b09-followup/`；每份成功下载输入 SHA256 见本目录 manifest.json。网络沙盒初次读取失败日志保留；获准后仅读取公开端点，没有凭据、403 绕过或联系作者。没有运行/import 下载源码或反序列化 pickle。LATEST、共享报告、parent revisions 和根 NEXT 均未修改。

来源：[正式论文](https://www.nature.com/articles/s41587-024-02526-3)、[作者仓库](https://github.com/the-matter-lab/quantum-generative-models)、[唯一 release](https://github.com/the-matter-lab/quantum-generative-models/releases/tag/1.0.0-beta.1)、[Zenodo](https://zenodo.org/records/11137638)。
