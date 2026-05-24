from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.validators import main_control_plane


if __name__ == "__main__":
    raise SystemExit(main_control_plane(sys.argv[1:]))
