from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.batch39_target_fixture_pack import (  # noqa: E402
    build_target_fixture_pack,
    validate_target_fixture_pack,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a redacted Batch 39 target fixture pack.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--target-label", required=True)
    parser.add_argument("--test-id", default="B39-TEST-M11")
    parser.add_argument("--attempt-id", default="B39-TEST-M11-A01")
    parser.add_argument("--generated-at")
    parser.add_argument("--development-stage", default="idea_stage")
    parser.add_argument("--architecture-complexity", default="complex")
    parser.add_argument("--lifecycle-state", default="p2b_design_planning")
    parser.add_argument("--usage-mode", default="read_only_pilot_fixture")
    parser.add_argument("--source-policy-status", default="present_unverified")
    args = parser.parse_args(argv)

    try:
        pack = build_target_fixture_pack(
            target_root=Path(args.target_root),
            target_label=args.target_label,
            test_id=args.test_id,
            attempt_id=args.attempt_id,
            generated_at=args.generated_at,
            development_stage=args.development_stage,
            architecture_complexity=args.architecture_complexity,
            lifecycle_state=args.lifecycle_state,
            usage_mode=args.usage_mode,
            source_policy_status=args.source_policy_status,
        )
    except ValueError as exc:
        print(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    errors = validate_target_fixture_pack(pack)
    if errors:
        print(json.dumps({"status": "error", "errors": errors}, indent=2, sort_keys=True))
        return 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(pack, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "output": _safe_output_ref(output),
                "fixture_pack_digest": pack["fixture_pack_digest"],
                "target_label": pack["target"]["target_label"],
                "overall": pack["status"]["overall"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0

def _safe_output_ref(path: Path) -> str:
    raw = str(path)
    if _looks_like_absolute_path(raw):
        return path.name
    return path.as_posix()


def _looks_like_absolute_path(value: str) -> bool:
    normalized = value.strip()
    if len(normalized) >= 3 and normalized[1] == ":" and normalized[2] in {"\\", "/"} and normalized[0].isalpha():
        return True
    if normalized.startswith("\\\\") or normalized.startswith("//"):
        return True
    if normalized.startswith("/"):
        return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
