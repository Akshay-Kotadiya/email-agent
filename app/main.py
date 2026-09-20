from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from .models import ApprovalRequest
from .scoring import score_email

app = FastAPI(title="Email Agent", version="0.1.0")

# Demo queue; production replaces this with PostgreSQL + Gmail sync worker.
queue = [score_email("client@example.com", "Urgent: contract approval", "Please review the contract before the deadline."),
         score_email("offers@shop.example", "50% off this week", "Sale ends soon. Unsubscribe if you do not want these emails."),
         score_email("security@example.com", "Verify your account", "Click here to reset your password immediately.")]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/emails")
def emails():
    return {"items": queue}

@app.post("/api/emails/{email_id}/draft")
def draft(email_id: str):
    email = next((item for item in queue if item.id == email_id), None)
    if not email:
        raise HTTPException(404, "Email not found")
    if email.classification.value == "suspicious":
        raise HTTPException(422, "Suspicious email cannot receive an automatic reply")
    email.reply_draft = f"Hello,\n\nThank you for your message regarding {email.subject!r}. I have received it and will review the requested next steps.\n\nBest regards,\n[Your name]"
    return email

@app.post("/api/emails/{email_id}/approve")
def approve(email_id: str, request: ApprovalRequest):
    email = next((item for item in queue if item.id == email_id), None)
    if not email:
        raise HTTPException(404, "Email not found")
    if email.classification.value == "suspicious":
        raise HTTPException(422, "Suspicious email cannot be sent")
    # Production: enqueue Gmail send after a second confirmation and write audit event.
    email.reply_draft = request.draft
    email.requires_approval = False
    return {"status": "approved_for_send", "message": "Queued for Gmail send worker after authorization."}

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return HTMLResponse(open("app/dashboard.html").read())
