"""Read-only methodology audit for Product-Agent OS Track 9."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from product_agent_os.contracts import CONTROL_PLANE_FILES
from product_agent_os.methodology_catalog import load_methodology_catalog


PRIORITY_ORDER = {
    "P0_blocker": 0,
    "P1_high_risk": 1,
    "P2_recommended": 2,
    "P3_optional_maturity": 3,
    "not_applicable": 4,
}

STACK_MARKERS = {
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
}

OPENAPI_MARKERS = {"openapi.yaml", "openapi.yml", "openapi.json"}
ASYNCAPI_MARKERS = {"asyncapi.yaml", "asyncapi.yml", "asyncapi.json"}
DOC_CONTROL_FILES = {"readme.md", "agents.md", "requirements.md", "plan.md", "test.md", "evals.md", "runlog.md"}
DEPLOY_MARKERS = {"dockerfile", "docker-compose.yml", "serverless.yml"}
RELEASE_FILE_MARKERS = {"changelog.md", "changes.md", "release.md", "release-notes.md"}

BUSINESS_INTENT_TERMS = {
    "analytics",
    "behavior",
    "dashboard",
    "experiment",
    "metric",
    "mvp",
    "product",
    "release",
    "success",
    "telemetry",
    "usage",
    "user",
    "value",
}
BEHAVIOR_INTENT_TERMS = {"behavior", "feature", "change", "ship", "release", "user"}
UI_INTENT_TERMS = {"frontend", "ui", "ux", "component", "screen", "page"}
BACKEND_INTENT_TERMS = {"server", "api", "service", "worker", "queue", "backend"}
API_INTENT_TERMS = {"api", "webhook", "integration", "external", "graphql", "grpc", "protobuf"}
AI_INTENT_TERMS = {"prompt", "model", "eval", "rag", "vector", "embedding", "ai", "llm"}
DELIVERY_INTENT_TERMS = {"production", "release", "deploy", "package", "docker", "kubernetes", "operations"}
BUSINESS_NOT_APPLICABLE_PHRASES = {
    "typo-only",
    "formatting-only",
    "dependency pin without behavior impact",
    "without behavior impact",
}
IMPLEMENTATION_OR_RELEASE_TERMS = {"implement", "implementation", "ship", "release", "build", "deliver"}
PRODUCT_ANALYTICS_TERMS = {"analytics", "usage", "event", "events", "dashboard", "telemetry", "tracking"}
PRODUCT_SUCCESS_TERMS = {"success", "north star", "value metric", "product value"}
WORKFLOW_PROMOTION_TERMS = {"workflow promotion", "promote workflow", "automation", "skill promotion", "playbook"}
HIGH_RISK_INTENT_TERMS = {
    "security",
    "privacy",
    "payment",
    "pii",
    "compliance",
    "healthcare",
    "finance",
    "production data",
    "auth",
    "authorization",
    "secret",
}
REGULATED_INTENT_TERMS = {"regulated", "compliance", "audit", "hipaa", "pci", "soc2", "finance", "healthcare", "minors"}


def build_methodology_audit(workspace: Path, intent_hint: str = "") -> dict[str, Any]:
    """Build a read-only methodology audit packet for a workspace."""

    root = Path(workspace)
    files, directories = _relative_inventory(root)
    lowered_files = {path.lower() for path in files}
    lowered_dirs = {path.lower() for path in directories}
    intent = intent_hint.lower()
    observed = _observed_signals(root, lowered_files, lowered_dirs)
    intent_signals = _intent_signals(intent)
    maturity_level = _classify_maturity(lowered_files, lowered_dirs, observed, intent)
    complexity_profile = _classify_complexity(lowered_files, lowered_dirs, observed, intent)
    methodology_domains = _methodology_domains(
        observed,
        intent,
        maturity_level["selected"],
        complexity_profile["selected"],
        bool(files),
    )
    recommendations = _prioritize_recommendations(
        _recommendations(root, lowered_files, lowered_dirs, observed, intent, complexity_profile["selected"])
    )

    return {
        "status": "ok",
        "write_policy": "read_only",
        "maturity_level": maturity_level,
        "complexity_profile": complexity_profile,
        "observed_signals": observed,
        "intent_signals": intent_signals,
        "unknowns": _unknowns(lowered_files, lowered_dirs, observed),
        "questions_for_owner": _questions_for_owner(lowered_files, lowered_dirs, observed, recommendations),
        "provisional_assumptions": _provisional_assumptions(files, intent),
        "delivery_map": _delivery_map(lowered_files, lowered_dirs, observed, methodology_domains, recommendations),
        "methodology_domains": methodology_domains,
        "recommendations": recommendations,
        "safe_next_action": _safe_next_action(recommendations),
    }


def _relative_inventory(root: Path) -> tuple[set[str], set[str]]:
    files: set[str] = set()
    directories: set[str] = set()
    if not root.exists() or not root.is_dir():
        return files, directories
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in {".git", "node_modules", "__pycache__"}]
        current_path = Path(current_root)
        for dirname in dirnames:
            try:
                directories.add((current_path / dirname).relative_to(root).as_posix())
            except ValueError:
                continue
        for filename in filenames:
            try:
                files.add((current_path / filename).relative_to(root).as_posix())
            except ValueError:
                continue
    return files, directories


def _observed_signals(root: Path, files: set[str], directories: set[str]) -> list[dict[str, Any]]:
    signals: list[dict[str, Any]] = []

    def add(signal_id: str, evidence: list[str]) -> None:
        if evidence:
            signals.append({"id": signal_id, "source": "workspace", "evidence": sorted(evidence)})

    add("stack_manifest", [path for path in files if path in STACK_MARKERS])
    add("openapi_contract", [path for path in files if _is_openapi(path)])
    add("asyncapi_contract", [path for path in files if _is_asyncapi(path)])
    add("graphql_schema", [path for path in files if path.endswith("schema.graphql")])
    add("protobuf_schema", [path for path in files if path.endswith(".proto")])
    add(
        "database_migration_or_schema",
        [path for path in files if path in {"alembic.ini", "dbt_project.yml"}]
        + [directory for directory in directories if directory in {"migrations", "prisma"}],
    )
    add(
        "ci_configuration",
        [path for path in files if path.startswith(".github/workflows/") or path in {".gitlab-ci.yml", "azure-pipelines.yml"}],
    )
    add(
        "deployment_configuration",
        [path for path in files if path in DEPLOY_MARKERS] + [directory for directory in directories if directory == "k8s"],
    )
    add("release_file", [path for path in files if path in RELEASE_FILE_MARKERS or path.startswith(".changeset/")])
    add("docs_or_control_plane", [path for path in files if path in DOC_CONTROL_FILES] + ["docs" for item in directories if item == "docs"])
    add(
        "ai_eval_or_rag",
        [
            path
            for path in files
            if path.startswith(("evals/", "prompts/", "rag/"))
            or "vector" in path
            or "embeddings" in path
        ]
        + [directory for directory in directories if directory in {"evals", "prompts", "rag", "vector", "embeddings"}],
    )
    add("test_evidence", [path for path in files if "test" in path or path.startswith("evals/")])
    if _has_package_test_script(root):
        add("test_command", ["package.json"])
    return signals


def _intent_signals(intent: str) -> list[dict[str, str]]:
    signals: list[dict[str, str]] = []
    for category, terms in [
        ("business_product", BUSINESS_INTENT_TERMS),
        ("behavior_change", BEHAVIOR_INTENT_TERMS),
        ("frontend", UI_INTENT_TERMS),
        ("backend", BACKEND_INTENT_TERMS),
        ("api_integrations", API_INTENT_TERMS),
        ("llm_ai_rag", AI_INTENT_TERMS),
        ("delivery_release_operations", DELIVERY_INTENT_TERMS),
        ("high_risk", HIGH_RISK_INTENT_TERMS),
        ("regulated", REGULATED_INTENT_TERMS),
    ]:
        for term in sorted(terms):
            if term in intent:
                signals.append({"category": category, "term": term})
    return signals


def _classify_maturity(
    files: set[str],
    directories: set[str],
    observed: list[dict[str, Any]],
    intent: str,
) -> dict[str, Any]:
    if _mentions_any(intent, REGULATED_INTENT_TERMS):
        return {
            "selected": "regulated",
            "confidence": "medium",
            "reasons": ["regulated intent term detected"],
        }
    has_ci = _has_signal(observed, "ci_configuration")
    has_release = _mentions_any(intent, {"production", "release"}) or _has_any_signal(
        observed,
        {"deployment_configuration", "release_file"},
    )
    if has_release and _has_any_signal(observed, {"ci_configuration", "deployment_configuration", "release_file"}):
        return {
            "selected": "production",
            "confidence": "medium",
            "reasons": ["production or release intent with CI or deployment evidence"],
        }
    if has_ci or len(files) > 1 or bool(directories - {"docs"}):
        return {
            "selected": "team",
            "confidence": "medium",
            "reasons": ["workspace has project or collaboration signals"],
        }
    return {
        "selected": "baseline",
        "confidence": "high" if not files or files <= {"readme.md"} else "medium",
        "reasons": ["empty or README-only workspace" if not files or files <= {"readme.md"} else "minimal workspace signals"],
    }


def _classify_complexity(
    files: set[str],
    directories: set[str],
    observed: list[dict[str, Any]],
    intent: str,
) -> dict[str, Any]:
    if _mentions_any(intent, HIGH_RISK_INTENT_TERMS | REGULATED_INTENT_TERMS):
        return {
            "selected": "high_risk",
            "confidence": "medium",
            "reasons": ["high-risk or regulated intent term detected"],
        }
    has_api = _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "graphql_schema", "protobuf_schema"})
    has_database = _has_signal(observed, "database_migration_or_schema")
    has_ci = _has_signal(observed, "ci_configuration")
    if has_api and (has_database or has_ci):
        return {
            "selected": "complex",
            "confidence": "high",
            "reasons": ["API contract plus database or CI signal detected"],
        }
    if has_api or has_database or _has_signal(observed, "deployment_configuration") or len(directories) > 3:
        return {
            "selected": "standard",
            "confidence": "medium",
            "reasons": ["multiple implementation surfaces detected"],
        }
    return {
        "selected": "simple",
        "confidence": "high" if not files or files <= {"readme.md"} else "medium",
        "reasons": ["empty or README-only workspace" if not files or files <= {"readme.md"} else "limited workspace signals"],
    }


def _methodology_domains(
    observed: list[dict[str, Any]],
    intent: str,
    maturity_level: str,
    complexity_profile: str,
    has_files: bool,
) -> list[dict[str, Any]]:
    catalog = load_methodology_catalog()
    applicable = {
        "business_product": _business_product_applies(intent),
        "requirements_domain": has_files or _mentions_any(intent, BEHAVIOR_INTENT_TERMS),
        "solution_architecture": complexity_profile in {"complex", "high_risk"}
        or maturity_level in {"team", "production", "regulated"}
        or _has_any_signal(observed, {"openapi_contract", "database_migration_or_schema", "ai_eval_or_rag", "deployment_configuration"}),
        "quality_testing_evals": has_files or _has_signal(observed, "test_evidence") or _has_signal(observed, "test_command"),
        "codex_agentic_workflow": True,
        "frontend": _has_signal(observed, "stack_manifest") and _mentions_any(intent, UI_INTENT_TERMS) or _mentions_any(intent, UI_INTENT_TERMS),
        "backend": _mentions_any(intent, BACKEND_INTENT_TERMS)
        or _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "database_migration_or_schema"}),
        "api_integrations": _mentions_any(intent, API_INTENT_TERMS)
        or _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "graphql_schema", "protobuf_schema"}),
        "database_data": _has_signal(observed, "database_migration_or_schema") or "production data" in intent,
        "llm_ai_rag": _mentions_any(intent, AI_INTENT_TERMS) or _has_signal(observed, "ai_eval_or_rag"),
        "security_privacy_compliance": complexity_profile == "high_risk"
        or maturity_level == "regulated"
        or _mentions_any(intent, HIGH_RISK_INTENT_TERMS),
        "delivery_release_operations": maturity_level in {"production", "regulated"}
        or _mentions_any(intent, DELIVERY_INTENT_TERMS)
        or _has_any_signal(observed, {"ci_configuration", "deployment_configuration"}),
    }

    domain_packets: list[dict[str, Any]] = []
    observed_domain_ids = _observed_domain_ids(observed)
    for domain in catalog["domains"]:
        domain_id = domain["id"]
        is_applicable = bool(applicable.get(domain_id, False))
        status = "present_unverified" if domain_id in observed_domain_ids else "applicable_missing"
        domain_packets.append(
            {
                "id": domain_id,
                "title": domain["title"],
                "source_file": domain["source_file"],
                "status": status if is_applicable else "not_applicable",
                "applicability_reason": "catalog domain applies to observed workspace or intent signals"
                if is_applicable
                else "no deterministic signal detected",
            }
        )
    return domain_packets


def _business_product_applies(intent: str) -> bool:
    if _business_product_not_applicable(intent):
        return False
    return _mentions_any(intent, BUSINESS_INTENT_TERMS | IMPLEMENTATION_OR_RELEASE_TERMS)


def _business_product_not_applicable(intent: str) -> bool:
    return any(phrase in intent for phrase in BUSINESS_NOT_APPLICABLE_PHRASES)


def _business_product_recommendations(files: set[str], intent: str) -> list[dict[str, Any]]:
    if not _business_product_applies(intent):
        return []

    recommendations: list[dict[str, Any]] = []
    implementation_or_release = bool(files) and _mentions_any(intent, IMPLEMENTATION_OR_RELEASE_TERMS)
    product_hypothesis_priority = "P1_high_risk" if implementation_or_release else "P2_recommended"
    recommendations.append(
        _recommendation(
            priority=product_hypothesis_priority,
            reason="Product or behavior-changing intent needs a product hypothesis before implementation.",
            domain="business_product",
            gate="product_hypothesis_present",
            artifact="product-brief.md",
            evidence_required=[
                "target user segment",
                "problem or opportunity",
                "expected outcome",
                "non-goals",
                "owner",
            ],
            evidence_owner="product owner",
            approval_boundary="not required for read-only audit; approval_required before broad implementation",
            accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
            residual_risk="Implementation can optimize the wrong behavior when product intent is implicit.",
            safe_next_action="Stage a product brief before requirements slicing or implementation.",
        )
    )
    recommendations.append(
        _recommendation(
            priority="P2_recommended",
            reason="Decision horizon is missing for product methodology depth.",
            domain="business_product",
            gate="decision_horizon_present",
            artifact="product-brief.md",
            evidence_required=["discovery, MVP, beta, production or scale", "owner", "review window"],
            evidence_owner="product owner",
            approval_boundary="not required for drafting methodology recommendations",
            accepted_gap_option="explicit_gap_accepted with owner and reason for unknown decision horizon",
            residual_risk="The same process depth can be over-applied to discovery work or under-applied to production work.",
            safe_next_action="Classify the decision horizon before choosing required artifacts.",
        )
    )
    recommendations.append(
        _recommendation(
            priority="P1_high_risk" if implementation_or_release else "P2_recommended",
            reason="Metric scope is not classified for product behavior work.",
            domain="business_product",
            gate="metric_scope_classified",
            artifact="REQUIREMENTS.md",
            evidence_required=["metric_scope required, not_applicable or accepted_gap", "owner", "residual risk"],
            evidence_owner="product owner",
            approval_boundary="not required for read-only classification",
            accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
            residual_risk="Unclassified metric scope can turn planned measurement into unsupported success claims.",
            safe_next_action="Classify metric scope before planning implementation or release text.",
        )
    )
    if _mentions_any(intent, PRODUCT_SUCCESS_TERMS):
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="Product success or North Star wording needs metric-level separation.",
                domain="business_product",
                gate="outcome_metric_level_separated",
                artifact="metric-spec.md",
                evidence_required=["business outcome", "product outcome", "feature traction metric"],
                evidence_owner="product owner",
                approval_boundary="not required for metric classification",
                accepted_gap_option="explicit_gap_accepted with owner and reason for metric-level ambiguity",
                residual_risk="A local feature traction metric can be mistaken for a product value metric.",
                safe_next_action="Separate business outcome, product outcome and feature traction metric.",
            )
        )
    if _mentions_any(intent, {"metric", "success", "measurement", "analytics", "dashboard"}):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Metric claim needs counter-metric, guardrail, qualitative review and privacy classification.",
                domain="business_product",
                gate="metric_hardening_when_product_behavior_changes",
                artifact="metric-spec.md",
                evidence_required=[
                    "primary metric",
                    "input metric",
                    "counter-metric",
                    "guardrail",
                    "proxy metric risk",
                    "qualitative review",
                    "privacy classification",
                ],
                evidence_owner="product owner",
                approval_boundary="approval_required before external analytics writes or product success claims",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="A single metric can improve while product quality, trust, support load or privacy degrades.",
                safe_next_action="Stage metric hardening before implementation or success claims.",
            )
        )
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="Metric claim needs qualitative feedback or an accepted qualitative evidence gap.",
                domain="business_product",
                gate="qualitative_feedback_loop_present",
                artifact="metric-spec.md",
                evidence_required=["user research, support, sales, customer-success or owner review evidence"],
                evidence_owner="product owner",
                approval_boundary="not required for read-only audit",
                accepted_gap_option="explicit_gap_accepted with owner and reason for missing qualitative loop",
                residual_risk="Quantitative movement can hide user trust, support or satisfaction regressions.",
                safe_next_action="Record a qualitative feedback loop or accepted gap.",
            )
        )
    if _mentions_any(intent, PRODUCT_ANALYTICS_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Product analytics claim needs event taxonomy, property definitions, owner and validation evidence.",
                domain="business_product",
                gate="analytics_tracking_plan_present",
                artifact="tracking-plan.md",
                evidence_required=[
                    "event names",
                    "properties",
                    "property types",
                    "taxonomy",
                    "owner",
                    "validation command or report",
                    "privacy classification",
                ],
                evidence_owner="data or product analytics owner",
                approval_boundary="approval_required before external analytics writes or production telemetry changes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="Analytics events without taxonomy or validation can make product decisions unreliable.",
                safe_next_action="Stage a tracking plan before instrumentation or analytics claims.",
            )
        )
    if _mentions_any(intent, AI_INTENT_TERMS):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="AI product behavior needs both eval evidence and product value evidence.",
                domain="business_product",
                gate="ai_product_eval_when_ai_behavior_changes",
                artifact="ai-eval-spec.md",
                evidence_required=["user-visible promise", "baseline eval", "threshold", "failure review owner"],
                evidence_owner="AI product owner",
                approval_boundary="not required for baseline planning; approval_required before external AI behavior release",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="AI eval score can be mistaken for product value without user outcome evidence.",
                safe_next_action="Stage AI product eval and value evidence before prompt, model, retrieval or agent changes.",
            )
        )
    if "release" in intent or "after release" in intent or "telemetry" in intent:
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Product success claim after release needs actual evidence or an accepted evidence gap.",
                domain="business_product",
                gate="release_measurement_evidence_present",
                artifact="RUNLOG.md",
                evidence_required=[
                    "actual metric",
                    "eval result",
                    "user feedback",
                    "support signal",
                    "owner review",
                    "accepted evidence gap",
                ],
                evidence_owner="learning-loop maintainer",
                approval_boundary="approval_required before release success claims or external release actions",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="Planned measurement alone is not product success evidence.",
                safe_next_action="Record post-release evidence or accepted gap before success claims.",
            )
        )
    if _mentions_any(intent, WORKFLOW_PROMOTION_TERMS):
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="Workflow promotion needs value evidence, verification, owner and safety boundary.",
                domain="business_product",
                gate="workflow_promotion_value_evidence_present",
                artifact="skill-promotion-record.md",
                evidence_required=["engineering time saved", "verification", "owner", "safety boundary"],
                evidence_owner="workflow owner",
                approval_boundary="approval_required before active automation or durable promotion",
                accepted_gap_option="explicit_gap_accepted with owner and reason for no external product metric",
                residual_risk="A repeated workflow can be automated before it has stable value or safety evidence.",
                safe_next_action="Record workflow value evidence before promotion to skill, plugin or automation.",
            )
        )
    return recommendations


def _recommendations(
    root: Path,
    files: set[str],
    directories: set[str],
    observed: list[dict[str, Any]],
    intent: str,
    complexity_profile: str,
) -> list[dict[str, Any]]:
    recommendations: list[dict[str, Any]] = []
    recommendations.extend(_business_product_recommendations(files, intent))
    missing_control_plane = [name for name in CONTROL_PLANE_FILES if name.lower() not in files]
    if missing_control_plane:
        recommendations.append(
            _recommendation(
                priority="P2_recommended",
                reason="Product-Agent OS control-plane files are missing.",
                domain="codex_agentic_workflow",
                gate="control_plane_present",
                artifact="AGENTS.md",
                evidence_required=["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"],
                evidence_owner="product-agent operator",
                approval_boundary="approval_required before writing staged control-plane artifacts into the workspace",
                accepted_gap_option="explicit_gap_accepted with owner and reason for operating without project control plane",
                residual_risk="Missing control-plane files can leave requirements, verification and ownership implicit.",
                safe_next_action="Stage control-plane artifact proposals without mutating existing workspace files.",
            )
        )
    if not _has_test_command_or_evidence(root, files, observed):
        recommendations.append(
            _recommendation(
                priority="P0_blocker",
                reason="No test command or test evidence was detected.",
                domain="quality_testing_evals",
                gate="quality_strategy_present",
                artifact="TEST.md",
                evidence_required=["test command", "expected output", "evidence owner or accepted gap"],
                evidence_owner="tester",
                approval_boundary="not required for drafting a test plan; approval_required before external CI changes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="Without test evidence, completion claims remain unsupported.",
                safe_next_action="Stage a test strategy proposal with the smallest local verification command.",
            )
        )
    if _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "graphql_schema", "protobuf_schema"}) and not _has_contract_tests(files):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="API contract signals exist without contract test evidence.",
                domain="api_integrations",
                gate="api_contract_source_present",
                artifact="api-contract-review.md",
                evidence_required=["contract source", "consumer impact", "contract test command", "compatibility notes"],
                evidence_owner="API owner",
                approval_boundary="approval_required before external API writes or breaking contract changes",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="A contract file does not prove consumers remain compatible.",
                safe_next_action="Stage an API contract review before changing implementation or release behavior.",
            )
        )
    if _has_signal(observed, "database_migration_or_schema"):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Database migration or schema signals were detected.",
                domain="database_data",
                gate="database_migration_plan_present",
                artifact="database-migration-plan.md",
                evidence_required=["ordered migration steps", "dry run command", "rollback or compensation", "owner approval"],
                evidence_owner="data owner",
                approval_boundary="approval_required before production database access or migration execution",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="Artifact presence does not prove the migration is safe.",
                safe_next_action="Stage a migration plan proposal without connecting to production data.",
            )
        )
    if complexity_profile == "high_risk":
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="High-risk security, privacy, payment, compliance or sensitive-data intent was detected.",
                domain="security_privacy_compliance",
                gate="security_risk_review_present",
                artifact="security-risk-review.md",
                evidence_required=["threat surface", "auth or data impact", "tests", "rollback", "owner review"],
                evidence_owner="security or product owner",
                approval_boundary="approval_required before touching secrets, payment, auth, PII or production data",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="Intent classification does not prove all security requirements are known.",
                safe_next_action="Stage a security risk review and list unknowns before implementation.",
            )
        )
    if _mentions_any(intent, DELIVERY_INTENT_TERMS) or _has_any_signal(
        observed,
        {"ci_configuration", "deployment_configuration", "release_file"},
    ):
        recommendations.append(
            _recommendation(
                priority="P1_high_risk",
                reason="Production, release, CI or deployment signals were detected.",
                domain="delivery_release_operations",
                gate="release_evidence_present",
                artifact="release-readiness.md",
                evidence_required=["build command", "test evidence", "artifact manifest", "rollback", "owner approval"],
                evidence_owner="release operator",
                approval_boundary="approval_required before publish, tag, deploy or release creation",
                accepted_gap_option="explicit_gap_accepted with owner, reason, residual risk and review date",
                residual_risk="CI or deployment files do not prove the release is ready.",
                safe_next_action="Stage release readiness evidence before external release actions.",
            )
        )
    return recommendations


def _recommendation(
    *,
    priority: str,
    reason: str,
    domain: str,
    gate: str,
    artifact: str,
    evidence_required: list[str],
    evidence_owner: str,
    approval_boundary: str,
    accepted_gap_option: str,
    residual_risk: str,
    safe_next_action: str,
) -> dict[str, Any]:
    return {
        "priority": priority,
        "reason": reason,
        "domain": domain,
        "gate": gate,
        "artifact": artifact,
        "evidence_required": evidence_required,
        "evidence_owner": evidence_owner,
        "approval_boundary": approval_boundary,
        "accepted_gap_option": accepted_gap_option,
        "residual_risk": residual_risk,
        "safe_next_action": safe_next_action,
    }


def _prioritize_recommendations(recommendations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        recommendations,
        key=lambda recommendation: (
            PRIORITY_ORDER.get(str(recommendation.get("priority", "not_applicable")), 99),
            str(recommendation.get("domain", "")),
            str(recommendation.get("gate", "")),
        ),
    )


def _delivery_map(
    files: set[str],
    directories: set[str],
    observed: list[dict[str, Any]],
    methodology_domains: list[dict[str, Any]],
    recommendations: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "surface_map": {
            "ui": _has_any_signal(observed, {"stack_manifest"}) and bool(files & {"package.json"}),
            "api": _has_any_signal(observed, {"openapi_contract", "asyncapi_contract", "graphql_schema", "protobuf_schema"}),
            "data": _has_signal(observed, "database_migration_or_schema"),
            "ai": _has_signal(observed, "ai_eval_or_rag"),
            "delivery": _has_any_signal(observed, {"ci_configuration", "deployment_configuration"}),
        },
        "system_map": {
            "files_observed": len(files),
            "directories_observed": len(directories),
            "control_plane_present": [name for name in CONTROL_PLANE_FILES if name.lower() in files],
        },
        "lifecycle_map": {
            "write_policy": "read_only",
            "artifact_strategy": "stage proposals before workspace writes",
        },
        "methodology_map": {
            packet["id"]: packet["status"]
            for packet in methodology_domains
            if packet["status"] != "not_applicable"
        },
        "next_action_map": [recommendation["safe_next_action"] for recommendation in recommendations[:5]],
    }


def _unknowns(files: set[str], directories: set[str], observed: list[dict[str, Any]]) -> list[str]:
    unknowns: list[str] = []
    if not _has_test_signal(files, observed):
        unknowns.append("current verification command")
    if not any(name in files for name in {"requirements.md", "plan.md"}):
        unknowns.append("accepted scope and implementation plan")
    if directories or files:
        unknowns.append("artifact owners and approval boundaries")
    return unknowns


def _questions_for_owner(
    files: set[str],
    directories: set[str],
    observed: list[dict[str, Any]],
    recommendations: list[dict[str, Any]],
) -> list[str]:
    questions = ["What is the smallest safe next artifact to stage?"]
    if not _has_test_signal(files, observed):
        questions.append("Which local command is the source of truth for verification?")
    if recommendations:
        questions.append("Who owns the highest-priority missing methodology gate?")
    if directories or files:
        questions.append("Which detected surfaces are in scope for this slice?")
    return questions


def _provisional_assumptions(files: set[str], intent: str) -> list[str]:
    assumptions = ["Audit is read-only and does not approve workspace writes."]
    if not files:
        assumptions.append("Empty workspace means methodology recommendations are provisional.")
    if intent:
        assumptions.append("Intent hint is routing context, not observed repository evidence.")
    return assumptions


def _safe_next_action(recommendations: list[dict[str, Any]]) -> str:
    if recommendations:
        return recommendations[0]["safe_next_action"]
    return "Record methodology audit output and proceed only with evidence-backed planning."


def _observed_domain_ids(observed: list[dict[str, Any]]) -> set[str]:
    mapping = {
        "test_evidence": "quality_testing_evals",
        "test_command": "quality_testing_evals",
        "openapi_contract": "api_integrations",
        "asyncapi_contract": "api_integrations",
        "graphql_schema": "api_integrations",
        "protobuf_schema": "api_integrations",
        "database_migration_or_schema": "database_data",
        "ai_eval_or_rag": "llm_ai_rag",
        "ci_configuration": "delivery_release_operations",
        "deployment_configuration": "delivery_release_operations",
        "release_file": "delivery_release_operations",
        "docs_or_control_plane": "codex_agentic_workflow",
    }
    return {mapping[signal["id"]] for signal in observed if signal["id"] in mapping}


def _has_package_test_script(root: Path) -> bool:
    package_file = root / "package.json"
    if not package_file.is_file():
        return False
    try:
        data = json.loads(package_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    scripts = data.get("scripts") if isinstance(data, dict) else None
    return isinstance(scripts, dict) and isinstance(scripts.get("test"), str) and bool(scripts["test"].strip())


def _has_test_command_or_evidence(root: Path, files: set[str], observed: list[dict[str, Any]]) -> bool:
    return _has_test_signal(files, observed) or _has_package_test_script(root)


def _has_test_signal(files: set[str], observed: list[dict[str, Any]]) -> bool:
    return _has_any_signal(observed, {"test_evidence", "test_command"}) or any(
        "test" in path or path.startswith("evals/") for path in files
    )


def _has_contract_tests(files: set[str]) -> bool:
    return any("contract" in path and "test" in path for path in files)


def _has_signal(observed: list[dict[str, Any]], signal_id: str) -> bool:
    return any(signal["id"] == signal_id for signal in observed)


def _has_any_signal(observed: list[dict[str, Any]], signal_ids: set[str]) -> bool:
    return any(signal["id"] in signal_ids for signal in observed)


def _mentions_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def _is_openapi(path: str) -> bool:
    return path in OPENAPI_MARKERS or path.startswith("openapi/") or path.endswith(("/openapi.yaml", "/openapi.yml", "/openapi.json"))


def _is_asyncapi(path: str) -> bool:
    return path in ASYNCAPI_MARKERS or path.startswith("asyncapi/") or path.endswith(("/asyncapi.yaml", "/asyncapi.yml", "/asyncapi.json"))
