# 贡献边界

## 优先接受

- 公开链接修正：GitHub、Zenodo、Hugging Face、DOI、自有站和中文区入口。
- 公开证据修正：registry、manifest、claim-to-evidence table、artifact scope、README。
- 反例与复现：最小公开输入、合成样例、公开数据、可运行命令和观察结果。
- 边界文本：claim boundary、counterexample boundary、no-go、stop rule、证据等级说明。
- 社区流程：issue template、PR template、贡献指南、安全政策和支持边界。

## 必须拒绝

- 密钥、token、密码、私有配置或任何凭证。
- 客户数据、真实交易日志、私有执行链、私有 agent 编排、商业调度器。
- 会议匿名包、审稿私有页面、邮件截图、未公开投稿材料或去匿名化信息。
- 未授权安全测试、攻击链、绕过步骤、武器化 exploit 或第三方系统攻击说明。
- 官网叙事、中文长文搬运、投资人叙事、销售材料或不可复核宣传。

## Claim 写法

公开 claim 必须至少具备以下一种支撑：

- 公开论文、公开 DOI 或公开数据入口。
- 可复核 registry、manifest、schema 或 claim-to-evidence 表。
- 最小 demo、合成样例或公开复现命令。
- 明确反证条件、适用范围或 no-go 边界。

没有证据入口的说法应降为背景说明；无法公开验证且涉及私有执行质量的说法不应进入公开仓库。

## PR 最小要求

- 修改范围与目标一致，不混入无关重构。
- 文档标题层级清楚，中文 UTF-8，无乱码。
- 链接使用稳定公开入口，避免临时本地路径。
- 对敏感或安全问题只写公开安全摘要，不公开利用细节。
