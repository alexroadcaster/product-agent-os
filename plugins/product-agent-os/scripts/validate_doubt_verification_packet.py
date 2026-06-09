from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.doubt_verification import main_doubt_verification  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main_doubt_verification(sys.argv[1:]))
