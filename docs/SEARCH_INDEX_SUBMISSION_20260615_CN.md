# Search Index Submission Pack - 2026-06-15

状态：`READY_FOR_ACCOUNT_SUBMISSION`

用途：记录 mianzhang.org 和 HF 技术镜像的搜索引擎 / AI 抓取入口。本文档不替代 Search Console 或 Bing Webmaster 的账号内提交回执；账号内动作完成后，把回执截图、时间和结果补回本文件。

## 1. 权威站点

| 入口 | URL | 用途 |
|---|---|---|
| 主站首页 | https://mianzhang.org/ | 公开统一入口 |
| 主站 sitemap | https://mianzhang.org/sitemap.xml | Google / Bing sitemap 提交 |
| 主站 llms | https://mianzhang.org/llms.txt | LLM / RAG 抓取入口 |
| 主站 concepts | https://mianzhang.org/concepts/ | 唯一术语入口 |
| 主站 papers | https://mianzhang.org/papers/ | 论文与 DOI 入口 |
| 主站 evidence | https://mianzhang.org/evidence/ | 证据边界入口 |
| 主站 press | https://mianzhang.org/press/ | 日更公开入口 |
| 主站中文 | https://mianzhang.org/zh/ | 中文解释入口 |

## 2. HF 技术镜像

| 入口 | URL | 用途 |
|---|---|---|
| HF 静态镜像 | https://mmjbds-mianzhang-org.static.hf.space/index.html | 技术证据镜像 |
| HF sitemap | https://mmjbds-mianzhang-org.static.hf.space/sitemap.xml | 镜像 sitemap |
| HF llms | https://mmjbds-mianzhang-org.static.hf.space/llms.txt | 技术镜像 LLM 入口 |
| HF concepts | https://mmjbds-mianzhang-org.static.hf.space/concepts/index.html | 技术术语入口 |

## 3. URL Inspection 队列

第一批逐个请求索引：

1. https://mianzhang.org/
2. https://mianzhang.org/llms.txt
3. https://mianzhang.org/sitemap.xml
4. https://mianzhang.org/concepts/
5. https://mianzhang.org/concepts/wisdombench.html
6. https://mianzhang.org/concepts/proof-carrying-action.html
7. https://mianzhang.org/concepts/no-proof-no-action-gate.html
8. https://mianzhang.org/concepts/grounding-canon.html
9. https://mianzhang.org/papers/
10. https://mianzhang.org/evidence/
11. https://mianzhang.org/press/
12. https://mianzhang.org/press/public-launch-2026-06-14.html
13. https://mianzhang.org/PUBLIC_EVIDENCE_FIELD_MANIFEST_20260527.json

第二批请求索引：

1. https://mmjbds-mianzhang-org.static.hf.space/index.html
2. https://mmjbds-mianzhang-org.static.hf.space/llms.txt
3. https://mmjbds-mianzhang-org.static.hf.space/sitemap.xml
4. https://mmjbds-mianzhang-org.static.hf.space/concepts/index.html
5. https://mmjbds-mianzhang-org.static.hf.space/press/public-launch-2026-06-14.html

## 4. 提交流程

Google Search Console：

1. 确认 property 为 `https://mianzhang.org/` 或 domain property `mianzhang.org`。
2. 验证根目录文件：`google9c7439a09f492752.html`、`googlee95cf06405c388af.html`。
3. 提交 sitemap：`https://mianzhang.org/sitemap.xml`。
4. 用 URL Inspection 请求上面的第一批 URL。
5. 记录每个 URL 的状态：`Discovered` / `Crawled` / `Indexed` / `Excluded`。

Bing Webmaster：

1. 添加 `https://mianzhang.org/`。
2. 如需 Bing 文件验证，新增 `BingSiteAuth.xml` 后再提交；不要伪造验证码。
3. 提交 sitemap：`https://mianzhang.org/sitemap.xml`。
4. 使用 URL Submission 提交第一批 URL。
5. 记录提交时间和返回状态。

## 5. 回执记录表

| 日期 | 平台 | URL | 动作 | 结果 | 证据 |
|---|---|---|---|---|---|
| 2026-06-15 | Google | https://mianzhang.org/sitemap.xml | 待账号提交 | `PENDING_ACCOUNT_ACTION` | 待补截图 |
| 2026-06-15 | Bing | https://mianzhang.org/sitemap.xml | 待账号提交 | `PENDING_ACCOUNT_ACTION` | 待补截图 |

## 6. 检索复查词

每周复查以下查询，记录真实结果，不用主观猜测：

- `site:mianzhang.org`
- `site:mianzhang.org WisdomBench`
- `site:mianzhang.org "No-Proof No-Action Gate"`
- `site:mianzhang.org "Proof-Carrying Action"`
- `site:mianzhang.org "The Grounding Canon"`
- `"mianzhang.org" "WisdomBench"`
- `"Mian Zhang" "Ouroboros Project"`
- `"Grounding Canon" "Mian Zhang"`
- `"Proof-Carrying Action" "Mian Zhang"`

## 7. 不应声称

- 不要声称“已被 Google/Bing 收录”，除非 Search Console / Bing Webmaster 或公开搜索结果已经确认。
- 不要声称“模型已经能检索到”，除非具体模型、具体日期、具体查询有记录。
- 不要把 HF 上传成功写成主站收录成功。
- 不要把 DOI 存在写成搜索可见。
