# 参与贡献

欢迎提交任何一道开放题的解法，也欢迎讨论题面和验收标准。负结果同样有价值：一条在给定预算下走不通的路线，能帮后来者少走弯路。

## 提交流程

1. 在 [problems/INDEX.md](problems/INDEX.md) 找到题目，读该题 `PROBLEM.md` 的「什么算解」和「现有参照」。
2. 想先讨论思路或细化标准，就开一个 issue，选「解法提案」或「题目讨论」模板。
3. 复制 [solutions/_template/](solutions/_template/SOLUTION.md) 到 `solutions/<题号>/<你的名字>-<短名>/`，填写 `SOLUTION.md` 和 `solution.json`。
4. 本地运行校验：

   ```bash
   python3 -I release/tools/check_submissions.py --root .
   ```

5. 用 `git commit -s` 提交（见下文 DCO），然后开 PR。CI 会再跑一次同样的校验。

代码可以直接放在提交目录里（单文件不超过 5MB），也可以放在你自己的仓库里，在 `solution.json` 的 `reproducibility.code` 中给出链接和提交哈希。大型数据请给下载地址和 SHA-256，不要提交进来。

## 审核与采纳

每份解法依次经过三个状态，由维护者写在提交目录的 `REVIEW.md` 中：

| 状态 | 条件 |
|---|---|
| 已审核 | 格式校验通过；五条验收标准都有回应；经典对照与被测方法使用同一模型或数据 |
| 已复现 | 维护者或另一位贡献者按 `reproducibility` 独立重跑，得到一致的结果，或明确记录了差异 |
| 已采纳 | 已复现，且结论和局限表述准确；合并后记入该题的「现有参照」 |

`solution.json` 中的 `self_assessment` 是作者的自评，不代表审核结论。审核意见和分歧都留在 PR 里公开讨论。

## 沉淀为 skill

被采纳的解法是 skill 的原料。同一类方法积累到足够多的采纳解法后，会按 [skills/README.md](skills/README.md) 的规则提炼为可复用的 skill，并署名所有来源解法的作者。

## 许可与 DCO

- 题面、图示和文档：CC BY 4.0，见 [LICENSE-CONTENT](LICENSE-CONTENT)。
- 代码，包括你提交的解法代码：Apache-2.0，见 [LICENSE](LICENSE)。`solution.json` 的 `license` 也可以写 MIT 或 BSD-3-Clause。
- 每个提交都需要 [Developer Certificate of Origin](https://developercertificate.org/) 签名，表示你有权以上述许可贡献这些内容。用 `git commit -s` 会自动在提交信息末尾加上：

  ```text
  Signed-off-by: Your Name <you@example.com>
  ```
