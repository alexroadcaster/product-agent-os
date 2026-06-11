from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.task_plan_lifecycle import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
