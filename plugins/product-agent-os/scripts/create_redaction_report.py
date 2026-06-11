from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.batch39_redaction import build_redaction_report, validate_redaction_report  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a Batch 39 redaction report fixture.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--test-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--artifact-ref", action="append", default=[])
    parser.add_argument("--sample-json", default="{}")
    parser.add_argument("--generated-at")
    args = parser.parse_args(argv)

    try:
        sample_payload = json.loads(args.sample_json)
    except json.JSONDecodeError as exc:
        print(json.dumps({"status": "error", "errors": [f"invalid sample json: {exc.msg}"]}, indent=2))
        return 1
    if not isinstance(sample_payload, dict):
        print(json.dumps({"status": "error", "errors": ["sample json must be an object"]}, indent=2))
        return 1

    report = build_redaction_report(
        test_id=args.test_id,
        attempt_id=args.attempt_id,
        artifact_refs=args.artifact_ref,
        sample_payload=sample_payload,
        generated_at=args.generated_at,
    )
    errors = validate_redaction_report(report)
    if errors:
        print(json.dumps({"status": "error", "errors": errors}, indent=2, sort_keys=True))
        return 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "output": str(output), "report_digest": report["report_digest"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
