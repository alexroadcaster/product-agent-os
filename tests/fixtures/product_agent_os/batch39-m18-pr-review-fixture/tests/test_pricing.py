from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pricing import discounted_total  # noqa: E402


def main() -> int:
    assert discounted_total(1000, 15) == 850
    assert discounted_total(999, 10) == 900
    assert discounted_total(500, 0) == 500
    assert discounted_total(500, 100) == 0

    try:
        discounted_total(-1, 10)
    except ValueError:
        pass
    else:
        raise AssertionError("negative subtotal should fail")

    try:
        discounted_total(100, 101)
    except ValueError:
        pass
    else:
        raise AssertionError("discount over 100 should fail")

    print("pricing tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

