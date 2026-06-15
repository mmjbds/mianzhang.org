# Contributing Guide

This project accepts public, evidence-focused contributions only.

## Useful Contributions

- Challenge a public claim that is too broad, ambiguous, unsupported, or contradicted by public evidence.
- Report a minimal public counterexample that falsifies or narrows a specific claim.
- Report a reproduction failure for a public artifact, demo, schema, paper card, registry row, or README path.
- Identify an evidence gap where a public claim needs a stronger receipt, provenance link, or boundary statement.
- Propose a stronger baseline or fairer comparison protocol.
- Improve public documentation, links, claim boundaries, issue templates, or safe public examples.

## Do Not Submit

- API keys, tokens, passwords, private configuration, or credentials.
- Customer data, private logs, private agent orchestration, private execution traces, real account records, or real transaction records.
- Restricted non-public material, private correspondence, non-public versions, or de-anonymizing information.
- Exploit chains, attack steps against real systems, or material that expands practical harm.
- Marketing copy that is not tied to public evidence, a DOI record, a GitHub route, a Hugging Face route, or a claim boundary.

## Issue Routes

- [Claim challenge](https://github.com/mmjbds/mianzhang.org/issues/new?template=challenge_claim.yml): use when the wording, scope, contradiction, or interpretation of a public claim is the main issue.
- [Counterexample](https://github.com/mmjbds/mianzhang.org/issues/new?template=counterexample.yml): use when you have a minimal public case that falsifies or narrows a specific claim.
- [Reproduction failure](https://github.com/mmjbds/mianzhang.org/issues/new?template=reproduction_failure.yml): use when a public artifact, command, demo, schema, or paper card cannot be reproduced.
- [Evidence gap](https://github.com/mmjbds/mianzhang.org/issues/new?template=evidence_gap.yml): use when the claim may be reasonable but the public receipt, provenance, registry link, or evidence grade is missing or unclear.
- [Baseline challenge](https://github.com/mmjbds/mianzhang.org/issues/new?template=baseline_challenge.yml): use when a stronger, simpler, fairer, or better documented baseline changes the interpretation.
- [Documentation boundary](https://github.com/mmjbds/mianzhang.org/issues/new?template=documentation_boundary.yml): use for public documentation wording, route, or link fixes.
- [Security boundary](https://github.com/mmjbds/mianzhang.org/issues/new?template=security_boundary.yml): use only for public security-boundary wording. Sensitive reports must follow [SECURITY.md](https://github.com/mmjbds/mianzhang.org/blob/main/.github/SECURITY.md).

## Decision Rule

If the public sentence itself is too broad, file a claim challenge. If a concrete public case breaks it, file a counterexample. If a public artifact fails to run, file a reproduction failure. If the claim needs a missing receipt or provenance link, file an evidence gap. If another public method changes the comparison, file a baseline challenge.

## Pull Request Checklist

Before opening a PR, confirm that:

- Every changed claim points to a public DOI, public page, public registry row, public code path, or explicit boundary statement.
- The change does not introduce secrets, private logs, customer data, local absolute paths, temporary artifacts, real account records, or restricted non-public material.
- Reproduction steps use public data, synthetic data, or sanitized examples only.
- If a claim is weakened, narrowed, downgraded, or marked unresolved, the status change is visible in the relevant page or registry.
- Links are checkable from the public site, GitHub, Hugging Face mirror, or Zenodo record.

## Public Cross-links

- Main site: https://mianzhang.org/
- GitHub source: https://github.com/mmjbds/mianzhang.org
- Hugging Face technical mirror: https://mmjbds-mianzhang-org.static.hf.space/
- Hugging Face Space: https://huggingface.co/spaces/MMJBDS/mianzhang-org
- Zenodo portfolio: https://zenodo.org/records/20027295
- Public completion audit: https://mianzhang.org/docs/public-completion-audit-2026-06-15.html
- Search discovery report: https://mianzhang.org/docs/search-discovery-2026-06-15.html
- Search weekly report JSON: https://mianzhang.org/docs/search-index-weekly-report-2026-06-15.json
