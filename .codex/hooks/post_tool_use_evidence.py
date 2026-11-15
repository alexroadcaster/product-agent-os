from __future__ import annotations

import sys


def main() -> int:
    """Compatibility no-op for already loaded hook definitions.

    Evidence belongs to the scoped verification result, not each file write.
    This hook never makes an approval or completion decision.
    """
    sys.stdin.read()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
