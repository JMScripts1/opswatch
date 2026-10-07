import os
import time

from opswatch_agent.checks.backups import check_backup_age
from opswatch_agent.checks.base import threshold
from opswatch_agent.checks.disk import check_disk


def test_threshold_higher_is_worse():
    assert threshold(50, 80, 90) == "ok"
    assert threshold(85, 80, 90) == "warn"
    assert threshold(95, 80, 90) == "crit"


def test_threshold_lower_is_worse():
    # e.g. days until cert expiry
    assert threshold(30, 21, 7, higher_is_worse=False) == "ok"
    assert threshold(10, 21, 7, higher_is_worse=False) == "warn"
    assert threshold(3, 21, 7, higher_is_worse=False) == "crit"


def test_disk_check_returns_results():
    results = check_disk()
    assert results
    assert all(r.status in ("ok", "warn", "crit") for r in results)


def test_backup_missing_folder_is_critical(tmp_path):
    assert check_backup_age(str(tmp_path / "nope")).status == "crit"


def test_backup_fresh_and_stale(tmp_path):
    f = tmp_path / "backup.tar"
    f.write_text("data")
    assert check_backup_age(str(tmp_path)).status == "ok"

    three_days_ago = time.time() - 72 * 3600
    os.utime(f, (three_days_ago, three_days_ago))
    assert check_backup_age(str(tmp_path)).status == "crit"
