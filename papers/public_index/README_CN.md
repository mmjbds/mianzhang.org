# 公开论文索引层 - 2026-06-08

本目录是给 GitHub / 官网 / HF 技术镜像共用的公开论文索引层。它不是 PDF 仓库，也不是匿名会议 supplement。

## 平台分工

- Zenodo：论文、数据、证据包的权威 DOI 归档。
- GitHub：索引、manifest、claim boundary、issue / PR / 反例挑战。
- HF：技术镜像、demo、registry、artifact delta。
- mianzhang.org：人类读者入口、中文区、站点导航。

## 文件

- `../../public_registry/paper_index_20260608.jsonl`：机器可读 JSONL，每行一篇/一条公开记录。
- `paper_index_20260608.csv`：表格版公开索引。
- `PAPER_ARCHIVE_POLICY_CN.md`：GitHub 是否镜像 PDF 的规则。

## 规则

1. 已有 DOI 的论文后续版本优先走 Zenodo `New version`。
2. GitHub 默认只存元数据和边界说明，不全量存 PDF。
3. 匿名会议稿、`DO_NOT_UPLOAD`、私有日志、客户数据、交易/机器人执行 hook 不进入公开索引。
4. `NOT_DEMONSTRATED`、`NO_CREDIT_RECEIPT`、`CANDIDATE_NOT_COMPLETED` 不得在摘要、站点、README 或 issue 中写成成功。
5. P22 当前公开版本为 `v0.2 / 10.5281/zenodo.20582195`；P41-P45 必须保留各自证据边界。
