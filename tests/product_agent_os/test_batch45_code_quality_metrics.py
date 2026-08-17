import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
TEMPLATE = ROOT / "plugins" / "product-agent-os" / "assets" / "templates" / "evals" / "code-quality-metrics.json"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.promotion_contract import evaluate_deterministic_promotion  # noqa: E402
from product_agent_os.code_quality_metrics import (  # noqa: E402
    METRICS_SCHEMA_VERSION,
    MetricsContractError,
    evaluate_code_quality_metrics,
)


def passed_evidence():
    return {
        "acceptance": {"status": "passed"},
        "regression": {"status": "passed"},
        "seeded_faults": {"status": "passed"},
        "reviewer": {"status": "passed", "verdict": "approve"},
        "dependency": {"status": "passed"},
        "performance": {"applicable": False, "status": "not_applicable"},
        "cost_latency": {"applicable": False, "status": "not_applicable"},
        "patch": {"changed_lines": 40, "test_changed_lines": 30, "dependency_delta_count": 0},
        "diagnostic_self_scores": {"behavior_score": 0.1},
    }


class Batch45CodeQualityMetricsTest(unittest.TestCase):
    def test_all_required_evidence_can_reach_ready_decision(self):
        result = evaluate_deterministic_promotion(passed_evidence())

        self.assertTrue(result["promotion_allowed"])
        self.assertEqual("promotion_evidence_ready", result["decision"])
        self.assertEqual(METRICS_SCHEMA_VERSION, result["schema_version"])
        self.assertFalse(result["diagnostics"]["self_scores_affect_promotion"])

    def test_missing_required_evidence_blocks_without_becoming_zero(self):
        evidence = passed_evidence()
        del evidence["seeded_faults"]

        result = evaluate_code_quality_metrics(evidence)

        self.assertFalse(result["promotion_allowed"])
        self.assertIn("seeded_faults:missing", result["blockers"])
        self.assertEqual("missing", result["signals"]["seeded_faults"]["status"])

    def test_self_score_and_single_proxy_cannot_override_regression(self):
        evidence = passed_evidence()
        evidence["regression"]["status"] = "failed"
        evidence["diagnostic_self_scores"] = {"behavior_score": 1.0, "dimension_scores": {"all": 10}}

        result = evaluate_code_quality_metrics(evidence)

        self.assertFalse(result["promotion_allowed"])
        self.assertIn("regression:failed", result["blockers"])
        self.assertEqual(1.0, result["diagnostics"]["model_self_scores"]["behavior_score"])

    def test_applicable_performance_and_cost_evidence_are_required(self):
        for gate in ("performance", "cost_latency"):
            with self.subTest(gate=gate):
                evidence = passed_evidence()
                evidence[gate] = {"applicable": True, "status": "missing"}
                result = evaluate_code_quality_metrics(evidence)
                self.assertIn(f"{gate}:missing", result["blockers"])

    def test_not_applicable_is_rejected_for_required_gate(self):
        evidence = passed_evidence()
        evidence["acceptance"]["status"] = "not_applicable"

        with self.assertRaisesRegex(MetricsContractError, "not_applicable_for_required_gate"):
            evaluate_code_quality_metrics(evidence)

    def test_patch_anomalies_warn_but_do_not_promote_or_block_alone(self):
        evidence = passed_evidence()
        evidence["patch"] = {"changed_lines": 600, "test_changed_lines": 1300, "dependency_delta_count": 0}
        result = evaluate_code_quality_metrics(evidence)

        self.assertTrue(result["promotion_allowed"])
        self.assertEqual(["patch_size_anomaly", "test_churn_anomaly"], result["warnings"])

    def test_input_is_not_mutated_and_template_is_valid(self):
        evidence = passed_evidence()
        before = copy.deepcopy(evidence)
        evaluate_code_quality_metrics(evidence)
        self.assertEqual(before, evidence)

        template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(METRICS_SCHEMA_VERSION, template["schema_version"])
        self.assertIn("model self-scores are diagnostic only and cannot affect promotion_allowed", template["decision_rules"])


if __name__ == "__main__":
    unittest.main()
