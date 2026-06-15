# Security Policy

## Public Issues Are Not For Sensitive Reports

Do not open a public GitHub issue if the report includes or requires any of the following:

- API keys, tokens, passwords, private configuration, or credentials.
- Customer data, private logs, internal execution traces, private prompts, private agent orchestration, or local caches.
- Real trading accounts, real transaction records, proprietary account exports, or account-specific operational data.
- Restricted non-public material, private correspondence, non-public versions, or de-anonymizing information.
- Exploit chains, bypass steps, proof-of-exploit details, or instructions that can be directly used to attack a real system.

Public issues are appropriate for security-boundary wording questions only when the discussion can stay at the level of public files, public documentation, public demos, and public registry rows.

## Private Reporting

If you believe you found a vulnerability or sensitive exposure, email `373743743@qq.com` before sharing details publicly. Include only the minimum information needed to begin triage:

- A short description of the affected public component or boundary.
- The impact category, without posting secrets or customer material.
- Whether the issue is already public anywhere else.
- A safe way for maintainers to request more details privately.

Do not attach API keys, credentials, private logs, account exports, exploit chains, restricted non-public material, or de-anonymizing screenshots in the first email. The first message should be enough to route the issue without expanding exposure.

## Evidence Handling

The project follows a local-first and public-evidence boundary. Maintainers will not ask for private customer data, private logs, real trading account exports, credentials, or restricted non-public material in a public thread.

If a public reproduction is needed, use synthetic data, public datasets, sanitized samples, or high-level redacted descriptions that cannot identify customers, accounts, private infrastructure, or third parties.

## Coordinated Disclosure

Please give maintainers a reasonable opportunity to investigate before publishing vulnerability details. Public documentation fixes, claim-boundary clarifications, and evidence-gap reports can proceed through the normal issue templates when they do not contain sensitive material.
