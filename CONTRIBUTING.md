# 参与贡献

欢迎提交任何一道开放题的解法，也欢迎讨论题面和验收标准。负结果同样有价值：一条在给定预算下走不通的路线，能帮后来者少走弯路。

## 提交流程

1. 在 [problems/INDEX.md](problems/INDEX.md) 找到题目，读该题 `PROBLEM.md` 的「什么算解」和「现有参照」。第一次参与建议先走 [入门轨道](starters/README.md)：从热身题的 starter 复现参照数字开始。
2. 想先讨论思路或细化标准，就开一个 issue，选「解法提案」或「题目讨论」模板；想做一个已经拆好的小任务，看 [milestones/](milestones/README.md) 并用「认领任务」模板。
3. 运行 `python3 -I release/tools/new_solution.py <题号> <名字>-<短名> --author "你的署名"`，例如 `python3 -I release/tools/new_solution.py B16 alice-shot-budget --author "王小明"`。目录名只用 ASCII 字母、数字、点、下划线和连字符；中文署名放在 `--author`。脚手架会从 [solutions/_template/](solutions/_template/SOLUTION.md) 建好目录，并把当前提交写进 `problem_revision`（你依据的题面版本）。填写 `SOLUTION.md` 和 `solution.json`。不必一次回应全部五条验收标准里的研发决策：只解决题目一小部分的解法同样欢迎，在「局限」里写清楚没覆盖什么即可，写法见 [B16 入门示例解法](solutions/B16/qaidao-vqe-shot-budget/SOLUTION.md)。
4. 本地运行校验：

   ```bash
   python3 -I release/tools/check_submissions.py --root .
   ```

   校验通过只说明：字段齐全、数值类型正确、本地代码路径存在、每个输入有 SHA-256（或整目录输入的 git 提交）、给出了运行命令和耗时、没有随机种子或误差条时说明了理由。它**不**说明结论科学上成立，也不说明结果已被复现。模板里的 `<...>` 占位符没填完时校验不会通过，这是有意的。

5. 用 `git commit -s` 提交（见下文 DCO），然后开 PR。CI 会再跑一次同样的校验，并检查每个提交的签名。

代码可以直接放在提交目录里（单文件不超过 5MB），也可以放在你自己的仓库里，在 `reproducibility.code` 中写成 `{"repository": "<URL>", "commit": "<哈希>"}`。大型数据请给下载地址和 SHA-256，不要提交进来。

`contribution_type` 说明这份贡献是哪一类：`reproduction`（复现）、`baseline`（基线实现）、`method-comparison`（方法比较）、`failure-analysis`（失败分析）、`hardware-validation`（硬件验证）、`input-curation`（输入整理）、`literature`（文献与文档）。后两类可以没有数值结果，不必为了模板编数字；某个结果没算出来时，`value` 写 `null` 并给出 `status`（`not_evaluable` 或 `skipped`）和 `reason`。

## 审核与采纳

四件事分开记录，互不代替：

| 记录 | 写在哪里 | 谁写 | 取值 |
|---|---|---|---|
| 研究结论 `claims.conclusion` | `solution.json` | 作者 | supported、refuted、inconclusive、not_applicable |
| 里程碑完成 `claims.milestone_status` | `solution.json` | 作者 | completed、partial、not_completed（相对 `scope` 声明的范围） |
| 审核状态 `status` | `review.json` + `REVIEW.md` | 审核者 | unreviewed、needs_changes、reviewed、independently_reproduced、accepted |
| 原题状态 `application_status` | `review.json` | 维护者 | open、completed |

一条被反驳的假设（refuted）可以是完整、已复现、被采纳的里程碑，同时原题仍是 open。

审核状态的含义：

| 状态 | 条件 |
|---|---|
| reviewed（已审核） | 格式校验通过；五条验收标准都有回应；经典对照与被测方法使用同一模型或数据 |
| independently_reproduced（已复现） | 解法作者以外的人按 `reproducibility` 在自己的环境重跑，`review.json` 里有一条 `kind: reproduction` 记录：被复现的提交、环境、命令、逐项结果与容差，全部在容差内 |
| accepted（已采纳） | 已复现，结论和局限表述准确；`accepted_claims` 写明采纳的具体命题；合并后记入该题的「现有参照」 |

PR 合并不等于采纳：解法经格式审核后以 unreviewed 合并，方便别人复现；复现与采纳由审核者另开 PR 更新 `review.json` 和 `REVIEW.md`（模板见 [solutions/_template/](solutions/_template/REVIEW.md)）。`solution.json` 里不能写审核状态，作者也不能用自己的复现记录升级状态，校验器会拒绝。审核意见和分歧都留在 PR 里公开讨论。

## 认领任务

长期的研究题拆成了可以单独完成的小任务，见 [milestones/](milestones/README.md)。认领规则：

- 用「认领任务」issue 模板留言认领，写明打算做的范围和预计第一次更新的日期（建议两周内）。
- 认领不排他：同一任务可以有人并行做，结果都可以提交；请在 issue 里说明，避免重复劳动。
- 超过约定更新日期没有进展，维护者会在 issue 里询问；再过两周无回应就释放认领。已经提交的部分工作保留署名。
- 任务状态：draft（未准备好）→ ready（输入、基线、验收者都已就绪）→ claimed → submitted → reproducing → accepted；也可以是 blocked、needs-changes 或 withdrawn。完成一个小任务不会把原题标为已解决。

## 沉淀为 skill

被采纳的解法是 skill 的原料。同一类方法积累到足够多的采纳解法后，会按 [skills/README.md](skills/README.md) 的规则提炼为可复用的 skill，并署名所有来源解法的作者。

## 许可与 DCO

- 题面、图示和文档：CC BY 4.0，见 [LICENSE-CONTENT](LICENSE-CONTENT)。
- 代码，包括你提交的解法代码：Apache-2.0，见 [LICENSE](LICENSE)。`solution.json` 的 `license` 也可以写 MIT 或 BSD-3-Clause。
- 每个提交都需要 [Developer Certificate of Origin](https://developercertificate.org/) 签名，表示你有权以上述许可贡献这些内容。用 `git commit -s` 会自动在提交信息末尾加上：

  ```text
  Signed-off-by: Your Name <you@example.com>
  ```

  DCO 签名和 GPG/SSH 提交签名是两回事，这里只要 `Signed-off-by` 一行；可以用公开的 GitHub noreply 邮箱，不必披露私人邮箱。CI 的 `dco` 检查失败时，在你的分支上补签再强推：

  ```bash
  git rebase --signoff origin/main
  ```

  ```bash
  git push --force-with-lease
  ```
