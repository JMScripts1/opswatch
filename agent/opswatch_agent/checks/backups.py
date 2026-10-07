import time
from pathlib import Path

from .base import CheckResult, threshold


def check_backup_age(path: str, warn_hours: float = 26, crit_hours: float = 50) -> CheckResult:
    """Alert when the newest file in a backup folder is too old."""
    folder = Path(path)
    files = [p for p in folder.rglob("*") if p.is_file()] if folder.exists() else []
    if not files:
        return CheckResult(f"backup:{path}", "crit", "no backup files found")
    newest = max(p.stat().st_mtime for p in files)
    age_h = (time.time() - newest) / 3600
    return CheckResult(
        name=f"backup:{path}",
        status=threshold(age_h, warn_hours, crit_hours),
        message=f"newest backup is {age_h:.1f}h old",
    )
