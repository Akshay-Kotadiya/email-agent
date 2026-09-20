from datetime import datetime
from enum import StrEnum
from typing import Optional
from pydantic import BaseModel, Field

class Classification(StrEnum):
    GENUINE = "genuine"
    IMPORTANT = "important"
    PROMOTION = "promotion"
    SUSPICIOUS = "suspicious"
    REVIEW = "review"

class EmailRecord(BaseModel):
    id: str
    sender: str
    subject: str
    preview: str
    received_at: datetime
    trust_score: int = Field(ge=0, le=100)
    importance_score: int = Field(ge=0, le=100)
    classification: Classification
    reason: Optional[str] = None
    reply_draft: Optional[str] = None
    requires_approval: bool = True
    notification_sent: bool = False

class ApprovalRequest(BaseModel):
    draft: str = Field(min_length=1)

class Settings(BaseModel):
    auto_trash_promotions: bool = False
    promotion_retention_days: int = Field(default=30, ge=1, le=365)
