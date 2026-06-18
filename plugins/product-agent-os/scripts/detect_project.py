from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.discovery import main


if __name__ == "__main__":
    if any(arg in {"-h", "--help"} for arg in sys.argv[1:]):
        print("usage: detect_project.py <workspace>")
        raise SystemExit(0)
    raise SystemExit(main(sys.argv[1:]))
