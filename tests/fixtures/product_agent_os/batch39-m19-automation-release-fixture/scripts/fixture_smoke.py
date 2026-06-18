from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "plugins" / "product-agent-os" / "scripts"))

from product_agent_os.automation_policy import validate_automation_candidate  # noqa: E402


def main() -> int:
    candidate = ROOT / ".codex" / "automation-candidates" / "automation-candidate.md"
    release_readiness = (ROOT / "release" / "release-readiness.md").read_text(encoding="utf-8")
    approval = (ROOT / "release" / "approval-record.md").read_text(encoding="utf-8")
    runlog = (ROOT / "RUNLOG.md").read_text(encoding="utf-8")
    automation = validate_automation_candidate(candidate)

    errors: list[str] = []
    if automation["status"] != "candidate_only":
        errors.append(f"automation_status:{automation['status']}")
    if automation["errors"]:
        errors.append("automation_errors_present")
    if automation["active_schedule_status"] != "not_created":
        errors.append("active_schedule_detected")
    for key in ("github_actions_active", "codex_app_automation_active", "hook_activation_active", "external_write_active"):
        if automation[key] is not False:
            errors.append(f"{key}_detected")
    if "Release-ready claim: unsupported" not in release_readiness:
        errors.append("release_readiness_gap_missing")
    for blocked in ("publish", "deploy", "tag", "create release", "external write", "active automation"):
        if blocked not in approval:
            errors.append(f"approval_boundary_missing:{blocked}")
    if "Release publication: not performed" not in runlog:
        errors.append("release_publication_ledger_missing")

    result = {
        "status": "ok" if not errors else "failed",
        "automation_status": automation["status"],
        "manual_success_count": automation["manual_success_count"],
        "future_activation_handoff_required": automation["future_activation_handoff_required"],
        "release_publication_performed": False,
        "deployment_performed": False,
        "tag_created": False,
        "errors": errors,
    }
    print(json.dumps(result, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
