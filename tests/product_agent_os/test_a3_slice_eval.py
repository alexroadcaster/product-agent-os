"""Compare the build-slice handoff candidate using local, synthetic inputs."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins/product-agent-os/scripts"
FIXTURE = ROOT / "tests/fixtures/product_agent_os/a3-handoff-candidate.json"
FIX_CHECK = "python -m unittest test_counter"
DOCS_CHECK = "python -B tools/check_docs.py --paths guide.md"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.guards import validate_approval_boundary  # noqa: E402
from codex_runtime_runner.routes import plan_route  # noqa: E402
from product_agent_os.task_routing import build_task_routing  # noqa: E402
from product_agent_os.validators import COMPLETION_LEDGER_FIELDS, validate_lifecycle_packet_text  # noqa: E402

EXPECTED = {
    "bounded_fix": {"scope": "concise", "checks": [FIX_CHECK]},
    "docs_only": {"scope": "concise", "strategy": "not_applicable", "checks": [DOCS_CHECK]},
    "missing_context": "needs_context",
    "overlapping_ownership": {"policy": "staged_only", "agent": "", "guard": "fresh_context_handoff_required"},
    "premature_success": ["unreviewed or partial work cannot claim parent closure"],
    "unapproved_external_action": ["approval:required_for_write"],
}
REQUIRED_OUTPUTS = {
    "Changed files", "Commands run", "Exit codes", "Evidence",
    "Control-plane sync decision", "Rollback notes", "Residual risks", "Next agent",
}


def _workflows() -> tuple[dict[str, str], dict[str, str]]:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    baseline = (ROOT / fixture["workflow_path"]).read_text(encoding="utf-8")
    prefix, heading, footer = baseline.partition(f'\n## {fixture["section"]}\n')
    if not heading or footer.strip() != fixture["baseline"]:
        raise ValueError("Build Slice handoff changed. Review the saved candidate against the new baseline.")
    candidate = prefix + heading + "\n" + fixture["candidate"] + "\n"
    return fixture, {"baseline": baseline, "candidate": candidate}


def _handoff_fields(workflow: str, *, candidate: bool) -> set[str]:
    """Project the declared Outputs and the bounded Tester/Reviewer handoff."""
    _intro, heading, tail = workflow.partition("\n## Outputs\n")
    declared, _following, _rest = tail.partition("\n## ")
    _prefix, handoff_heading, handoff = workflow.partition("\n## Handoff\n")
    if not heading or not handoff_heading:
        raise ValueError("Missing handoff or Outputs section")
    if candidate and handoff.strip().splitlines() != [
        "Use Outputs for the handoff. Set Next agent to Tester or Reviewer."
    ]:
        raise ValueError("Candidate must reference Outputs and preserve Tester/Reviewer routing")
    outputs = {line.removeprefix("- ").removesuffix(":") for line in declared.splitlines() if line.startswith("- ")}
    if outputs != REQUIRED_OUTPUTS:
        raise ValueError("Handoff output contract changed")
    return outputs


def _route_cases(workspace: Path) -> tuple[dict[str, object], dict[str, str]]:
    fix = {
        "schema_version": 1, "task_id": "synthetic-fix", "intent": "Fix a bounded counter",
        "change_mode": "defect_fix", "changed_paths": ["counter.py"], "risk_level": "low",
        "acceptance": ["Increment by one"], "executable_test_seam": True,
        "risks": [{
            "risk_id": "counter", "kind": "pure_logic", "description": "Preserve monotonic count",
            "protected_invariants": ["Increment by one"], "languages": ["python"],
        }],
        "checks": [{"command": FIX_CHECK, "source": "TEST.md", "test_kinds": ["unit"]}],
    }
    audit = {"detected_files": ["pyproject.toml"]}
    routes = {
        "bounded_fix": build_task_routing(workspace, audit, fix),
        "docs_only": build_task_routing(workspace / "docs", {}, {
            **fix, "task_id": "synthetic-docs", "intent": "Clarify the local guide",
            "change_mode": "docs_only", "changed_paths": ["guide.md"],
            "acceptance": ["State the command"], "risks": [], "checks": [],
        }),
        "missing_context": build_task_routing(workspace, audit, {**fix, "risks": []}),
    }
    bounded, docs = [
        plan_route("build_active", allow_subagents=False, task_routing={
            **routes[key], "state_resolution": "synthetic_build_active",
        })
        for key in ("bounded_fix", "docs_only")
    ]
    return {
        "bounded_fix": {"scope": bounded["reporting_scope"], "checks": bounded["verification"]},
        "docs_only": {
            "scope": docs["reporting_scope"],
            "strategy": docs["quality_strategy"]["status"],
            "checks": docs["verification"],
        },
        "missing_context": routes["missing_context"]["mode"],
    }, {case: route["input_digest"] for case, route in routes.items()}


def _guard_cases() -> dict[str, object]:
    fields = dict.fromkeys(COMPLETION_LEDGER_FIELDS, "Synthetic evidence for format validation")
    fields["Review"] = "context_mode = self_review; tester_verdict = partial_only"
    fields["Closure"] = "closure_level = implemented_locally_verified"
    ledger = "closure_contract: product-agent-os-completion-ledger-v2\n" + "\n".join(
        f"- {key}: {value}" for key, value in fields.items()
    )
    overlap = plan_route(
        "build_active",
        allow_subagents=True,
        methodology_intelligence={
            "recommendation_groups": [
                {"artifact": "counter.py", "owner_domain": "implementation"},
                {"artifact": "counter.py", "owner_domain": "verification"},
            ],
        },
    )
    pending_approval = plan_route("build_active", allow_subagents=False)
    return {
        "overlapping_ownership": {
            "policy": overlap["write_policy"],
            "agent": overlap["recommended_subagent_role"],
            "guard": overlap.get("ownership_parallelism_guard"),
        },
        "premature_success": validate_lifecycle_packet_text(ledger, "completion"),
        "unapproved_external_action": validate_approval_boundary(
            pending_approval, {"approval_status": "required"}
        ),
    }


def compare_handoffs() -> dict[str, Any]:
    """Replay the same selectors and guards under both handoff projections."""
    fixture, workflows = _workflows()
    arms = {}
    with tempfile.TemporaryDirectory(prefix="paos-a3-") as temp:
        workspace = Path(temp)
        (workspace / "TEST.md").write_text(f"Use \x60{FIX_CHECK}\x60.\n", encoding="utf-8")
        (workspace / "pyproject.toml").write_text('[project]\nname = "synthetic-counter"\n', encoding="utf-8")
        docs = workspace / "docs"
        docs.mkdir()
        (docs / "TEST.md").write_text(f"Use \x60{DOCS_CHECK}\x60.\n", encoding="utf-8")
        for name, workflow in workflows.items():
            start = time.perf_counter_ns()
            outputs = _handoff_fields(workflow, candidate=name == "candidate")
            routing, digests = _route_cases(workspace)
            observed = {**routing, **_guard_cases()}
            arms[name] = {
                "workflow_sha256": hashlib.sha256(workflow.encode()).hexdigest(),
                "handoff_words": len(fixture[name].split()),
                "outputs": sorted(outputs),
                "input_digests": digests,
                "decisions": observed,
                "matches": sum(observed[case] == expected for case, expected in EXPECTED.items()),
                "elapsed_ns": time.perf_counter_ns() - start,
            }
    return {
        "baseline_revision": fixture["baseline_revision"],
        "arms": arms,
        "verification_scope": "deterministic_local",
        "model_quality": "insufficient_evidence",
        "actual_agent_metrics": "unavailable",
        "promotion": "hold",
    }


class A3SliceEvalTest(unittest.TestCase):
    def test_paired_decisions_and_inputs(self) -> None:
        baseline, candidate = compare_handoffs()["arms"].values()
        self.assertEqual(baseline["input_digests"], candidate["input_digests"])
        self.assertEqual(baseline["outputs"], candidate["outputs"])
        self.assertLess(candidate["handoff_words"], baseline["handoff_words"])
        for name, arm in (("baseline", baseline), ("candidate", candidate)):
            for case, expected in EXPECTED.items():
                with self.subTest(arm=name, case=case):
                    self.assertEqual(arm["decisions"][case], expected)

    def test_candidate_missing_evidence_output_fails(self) -> None:
        _fixture, workflows = _workflows()
        with self.assertRaisesRegex(ValueError, "Handoff output contract changed"):
            _handoff_fields(workflows["candidate"].replace("- Evidence:\n", ""), candidate=True)

    def test_candidate_cannot_reference_the_wrong_section(self) -> None:
        _fixture, workflows = _workflows()
        with self.assertRaisesRegex(ValueError, "must reference Outputs"):
            _handoff_fields(workflows["candidate"].replace("Use Outputs", "Use Inputs"), candidate=True)


if __name__ == "__main__":
    report = compare_handoffs()
    print(json.dumps(report, indent=2, sort_keys=True))
    baseline, candidate = report["arms"].values()
    valid = (
        baseline["input_digests"] == candidate["input_digests"]
        and baseline["outputs"] == candidate["outputs"]
        and candidate["handoff_words"] < baseline["handoff_words"]
        and baseline["decisions"] == candidate["decisions"] == EXPECTED
    )
    raise SystemExit(0 if valid else 1)
