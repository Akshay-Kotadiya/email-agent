# Architecture

## Pipeline

1. Gmail OAuth obtains least-privilege access (`gmail.readonly` for sync; add `gmail.modify` only for labels/trash and `gmail.send` only for approved sends).
2. A webhook/polling worker stores normalized messages and immutable audit events.
3. Authentication evidence is collected from Gmail headers and external reputation providers. A conservative rules engine and an LLM using a strict JSON schema produce trust, importance, category, indicators, and action items.
4. Suspicious messages are quarantined/labelled and cannot enter the send queue. Promotions are labelled and optionally moved to Trash; permanent deletion requires an explicit retention job and setting.
5. Important genuine messages generate a Web Push notification. Reply drafts are shown in the dashboard and require an explicit approval action.
6. A send worker re-checks classification, approval, recipient, and idempotency before Gmail send; all actions are audited.

## Production controls

- Encrypt OAuth refresh tokens at rest; use a secret manager.
- Add CSRF protection, authenticated sessions, rate limiting, tenant isolation, and signed webhook verification.
- Never trust the model as the sole phishing detector. Treat low confidence and sensitive categories as manual review.
- Add PostgreSQL migrations, Redis queue retries/dead-letter handling, observability, and automated tests before deployment.
