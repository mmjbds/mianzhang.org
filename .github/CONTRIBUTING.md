# Contributing Guide

This project accepts public, evidence-focused contributions only.

## Useful Contributions

- Challenge a public claim that is too broad, ambiguous, unsupported, or contradicted by public evidence.
- Report a reproduction failure for a public artifact, demo, schema, paper card, registry row, or README path.
- Identify an evidence gap where a public claim needs a stronger receipt, provenance link, or boundary statement.
- Propose a stronger baseline or fairer comparison protocol.
- Improve public documentation, links, claim boundaries, issue templates, or safe public examples.

## Do Not Submit

- API keys, tokens, passwords, private configuration, or credentials.
- Customer data, private logs, private agent orchestration, private execution traces, real account records, or real transaction records.
- Confidential review material, private reviewer pages, email screenshots, de-anonymizing information, or venue-specific non-public files.
- Exploit chains, attack steps against real systems, or material that expands practical harm.
- Marketing copy that is not tied to public evidence, a DOI record, a GitHub route, a Hugging Face route, or a claim boundary.

## Issue Routes

- Claim challenge: use the `challenge_claim.yml` template.
- Reproduction failure: use the `reproduction_failure.yml` template.
- Evidence gap: use the `evidence_gap.yml` template.
- Baseline challenge: use the `baseline_challenge.yml` template.
- Security-sensitive material: do not open a public issue. Follow `SECURITY.md`.

## Pull Request Checklist

Before opening a PR, confirm that:

- Every changed claim points to a public DOI, public page, public registry row, public code path, or explicit boundary statement.
- The change does not introduce secrets, private logs, customer data, local absolute paths, temporary artifacts, or private review material.
- Reproduction steps use public data, synthetic data, or sanitized examples only.
- If a claim is weakened, narrowed, downgraded, or marked unresolved, the status change is visible in the relevant page or registry.
- Links are checkable from the public site, GitHub, Hugging Face mirror, or Zenodo record.

## Public Cross-links

- Main site: https://mianzhang.org/
- GitHub source: https://github.com/mmjbds/mianzhang.org
- Hugging Face technical mirror: https://mmjbds-mianzhang-org.static.hf.space/
- Hugging Face Space: https://huggingface.co/spaces/MMJBDS/mianzhang-org
- Zenodo portfolio: https://zenodo.org/records/20027295
