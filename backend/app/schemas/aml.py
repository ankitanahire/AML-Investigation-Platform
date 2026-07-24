from datetime import datetime
from pydantic import BaseModel


class AMLAlertResponse(BaseModel):
    id: int
    account_id: int
    transaction_id: int | None
    rule_triggered: str
    severity: str
    status: str
    remarks: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class AMLStatusUpdate(BaseModel):
    status: str


class SuspiciousAccount(BaseModel):
    account_id: int
    alerts: int


class AMLDashboard(BaseModel):
    total_alerts: int
    open_alerts: int
    resolved_alerts: int
    high_risk: int
    critical: int
    top_suspicious_accounts: list[SuspiciousAccount]