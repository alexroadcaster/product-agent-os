"""Explicit G7 generation-only comparison; never executes generated candidates."""
from __future__ import annotations
import argparse
import ast
import difflib
import hashlib
import json
import time
from pathlib import Path
from g7_codex_trace_receipt import run_preflight

ROOT = Path(__file__).resolve().parents[3]
DESIGN = ROOT / "docs/superpowers/specs/paos-aud-g7-attested-design.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_text(output: str) -> str:
    """Remove only one complete Markdown code fence; retain exact trace output digest."""
    text = output.strip()
    if text.startswith("```python\n") and text.endswith("\n```"):
        text = text[len("```python\n"):-len("\n```")]
    elif text.startswith("```\n") and text.endswith("\n```"):
        text = text[4:-4]
    ast.parse(text)
    if any(marker in text.lower() for marker in ("c:\\users", "c:/users", "sk-proj-", "/users/")):
        raise ValueError("non-synthetic candidate")
    return text + "\n"


def run(executable: Path) -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    for name, expected in design["frozen_files"].items():
        if sha((ROOT/name).read_bytes()) != expected:
            raise ValueError("frozen input drift: " + name)
    destination = ROOT / design["output_directory"]
    destination.mkdir(parents=True, exist_ok=True)
    if (destination/"receipt.json").exists():
        raise ValueError("run already recorded; no overwrite or hidden retry")
    receipt = dict(schema_version="g7_attested_generation_v1", design_digest=sha(DESIGN.read_bytes()),
                   executed_design=design, calls=[], expected_calls=12, context_equivalent=True,
                   comparison_eligible=False, owner_acceptance=None,
                   evidence_ceiling="generation-only; not filesystem isolation or end-to-end")
    previous = {}
    common_digest = None
    started = time.monotonic()
    def save():
        (destination/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    save()
    for chain in design["chains"]:
        for step_index, step in enumerate(chain["steps"]):
            for arm in ("baseline", "treatment"):
                source = previous.get((chain["id"],arm), chain["initial_source"])
                prompt = design["contracts"][arm] + "\n" + design["output_contract"] + "\n" + json.dumps(
                    {"request":step["request"],"input_source":source,"untrusted_note":step.get("untrusted_note", "")},sort_keys=True)
                call_started = time.monotonic()
                record = dict(arm=arm,chain=chain["id"],step=step["id"],step_index=step_index,
                              parent_source_sha256=sha(source.encode()), prompt_sha256=sha(prompt.encode()))
                if time.monotonic()-started > design["max_total_seconds"]:
                    record.update(status="budget_stopped",attempted=False)
                    receipt["calls"].append(record);save();return receipt
                observed = run_preflight(ROOT,executable,tuple(design["disabled_mcp"]),ROOT/design["catalog"],
                                         prompt=prompt,include_output=True)
                output = observed.pop("candidate", None)
                record.update(trace=observed,elapsed_seconds=round(time.monotonic()-call_started,3),attempted=True)
                digest = observed.get("normalized_common_context_sha256")
                if observed.get("status") != "passed" or output is None:
                    record["status"]="admission_failed"
                elif common_digest is not None and digest != common_digest:
                    record["status"]="context_mismatch"
                    receipt["context_equivalent"]=False
                else:
                    common_digest=digest
                    try:
                        candidate=source_text(output)
                    except (SyntaxError,ValueError):
                        record["status"]="invalid_candidate"
                    else:
                        filename=f"candidate-{len(receipt['calls'])+1:02d}.py"
                        (destination/filename).write_text(candidate,encoding="utf-8")
                        record.update(status="generated_not_judged",candidate_file=filename,source_sha256=sha(candidate.encode()),
                                      changed_lines=sum(line.startswith(("+","-")) and not line.startswith(("+++","---"))
                                                        for line in difflib.unified_diff(source.splitlines(),candidate.splitlines())))
                        previous[(chain["id"],arm)]=candidate
                receipt["calls"].append(record)
                print(chain["id"],step["id"],arm,record["status"],flush=True)
                save()
                if record["status"] != "generated_not_judged":
                    return receipt
    receipt["comparison_eligible"]=len(receipt["calls"])==12 and receipt["context_equivalent"]
    receipt["elapsed_seconds"]=round(time.monotonic()-started,3)
    save()
    return receipt


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute",action="store_true",required=True)
    parser.add_argument("--codex-executable",type=Path,required=True)
    args=parser.parse_args()
    result=run(args.codex_executable)
    raise SystemExit(0 if result["comparison_eligible"] else 1)
