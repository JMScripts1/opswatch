"""OpsWatch agent: run checks on this machine and report them to the server.

    python -m opswatch_agent.cli --config config.yaml --once
    python -m opswatch_agent.cli --config config.yaml            # loop forever
"""

import argparse
import logging
import platform
import socket
import time

import httpx
import yaml

from .runner import run_all

log = logging.getLogger("opswatch.agent")


def report_once(cfg: dict) -> None:
    results = run_all(cfg)
    payload = {
        "hostname": cfg.get("hostname") or socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
        "checks": [r.to_dict() for r in results],
    }
    r = httpx.post(
        f"{cfg['server_url'].rstrip('/')}/api/v1/reports",
        json=payload,
        headers={"X-Agent-Token": cfg["agent_token"]},
        timeout=15,
    )
    r.raise_for_status()
    log.info("Sent %d results: %s", len(results), r.json())


def main() -> None:
    p = argparse.ArgumentParser(description="OpsWatch agent")
    p.add_argument("--config", default="config.yaml")
    p.add_argument("--once", action="store_true", help="run one cycle and exit")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    while True:
        try:
            report_once(cfg)
        except httpx.HTTPError:
            log.exception("Report failed; will retry next cycle")
        if args.once:
            break
        time.sleep(cfg.get("interval_seconds", 300))


if __name__ == "__main__":
    main()
