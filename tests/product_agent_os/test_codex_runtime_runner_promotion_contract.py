import copy
import json
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "tests" / "fixtures" / "product_agent_os" / "batch45" / "promotion-contract"
T18_DESIGN = ROOT / "docs" / "superpowers" / "specs" / "batch45-postq4-t18-promotion-grade-eval-design.json"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner import model_output  # noqa: E402
from codex_runtime_runner.promotion_contract import (  # noqa: E402
    PRIMARY_RESULT_SCHEMA,
    PROMOTION_CONTRACT_VERSION,
    QuarantinedPrimaryResult,
    ValidatedPrimaryResult,
    normalize_primary_result,
    parse_primary_result,
    validate_primary_result,
)


class CodexRuntimeRunnerPromotionContractTest(unittest.TestCase):
    def test_runtime_schema_and_valid_fixture_match_t18_public_contract(self):
        design = json.loads(T18_DESIGN.read_text(encoding="utf-8"))
        payload = self._fixture("valid-primary-result.json")

        self.assertEqual(design["strict_output_schema"]["root_schema"], PRIMARY_RESULT_SCHEMA)
        result = parse_primary_result(payload)
        self.assertIsInstance(result, ValidatedPrimaryResult)
        self.assertEqual(PROMOTION_CONTRACT_VERSION, result.payload["schema_version"])
        self.assertEqual((), result.normalization_paths)

    def test_narrow_frozen_status_alias_table_only_strips_and_lowercases(self):
        payload = self._fixture("status-alias-pass.json")

        result = parse_primary_result(payload)

        self.assertIsInstance(result, ValidatedPrimaryResult)
        self.assertEqual("passed", result.payload["tests_or_checks"][0]["status"])
        self.assertEqual(("tests_or_checks[0].status",), result.normalization_paths)
        self.assertEqual("PASS", payload["tests_or_checks"][0]["status"])
        cases = (
            ("pass", "passed"),
            ("passed", "passed"),
            ("fail", "failed"),
            ("failed", "failed"),
            ("skip", "skipped"),
            ("skipped", "skipped"),
            ("not_run", "not_run_with_gap"),
            ("not_run_with_gap", "not_run_with_gap"),
            ("  PASS  ", "passed"),
        )

        for raw_status, canonical_status in cases:
            with self.subTest(raw_status=raw_status):
                payload = self._fixture("valid-primary-result.json")
                payload["tests_or_checks"][0]["status"] = raw_status

                normalized, paths = normalize_primary_result(payload)

                self.assertEqual(canonical_status, normalized["tests_or_checks"][0]["status"])
                expected_paths = () if raw_status == canonical_status else ("tests_or_checks[0].status",)
                self.assertEqual(expected_paths, paths)
                self.assertEqual(raw_status, payload["tests_or_checks"][0]["status"])
                self.assertEqual((), validate_primary_result(normalized))

    def test_unsupported_status_aliases_remain_quarantined(self):
        for unsupported in ("ok", "green", "complete", "not run", "not-run", "not__run", "NOT---__RUN"):
            with self.subTest(status=unsupported):
                payload = self._fixture("valid-primary-result.json")
                payload["tests_or_checks"][0]["status"] = unsupported

                result = parse_primary_result(payload)

                self._assert_quarantined(
                    result,
                    reason="schema_validation_failed",
                    error="tests_or_checks[0].status:enum_mismatch",
                )

    def test_unknown_status_is_quarantined_with_path_specific_enum_error(self):
        payload = self._fixture("unknown-test-status.json")

        result = parse_primary_result(payload)

        self.assertIsInstance(result, QuarantinedPrimaryResult)
        self.assertEqual("schema_validation_failed", result.reason)
        self.assertIn("tests_or_checks[0].status:enum_mismatch", result.errors)
        self.assertFalse(hasattr(result, "payload"))
        self.assertFalse(hasattr(result, "behavior_score"))

    def test_root_and_nested_required_fields_use_stable_missing_errors(self):
        payload = self._fixture("valid-primary-result.json")
        required_fields = (
            "schema_version",
            "corpus_id",
            "corpus_version",
            "task_id",
            "arm",
            "model_id",
            "model_reasoning_effort",
            "result_class",
            "changed_files",
            "behavior_score",
            "dimension_scores",
            "evidence_summary",
            "tests_or_checks",
            "unsupported_claims",
            "privacy_safety",
            "final_summary_retention",
        )

        for field in required_fields:
            with self.subTest(field=field):
                mutated = copy.deepcopy(payload)
                del mutated[field]

                self.assertIn(f"{field}:missing", validate_primary_result(mutated))
        cases = (
            (("changed_files", 0, "path"), "changed_files[0].path:missing"),
            (("changed_files", 0, "change_type"), "changed_files[0].change_type:missing"),
            (("tests_or_checks", 0, "name"), "tests_or_checks[0].name:missing"),
            (("tests_or_checks", 0, "status"), "tests_or_checks[0].status:missing"),
            (("privacy_safety", "raw_private_source_body_retained"), "privacy_safety.raw_private_source_body_retained:missing"),
            (("privacy_safety", "secret_or_unredacted_pii_retained"), "privacy_safety.secret_or_unredacted_pii_retained:missing"),
            (("privacy_safety", "raw_private_chat_retained"), "privacy_safety.raw_private_chat_retained:missing"),
        )
        cases += tuple(
            (("dimension_scores", field), f"dimension_scores.{field}:missing")
            for field in payload["dimension_scores"]
        )

        for path, expected in cases:
            with self.subTest(path=path):
                mutated = copy.deepcopy(payload)
                self._delete_at(mutated, path)

                self.assertIn(expected, validate_primary_result(mutated))

    def test_closed_objects_reject_unknown_fields_at_stable_paths(self):
        payload = self._fixture("valid-primary-result.json")
        cases = (
            ((), "unexpected", "unexpected:unknown_field"),
            (("changed_files", 0), "unexpected", "changed_files[0].unexpected:unknown_field"),
            (("dimension_scores",), "unexpected", "dimension_scores.unexpected:unknown_field"),
            (("tests_or_checks", 0), "unexpected", "tests_or_checks[0].unexpected:unknown_field"),
            (("privacy_safety",), "unexpected", "privacy_safety.unexpected:unknown_field"),
        )

        for path, key, expected in cases:
            with self.subTest(path=path):
                mutated = copy.deepcopy(payload)
                target = self._value_at(mutated, path)
                target[key] = "synthetic"

                self.assertIn(expected, validate_primary_result(mutated))

    def test_type_and_array_corruption_use_stable_expected_type_errors(self):
        cases = (
            ((), [], "root:expected_object"),
            (("changed_files",), {}, "changed_files:expected_array"),
            (("changed_files", 0), "not-an-object", "changed_files[0]:expected_object"),
            (("dimension_scores",), [], "dimension_scores:expected_object"),
            (("evidence_summary",), 1, "evidence_summary:expected_string"),
            (("behavior_score",), True, "behavior_score:expected_number"),
            (("dimension_scores", "existing_capability_scan"), True, "dimension_scores.existing_capability_scan:expected_integer"),
            (("privacy_safety", "raw_private_chat_retained"), 1, "privacy_safety.raw_private_chat_retained:expected_boolean"),
            (("tests_or_checks",), {}, "tests_or_checks:expected_array"),
            (("tests_or_checks", 0), "not-an-object", "tests_or_checks[0]:expected_object"),
            (("unsupported_claims", 0), 1, "unsupported_claims[0]:expected_string"),
        )

        for path, value, expected in cases:
            with self.subTest(path=path):
                if not path:
                    mutated = value
                else:
                    mutated = self._fixture("valid-primary-result.json")
                if path == ("unsupported_claims", 0):
                    mutated["unsupported_claims"] = [1]
                elif path:
                    self._set_at(mutated, path, value)

                self.assertIn(expected, validate_primary_result(mutated))

    def test_all_enum_surfaces_reject_unknown_values(self):
        cases = (
            (("schema_version",), "v999", "schema_version:enum_mismatch"),
            (("corpus_id",), "synthetic-unknown", "corpus_id:enum_mismatch"),
            (("corpus_version",), "v999", "corpus_version:enum_mismatch"),
            (("task_id",), "synthetic-unknown", "task_id:enum_mismatch"),
            (("arm",), "control", "arm:enum_mismatch"),
            (("model_reasoning_effort",), "ultra", "model_reasoning_effort:enum_mismatch"),
            (("result_class",), "success", "result_class:enum_mismatch"),
            (("changed_files", 0, "change_type"), "X", "changed_files[0].change_type:enum_mismatch"),
            (("tests_or_checks", 0, "status"), "unknown", "tests_or_checks[0].status:enum_mismatch"),
            (("final_summary_retention",), "raw_repo", "final_summary_retention:enum_mismatch"),
        )

        for path, value, expected in cases:
            with self.subTest(path=path):
                mutated = self._fixture("valid-primary-result.json")
                self._set_at(mutated, path, value)

                self.assertIn(expected, validate_primary_result(mutated))

    def test_numeric_bounds_and_string_lengths_use_stable_errors(self):
        cases = (
            (("behavior_score",), -0.01, "behavior_score:below_minimum"),
            (("behavior_score",), 1.01, "behavior_score:above_maximum"),
            (("behavior_score",), 10**400, "behavior_score:above_maximum"),
            (("dimension_scores", "flake_cost_control"), -1, "dimension_scores.flake_cost_control:below_minimum"),
            (("dimension_scores", "flake_cost_control"), 11, "dimension_scores.flake_cost_control:above_maximum"),
            (("model_id",), "", "model_id:min_length"),
            (("changed_files", 0, "path"), "", "changed_files[0].path:min_length"),
            (("evidence_summary",), "", "evidence_summary:min_length"),
            (("evidence_summary",), "x" * 2001, "evidence_summary:max_length"),
            (("tests_or_checks", 0, "name"), "", "tests_or_checks[0].name:min_length"),
        )

        for path, value, expected in cases:
            with self.subTest(path=path):
                mutated = self._fixture("valid-primary-result.json")
                self._set_at(mutated, path, value)

                self.assertIn(expected, validate_primary_result(mutated))

        mutated = self._fixture("valid-primary-result.json")
        mutated["unsupported_claims"] = [""]
        self.assertIn("unsupported_claims[0]:min_length", validate_primary_result(mutated))

        for value in (math.nan, math.inf, -math.inf):
            with self.subTest(non_finite=value):
                mutated = self._fixture("valid-primary-result.json")
                mutated["behavior_score"] = value
                self.assertIn("behavior_score:expected_number", validate_primary_result(mutated))

    def test_result_class_material_privacy_and_retention_quarantine_policies(self):
        for result_class in ("no_op", "invalid_json", "schema_validation_failed", "timeout", "runner_error"):
            with self.subTest(result_class=result_class):
                payload = self._fixture("valid-primary-result.json")
                payload["result_class"] = result_class

                result = parse_primary_result(payload)

                self._assert_quarantined(result, reason=result_class)
        payload = self._fixture("valid-primary-result.json")
        payload["changed_files"] = []

        result = parse_primary_result(payload, material_change_required=True)

        self._assert_quarantined(result, reason="no_op")

        for flag in (
            "raw_private_source_body_retained",
            "secret_or_unredacted_pii_retained",
            "raw_private_chat_retained",
        ):
            with self.subTest(privacy_flag=flag):
                payload = self._fixture("valid-primary-result.json")
                payload["privacy_safety"][flag] = True

                result = parse_primary_result(payload)

                self._assert_quarantined(
                    result,
                    reason="privacy_safety_violation",
                    error=f"privacy_safety.{flag}:must_be_false",
                )

        payload = self._fixture("valid-primary-result.json")
        payload["final_summary_retention"] = "retention_violation_quarantine"
        self._assert_quarantined(
            parse_primary_result(payload),
            reason="retention_violation_quarantine",
        )

    def test_final_json_gateway_preserves_error_suffixes_and_validated_type(self):
        cases = (
            ("{}", "marker_missing"),
            ("FINAL_JSON: {}\nFINAL_JSON: {}", "multiple_markers"),
            ("FINAL_JSON: {not-json", "invalid_json"),
            ("FINAL_JSON: {} trailing", "trailing_content"),
            ("FINAL_JSON: []", "not_object"),
        )

        for text, suffix in cases:
            with self.subTest(suffix=suffix):
                result = model_output.extract_promotion_result(text)

                self._assert_quarantined(result, reason="invalid_json", error=f"final_json:{suffix}")
        payload = self._fixture("valid-primary-result.json")

        result = model_output.extract_promotion_result(f"progress\nFINAL_JSON: {json.dumps(payload)}")

        self.assertIsInstance(result, ValidatedPrimaryResult)
        self.assertEqual(payload, result.payload)

    def test_promotion_pair_classifier_enforces_gateway_and_score_boundary(self):
        invalid_payload = self._fixture("unknown-test-status.json")
        valid_payload = self._fixture("valid-primary-result.json")
        baseline = parse_primary_result(invalid_payload)
        treatment = parse_primary_result(valid_payload)

        with self.subTest(route="quarantined_arm"):
            pair = model_output.classify_promotion_pair(baseline, treatment)
            self.assertEqual(
                {
                    "pair_valid_for_scoring": False,
                    "invalid_reason": "baseline_schema_validation_failed",
                    "score_delta": None,
                    "reviewer_required": False,
                },
                pair,
            )

        with self.subTest(route="plain_dict_bypass"):
            with self.assertRaises(TypeError):
                model_output.classify_promotion_pair(valid_payload, valid_payload)

        baseline_payload = self._fixture("valid-primary-result.json")
        treatment_payload = copy.deepcopy(baseline_payload)
        treatment_payload["arm"] = "treatment"
        treatment_payload["behavior_score"] = 0.9
        baseline = parse_primary_result(baseline_payload)
        treatment = parse_primary_result(treatment_payload)

        with self.subTest(route="validated_score"):
            pair = model_output.classify_promotion_pair(baseline, treatment)
            self.assertEqual(
                {
                    "pair_valid_for_scoring": True,
                    "invalid_reason": None,
                    "score_delta": 0.15000000000000002,
                    "reviewer_required": True,
                },
                pair,
            )

    def test_pair_classifier_revalidates_forged_and_mutated_gateway_payloads(self):
        treatment_payload = self._fixture("valid-primary-result.json")
        treatment_payload["arm"] = "treatment"
        treatment = parse_primary_result(treatment_payload)

        with self.subTest(bypass="forged_dataclass"):
            forged = ValidatedPrimaryResult({"behavior_score": 0.1}, ())
            pair = model_output.classify_promotion_pair(forged, treatment)
            self._assert_invalid_pair(pair, "baseline_schema_validation_failed")

        with self.subTest(bypass="nested_post_parse_mutation"):
            baseline = parse_primary_result(self._fixture("valid-primary-result.json"))
            baseline.payload["tests_or_checks"][0]["status"] = "forged_after_validation"
            pair = model_output.classify_promotion_pair(baseline, treatment)
            self._assert_invalid_pair(pair, "baseline_schema_validation_failed")

    def test_pair_classifier_enforces_arm_and_comparability_invariants(self):
        cases = (
            ("baseline_arm_mismatch", {"arm": "treatment"}, {}),
            ("treatment_arm_mismatch", {}, {"arm": "baseline"}),
            ("task_id_mismatch", {}, {"task_id": "B45-POSTQ4-H2-ARTIFACT-COMPATIBILITY"}),
            ("corpus_id_mismatch", {}, {"corpus_id": "synthetic-other-corpus"}),
            ("corpus_version_mismatch", {}, {"corpus_version": "synthetic-other-version"}),
            ("model_id_mismatch", {}, {"model_id": "synthetic-other-model"}),
            ("model_reasoning_effort_mismatch", {}, {"model_reasoning_effort": "high"}),
        )

        for reason, baseline_updates, treatment_updates in cases:
            with self.subTest(reason=reason):
                baseline = parse_primary_result(self._fixture("valid-primary-result.json"))
                treatment_payload = self._fixture("valid-primary-result.json")
                treatment_payload["arm"] = "treatment"
                treatment = parse_primary_result(treatment_payload)
                baseline.payload.update(baseline_updates)
                treatment.payload.update(treatment_updates)

                pair = model_output.classify_promotion_pair(baseline, treatment)

                self._assert_invalid_pair(pair, reason)

    def test_seeded_corruption_table_maps_each_fault_class_to_stable_output(self):
        cases = (
            ("missing", lambda value: value.pop("schema_version"), "schema_version:missing", None),
            ("unknown", lambda value: value.__setitem__("unexpected", True), "unexpected:unknown_field", None),
            ("type", lambda value: value.__setitem__("changed_files", {}), "changed_files:expected_array", None),
            ("enum", lambda value: value.__setitem__("arm", "control"), "arm:enum_mismatch", None),
            ("range", lambda value: value.__setitem__("behavior_score", 2), "behavior_score:above_maximum", None),
            ("length", lambda value: value.__setitem__("model_id", ""), "model_id:min_length", None),
            ("quarantine", lambda value: value.__setitem__("result_class", "timeout"), None, "timeout"),
        )

        for fault_class, corrupt, expected_error, expected_reason in cases:
            with self.subTest(fault_class=fault_class):
                payload = self._fixture("valid-primary-result.json")
                corrupt(payload)

                result = parse_primary_result(payload)

                self._assert_quarantined(
                    result,
                    reason=expected_reason or "schema_validation_failed",
                    error=expected_error,
                )

    def _assert_quarantined(self, result, *, reason: str, error: str | None = None) -> None:
        self.assertIsInstance(result, QuarantinedPrimaryResult)
        self.assertEqual(reason, result.reason)
        if error is not None:
            self.assertIn(error, result.errors)
        self.assertFalse(hasattr(result, "payload"))
        self.assertFalse(hasattr(result, "behavior_score"))

    def _assert_invalid_pair(self, pair, reason: str) -> None:
        self.assertEqual(
            {
                "pair_valid_for_scoring": False,
                "invalid_reason": reason,
                "score_delta": None,
                "reviewer_required": False,
            },
            pair,
        )

    def _value_at(self, payload, path):
        value = payload
        for part in path:
            value = value[part]
        return value

    def _set_at(self, payload, path, value) -> None:
        parent = self._value_at(payload, path[:-1])
        parent[path[-1]] = value

    def _delete_at(self, payload, path) -> None:
        parent = self._value_at(payload, path[:-1])
        del parent[path[-1]]

    def _fixture(self, name: str) -> dict[str, object]:
        return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
