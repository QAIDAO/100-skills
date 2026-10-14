<!-- 由 release/tools/build_problems.py 自 tasks/M10-corrosion-mg-niobium/execution/public-input-v2/RESEARCH.md 生成，勿手改 -->

> M10 的现有参照：本项目最新一轮研究报告。供对照与复用，不代表最优解。

# M10 原公开输入闭包 v2

本轮完成新的来源与数值输入审计，**量子执行0、SCF0、shots0**，原Mg水/MgAl腐蚀与Nb氧迁移目标仍为 **incomplete**。取得了真实公开64Mg裸金属坐标和PEST Hamiltonian；其数据身份可独立复算，但不能作为原含水反应电子态求解。没有重算旧资源表，也没有用任意小粒子数、替代分子或示意图猜坐标。

## 原文与版本

[Nature出版全文](https://www.nature.com/articles/s41534-025-01171-1)发表于2026-01-23。本轮取得官方全文、PDF和[36页SI](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41534-025-01171-1/MediaObjects/41534_2025_1171_MOESM1_ESM.pdf)。官方dataavailability指向pyLIQTR，没有给出原Mg水/MgAl/Nb各驻点输入包。

[arXiv版本记录](https://arxiv.org/abs/2406.18759)保留v1 2024-06-26与v2 2025-04-04的差别。v1官方HTML另存；已取得latest HTML/source快照，源包43个regular文件只有TeX、参考文献、样式和图像，未含原坐标、积分或样本。latest源包与同时获取的abs metadata关联，不冒充成功下载固定v2端点；固定v1/v2 source请求均HTTP406，失败记录保留，未变更请求绕过。当前旧M10.html与新latest HTML SHA256相同，只是新增SI/版本/真实数据核验。

## 真实公开数据与固定Git身份

作者引述[pyLIQTR](https://github.com/isi-usc-edu/pyLIQTR)的v1.2.0固定commit `e63e18a2b82ac48cf7b9f3bd0724431e13740501`，root tree `81dce4aaca610506ea5edfe8d1b64b0d274a68a9`，完整递归363条。当前main另固定 `0465e1d9ed8ca4fd5ff08df350010ea35ebead66`，root tree `1660b0a311bb7f6531a367f20b819ec7dd684afd`，500条。请求的真实treeSHA与commit元数据一致，31个已取raw文件的Git blob SHA1全部通过。两个版本的几何与最小HDF5逐字节一致。PEST静态源码在两个版本均已获取；当前文件不冒充原作者生成数据的确切commit。

仓库公开两套64Mg bare-slab XYZ，每套都没有H/O/水，含orthorhombic结构。_info固定cell为12.83708×11.11724×15.631000Å，三向周期。_info把法向真空称为slab厚度两倍；按原子中心z范围，厚度7.815499Å、剩余空隙7.815501Å，约等于一倍厚度，这个真空/厚度口径也未静默修正。它与原Dimer的12.7×12.7×19.9Å含水胞不同。目录存在更高cutoff裸Mg HDF5，但未见命名为原Mg水/MgAl/Nb目标的坐标/H；10个分支只核名字，未声称全部分支内容或全球公开数据均不存在。

最小0.5Ry原HDF5含36个spinless轨道、n_qb36、grid3×3×4、138个displacement，真实T/V/U及Pauli系数均有限numeric数组，h5py直接读取，不pickle。Notebook明确这是unphysically low cutoff的资源演示；没有物理Nα/Nβ、原波函数或匹配经典电子能。64Mg中性全电子768，即便假设Mg仅2价电子也是128，超过spinless36和假设扩spinful72的容量。任取N≤36可构造形式上的粒子扇区，却失去原物理体系；这里不执行。直接36q complex128fullvector还需1024GiB，但这不是所有compact算法不可行的证明。

自写recompute_coefficients.py（本地证据，未随题库发布）按静态PEST公式和原XYZ/grid重算全部138项T/V与36项U。最大残差T3.82e−17、V6.25e−17、U3.20e−14Ha，独立确认bareMgZ12而非Mg2valence核势。初版把作者Atoms居中当成通常bbox居中，U差6.57733Ha，原失败脚本保留。查源码后使用其明确sum(abs(min,max))/2−max约定才通过；原坐标未改，没有根据电子能调模型。该源约定在全正轴不等于标准bbox居中，需保留以复现数值。

## 原模型不一致与仍缺输入

正文写4×4×4 slab、1water、70total；SI叙述四层每层4×4Mg并加2water，若按64Mg计为70total；SI TableS.I却逐字写70Mg加2water，即76total。SI第6页本地渲染（本地证据，未随题库发布）已视觉确认，未静默修正。中/大模型main总原子数与SI literal Mg数量也不同：257total/26water与257Mg/26water；586total/99water/36OH与587Mg/100water。不能由这些互相冲突的计数唯一恢复结构，更不能摆放两个水冒充原几何。

出版正文将主要模型称valence-only PP；**SI S-IV明确说明乐观资源估算未包含实际PP Hamiltonian实现，而把非PP H与价电子计数配用**。相应SELECT/PREPARE的PP成本也未纳入。仓库PEST裸核Z12系数已复算，不能把它简单换成128electron就称真实valenceH。原USPP/GTH/HGH参数文件、augmentation/nonlocal terms与对应原结构没有取得。正文/latestarxiv文字1Ry=2Ha，而静态代码0.5Ha/Ry，二者保留，不将文字错误静默用于cutoff重建或修算旧资源。

Mg目标需要原水解/析氢驻点R/TS/P、cell/电化学条件与匹配H；MgAl需要具体Mg17Al12表面占据/终止与含水端点。Nb原目标需要原SQS金属占据、oxygen-oct/CI-NEB TS、氧-free胞和O2参考。原氧solutionenergy组装为E(alloy+O)−E(alloy)−0.5E(O2)，迁移势垒再取TS−oct；仅给合金化学式/随机SQS recipe不固定这些坐标和状态。没有用资源表或几何图像替代数据。主文所引local-embedding表面反应论文 [arxiv2203.07536](https://arxiv.org/abs/2203.07536) 是另一模型；其request-only数据/代码声明来自官方索引摘要旁证，未取得数据、未联系作者。Nature工具读取遇重定向失败、arxiv源包406保留，见web-access-notes；这些发现性摘要不用于证明本M10全网缺数据。

## 停止条件、误差边界与下一步

226项来源核验通过，包括请求SHA/大小、真实commit→tree绑定、31个rawblob、两个XYZ计量、numericHDF、独立系数身份及11个旧文件保持。来源审计通过与原物理输入闭包失败分开。最小H粒子容量失败属于输入可执行性判定，不是预冻结量子求解失败门。没有新能量、SCF、FCI、VQE、QPE、线路资源或shot结果。

模型误差：实际水/合金/氧结构、PP和sector未闭合；solver误差：没有原H求解，不能测；measurement误差：无shots；全局组装：无匹配端点和constants，不能报告势垒、HER/腐蚀速率或KMC。取得原completeconfiguration即可自写重建，无须强求现成FCIDUMP；但不能省略PP/electron/constant身份。

最小下一步是原64Mg+water一个真实驻点对及完整PP/cell/state定义，或Nb原occupancy/oct/TS与reference配对包。之后另冻物理有据的原体系active/embedded空间、同H强经典、守粒子数实际线路、3seed、有限shot与编译资源，并保留空间/PP敏感性；预算600单线程CPU秒、设计RSS≤2GiB。当前不因小模型方便而造空间，不创建后台任务。此次source audit独立归档，旧冻结文件、LATEST与共享汇总未写。
