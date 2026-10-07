from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import CheckResult, Host, utcnow
from app.schemas import ReportIn, ReportOut
from app.services import notifier
from app.services.rules import apply_rules

router = APIRouter(prefix="/api/v1", tags=["agent"])


def require_agent_token(x_agent_token: str = Header(...)) -> None:
    if x_agent_token != settings.agent_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid agent token")


@router.post("/reports", response_model=ReportOut, dependencies=[Depends(require_agent_token)])
def submit_report(payload: ReportIn, db: Session = Depends(get_db)) -> ReportOut:
    host = db.scalars(select(Host).where(Host.hostname == payload.hostname)).first()
    if host is None:
        host = Host(hostname=payload.hostname, os=payload.os)
        db.add(host)
        db.flush()
    host.os = payload.os
    host.last_seen = utcnow()

    for c in payload.checks:
        db.add(CheckResult(host_id=host.id, check_name=c.name, status=c.status, message=c.message))

    outcome = apply_rules(db, host, payload.checks)
    db.commit()

    for t in outcome.opened:
        notifier.send(f"Opened #{t.id}: {t.title} - {t.details}")
    for t in outcome.resolved:
        notifier.send(f"Resolved #{t.id}: {t.title}")

    return ReportOut(
        host_id=host.id,
        opened=[t.id for t in outcome.opened],
        resolved=[t.id for t in outcome.resolved],
    )
