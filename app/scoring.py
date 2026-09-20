from datetime import datetime, timezone
from .models import Classification, EmailRecord

# Conservative, deterministic baseline. Replace enrichment calls with SPF/DKIM/DMARC,
# reputation, and LLM structured outputs in the worker layer.
SUSPICIOUS_TERMS = ("password reset", "verify your account", "wire transfer", "claim prize")
PROMOTION_TERMS = ("unsubscribe", "sale", "% off", "promotion", "newsletter")
IMPORTANT_TERMS = ("urgent", "deadline", "invoice", "contract", "meeting", "approval", "interview")


def score_email(sender: str, subject: str, body: str) -> EmailRecord:
    text = f"{subject} {body}".lower()
    domain = sender.rsplit("@", 1)[-1].lower() if "@" in sender else ""
    suspicious = any(term in text for term in SUSPICIOUS_TERMS)
    promotion = any(term in text for term in PROMOTION_TERMS)
    important_hits = sum(term in text for term in IMPORTANT_TERMS)

    if suspicious:
        classification, trust, importance, reason = Classification.SUSPICIOUS, 15, 80, "Suspicious security or financial language detected."
    elif promotion and important_hits == 0:
        classification, trust, importance, reason = Classification.PROMOTION, 75, 10, "Likely bulk marketing or promotional mail."
    elif important_hits:
        classification, trust, importance, reason = Classification.IMPORTANT, 85, min(40 + important_hits * 15, 100), "Action, deadline, or business-priority language detected."
    else:
        classification, trust, importance, reason = Classification.GENUINE, 70, 25, "No high-risk indicators detected."

    return EmailRecord(id=f"demo-{abs(hash(sender + subject))}", sender=sender,
        subject=subject, preview=body[:180], received_at=datetime.now(timezone.utc),
        trust_score=trust, importance_score=importance, classification=classification,
        reason=reason, requires_approval=True)
