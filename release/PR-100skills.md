# release: v0.1.0 开放 84 道量子计算与科学计算研究问题

面向量子开源社区发布 84 道开放题，并建立贡献与沉淀机制：社区按统一格式提交解法，被采纳的解法按公开规则提炼为可复用的 skill。

## 内容

| 目录 | 题数 | 有执行记录 |
|---|---|---|
| `problems/biomedicine` | 26 | 26 |
| `problems/applied-materials` | 24 | 22 |
| `problems/model-dynamics` | 19 | 17 |
| `problems/extensions` | 15 | 15 |

- 每题包含 `PROBLEM.md`（题面、什么算解、现有参照、如何提交）、`problem.json`、`evidence.json`、图示 SVG；有执行记录的另附 `REFERENCE.md`。
- 贡献机制：`CONTRIBUTING.md`、`solutions/_template/`、`release/tools/check_submissions.py`、`.github/` 下的 PR 与 issue 模板和 CI。
- 沉淀规则：`skills/README.md`。
- 宣发：`release/promo/` 下的发布稿与展示页。
- 许可：`LICENSE`（Apache-2.0）、`LICENSE-CONTENT`（CC BY 4.0）。

## 证据边界

- 没有新增任何计算。题面五段逐字取自案例目录；背景与参照由构建脚本从源文件生成，只改写链接、去掉本机路径，结论未经改写。
- 现有参照全部来自经典计算机上的计算与模拟；原应用目标完成数为 0，不声称量子优势。
- 「什么算解」由五段拆解按统一模板生成，逐题细化留给社区讨论。
- 原始数据和第三方数据集不随题库发布。

## 验证

- `build_problems.py` 连续两次输出一致，并与仓库内的 `problems/` 逐字节相同；题面五段逐题与案例目录一致，来源哈希逐题一致。
- `check_submissions.py` 接受合规样例、拒绝 6 类坏样例；仓库内 `solutions/` 校验通过。
- 展示页在 1440、768、390 三种宽度下通过浏览器检查，无 JS 错误，84 题全部可达，并已人工视觉复核。
- 入库文件无本机路径、数据文件或凭证，Markdown 链接全部可解析。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
