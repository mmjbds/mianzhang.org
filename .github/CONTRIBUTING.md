# Contributing Guide

Contributions should make a public artifact easier to understand, use, inspect, compare, or extend. A contribution does not need to begin as a challenge.

## Start Here

- Use [GitHub Discussions](https://github.com/mmjbds/mianzhang.org/discussions) for questions, research extensions, use cases, and work you have built.
- Use the [public artifact improvement form](https://github.com/mmjbds/mianzhang.org/issues/new?template=public_artifact_improvement.yml) for scoped documentation, examples, fixtures, metadata, or interoperability repairs.
- Use advanced Issue routes when a claim, result, baseline, or reproduction path needs formal review.
- Read [COMMUNITY.md](../COMMUNITY.md) and [OPEN_SOURCE_BOUNDARY.md](../OPEN_SOURCE_BOUNDARY.md) before sharing implementation details or data.

## Useful Contributions

- Ask a concrete question about a public paper, method, benchmark, or interface.
- Describe a real use case without confidential or identifying data.
- Improve documentation, navigation, citations, metadata, safe examples, or small synthetic fixtures.
- Add a public baseline, experiment, adapter, validator, or interoperability test.
- Challenge a public claim that is too broad, ambiguous, unsupported, or contradicted by public evidence.
- Report a minimal public counterexample, reproduction failure, evidence gap, or comparison that changes interpretation.

## First Contribution Paths

**No code:** correct a link or citation, clarify a concept, describe a use case, or identify an onboarding gap.

**Light code:** add a safe fixture, parser example, schema check, documentation test, or minimal adapter.

**Full experiment:** publish the question, protocol, versions, data rights, result, limitations, and a route others can inspect.

## Do Not Submit

- API keys, tokens, passwords, credentials, private configuration, or local absolute paths.
- Customer data, private logs, private prompts, private orchestration, production traces, real account records, or commercial terms.
- Exact production weights, thresholds, routing logic, tuning history, private evaluation rubrics, or unpublished training data.
- Restricted non-public material, private correspondence, unreleased papers, or de-anonymizing information.
- Exploit chains or attack instructions against real systems.

If a useful contribution depends on excluded material, reduce it to a public interface, synthetic fixture, or non-confidential problem statement. Do not upload the excluded material.

## Advanced Issue Routes

- [Claim challenge](https://github.com/mmjbds/mianzhang.org/issues/new?template=challenge_claim.yml)
- [Counterexample](https://github.com/mmjbds/mianzhang.org/issues/new?template=counterexample.yml)
- [Reproduction failure](https://github.com/mmjbds/mianzhang.org/issues/new?template=reproduction_failure.yml)
- [Evidence gap](https://github.com/mmjbds/mianzhang.org/issues/new?template=evidence_gap.yml)
- [Baseline challenge](https://github.com/mmjbds/mianzhang.org/issues/new?template=baseline_challenge.yml)
- [Documentation boundary](https://github.com/mmjbds/mianzhang.org/issues/new?template=documentation_boundary.yml)
- [Security boundary](https://github.com/mmjbds/mianzhang.org/issues/new?template=security_boundary.yml)

## Pull Request Requirements

- Keep the change narrow and explain the public problem it solves.
- Identify the artifact, version, and public source for factual or scientific claims.
- State the claim boundary and limitations when adding a result or evaluation.
- Use public, synthetic, or properly licensed data only.
- Confirm that no secret, private path, customer material, account record, or restricted implementation is present.
- Run the checks listed in the pull request template.

Accepted contributions are credited through commit history and release notes. Paper authorship follows substantial scholarly contribution and publication requirements; it is not promised for ordinary community participation.

## Public Routes

- Community: https://mianzhang.org/community/
- GitHub: https://github.com/mmjbds/mianzhang.org
- Hugging Face: https://huggingface.co/MMJBDS
- Zenodo portfolio: https://zenodo.org/records/20027295
