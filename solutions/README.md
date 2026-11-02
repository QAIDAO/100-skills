# 解法

每份解法一个目录：

```text
solutions/<题号>/<你的名字>-<短名>/
  SOLUTION.md      # 方法、结果、经典对照、复现、局限
  solution.json    # 机器可读的摘要，供校验与检索（schema_version 2）
  REVIEW.md        # 审核者写：审核、复现与采纳记录（与 review.json 一起，另开 PR）
  review.json      # 审核者写：机器可读的审核状态；没有这个文件即 unreviewed
  ...              # 可选：代码、小型输入、图（单文件不超过 5MB）
```

从 [_template/](_template/SOLUTION.md) 复制开始，提交前运行 `python3 -I release/tools/check_submissions.py --root .`。流程和审核标准见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

现有两份维护者示例：[B16 测量预算](B16/qaidao-vqe-shot-budget/SOLUTION.md)、[M17 两级活性空间审计](M17/qaidao-two-level-audit/SOLUTION.md)，都还没有独立复现（review.json 为 unreviewed），欢迎认领复现。

## 从 schema_version 1 迁移

2026-11 起 `solution.json` 改为 `schema_version: 2`：

- 新增 `problem_revision`（所依据题面的本仓库提交哈希）、`contribution_type`、`scope`；
- `reproducibility.code` 改为列表（仓库内路径必须存在，外部代码写 `{repository, commit}`），新增 `command`；没有随机种子时加 `seeds_note`，结果都没有 `uncertainty` 时加 `uncertainty_note`；
- 每个输入给 64 位 `sha256`，整目录输入给 `git_commit`；`compute.wall_time` 必填；
- `self_assessment` 拆为 `claims.conclusion` 与 `claims.milestone_status`；审核与原题状态移到 `review.json`。

两份示例已迁移，可对照它们改写。
