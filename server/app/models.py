from datetime import UTC, datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class Status(StrEnum):
    OK = "ok"
    WARN = "warn"
    CRIT = "crit"


class TicketState(StrEnum):
    OPEN = "open"
    RESOLVED = "resolved"


class Host(Base):
    __tablename__ = "hosts"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostname: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    os: Mapped[str] = mapped_column(String(100), default="unknown")
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    results: Mapped[list["CheckResult"]] = relationship(back_populates="host")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="host")


class CheckResult(Base):
    __tablename__ = "check_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id"), index=True)
    check_name: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[Status] = mapped_column(Enum(Status))
    message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    host: Mapped[Host] = relationship(back_populates="results")


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id"), index=True)
    check_name: Mapped[str] = mapped_column(String(100))
    severity: Mapped[Status] = mapped_column(Enum(Status))
    state: Mapped[TicketState] = mapped_column(Enum(TicketState), default=TicketState.OPEN)
    title: Mapped[str] = mapped_column(String(255))
    details: Mapped[str] = mapped_column(Text, default="")
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    host: Mapped[Host] = relationship(back_populates="tickets")
