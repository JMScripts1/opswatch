import psutil

from .base import CheckResult, threshold


def check_disk(warn_pct: float = 80, crit_pct: float = 90) -> list[CheckResult]:
    results = []
    for part in psutil.disk_partitions(all=False):
        if "cdrom" in part.opts or part.fstype in ("", "squashfs"):
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue
        status = threshold(usage.percent, warn_pct, crit_pct)
        free_gb = usage.free / 1e9
        results.append(
            CheckResult(
                name=f"disk:{part.mountpoint}",
                status=status,
                message=f"{usage.percent:.0f}% used ({free_gb:.1f} GB free)",
            )
        )
    return results
