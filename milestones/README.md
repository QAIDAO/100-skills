# 小任务

`problems/` 里的 100 道题是长期研究问题，一道题往往要很多份工作才能回答。这里把其中一部分拆成有边界、有输入、有验收标准的小任务，可以单独认领、单独完成、单独被复现和采纳。

- 完成一个小任务不会把原题标为已解决；原题没解决也不影响小任务被采纳。
- 负结果同样算完成：比如事先声明的方法没有带来改进，只要比较公平、证据完整，就能采纳。
- 认领、更新与释放规则见 [CONTRIBUTING.md](../CONTRIBUTING.md#认领任务)，用「认领任务」issue 模板。

## 状态

| 状态 | 含义 |
|---|---|
| draft | 方向已定，但输入、基线或验收者还没准备好，暂不接受认领 |
| ready | 输入可公开取得，验收判据已冻结，有确认的审核角色 |
| claimed / submitted / reproducing / accepted | 已认领 / 已提交 PR / 正在独立复现 / 已采纳 |
| blocked | 缺输入或外部条件，说明见任务卡 |

## 任务板

| 任务 | 题 | 类型 | 状态 | 发布前置 |
|---|---|---|---|---|
| [B16-M01](B16-M01.md) 独立复现 quick 基准 | [B16](../problems/biomedicine/B16/PROBLEM.md) | reproduction | ready | — |
| [B16-M02](B16-M02.md) 同总 shots 下的测量分配比较 | [B16](../problems/biomedicine/B16/PROBLEM.md) | method-comparison | ready | — |
| B14 时间步收敛 starter | [B14](../problems/biomedicine/B14/PROBLEM.md) | baseline | draft | 发布最小参数与轨迹种子；维护者试跑 |
| C07 连续反应产率 starter | [C07](../problems/extensions/C07/PROBLEM.md) | baseline | draft | 选定一种自旋与 ħ 约定，公开最小输入 |
| B22 结构映射与单分子基线 | [B22](../problems/biomedicine/B22/PROBLEM.md) | input-curation | draft | 领域导师核对结构编号映射 |
| B32 6 比特输入与 ED 基准 | [B32](../problems/biomedicine/B32/PROBLEM.md) | input-curation | draft | 从论文系数建立机读 Pauli 输入包，两人核对 |
| M17 冻结芯与截断审计复现 | [M17](../problems/applied-materials/M17/PROBLEM.md) | reproduction | draft | 固定作者仓库下载与环境；平衡空间 FCIDUMP 另列前置任务 |
| F11 双支响应基准 | [F11](../problems/model-dynamics/F11/PROBLEM.md) | baseline | draft | 公开参考态或重建路径 |
| F15 响应子空间公平比较 | [F15](../problems/model-dynamics/F15/PROBLEM.md) | method-comparison | draft | 固定参数、输入子空间与 seed |

draft 任务转为 ready 时会补一张和 B16-M01 同样结构的任务卡。F16 暂不拆任务：先要补相关函数数据与散射归一化约定。

## 任务卡写什么

任务 ID 与版本、所属题、目标与覆盖范围（以及明确不覆盖的部分）、输入（地址、版本、SHA-256、许可）、经典基线、执行环境、预计资源、交付物、验收方法与阈值、停止与失败条件、审核角色、认领状态。验收阈值在任务发布时冻结；要改阈值就发新版本并说明原因，不在看到结果后改。
