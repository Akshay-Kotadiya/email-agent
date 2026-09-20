# Email Agent

Production-oriented Gmail assistant with trust scoring, AI reply drafts, approvals, notifications, and safe promotion cleanup.

## Safety defaults

- Never sends a reply without explicit approval.
- Suspicious messages are flagged and never answered.
- Promotions are moved to Trash only when enabled; permanent deletion is disabled by default.
- Financial, legal, security, and password-related mail always requires review.

## Quick start

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000. Gmail OAuth and AI integrations are intentionally configured through environment variables; never commit credentials.

## Planned production integrations

- Gmail API with least-privilege OAuth scopes
- PostgreSQL persistence and Redis/Celery processing
- SPF/DKIM/DMARC and link reputation enrichment
- OpenAI structured classification and reply drafts
- Web Push/Slack notifications

See `docs/architecture.md` for the design and deployment boundaries.
