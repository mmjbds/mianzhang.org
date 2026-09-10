# Research portal update, 10 September 2026

Source of truth: mmjbds/mianzhang.org main, based on
3eab430c5d594fdec84227f74a7e0149d57e04b0. GitHub Pages API confirms legacy
branch publication from main at /. The large private workspace has no remote;
its older site and release copies were not used to overwrite the current repository.

Scope: existing research pages only. No papers, experiment results, author credentials,
publication status, private artifacts, other sites, DNS or hosting were changed.
Robots, verification files, IndexNow keys, Cloudflare analytics and existing search
notification workflows are retained. HF mirror was not synchronized in this change.

## Requirements and evidence

| Requirement | Pages | Verification |
|---|---|---|
| Reader-facing research introduction | / and /zh/ | concise hero; conceptual illustration identified |
| Question to method and public artifact | /, /zh/, /guides/, /evidence/, /demos/, /technology/ | three linked research paths |
| Code and demo distinction | same paths | ReflexBench orientation receipt is not a benchmark score; proof gate is a demonstration |
| Entity clarity | / and /zh/ | research archive, AI Tool Show and Ouroboros Check distinguished |
| Metadata and canonical URLs | 152 HTML, 150 canonical URLs | existing audit_search_metadata.py and sitemap check |
| Internal navigation and resources | 152 HTML | audit_portal_links.py reports zero missing local targets |
| Responsive reading | 11 priority routes | Edge 1440/1280/390/430; Chrome unavailable on this machine |
| Analytics and public asset constraints | site | existing analytics and asset budget checks |

Official public repositories inspected on 2026-09-10:
- https://github.com/mmjbds/reflexbench : public v2 mirror; 20 scenarios, four levels;
  browser orientation receipt explicitly not automatic scoring.
- https://github.com/mmjbds/wisdombench : longitudinal failure/feedback benchmark.
- https://github.com/mmjbds/proof-carrying-action : public reference interfaces for
  proof-gated action and authority boundaries.
- https://zenodo.org/records/20027295 : existing portfolio archive link retained;
  browser retrieval unavailable during this check. No DOI/title/status changed on that basis.

No new claims of acceptance, independent replication, benchmark performance or commercial
effectiveness were added. Linked repository versions remain the place to inspect the
specific artifact contract. Illustrations are not experiment plots.

## Reproducibility

Static HTML is the publication source. refine_research_portal.py updates bounded existing
sections idempotently; it does not regenerate paper cards. Existing sitemap builder retains
150 routes and updates lastmod only for six substantively changed pages.
Run metadata, sitemap, analytics, local links, reliability, community and asset audits;
then run the 14 existing helper unit tests. Browser checks are in portal_browser.cjs.

## Search and AI outcomes

Construction checks are not indexing, traffic or AI citations. Those outcomes remain unmeasured.
No new subscriptions, sampling services, marketing schedule or manual full-site submission.
Existing push-triggered changed-URL notifications remain enabled; receipts must be read from CI.
Brand questions: “What does Mian Zhang research?” / “Mian Zhang 研究什么？”
Non-brand questions: “How can I inspect repeated-failure learning in an AI agent?” /
“怎样检查 AI 是否从重复失败中学习？”; “What evidence should precede tool execution?” /
“工具执行之前需要什么证据？”
Record language, web/API environment, source links and actual answer separately on future tests.
No causal improvement inferred from this release.

Rollback: revert the scoped publication commit on main; prior Pages source is the baseline SHA above.
