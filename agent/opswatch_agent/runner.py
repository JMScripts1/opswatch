"""Run every check enabled in the config and collect results."""

from .checks import (
    CheckResult,
    check_backup_age,
    check_cert_expiry,
    check_disk,
    check_pending_updates,
    check_services,
)


def run_all(cfg: dict) -> list[CheckResult]:
    checks = cfg.get("checks", {})
    results: list[CheckResult] = []

    if disk := checks.get("disk"):
        results += check_disk(disk.get("warn_pct", 80), disk.get("crit_pct", 90))
    if services := checks.get("services"):
        results += check_services(services)
    for path in checks.get("backups", []):
        results.append(check_backup_age(path))
    for host in checks.get("certs", []):
        results.append(check_cert_expiry(host))
    if checks.get("updates"):
        results.append(check_pending_updates())

    return results
