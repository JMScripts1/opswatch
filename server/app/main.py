import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from app.config import settings
from app.db import Base, SessionLocal, engine
from app.routers import hosts, reports, tickets
from app.services import notifier
from app.services.report import build_daily_report

logging.basicConfig(level=logging.INFO)


def send_daily_report() -> None:
    with SessionLocal() as db:
        notifier.send(build_daily_report(db))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO(milestone 2): replace create_all with Alembic migrations
    Base.metadata.create_all(engine)
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_report, "cron", hour=settings.report_hour)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title="OpsWatch", version="0.1.0", lifespan=lifespan)
app.include_router(reports.router)
app.include_router(hosts.router)
app.include_router(tickets.router)


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok"}
