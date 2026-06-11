from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    corpus = _jsonl(ROOT / "rag" / "corpus.jsonl")
    cases = _jsonl(ROOT / "evals" / "rag-eval-cases.jsonl")
    schema = json.loads((ROOT / "structured-output" / "answer-schema.json").read_text(encoding="utf-8"))
    trace = json.loads((ROOT / "traces" / "sample-trace.json").read_text(encoding="utf-8"))
    required_schema_fields = {"answer", "citations", "confidence", "unsupported"}
    missing_schema_fields = sorted(required_schema_fields - set(schema.get("properties", {})))
    if len(corpus) < 2 or len(cases) < 2 or missing_schema_fields:
        print(
            json.dumps(
                {
                    "status": "error",
                    "corpus_count": len(corpus),
                    "case_count": len(cases),
                    "missing_schema_fields": missing_schema_fields,
                },
                sort_keys=True,
            )
        )
        return 1
    if trace.get("provider_call_performed") is not False:
        print(json.dumps({"status": "error", "provider_call_performed": trace.get("provider_call_performed")}, sort_keys=True))
        return 1
    print(
        json.dumps(
            {
                "status": "ok",
                "corpus_count": len(corpus),
                "case_count": len(cases),
                "schema_fields": sorted(schema.get("properties", {})),
                "provider_call_performed": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

