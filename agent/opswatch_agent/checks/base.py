from dataclasses import asdict, dataclass
from typing import Literal

Status = Literal["ok", "warn", "crit"]


@dataclass
class CheckResult:
    name: str
    status: Status
    message: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def threshold(value: float, warn: float, crit: float, higher_is_worse: bool = True) -> Status:
    """Map a numeric reading onto ok/warn/crit."""
    if not higher_is_worse:
        value, warn, crit = -value, -warn, -crit
    if value >= crit:
        return "crit"
    if value >= warn:
        return "warn"
    return "ok"
