<!-- 由 release/tools/build_problems.py 自 tasks/B06-thermolysin-free-energy/execution/revision-4-input-closure/RESEARCH.md 生成，勿手改 -->

> B06 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# B06 revision4：原Thermolysin输入闭包

本轮完成公开输入审计，原任务仍未完成。没有取得原Thermolysin积分/offset或bookending采样数据，因此量子线路执行、模拟shots、H求解和科学计算CPU均为0。未从晶体结构重建一个替代QM/MM模型。

## 新增可核实证据

原论文最新官方版本为[arXiv2604.09857v2](https://arxiv.org/abs/2604.09857v2)，修订于2026-04-30。官方下载源包3,632,755字节，SHA256 `5386c05d235d1053fff33c6dba1306b8486cf4803318fc4332e3a9379e7223e3`。11个成员恰为README JSON、TeX、Bib与8张PNG；SI嵌在TeX中，不存在另一个被忽略的数值SI附件。没有FCIDUMP、Molden、counts、拓扑、轨迹或MBAR矩阵。

原文TeX行302–324仍指向通用软件和按请求提供的AMBER/QUICK接口。新增发现的[quantum-aimd v0.1.1 / Zenodo22923052](https://zenodo.org/records/22923052)于2026-09-23公开，为**同作者后续工作流**，其README引用2607.28548，目标为H2O/NH3/CH4。它不是B06原bookending实现恢复。归档77,232字节，SHA256 `21b3557b0a3b09dab763e8e36df1df6ebfa7b98c3c4b16d693cb435cdbd7c53a`；49个常规文件的Git blob均匹配[固定提交4663d534d7872787ab459a122e10393814cf3226](https://github.com/isusanta/quantum-aimd/tree/4663d534d7872787ab459a122e10393814cf3226)，最新版README与归档一致。README明确排除轨迹/处理结果，演示QUICK输出为合成格式fixture；源码仅静态阅读，未运行demo、测试或账户加载。

已检查官方merzlab的QUICK、QUICK-tests、cchemtools完整未截断树，及上述后续工作流。文件树检查只能支持已审入口和文件名边界，不宣称全网无数据。精确标题Zenodo与thermolysin AND SQD查询均0条；DataCite精确标题只有原arXiv DOI。宽OR查询返回的其他SQD记录保留，未误当Thermolysin数据。首次误用merzgroup入口返回404，之后查官方merzlab，失败记录未删除。

## 原模型定义与不足

SI TeX行404–454描述了quick.out点电荷、Molden轨道、AVAS、积分输出及gas-phase CCSD初态参数化。作者公布活性空间0PJ(26e,19o)、0PI(26e,18o)，RHF闭壳层，LUCJ两重复及SQD/extSQD批次规则。**这些文字不是实际系数。** 缺原QM原子mask、边界/质子化、AVAS变换、嵌入场和完整常数；不能确认文件级电子数/自旋、轨道顺序或嵌入H与gas-phase准备H的关系。

Fig1虚线框只覆盖配体的一部分，正文另以solute概述QM区。图可辨认区域，却不能指定链接原子与边界处理。本轮保留此差异，不擅自解释为整个配体都在QM区。

[RCSB5TMN](https://www.rcsb.org/structure/5TMN)含0PJ，[RCSB6TMN](https://www.rcsb.org/structure/6TMN)含0PI；各在E317有32条配体坐标，重原子组分分别C21/O7/N3/P1与C21/O8/N2/P1。PDB SHA分别`9ca982b2949c287890f3690b221911c40e69d44e164208a6e4e4425f2e24754c`、`7125e003d1962188d7c4db9ea8daba5fb8b8f2d0a1ef9cd21f531c48aa06394e`。化学组分库形式电荷0，原文QM区含带负电磷酸基；不能用该中性组分默认值替代原计算电荷。晶体坐标缺作者平衡后溶剂、拓扑和点电荷，不能当bookending轨迹。

## 成本边界与计算可行性

SI FigS1（TeX行414）给出50触发×4端点×6窗口×2重复=2400次线路，作者1min/线路，合计40h硬件时间。这是**作者账目的独立整数复算**，不是本轮量子运行。旧revision3的1fs/2fs单重复条件情景保持原样；新caption额外包含两重复，不能据此反推唯一MD步长或覆盖全部前处理、平衡、排队及经典后处理。Fig5排除了extSQD附加成本；8CPU/100GB的比较图与SI10CPU批次设置上下文不同，不能合并成完整等成本优势。没有匹配ext-HCI原输出。

按闭壳层推断Na=Nb=13，Ms0维数分别736,145,424与73,410,624；这不是纯单重态维数，也尚无文件级spin核验。38/36个逻辑JW qubit（不含辅助位）的complex128全态矢分别4096/1024GiB。固定粒子数单个复向量分别10.9694/1.0939GiB，未含工作向量或算符；后者单向量小于2GiB不代表整个求解可行。缺真实H时，不冻结600CPU秒实验、不裁小活性空间凑量子计数。

## 最小缺口与下一步

先取得**一个标识到端点/窗口/重复/帧的原Thermolysin快照包**：完整h1/h2（或FCIDUMP）、NORB/NELEC/MS2、单位/积分约定/轨道顺序、含核/冻结core/嵌入贡献的总offset、QM mask与链接/质子化、原Molden/AVAS变换和quick.out点电荷；再加原t2/LUCJ参数或相同快照的raw counts以及同H HCI/ext-HCI参考/阈值/耗时。该包只允许固定H量子组件核验，不能独自得到结合自由能。

复现原相对结合自由能还需四端点六窗口两重复的拓扑/坐标/restart/轨迹、MD输入和实际dt、各采样的跨窗口能量u_kn与N_k、β/能量单位/时间戳/去相关选择、MM TI dU/dλ样本与权重、独立重复/相关时间/ESS/MBAR重叠和误差记录。可先对公开的现成u_kn进行统计重算；当前尚无这些payload，不以图像曲线补猜矩阵。

## 验证与交付

`audit_input_closure.py`只使用标准库静态容器/文本读取、RCSB固定列解析、哈希和组合数。全部断言通过；没有下载源码执行或pickle。B06已有13个受保护文件逐字hash未变，未改LATEST/shared。setup缺json导入的技术失败保留于technical-attempt-1.json，不是科学失败。

证据目录：`tasks/_execution/2026-10-04/bio/b06-followup/`。入口为`input-closure-audit.json`、`summary.json`、`validation.json`与`FINAL-MANIFEST.json`。新修订仅完成输入审计，科学门仍为blocked；原自由能目标incomplete。
