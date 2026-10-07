"""Send alerts to a Discord/Slack-compatible incoming webhook."""

import logging

import httpx

from app.config import settings

log = logging.getLogger(__name__)


def send(text: str) -> bool:
    if not settings.webhook_url:
        log.info("No WEBHOOK_URL set; would have sent: %s", text)
        return False
    try:
        # "content" is Discord's field, "text" is Slack's; sending both works for either.
        r = httpx.post(settings.webhook_url, json={"content": text, "text": text}, timeout=10)
        r.raise_for_status()
        return True
    except httpx.HTTPError:
        log.exception("Webhook delivery failed")
        return False
