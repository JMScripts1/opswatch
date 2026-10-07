import platform
import subprocess

import psutil

from .base import CheckResult


def check_services(watch: list[str]) -> list[CheckResult]:
    """Check that each named service is running (systemd on Linux, SCM on Windows)."""
    system = platform.system()
    results = []
    for svc in watch:
        if system == "Windows":
            running = _windows_running(svc)
        elif system == "Linux":
            running = _systemd_running(svc)
        else:
            results.append(CheckResult(f"service:{svc}", "warn", f"unsupported OS {system}"))
            continue
        results.append(
            CheckResult(
                name=f"service:{svc}",
                status="ok" if running else "crit",
                message="running" if running else "not running",
            )
        )
    return results


def _systemd_running(name: str) -> bool:
    r = subprocess.run(
        ["systemctl", "is-active", "--quiet", name], capture_output=True, check=False
    )
    return r.returncode == 0


def _windows_running(name: str) -> bool:
    try:
        return psutil.win_service_get(name).status() == "running"  # type: ignore[attr-defined]
    except Exception:
        return False
