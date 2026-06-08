# 公开论文索引层 - 2026-06-08

本目录维护 GitHub / 官网 / HF 技术镜像共用的公开论文索引。这里记录 DOI、版本、状态、hash 和 claim boundary，方便读者与工具按同一套公开记录检索。

## 平台分工

- Zenodo：论文、数据、证据包的权威 DOI 归档。
- GitHub：索引、manifest、claim boundary、issue / PR / 反例挑战。
- HF：技术镜像、demo、registry、artifact delta。
- mianzhang.org：读者入口、中文说明、站点导航。

## 文件

- `../../public_registry/paper_index_20260608.jsonl`：机器可读 JSONL，每行一篇/一条公开记录。
- `paper_index_20260608.csv`：表格版公开索引。
- `PAPER_ARCHIVE_POLICY_CN.md`：GitHub 是否镜像 PDF 的规则。

## 规则

1. 已有 DOI 的论文后续版本优先走 Zenodo `New version`。
2. GitHub 默认存元数据和边界说明；PDF 以 Zenodo DOI 记录为权威来源。
3. 非公开版本、私有日志、客户数据、交易或机器人执行接口不进入公开索引。
4. `NOT_DEMONSTRATED`、`NO_CREDIT_RECEIPT`、`CANDIDATE_NOT_COMPLETED` 不应在摘要、站点、README 或 issue 中写成成功。
5. P22 当前公开版本为 `v0.2 / 10.5281/zenodo.20582195`；P41-P45 必须保留各自证据边界。
