<!-- 由 release/tools/build_problems.py 自 tasks/C02-euv-tin-photoresist/execution/public-source-v3/RESEARCH.md 生成，勿手改 -->

> C02 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# C02 原有机锡公开输入审计 v3

本轮闭合作者公开源码快照与条件性基组规模，未闭合原 FOMO 电子模型。原应用 incomplete；没有 SCF、FOMO、量子线路、shots 或动力学执行。

原论文 [Ab initio photodynamics of model EUV photoresists](https://doi.org/10.1016/j.chemphys.2018.06.009) 的 TMTH 为 Sn(CH3)3OH（15 原子），THMS 为 Sn(OH)3CH3（11 原子）。现有合法出版索引摘要/方法片段说明 MP2 中性/阳离子优化及振动检查、H/C/O aug-cc-pVDZ、Sn aug-cc-pVDZ-PP 与小相对论赝势；未取得完整正文或 SI，不能由片段补出原 FOMO 参数。原 case 的 11 原子 CAS6e6o/5e6o 是后续方案，不是原文已给定输入。

新增来源和版本

PHOTOX 官方 org 16 个公开仓库清单、3 个相关完整路径树与 API commit→tree 绑定已保存。photoxrepo 固定 f4f16610673ce8835f329dd6dc39194f0ce8eae8（239 节点）；ABIN 固定 9c4c611048caadcacd660105ef174f60c0153237（1525 节点）；ABIN-Documentation 固定 3641169ea0b8063ecb72eb438702e6688af1dec3（8 节点）。独立重建 175 个 Git tree 哈希；前两仓库合法 codeload archive 的 1592 个 blob 全部逐项匹配（含 photoxrepo 的 3 个符号链接目标字符串），未跟随链接、导入或执行作者代码。Documentation 只核完整路径树，不能称已读全部文件内容。来源、HTTP 与 SHA256 见 source-ledger.json；对象明细见 source-scale-audit.json。

198/1365 个 UTF8 常规文件作有界身份搜索，未找到精确 DOI/PII、目标分子名或 Sn XYZ 行。初始无词界 THMS 正则误匹配 algorithms，候选命中不能证明原论文关联；identifier-match-erratum.json 的词界复核零命中。不能由这项有限搜索证明所有无名或二进制输入都不存在。photoxrepo 的 fomo.inp 指向 methaniminium.xyz、6-31g 和温度0.2，是其他体系通用示例，不能套用到原有机锡。

[作者官方 people 页面](https://photox.vscht.cz/people/) 确认相关 2020 博士论文及 2017 EUV 本科论文，页面未给下载文件。官方 2016 学生会议摘要有 Dvořák 的 EUV/TMTH 一/二次电离与断键描述，没有坐标/FOMO 定义。机构库作者搜索 HTTP503、Zenodo DOI 查询500 均原样保留，不当成空数据。Figshare DOI 查询200返回空列表只说明该查询。Crossref仅给出版商TDM链接，没有公开SI链接；未使用凭据/付费访问或猜测附件URL，旧组内出版页未重复下载。

条件性规模与经典对照

[Basis Set Exchange Sn 标准库](https://www.basissetexchange.org/api/basis/aug-cc-pvdz-pp/format/json/?elements=50) 和 H/C/O 对应库给球谐 AO H9、C/O23、Sn32；Sn 当前标准条目是28核心 scalar ECP。这是当前库的透明尺度假设，不能证明原2018精确ECP/SOC设置。两分子中性全电子均86、单阳离子85；使用该标准28核心ECP后条件性显式电子58/57。并未因此指定原态的自旋或原活性电子数。

|条件模型|球谐AO|完整float64 ERI字节|8折压缩ERI字节|
|---|---:|---:|---:|
|TMTH|214|16778188928|2117012120|
|THMS|178|8031006848|1015250768|

TMTH 压缩 ERI 已接近2GiB，不能把完整 in-core MP2/FOMO 重建当作轻量已可执行任务；THMS还需波函数、转换中间量和求解开销。direct/DF可能改变资源及模型误差，但本轮没有测量其性能。后续 CAS6 提案的12q/4096 Fock维与中性Ms0=400、阳离子Ms1/2=300，仅是条件组合数学；256MiB dense complex128 H 不提供缺失的物理投影。

原输入到齐后，强经典优先同一 FOMO 轨道、同一 h1/ERI/core offset 的 CASCI 多根，不能用 CASSCF 优化后不同轨道冒充同 H。量子组件要报告态身份、原生门成本、有限 shots/编译误差与空间敏感性。单点电子能验证仍不提供 surface-hopping 产率或 EUV 分辨率；完整动力学还缺 forces/NAC、时间单位和初态系综。

验收与失败保留

来源哈希与尺度算术完成；原模型输入门未过。没有冻结可执行科学协议，未来≤600单线程CPU秒/≤2GiB仅是到齐后另行冻结的上限。自身静态对象/规模审计用时6.54秒（wall），整体抓取/整理CPU未知；科学计算CPU为0。TarFile关闭错误保存，首次把3个符号链接排除的扫描保存，v2仅修正为合法Git blob目标字符串；原结果未删改。18个旧case/来源文件哈希均保持。
