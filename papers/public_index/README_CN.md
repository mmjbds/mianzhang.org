# 公开论文索引层 - 2026-06-15

本目录维护 GitHub、mianzhang.org 和 Hugging Face 技术镜像共用的公开论文索引。这里记录 DOI、版本、公开状态、证据等级和边界说明，方便读者、搜索引擎和复现者按同一套公开记录检索。

## 平台分工

- Zenodo：论文、数据和证据包的 DOI 归档与引用权威。
- GitHub：公开索引、manifest、边界说明、issue、PR 和反例挑战入口。
- Hugging Face：技术镜像、demo、registry 和 artifact 页面。
- mianzhang.org：统一公共入口、中文入口、站点导航和读者解释层。

## 文件

- `../../public_registry/paper_index_20260608.jsonl`：机器可读 JSONL，每行一条公开论文记录。
- `paper_index_20260608.csv`：表格版公开索引。
- `PAPER_ARCHIVE_POLICY_CN.md`：GitHub 是否镜像 PDF 的规则。
- `P*.md`：单篇论文公开卡片，包含 DOI、GitHub、HF、证据等级、当前状态和挑战入口。

## 规则

1. 已有 DOI 的论文，以 Zenodo DOI landing page 作为引用权威。
2. GitHub 默认保存元数据、边界说明和公开挑战入口；PDF 是否镜像按归档策略执行。
3. 非公开版本、私有日志、客户数据、真实账号记录、交易接口和机器人执行接口不进入公开索引。
4. `NOT_DEMONSTRATED`、`NO_CREDIT_RECEIPT`、`CANDIDATE_NOT_COMPLETED` 不能在摘要、站点、README 或 issue 中写成成功。
5. P22 当前公开版本为 `v0.2 / 10.5281/zenodo.20582195`；P41-P47 必须保留各自证据边界。
6. P46/P47 是 P45 之后新增的公开 DOI 记录。它们可以进入公开索引，但不得被写成真实机器人部署、第三方复现、外部标准采纳或无边界的系统成功。
