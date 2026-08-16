# Mian Zhang | Ouroboros Project: Evidence-Gated AI Systems

This is the public static website package for `mianzhang.org`.

## Latest Research Feature

- KDD 2026 two workshop papers: https://mianzhang.org/press/kdd-2026-two-workshop-papers.html
- Chinese feature: https://mianzhang.org/zh/kdd-2026-two-workshop-papers/
- Papers and machine-readable facts: https://mianzhang.org/papers/kdd-2026/

## Latest Daily Note

- Active Compute Cost Sheet v1: https://mianzhang.org/press/public-launch-2026-07-24.html

## Cross-links

- Main site: https://mianzhang.org/
- GitHub source: https://github.com/mmjbds/mianzhang.org
- GitHub issues: https://github.com/mmjbds/mianzhang.org/issues
- GitHub discussions: https://github.com/mmjbds/mianzhang.org/discussions
- Hugging Face technical mirror: https://mmjbds-mianzhang-org.static.hf.space/
- Hugging Face Space repository: https://huggingface.co/spaces/MMJBDS/mianzhang-org
- Zenodo portfolio index: https://zenodo.org/records/20027295
- LLM retrieval file: https://mianzhang.org/llms.txt
- XML sitemap: https://mianzhang.org/sitemap.xml
- Search discovery entry: https://mianzhang.org/docs/search-discovery-2026-06-15.html
- Public completion audit: https://mianzhang.org/docs/public-completion-audit-2026-06-15.html

## Public Routes

- Papers and DOI map: `papers/index.html`
- Per-paper public cards: `papers/public_index/*.md`
- Evidence map: `evidence/index.html`
- Concepts: `concepts/index.html`
- Counterexamples: `counterexamples/index.html`
- Community route: `community/index.html`
- Chinese community route: `zh/community/index.html`
- Community guide: `COMMUNITY.md`
- Open-source boundary: `OPEN_SOURCE_BOUNDARY.md`
- Public roadmap: `docs/public-roadmap.html`
- Weekly digest: `docs/weekly-digest-2026-06-15.html`
- Public completion audit: `docs/public-completion-audit-2026-06-15.html`

## Platform Roles

- Zenodo is the canonical DOI archive for public papers and files.
- GitHub is the community layer for source, issue templates, reproduction reports, baseline challenges, and evidence-gap reports.
- Hugging Face is the technical static mirror for demos, registries, boundaries, and artifact pages.
- `mianzhang.org/zh/` is the canonical Chinese-language entry.

## Search Notification Utilities

Search notification helpers are kept under `scripts/` and never contain account credentials. `submit_indexnow.py` uses the public root key file; `submit_baidu.py` reads the Baidu credential from the `BAIDU_PUSH_TOKEN` environment variable.

```powershell
$env:BAIDU_PUSH_TOKEN="<set-locally>"
python scripts/submit_baidu.py `
  --url-list docs/baidu-url-list-initial-20260817.txt `
  --site https://mianzhang.org `
  --receipt docs/baidu-submission-receipt-local.json `
  --dry-run
```

Remove `--dry-run` only after the URL list has been reviewed. API acceptance is a submission receipt, not evidence of crawling, indexing, ranking, traffic, or AI retrieval. Never commit the token or a command containing its value.

## Boundary

This public site is a research and evidence index. Use Zenodo DOI records for citation authority and GitHub issues for public challenges. Do not place restricted non-public material, customer data, credentials, private logs, real account records, or non-public execution traces in the public layer.

## Open-Source Scope

Source code intentionally released by this repository is available under Apache-2.0 unless a file or directory states otherwise. Papers, datasets, photographs, logos, and third-party material retain their item-specific rights. An accessible URL does not automatically relicense non-code content.

- License: [LICENSE](LICENSE)
- Content and media terms: [CONTENT_AND_MEDIA_LICENSE.md](CONTENT_AND_MEDIA_LICENSE.md)
- Public/private release boundary: [OPEN_SOURCE_BOUNDARY.md](OPEN_SOURCE_BOUNDARY.md)
- Contribution routes: [COMMUNITY.md](COMMUNITY.md) and [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)
