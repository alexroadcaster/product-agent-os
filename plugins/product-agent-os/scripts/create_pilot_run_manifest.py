from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.batch39_pilot_manifest import (  # noqa: E402
    PILOT_RUN_MANIFEST_SCHEMA,
    build_pilot_run_manifest,
    validate_pilot_run_manifest,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a Batch 39 pilot-run manifest fixture.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--schema-output")
    parser.add_argument("--test-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--slice", required=True)
    parser.add_argument("--pilot-id", required=True)
    parser.add_argument("--archetype", required=True)
    parser.add_argument("--target-ref", required=True)
    parser.add_argument("--source-inventory-ref", required=True)
    parser.add_argument("--command-planned", action="append", default=[])
    parser.add_argument("--check-planned", action="append", default=[])
    parser.add_argument("--evidence-artifact", action="append", default=[])
    parser.add_argument("--expected-output", action="append", default=[])
    parser.add_argument("--target-kind", default="fixture")
    parser.add_argument("--mode", default="schema_fixture")
    parser.add_argument("--source-policy-status", default="not_applicable")
    parser.add_argument("--generated-at")
    args = parser.parse_args(argv)

    manifest = build_pilot_run_manifest(
        test_id=args.test_id,
        attempt_id=args.attempt_id,
        slice_id=args.slice,
        pilot_id=args.pilot_id,
        archetype=args.archetype,
        target_ref=args.target_ref,
        source_inventory_ref=args.source_inventory_ref,
        generated_at=args.generated_at,
        commands_planned=args.command_planned,
        checks_planned=args.check_planned,
        evidence_artifacts=args.evidence_artifact,
        expected_outputs=args.expected_output,
        target_kind=args.target_kind,
        mode=args.mode,
        source_policy_status=args.source_policy_status,
    )
    errors = validate_pilot_run_manifest(manifest)
    if errors:
        print(json.dumps({"status": "error", "errors": errors}, indent=2, sort_keys=True))
        return 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    schema_output_ref = "not_requested"
    if args.schema_output:
        schema_output = Path(args.schema_output)
        schema_output.parent.mkdir(parents=True, exist_ok=True)
        schema_output.write_text(
            json.dumps(PILOT_RUN_MANIFEST_SCHEMA, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        schema_output_ref = str(schema_output)

    print(
        json.dumps(
            {
                "status": "ok",
                "output": str(output),
                "schema_output": schema_output_ref,
                "manifest_digest": manifest["manifest_digest"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
