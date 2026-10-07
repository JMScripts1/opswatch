"""Send fake reports from several 'machines' so the dashboard has data to show.

Usage: python scripts/seed_demo.py --url http://localhost:8000 --token change-me-too
"""

import argparse
import random

import httpx

HOSTS = ["reception-pc", "accounting-01", "file-server", "dentist-laptop", "warehouse-pos"]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="http://localhost:8000")
    p.add_argument("--token", default="change-me-too")
    args = p.parse_args()

    for host in HOSTS:
        pct = random.randint(40, 98)
        disk_status = "crit" if pct >= 90 else "warn" if pct >= 80 else "ok"
        backup_ok = random.random() > 0.3
        payload = {
            "hostname": host,
            "os": "Windows 11",
            "checks": [
                {"name": "disk:C:\\", "status": disk_status, "message": f"{pct}% used"},
                {"name": "backup:D:\\Backups", "status": "ok" if backup_ok else "crit",
                 "message": "newest backup 3h old" if backup_ok else "newest backup 74h old"},
            ],
        }
        r = httpx.post(f"{args.url}/api/v1/reports", json=payload,
                       headers={"X-Agent-Token": args.token})
        print(host, r.status_code, r.json())


if __name__ == "__main__":
    main()
