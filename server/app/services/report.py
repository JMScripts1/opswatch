"""Build the daily summary of open tickets."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Status, Ticket, TicketState


def build_daily_report(db: Session) -> str:
    tickets = db.scalars(select(Ticket).where(Ticket.state == TicketState.OPEN)).all()
    if not tickets:
        return "OpsWatch daily report: all systems healthy."

    crit = [t for t in tickets if t.severity == Status.CRIT]
    warn = [t for t in tickets if t.severity == Status.WARN]
    lines = [f"OpsWatch daily report: {len(crit)} critical, {len(warn)} warning"]
    for t in crit + warn:
        lines.append(f"  #{t.id} {t.title}: {t.details}")
    return "\n".join(lines)
