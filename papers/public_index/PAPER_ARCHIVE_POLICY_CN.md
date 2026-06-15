# GitHub 论文归档策略 - 2026-06-08

## 结论

GitHub 是可信索引层和可复核导航层。公开论文与证据包的权威长期归档以 Zenodo DOI 为准。

## 默认放入 GitHub 的内容

- DOI registry：`paper_id`、标题、DOI、record URL、版本、发布日期、状态。
- Manifest：公开 record 文件列表、hash、上传包 SHA、文件数量。
- Claim boundary：允许主张、禁止主张、证据等级、公开传播状态。
- README / CSV / JSONL：方便人类阅读和机器索引。
- Issue templates：反例、hash mismatch、边界挑战、复现失败。

## 默认不放入 GitHub 的内容

- 全量 PDF 批量镜像。
- 非公开版本、私人通信截图和无法公开复核的材料。
- 非公开版本、私有材料、客户数据、执行日志、交易或机器人执行接口。
- 大 zip、原始返回包、私有运行环境或凭证。

## PDF 例外

只有同时满足以下条件，才考虑把少数 PDF 放到 GitHub Releases：

1. 已经公开，且适合实名引用或公开引用。
2. 已有 Zenodo DOI，且页面明确写明 Zenodo 是权威引用目标。
3. 许可证清楚。
4. 文件体积小，且不会污染 git history。
5. 附带 SHA / manifest / boundary。

常规 git tree 不直接放大型 PDF；若未来确需大规模二进制镜像，再单独评估 Git LFS 或 Release assets。

## 最新边界提醒

- P22：当前版本为 `v0.2 / 10.5281/zenodo.20582195`；previous version 为 `10.5281/zenodo.20156365`；concept DOI 为 `10.5281/zenodo.20156364`。
- P41：local constructed evidence only；不能写真实机器人部署或第三方复现。
- P42：shadow-only runtime evidence；不能写 alpha、实盘、收益、交易执行接口。
- P43：theory + constructed witnesses only；不能写 real-stack validation。
- P44：R-shadow full-rollout candidate included, not completed；不能写完成 OpenVLA/V-JEPA2 R-shadow 或真实机器人。
- P45：C-controlled success + public no-credit receipts；不能写超出已记录 C-controlled positive / public no-credit receipts 的 external task-relevant public model validation、真实机器人、第三方复现、hard 0.05 margin 或无条件 GEE 最优。
