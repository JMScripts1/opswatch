from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Ticket, TicketState, utcnow
from app.schemas import TicketOut

router = APIRouter(prefix="/api/v1/tickets", tags=["tickets"])


@router.get("", response_model=list[TicketOut])
def list_tickets(state: TicketState | None = None, db: Session = Depends(get_db)) -> list[Ticket]:
    q = select(Ticket).order_by(Ticket.opened_at.desc())
    if state:
        q = q.where(Ticket.state == state)
    return list(db.scalars(q))


@router.post("/{ticket_id}/resolve", response_model=TicketOut)
def resolve_ticket(ticket_id: int, db: Session = Depends(get_db)) -> Ticket:
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(404, "Ticket not found")
    ticket.state = TicketState.RESOLVED
    ticket.resolved_at = utcnow()
    db.commit()
    return ticket
