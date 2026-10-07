"""Ticketing rules: turn check results into ticket opens/resolves.

Rules (keep these in sync with the README):
  * non-OK result and no open ticket for (host, check)  -> open a ticket
  * non-OK result and an open ticket exists             -> update it, escalate severity if worse
  * OK result and an open ticket exists                 -> auto-resolve it
This de-duplicates alerts: one ongoing problem = one ticket, not one per check run.
"""

from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Host, Status, Ticket, TicketState, utcnow
from app.schemas import CheckIn

_SEVERITY_RANK = {Status.OK: 0, Status.WARN: 1, Status.CRIT: 2}


@dataclass
class RuleOutcome:
    opened: list[Ticket] = field(default_factory=list)
    resolved: list[Ticket] = field(default_factory=list)


def apply_rules(db: Session, host: Host, checks: list[CheckIn]) -> RuleOutcome:
    outcome = RuleOutcome()
    for check in checks:
        open_ticket = db.scalars(
            select(Ticket).where(
                Ticket.host_id == host.id,
                Ticket.check_name == check.name,
                Ticket.state == TicketState.OPEN,
            )
        ).first()

        if check.status == Status.OK:
            if open_ticket:
                open_ticket.state = TicketState.RESOLVED
                open_ticket.resolved_at = utcnow()
                outcome.resolved.append(open_ticket)
            continue

        if open_ticket:
            open_ticket.details = check.message
            if _SEVERITY_RANK[check.status] > _SEVERITY_RANK[open_ticket.severity]:
                open_ticket.severity = check.status
            continue

        ticket = Ticket(
            host_id=host.id,
            check_name=check.name,
            severity=check.status,
            title=f"[{check.status.upper()}] {check.name} on {host.hostname}",
            details=check.message,
        )
        db.add(ticket)
        outcome.opened.append(ticket)

    db.flush()
    return outcome
