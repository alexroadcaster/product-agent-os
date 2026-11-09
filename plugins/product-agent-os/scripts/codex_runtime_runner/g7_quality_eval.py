"""G7 evidence contracts, separate from the byte-frozen T34 instrument.

This module evaluates supplied evidence, never executes candidate code or calls
providers. A valid receipt is provenance, not proof that its author is truthful.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

STATUSES = {"passed", "failed", "skipped", "unknown", "structural_only", "timeout", "setup_error"}


def verify_fixture_files(folder: Path, manifest: dict[str, Any]) -> None:
    """Reject fixture drift and paths outside the explicitly frozen synthetic corpus."""
    for name, expected in manifest['exact_fixture_files'].items():
        if not re.fullmatch(r'[a-z_]+\.py', name):
            raise ValueError('invalid fixture path')
        path = folder / name
        if path.resolve().parent != folder.resolve() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('fixture drift: ' + name)


def render_generation_context(root: Path, arm: str, chain_id: str, step_index: int,
                              previous_candidate: str | None = None) -> dict[str, Any]:
    """Render only synthetic task/source inputs; oracle assets never enter the prompt.

    This proves projection and hashes, not isolation of the future model runtime.
    Sequential callers must supply the prior arm's candidate after step zero.
    """
    design = json.loads((root / 'docs/superpowers/specs/paos-aud-g7-code-quality-eval-design.json').read_text(encoding='utf-8'))
    manifest = json.loads((root / design['manifest_path']).read_text(encoding='utf-8'))
    if evidence_fingerprint(manifest) != design['manifest_digest']:
        raise ValueError('manifest drift')
    verify_fixture_files((root / design['manifest_path']).parent, manifest)
    if arm not in ('baseline', 'treatment') or type(step_index) is not int:
        raise ValueError('invalid arm/step')
    chains = [c for c in manifest['future_generation_chains'] if c['id'] == chain_id]
    if len(chains) != 1 or not 0 <= step_index < len(chains[0]['steps']):
        raise ValueError('unknown chain/step')
    if step_index and (not isinstance(previous_candidate, str) or not previous_candidate):
        raise ValueError('sequential step requires prior candidate')
    source = previous_candidate if step_index else chains[0]['initial_source']
    if len(source) > 50000:
        raise ValueError('candidate exceeds context budget')
    context = {'request': chains[0]['steps'][step_index]['request'], 'input_source': source}
    prompt = design['generation_prompts'][arm] + '\n' + design['generation_output'] + '\n' + json.dumps(context, sort_keys=True)
    return {'prompt': prompt, 'prompt_digest': evidence_fingerprint(prompt),
            'context_keys': sorted(context), 'previous_candidate_digest': evidence_fingerprint(source),
            'design_digest': evidence_fingerprint(design), 'manifest_digest': design['manifest_digest'],
            'context_isolation': 'projection_only_runtime_not_attested', 'provider_call_performed': False}


def evidence_fingerprint(context: dict[str, Any]) -> str:
    """Bind evidence to explicit public inputs without collecting environment secrets."""
    return hashlib.sha256(json.dumps(context, sort_keys=True, ensure_ascii=False,
                                    allow_nan=False).encode()).hexdigest()


def summarize_outcomes(rows: list[dict[str, Any]], expected_cases: list[str]) -> dict[str, Any]:
    """Account for every eligible case; unknown/missing never contributes a pass."""
    if (not isinstance(expected_cases, list) or not expected_cases
            or any(not isinstance(x, str) or not x for x in expected_cases)
            or len(set(expected_cases)) != len(expected_cases)):
        raise ValueError("expected cases must be unique nonempty identifiers")
    if not isinstance(rows, list):
        raise ValueError("outcomes must be a list")
    counts = dict.fromkeys(sorted(STATUSES | {"missing"}), 0)
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("case_id"), str):
            raise ValueError("invalid outcome")
        case = row["case_id"]
        if case not in expected_cases or case in seen or row.get("status") not in STATUSES:
            raise ValueError("unknown, duplicate case or invalid outcome status")
        seen.add(case)
        counts[row["status"]] += 1
    counts["missing"] = len(expected_cases) - len(seen)
    executed = counts["passed"] + counts["failed"]
    return {"eligible": len(expected_cases), "recorded": len(rows),
            "attempted": executed + counts["timeout"] + counts["setup_error"],
            "executed": executed, "counts": counts,
            "executable_pass_rate": counts["passed"] / executed if executed else None,
            "eligible_pass_rate": counts["passed"] / len(expected_cases),
            "complete": counts["passed"] == len(expected_cases),
            "evidence_ceiling": "supplied outcomes; not independent execution or owner acceptance"}


def review_findings(findings: list[dict[str, Any]], revision: str) -> dict[str, Any]:
    """Require source-bound review evidence; model scores and preferences cannot veto.

    Deferred confirmed risks remain unresolved until explicit owner acceptance;
    the reviewer cannot grant that acceptance by changing a disposition.
    """
    if not isinstance(revision, str) or not re.fullmatch(r"[a-f0-9]{64}", revision):
        raise ValueError("candidate revision must be a SHA-256")
    if not isinstance(findings, list):
        raise ValueError("findings must be a list")
    gaps, defects, advisory = [], [], []
    seen: set[str] = set()
    for finding in findings:
        required = ("id", "revision", "source", "scenario", "consequence", "action", "confidence", "kind", "disposition", "evidence")
        if not isinstance(finding, dict):
            raise ValueError("invalid finding")
        identifier = finding.get("id", "missing-id")
        if not isinstance(identifier, str) or identifier in seen:
            raise ValueError("duplicate or invalid finding id")
        seen.add(identifier)
        if any(not isinstance(finding.get(k), str) or not finding[k].strip() for k in required):
            gaps.append(identifier)
            continue
        if (finding["revision"] != revision or finding["confidence"] not in {"low", "medium", "high"}
                or finding["kind"] not in {"correctness", "security", "data_loss", "maintainability", "preference"}
                or finding["disposition"] not in {"confirmed", "fixed", "rejected", "false_positive", "deferred", "unresolved"}):
            gaps.append(identifier)
            continue
        disposition = finding["disposition"]
        if disposition == 'deferred' and any(not isinstance(finding.get(k), str) or not finding[k].strip()
                                             for k in ('owner', 'revisit_trigger')):
            raise ValueError('deferred finding requires owner and revisit_trigger')
        if disposition in {"deferred", "unresolved"}:
            gaps.append(identifier)
        elif disposition == "confirmed" and finding["kind"] != "preference":
            defects.append(identifier)
        else:
            advisory.append(identifier)
    return {"schema_version": "g7_review_v2", "revision": revision,
            "verdict": "blocked" if gaps else "changes_requested" if defects else "approve",
            "evidence_gaps": gaps, "confirmed_defects": defects, "advisory_or_resolved": advisory,
            "evidence_ceiling": "contract validation; evidence content needs independent review"}
