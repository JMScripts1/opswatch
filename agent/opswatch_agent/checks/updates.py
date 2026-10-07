import platform
import subprocess

from .base import CheckResult, threshold


def check_pending_updates(warn: int = 10, crit: int = 50) -> CheckResult:
    """Count pending OS updates.

    TODO(milestone 3): Windows support via PowerShell (PSWindowsUpdate or the
    Microsoft.Update.Session COM object) - see scripts/check_updates.ps1.
    """
    if platform.system() != "Linux":
        return CheckResult("updates", "ok", "update check not implemented on this OS yet")
    try:
        out = subprocess.run(
            ["apt", "list", "--upgradable"], capture_output=True, text=True, timeout=60, check=False
        ).stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return CheckResult("updates", "warn", "apt not available")
    count = sum(1 for line in out.splitlines() if "upgradable from" in line)
    return CheckResult("updates", threshold(count, warn, crit), f"{count} packages upgradable")
