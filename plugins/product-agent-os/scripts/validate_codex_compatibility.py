from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.codex_compatibility import validate_codex_compatibility  # noqa: E402
from product_agent_os.plugin_components import unique_json_object  # noqa: E402


def main() -> int:
    """Exit status covers local structure; diagnostic gaps remain explicit JSON."""
    parser = argparse.ArgumentParser(description="Read-only local compatibility; no host activation or provider calls.")
    parser.add_argument("--plugin-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--observations", type=Path, help="Explicit non-secret JSON observations; not a verified host receipt")
    parser.add_argument("--cache-root", type=Path, help="Explicit cache directory for read-only component comparison")
    args = parser.parse_args()
    observations = None
    if args.observations is not None:
        try:
            if args.observations.stat().st_size > 16 * 1024:
                raise ValueError("oversized_input")
            observations = json.loads(args.observations.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_json_object)
            if not isinstance(observations, dict):
                raise ValueError("object_required")
        except (OSError, ValueError):
            print(json.dumps({"status": "needs_review", "error": "invalid_observations_file"}))
            return 2
    report = validate_codex_compatibility(args.plugin_root, observations=observations, cache_root=args.cache_root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "compatible" else 1


if __name__ == "__main__":
    raise SystemExit(main())
