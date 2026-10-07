from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import Status, TicketState


class CheckIn(BaseModel):
    name: str
    status: Status
    message: str = ""


class ReportIn(BaseModel):
    """Payload an agent POSTs after running its checks."""

    hostname: str
    os: str = "unknown"
    checks: list[CheckIn]


class ReportOut(BaseModel):
    host_id: int
    opened: list[int]
    resolved: list[int]


class HostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    hostname: str
    os: str
    last_seen: datetime


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    host_id: int
    check_name: str
    severity: Status
    state: TicketState
    title: str
    details: str
    opened_at: datetime
    resolved_at: datetime | None
