import socket
import ssl
from datetime import UTC, datetime

from .base import CheckResult, threshold


def check_cert_expiry(
    host: str, port: int = 443, warn_days: int = 21, crit_days: int = 7
) -> CheckResult:
    name = f"cert:{host}"
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as tls:
                not_after = tls.getpeercert()["notAfter"]
    except (OSError, ssl.SSLError) as e:
        return CheckResult(name, "crit", f"TLS check failed: {e}")

    expires = datetime.fromtimestamp(ssl.cert_time_to_seconds(not_after), UTC)
    days_left = (expires - datetime.now(UTC)).days
    return CheckResult(
        name=name,
        status=threshold(days_left, warn_days, crit_days, higher_is_worse=False),
        message=f"expires in {days_left} days ({expires:%Y-%m-%d})",
    )
