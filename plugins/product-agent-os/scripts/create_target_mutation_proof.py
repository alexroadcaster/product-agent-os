from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.batch39_target_mutation import (  # noqa: E402
    build_target_mutation_proof,
    validate_target_mutation_proof,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a redacted Batch 39 target mutation proof JSON artifact.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--test-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--before-root", required=True)
    parser.add_argument("--after-root", required=True)
    parser.add_argument("--target-ref", required=True)
    parser.add_argument("--generated-at")
    parser.add_argument("--mutation-allowed", action="store_true")
    parser.add_argument("--approval-ref", default="none")
    args = parser.parse_args(argv)

    try:
        proof = build_target_mutation_proof(
            test_id=args.test_id,
            attempt_id=args.attempt_id,
            before_root=Path(args.before_root),
            after_root=Path(args.after_root),
            target_ref=args.target_ref,
            generated_at=args.generated_at,
            mutation_allowed=args.mutation_allowed,
            approval_ref=args.approval_ref,
        )
    except ValueError as exc:
        print(json.dumps({"status": "error", "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    errors = validate_target_mutation_proof(proof)
    if errors:
        print(json.dumps({"status": "error", "errors": errors}, indent=2, sort_keys=True))
        return 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(proof, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "output": str(output),
                "proof_digest": proof["proof_digest"],
                "verdict": proof["verdict"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
