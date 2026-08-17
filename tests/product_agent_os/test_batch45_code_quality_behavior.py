import ast
import json
import re
import sys
import unittest
from dataclasses import FrozenInstanceError, fields, is_dataclass, replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
TEMPLATE_ROOT = ROOT / "plugins" / "product-agent-os" / "assets" / "templates"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.code_quality_selector import (  # noqa: E402
    CategoryProfile,
    CodeQualityProfile,
    DeclaredToolSignal,
    ProjectCommandSignal,
    ProjectInventory,
    ProjectUtilityProfile,
    StackProfile,
    ToolEvidence,
    code_quality_profile_as_dict,
    select_code_quality_profile,
)


class Batch45CodeQualitySelectorTracerTest(unittest.TestCase):
    def test_quality_strategy_template_leads_with_risk_contract_and_keeps_legacy(self):
        strategy_path = TEMPLATE_ROOT / "artifact-templates" / "quality-strategy.md"
        text = strategy_path.read_text(encoding="utf-8")
        normalized_text = text.replace("`", "").lower()
        section_headings = tuple(
            line for line in text.splitlines() if line.startswith("## ")
        )
        self.assertTrue(section_headings)
        self.assertEqual(section_headings[0], "## Risk-Based Code Strategy")

        strategy_start = text.index("## Risk-Based Code Strategy")
        strategy_end = next(
            (
                index
                for index in range(strategy_start + 1, len(text))
                if text.startswith("\n## ", index)
            ),
            len(text),
        )
        strategy_section = text[strategy_start:strategy_end]
        normalized_strategy = strategy_section.replace("`", "").lower()
        self.assertIn("schema_version", normalized_strategy)
        self.assertIn("quality_strategy_v1", normalized_strategy)
        self.assertIn("profile_schema_version", normalized_strategy)
        self.assertIn("code_quality_profile_v1", normalized_strategy)

        expected_subheadings = (
            "### Test-First Decision",
            "### Risk-To-Test Decisions",
            "### Coverage Decision",
            "### Comment Decision",
            "### Performance Decision",
            "### Strategy Gaps",
            "### Selection Evidence Ceiling",
        )
        self.assertEqual(
            tuple(
                line
                for line in strategy_section.splitlines()
                if line.startswith("### ")
            ),
            expected_subheadings,
        )
        for table_header in (
            "| status | risk_ids | reason |",
            "| test_kind | status | risk_ids | protected_invariants | rationale |",
            "| status | risk_ids | reasons | rationale |",
            "| status | risk_ids | rationale |",
        ):
            with self.subTest(table_header=table_header):
                self.assertIn(table_header, normalized_strategy)

        coverage_start = normalized_strategy.index("### coverage decision")
        coverage_end = normalized_strategy.index("### comment decision")
        coverage_section = normalized_strategy[coverage_start:coverage_end]
        self.assertIn("status: not_applicable", coverage_section)
        self.assertIn(
            "reason: coverage is telemetry, not a correctness target",
            coverage_section,
        )

        ceiling_start = normalized_strategy.index("### selection evidence ceiling")
        ceiling_section = normalized_strategy[ceiling_start:]
        self.assertIn(
            "evidence_ceiling: strategy selection only; tests, comments and benchmarks not executed or verified",
            ceiling_section,
        )
        self.assertIn("tests_executed: false", ceiling_section)
        self.assertIn("benchmarks_executed: false", ceiling_section)

        legacy_headings = (
            "# Quality Strategy",
            "## Scope",
            "## Current Evidence",
            "## Risk Based Scope",
            "## Professional Code Quality Evidence",
            "## Backend Runtime Evidence",
            "## Quality Gate References",
            "## Unsupported Claims",
            "## Accepted Gap",
            "## Residual Risk",
            "## Approval Boundary",
            "## Verification",
            "## Rollback",
            "## Test Data Privacy",
        )
        legacy_markers = (
            "quality_strategy_present",
            "risk_based_scope_present",
            "test_first_or_gap_present",
            "acceptance_traceability_present",
            "contract_check_present",
            "runtime_evidence_present",
            "manual_qa_evidence_present",
            "visual_a11y_evidence_present",
            "eval_spec_present",
            "eval_rerun_evidence_present",
            "current_evidence_before_completion",
            "ci_quality_gate_present",
            "flaky_test_policy_present",
            "coverage_policy_present",
            "test_data_privacy_present",
            "bug_reproduction_evidence_present",
            "regression_impact_present",
            "professional_code_authoring_evidence_present",
        )
        for legacy_value in (*legacy_headings, *legacy_markers):
            with self.subTest(legacy_value=legacy_value):
                self.assertIn(legacy_value.lower(), normalized_text)

    def test_pure_logic_risk_selects_only_unit_evidence(self):
        from product_agent_os.test_strategy_selector import (
            ChangeRisk,
            CommentDecision,
            CommentSignal,
            CoverageDecision,
            PerformanceDecision,
            QualityStrategy,
            TestDecision,
            TestFirstDecision,
            TestStrategyRequest,
            quality_strategy_as_dict,
            select_test_strategy,
        )

        profile = select_code_quality_profile(
            ProjectInventory(
                paths=("pyproject.toml",),
                declared_tools=(
                    DeclaredToolSignal("black", "pyproject.toml"),
                    DeclaredToolSignal("ruff", "pyproject.toml"),
                    DeclaredToolSignal("mypy", "pyproject.toml"),
                    DeclaredToolSignal("pytest", "pyproject.toml"),
                    DeclaredToolSignal("hatch", "pyproject.toml"),
                ),
                project_commands=(),
            )
        )
        risk_id = "pure-logic-normalization"
        invariant = "equivalent inputs produce the same normalized profile"
        strategy = select_test_strategy(
            TestStrategyRequest(
                profile=profile,
                change_mode="refactor",
                executable_test_seam=True,
                test_seam_reason="",
                risks=(
                    ChangeRisk(
                        risk_id=risk_id,
                        kind="pure_logic",
                        description="normalization may change deterministic selection",
                        protected_invariants=(invariant,),
                        languages=("python",),
                    ),
                ),
                comment_signals=(),
            )
        )

        self.assertIsInstance(strategy, QualityStrategy)
        self.assertIsInstance(strategy.test_first_decision, TestFirstDecision)
        self.assertIsInstance(strategy.coverage_decision, CoverageDecision)
        self.assertIsInstance(strategy.comment_decision, CommentDecision)
        self.assertIsInstance(strategy.performance_decision, PerformanceDecision)
        self.assertEqual(strategy.schema_version, "quality_strategy_v1")
        self.assertEqual(strategy.profile_schema_version, "code_quality_profile_v1")
        expected_test_kinds = (
            "unit",
            "property",
            "characterization",
            "contract_integration",
            "end_to_end",
            "mutation",
            "benchmark",
        )
        self.assertEqual(
            tuple(decision.test_kind for decision in strategy.test_decisions),
            expected_test_kinds,
        )
        decision = strategy.test_decisions[0]
        self.assertIsInstance(decision, TestDecision)
        self.assertEqual(decision.test_kind, "unit")
        self.assertEqual(decision.status, "required")
        self.assertEqual(decision.risk_ids, (risk_id,))
        self.assertEqual(decision.protected_invariants, (invariant,))
        self.assertEqual(strategy.test_first_decision.status, "required")
        self.assertEqual(strategy.test_first_decision.risk_ids, (risk_id,))
        for deferred in strategy.test_decisions[1:]:
            with self.subTest(deferred_test_kind=deferred.test_kind):
                self.assertEqual(deferred.status, "not_applicable")
                self.assertFalse(deferred.risk_ids)
                self.assertFalse(deferred.protected_invariants)
                self.assertEqual(
                    deferred.rationale,
                    f"no_changed_risk_requires_{deferred.test_kind}",
                )
        self.assertEqual(strategy.coverage_decision.status, "not_applicable")
        self.assertEqual(strategy.comment_decision.status, "not_applicable")
        self.assertEqual(
            strategy.comment_decision.rationale,
            "no non-obvious comment trigger was supplied",
        )
        self.assertEqual(strategy.performance_decision.status, "not_applicable")
        self.assertEqual(
            strategy.evidence_ceiling,
            "strategy selection only; tests, comments and benchmarks not executed or verified",
        )

        payload = quality_strategy_as_dict(strategy)
        self.assertEqual(
            tuple(payload),
            (
                "schema_version",
                "profile_schema_version",
                "test_first_decision",
                "test_decisions",
                "coverage_decision",
                "comment_decision",
                "performance_decision",
                "gaps",
                "evidence_ceiling",
            ),
        )

    def test_strategy_routes_frozen_risks_comments_and_optional_evidence(self):
        from product_agent_os.test_strategy_selector import (
            ChangeRisk,
            CommentSignal,
            TestStrategyRequest,
            quality_strategy_as_dict,
            select_test_strategy,
        )

        test_order = (
            "unit",
            "property",
            "characterization",
            "contract_integration",
            "end_to_end",
            "mutation",
            "benchmark",
        )
        risk_mappings = (
            ("pure_logic", "unit"),
            ("property_invariant", "property"),
            ("legacy_behavior", "characterization"),
            ("external_boundary", "contract_integration"),
            ("critical_user_flow", "end_to_end"),
            ("high_risk_rule", "mutation"),
            ("hot_path", "benchmark"),
            ("performance_claim", "benchmark"),
        )
        comment_reasons = (
            "non_obvious_intent",
            "invariant",
            "trade_off",
            "compatibility",
            "concurrency",
            "security",
            "operational_boundary",
        )
        profile = select_code_quality_profile(
            ProjectInventory(
                paths=("pyproject.toml",),
                declared_tools=(DeclaredToolSignal("black", "pyproject.toml"),),
                project_commands=(),
            )
        )

        def risk(risk_id, kind, invariants=("behavior remains deterministic",), languages=("python",)):
            return ChangeRisk(
                risk_id=risk_id,
                kind=kind,
                description=f"{kind} behavior can regress",
                protected_invariants=tuple(invariants),
                languages=tuple(languages),
            )

        def request(
            risks=(),
            *,
            mode="refactor",
            seam=True,
            seam_reason="",
            comments=(),
        ):
            return TestStrategyRequest(
                profile=profile,
                change_mode=mode,
                executable_test_seam=seam,
                test_seam_reason=seam_reason,
                risks=tuple(risks),
                comment_signals=tuple(comments),
            )

        for risk_kind, expected_kind in risk_mappings:
            with self.subTest(risk_mapping=risk_kind):
                risk_id = f"risk-{risk_kind}"
                strategy = select_test_strategy(request((risk(risk_id, risk_kind),)))
                self.assertEqual(
                    tuple(decision.test_kind for decision in strategy.test_decisions),
                    test_order,
                )
                required = tuple(
                    decision
                    for decision in strategy.test_decisions
                    if decision.status == "required"
                )
                self.assertEqual(tuple(item.test_kind for item in required), (expected_kind,))
                self.assertEqual(required[0].risk_ids, (risk_id,))
                for decision in strategy.test_decisions:
                    if decision.test_kind != expected_kind:
                        self.assertEqual(decision.status, "not_applicable")
                        self.assertEqual(
                            decision.rationale,
                            f"no_changed_risk_requires_{decision.test_kind}",
                        )
                benchmark = next(
                    item for item in strategy.test_decisions if item.test_kind == "benchmark"
                )
                expected_performance = (
                    "required"
                    if risk_kind in {"hot_path", "performance_claim"}
                    else "not_applicable"
                )
                self.assertEqual(strategy.performance_decision.status, expected_performance)
                self.assertEqual(
                    strategy.performance_decision.risk_ids,
                    benchmark.risk_ids,
                )
                self.assertEqual(strategy.coverage_decision.status, "not_applicable")
                self.assertEqual(
                    strategy.coverage_decision.reason,
                    "coverage is telemetry, not a correctness target",
                )
                self.assertIsNone(
                    re.search(
                        r"\d",
                        json.dumps(
                            quality_strategy_as_dict(strategy)["coverage_decision"]
                        ),
                    )
                )

        coalesced_risks = (
            risk("risk-b", "pure_logic", ("z invariant", "a invariant")),
            risk("risk-c", "property_invariant", ("property invariant",)),
            risk("risk-a", "pure_logic", ("a invariant",)),
        )
        with self.subTest(boundary="coalesce_and_permutation"):
            first = select_test_strategy(request(coalesced_risks))
            permuted = select_test_strategy(request(tuple(reversed(coalesced_risks))))
            self.assertEqual(
                quality_strategy_as_dict(first), quality_strategy_as_dict(permuted)
            )
            by_kind = {item.test_kind: item for item in first.test_decisions}
            self.assertEqual(by_kind["unit"].risk_ids, ("risk-a", "risk-b"))
            self.assertEqual(
                by_kind["unit"].protected_invariants,
                ("a invariant", "z invariant"),
            )
            self.assertEqual(by_kind["property"].risk_ids, ("risk-c",))

        test_first_cases = tuple(
            (mode, (risk(f"risk-{mode}", "pure_logic"),), True, "", "required")
            for mode in (
                "new_behavior",
                "defect_fix",
                "refactor",
                "legacy_change",
                "generated_code",
            )
        ) + (
            ("configuration", (risk("risk-config", "pure_logic"),), True, "", "not_applicable"),
            ("refactor", (), True, "", "not_applicable"),
            (
                "refactor",
                (risk("risk-no-seam", "pure_logic"),),
                False,
                "no executable seam is available",
                "not_applicable",
            ),
        )
        for mode, risks, seam, reason, expected_status in test_first_cases:
            with self.subTest(test_first=(mode, bool(risks), seam)):
                strategy = select_test_strategy(
                    request(risks, mode=mode, seam=seam, seam_reason=reason)
                )
                self.assertEqual(strategy.test_first_decision.status, expected_status)

        comment_risk = risk("risk-comment", "pure_logic")
        comment_signals = tuple(
            CommentSignal(
                risk_id=comment_risk.risk_id,
                reason=reason,
                detail=f"document {reason.replace('_', ' ')}",
            )
            for reason in comment_reasons
        )
        with self.subTest(boundary="comment_reason_set_and_permutation"):
            first = select_test_strategy(
                request((comment_risk,), comments=comment_signals)
            )
            permuted = select_test_strategy(
                request((comment_risk,), comments=tuple(reversed(comment_signals)))
            )
            self.assertEqual(
                quality_strategy_as_dict(first), quality_strategy_as_dict(permuted)
            )
            self.assertEqual(first.comment_decision.status, "required")
            self.assertEqual(first.comment_decision.risk_ids, (comment_risk.risk_id,))
            self.assertEqual(first.comment_decision.reasons, comment_reasons)
            self.assertEqual(
                first.comment_decision.rationale,
                "comment documents non-obvious intent, invariant, trade-off or boundary",
            )

        with self.subTest(boundary="empty_request"):
            empty = select_test_strategy(
                request(
                    (),
                    mode="configuration",
                    seam=False,
                    seam_reason="configuration-only change",
                )
            )
            self.assertEqual(
                tuple(item.status for item in empty.test_decisions),
                ("not_applicable",) * 7,
            )
            self.assertEqual(empty.test_first_decision.status, "not_applicable")
            self.assertEqual(empty.comment_decision.status, "not_applicable")
            self.assertEqual(empty.performance_decision.status, "not_applicable")
            self.assertEqual(empty.coverage_decision.status, "not_applicable")
            self.assertEqual(empty.gaps, ("no_changed_risks",))

        with self.subTest(boundary="profile_language_gap"):
            language_risk = risk(
                "risk-go-boundary",
                "external_boundary",
                languages=("go",),
            )
            strategy = select_test_strategy(request((language_risk,)))
            self.assertIn(
                "profile_language_missing:risk-go-boundary:go",
                strategy.gaps,
            )

    def test_strategy_validates_public_schema_inputs_and_purity(self):
        from product_agent_os.test_strategy_selector import (
            ChangeRisk,
            CommentDecision,
            CommentSignal,
            CoverageDecision,
            PerformanceDecision,
            QualityStrategy,
            TestDecision,
            TestFirstDecision,
            TestStrategyRequest,
            quality_strategy_as_dict,
            select_test_strategy,
        )

        profile = select_code_quality_profile(
            ProjectInventory(
                paths=("pyproject.toml",),
                declared_tools=(DeclaredToolSignal("black", "pyproject.toml"),),
                project_commands=(
                    ProjectCommandSignal("check", "pytest", "README.md"),
                ),
            )
        )
        valid_risk = ChangeRisk(
            risk_id="risk-valid",
            kind="pure_logic",
            description="selection can change",
            protected_invariants=("selection remains deterministic",),
            languages=("python",),
        )
        valid_comment = CommentSignal(
            risk_id=valid_risk.risk_id,
            reason="invariant",
            detail="document the invariant boundary",
        )

        def make_request(
            *,
            request_profile=profile,
            mode="refactor",
            seam=True,
            seam_reason="",
            risks=(valid_risk,),
            comments=(),
        ):
            return TestStrategyRequest(
                profile=request_profile,
                change_mode=mode,
                executable_test_seam=seam,
                test_seam_reason=seam_reason,
                risks=risks,
                comment_signals=comments,
            )

        strategy = select_test_strategy(
            make_request(comments=(valid_comment,))
        )
        expected_fields = {
            ChangeRisk: (
                "risk_id",
                "kind",
                "description",
                "protected_invariants",
                "languages",
            ),
            CommentSignal: ("risk_id", "reason", "detail"),
            TestStrategyRequest: (
                "profile",
                "change_mode",
                "executable_test_seam",
                "test_seam_reason",
                "risks",
                "comment_signals",
            ),
            TestFirstDecision: ("status", "risk_ids", "reason"),
            TestDecision: (
                "test_kind",
                "status",
                "risk_ids",
                "protected_invariants",
                "rationale",
            ),
            CoverageDecision: ("status", "reason"),
            CommentDecision: ("status", "risk_ids", "reasons", "rationale"),
            PerformanceDecision: ("status", "risk_ids", "rationale"),
            QualityStrategy: (
                "schema_version",
                "profile_schema_version",
                "test_first_decision",
                "test_decisions",
                "coverage_decision",
                "comment_decision",
                "performance_decision",
                "gaps",
                "evidence_ceiling",
            ),
        }
        for data_type, field_names in expected_fields.items():
            with self.subTest(schema=data_type.__name__):
                self.assertTrue(is_dataclass(data_type))
                self.assertEqual(
                    tuple(item.name for item in fields(data_type)), field_names
                )

        frozen_instances = (
            valid_risk,
            valid_comment,
            make_request(comments=(valid_comment,)),
            strategy,
            strategy.test_first_decision,
            *strategy.test_decisions,
            strategy.coverage_decision,
            strategy.comment_decision,
            strategy.performance_decision,
        )
        for instance in frozen_instances:
            with self.subTest(frozen=type(instance).__name__):
                field_name = fields(instance)[0].name
                with self.assertRaises(FrozenInstanceError):
                    setattr(instance, field_name, getattr(instance, field_name))

        with self.subTest(boundary="serializer_field_order"):
            payload = quality_strategy_as_dict(strategy)
            self.assertEqual(
                tuple(payload),
                (
                    "schema_version",
                    "profile_schema_version",
                    "test_first_decision",
                    "test_decisions",
                    "coverage_decision",
                    "comment_decision",
                    "performance_decision",
                    "gaps",
                    "evidence_ceiling",
                ),
            )
            self.assertEqual(
                tuple(payload["test_first_decision"]),
                ("status", "risk_ids", "reason"),
            )
            self.assertEqual(
                tuple(payload["test_decisions"][0]),
                (
                    "test_kind",
                    "status",
                    "risk_ids",
                    "protected_invariants",
                    "rationale",
                ),
            )
            self.assertEqual(
                tuple(payload["coverage_decision"]), ("status", "reason")
            )
            self.assertEqual(
                tuple(payload["comment_decision"]),
                ("status", "risk_ids", "reasons", "rationale"),
            )
            self.assertEqual(
                tuple(payload["performance_decision"]),
                ("status", "risk_ids", "rationale"),
            )

        stacks = list(profile.stack_profiles)
        python_stack = stacks[0]
        categories = list(python_stack.categories)
        formatter = categories[0]
        tools = list(formatter.tools)

        def forge_stack_status(status):
            forged = list(stacks)
            forged[0] = replace(python_stack, status=status)
            return replace(profile, stack_profiles=tuple(forged))

        def forge_category_status(status):
            forged_categories = list(categories)
            forged_categories[0] = replace(formatter, status=status)
            forged_stacks = list(stacks)
            forged_stacks[0] = replace(
                python_stack, categories=tuple(forged_categories)
            )
            return replace(profile, stack_profiles=tuple(forged_stacks))

        def forge_tool_status(status):
            forged_tools = list(tools)
            forged_tools[0] = replace(tools[0], status=status)
            forged_categories = list(categories)
            forged_categories[0] = replace(formatter, tools=tuple(forged_tools))
            forged_stacks = list(stacks)
            forged_stacks[0] = replace(
                python_stack, categories=tuple(forged_categories)
            )
            return replace(profile, stack_profiles=tuple(forged_stacks))

        def forge_utility_status(status):
            utilities = list(profile.project_utilities)
            utilities[0] = replace(utilities[0], status=status)
            return replace(profile, project_utilities=tuple(utilities))

        profile_state_cases = []
        for invalid_status in ("present_verified", "unknown"):
            profile_state_cases.extend(
                (
                    (
                        f"inventory:{invalid_status}",
                        replace(profile, inventory_status=invalid_status),
                    ),
                    (f"stack:{invalid_status}", forge_stack_status(invalid_status)),
                    (
                        f"category:{invalid_status}",
                        forge_category_status(invalid_status),
                    ),
                    (f"tool:{invalid_status}", forge_tool_status(invalid_status)),
                    (
                        f"utility:{invalid_status}",
                        forge_utility_status(invalid_status),
                    ),
                )
            )
        profile_state_cases.append(
            ("profile_version", replace(profile, schema_version="forged_profile_v2"))
        )
        for name, forged_profile in profile_state_cases:
            with self.subTest(invalid_profile=name):
                with self.assertRaises(ValueError):
                    select_test_strategy(make_request(request_profile=forged_profile))

        type_error_cases = (
            ("wrong_root", lambda: select_test_strategy(None)),
            (
                "wrong_profile",
                lambda: select_test_strategy(make_request(request_profile=object())),
            ),
            (
                "risks_not_tuple",
                lambda: select_test_strategy(make_request(risks=[valid_risk])),
            ),
            (
                "comments_not_tuple",
                lambda: select_test_strategy(make_request(comments=[valid_comment])),
            ),
            (
                "nested_risk_type",
                lambda: select_test_strategy(make_request(risks=(object(),))),
            ),
            (
                "seam_not_bool",
                lambda: select_test_strategy(make_request(seam=1)),
            ),
        )
        for name, action in type_error_cases:
            with self.subTest(type_error=name):
                with self.assertRaises(TypeError):
                    action()

        def altered_risk(**changes):
            return replace(valid_risk, **changes)

        value_error_cases = (
            (
                "invalid_change_mode",
                lambda: select_test_strategy(make_request(mode="ship_it")),
            ),
            (
                "invalid_risk_kind",
                lambda: select_test_strategy(
                    make_request(risks=(altered_risk(kind="unknown"),))
                ),
            ),
            (
                "blank_risk_id",
                lambda: select_test_strategy(
                    make_request(risks=(altered_risk(risk_id="  "),))
                ),
            ),
            (
                "nul_risk_id",
                lambda: select_test_strategy(
                    make_request(risks=(altered_risk(risk_id="risk\0id"),))
                ),
            ),
            (
                "path_like_risk_id",
                lambda: select_test_strategy(
                    make_request(risks=(altered_risk(risk_id="../risk"),))
                ),
            ),
            (
                "blank_description",
                lambda: select_test_strategy(
                    make_request(risks=(altered_risk(description=""),))
                ),
            ),
            (
                "blank_invariant",
                lambda: select_test_strategy(
                    make_request(risks=(altered_risk(protected_invariants=(" ",)),))
                ),
            ),
            (
                "nul_invariant",
                lambda: select_test_strategy(
                    make_request(risks=(altered_risk(protected_invariants=("a\0b",)),))
                ),
            ),
            (
                "blank_language",
                lambda: select_test_strategy(
                    make_request(risks=(altered_risk(languages=("",)),))
                ),
            ),
            (
                "unknown_language",
                lambda: select_test_strategy(
                    make_request(risks=(altered_risk(languages=("ruby",)),))
                ),
            ),
            (
                "duplicate_risk_id",
                lambda: select_test_strategy(make_request(risks=(valid_risk, valid_risk))),
            ),
            (
                "unknown_comment_reference",
                lambda: select_test_strategy(
                    make_request(
                        comments=(
                            replace(valid_comment, risk_id="risk-missing"),
                        )
                    )
                ),
            ),
            (
                "unknown_comment_reason",
                lambda: select_test_strategy(
                    make_request(
                        comments=(replace(valid_comment, reason="unknown"),)
                    )
                ),
            ),
            (
                "line_narration_comment",
                lambda: select_test_strategy(
                    make_request(
                        comments=(replace(valid_comment, reason="line_narration"),)
                    )
                ),
            ),
            (
                "blank_comment_detail",
                lambda: select_test_strategy(
                    make_request(comments=(replace(valid_comment, detail=" "),))
                ),
            ),
            (
                "nul_comment_detail",
                lambda: select_test_strategy(
                    make_request(comments=(replace(valid_comment, detail="a\0b"),))
                ),
            ),
            (
                "seam_false_without_reason",
                lambda: select_test_strategy(
                    make_request(seam=False, seam_reason="")
                ),
            ),
            (
                "seam_true_with_reason",
                lambda: select_test_strategy(
                    make_request(seam=True, seam_reason="already executable")
                ),
            ),
            (
                "conflicting_duplicate_comment_details",
                lambda: select_test_strategy(
                    make_request(
                        comments=(
                            valid_comment,
                            replace(valid_comment, detail="different detail"),
                        )
                    )
                ),
            ),
        )
        for name, action in value_error_cases:
            with self.subTest(value_error=name):
                with self.assertRaises(ValueError):
                    action()

        with self.subTest(boundary="strategy_source_purity"):
            source_path = SCRIPTS / "product_agent_os" / "test_strategy_selector.py"
            source = source_path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            imported_modules = {
                alias.name.split(".", 1)[0]
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            imported_modules.update(
                node.module.split(".", 1)[0]
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module
            )
            self.assertTrue(
                {"os", "pathlib", "subprocess"}.isdisjoint(imported_modules)
            )
            self.assertNotRegex(
                source,
                r"(?:^|\n)\s*(?:from|import)\s+[^\n]*discovery",
            )
            self.assertNotRegex(source, r"\b_?discover[a-z0-9_]*\s*\(")
            forbidden_calls = {
                "open",
                "popen",
                "run",
                "system",
                "read_text",
                "write_text",
            }
            called_names = {
                node.func.id.lower()
                for node in ast.walk(tree)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            }
            called_names.update(
                node.func.attr.lower()
                for node in ast.walk(tree)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            )
            self.assertTrue(forbidden_calls.isdisjoint(called_names))

    def test_selector_safety_and_completeness_boundaries(self):
        category_order = (
            "formatter",
            "linter",
            "type_checker",
            "test_runner",
            "build_tool",
        )
        install_pattern = re.compile(
            r"\b(?:pip|pipx|uv|poetry|npm|pnpm|yarn|cargo|dotnet|mvn|gradle)"
            r"\s+install\b",
            re.IGNORECASE,
        )

        def make_inventory(paths=(), tools=(), commands=()):
            return ProjectInventory(
                paths=tuple(paths),
                declared_tools=tuple(
                    DeclaredToolSignal(name=name, source=source)
                    for name, source in tools
                ),
                project_commands=tuple(
                    ProjectCommandSignal(name=name, command=command, source=source)
                    for name, command, source in commands
                ),
            )

        def stack_by_family(profile, family):
            return next(stack for stack in profile.stack_profiles if stack.family == family)

        def categories_by_name(stack):
            return {category.category: category for category in stack.categories}

        def assert_conservative(profile):
            payload = code_quality_profile_as_dict(profile)
            self.assertNotIn("present_verified", json.dumps(payload, sort_keys=True))
            for stack in profile.stack_profiles:
                for category in stack.categories:
                    for tool in category.tools:
                        for command in tool.proposed_commands:
                            self.assertIsNone(
                                install_pattern.search(command),
                                f"invented installation command for {tool.name}: {command}",
                            )

        empty_profile = select_code_quality_profile(make_inventory())
        self.assertEqual(empty_profile.inventory_status, "not_applicable")
        self.assertEqual(empty_profile.gaps, ("no_stack_or_tool_signals",))
        self.assertFalse(empty_profile.project_utilities)
        self.assertTrue(
            all(stack.status == "not_applicable" for stack in empty_profile.stack_profiles)
        )
        assert_conservative(empty_profile)

        full_stack_cases = (
            (
                "python",
                "python",
                ("pyproject.toml",),
                (
                    ("black", "formatter"),
                    ("ruff", "linter"),
                    ("mypy", "type_checker"),
                    ("pytest", "test_runner"),
                    ("hatch", "build_tool"),
                ),
            ),
            (
                "javascript_typescript",
                "typescript",
                ("package.json", "tsconfig.json"),
                (
                    ("prettier", "formatter"),
                    ("eslint", "linter"),
                    ("typescript", "type_checker"),
                    ("vitest", "test_runner"),
                    ("vite", "build_tool"),
                ),
            ),
            (
                "compiled_systems",
                "go",
                ("go.mod",),
                (
                    ("gofmt", "formatter"),
                    ("golangci-lint", "linter"),
                    ("go vet", "type_checker"),
                    ("go test", "test_runner"),
                    ("go build", "build_tool"),
                ),
            ),
            (
                "compiled_systems",
                "rust",
                ("Cargo.toml",),
                (
                    ("rustfmt", "formatter"),
                    ("clippy", "linter"),
                    ("rustc", "type_checker"),
                    ("cargo test", "test_runner"),
                    ("cargo build", "build_tool"),
                ),
            ),
            (
                "enterprise_oop",
                "java",
                ("pom.xml",),
                (
                    ("google-java-format", "formatter"),
                    ("checkstyle", "linter"),
                    ("javac", "type_checker"),
                    ("junit", "test_runner"),
                    ("maven", "build_tool"),
                ),
            ),
            (
                "enterprise_oop",
                "csharp",
                ("src/App/App.csproj",),
                (
                    ("dotnet format", "formatter"),
                    ("stylecop", "linter"),
                    ("csc", "type_checker"),
                    ("dotnet test", "test_runner"),
                    ("dotnet build", "build_tool"),
                ),
            ),
        )
        for family, language, paths, tool_categories in full_stack_cases:
            with self.subTest(full_stack=language):
                source = paths[0]
                profile = select_code_quality_profile(
                    make_inventory(
                        paths=paths,
                        tools=tuple((name, source) for name, _ in tool_categories),
                    )
                )
                stack = stack_by_family(profile, family)
                self.assertEqual(stack.status, "present_unverified")
                self.assertIn(language, stack.languages)
                categories = categories_by_name(stack)
                self.assertEqual(tuple(categories), category_order)
                for tool_name, category_name in tool_categories:
                    category = categories[category_name]
                    self.assertEqual(category.status, "present_unverified")
                    self.assertIn(tool_name, tuple(tool.name for tool in category.tools))
                self.assertFalse(
                    tuple(
                        gap
                        for gap in profile.gaps
                        if gap.startswith(f"{family}:{language}:")
                    )
                )
                assert_conservative(profile)

        unique_inventory = make_inventory(
            paths=("pyproject.toml",),
            tools=(("black", "pyproject.toml"),),
            commands=(("repo_check", "pytest -q", "pyproject.toml"),),
        )
        duplicate_permuted_inventory = make_inventory(
            paths=("pyproject.toml", "pyproject.toml"),
            tools=(("black", "pyproject.toml"), ("black", "pyproject.toml")),
            commands=(
                ("repo_check", "pytest -q", "pyproject.toml"),
                ("repo_check", "pytest -q", "pyproject.toml"),
            ),
        )
        with self.subTest(boundary="exact_duplicates_and_permutation"):
            unique_dict = code_quality_profile_as_dict(
                select_code_quality_profile(unique_inventory)
            )
            duplicate_dict = code_quality_profile_as_dict(
                select_code_quality_profile(duplicate_permuted_inventory)
            )
            self.assertEqual(unique_dict, duplicate_dict)

        with self.subTest(boundary="unknown_only_signals"):
            unknown_profile = select_code_quality_profile(
                make_inventory(
                    paths=("unknown.project",),
                    tools=(("mystery-quality-tool", "tools.conf"),),
                )
            )
            self.assertEqual(unknown_profile.inventory_status, "applicable_missing")
            self.assertTrue(unknown_profile.gaps)
            self.assertTrue(any("unknown" in gap for gap in unknown_profile.gaps))
            self.assertFalse(
                any(
                    stack.status == "present_unverified"
                    for stack in unknown_profile.stack_profiles
                )
            )
            assert_conservative(unknown_profile)

        with self.subTest(boundary="missing_categories_have_no_commands"):
            partial_profile = select_code_quality_profile(
                make_inventory(
                    paths=("pyproject.toml",),
                    tools=(("black", "pyproject.toml"),),
                )
            )
            python_stack = stack_by_family(partial_profile, "python")
            missing = tuple(
                category
                for category in python_stack.categories
                if category.status == "applicable_missing"
            )
            self.assertTrue(missing)
            self.assertTrue(
                all(
                    not category.tools
                    or all(not tool.proposed_commands for tool in category.tools)
                    for category in missing
                )
            )
            assert_conservative(partial_profile)

        with self.subTest(boundary="absent_family_is_not_applicable"):
            python_only = select_code_quality_profile(
                make_inventory(paths=("pyproject.toml",))
            )
            self.assertEqual(
                stack_by_family(python_only, "enterprise_oop").status,
                "not_applicable",
            )

        cross_family_cases = (
            (
                "go_and_rust",
                ("go.mod", "Cargo.toml"),
                (
                    ("gofmt", "go.mod"),
                    ("golangci-lint", "go.mod"),
                    ("go vet", "go.mod"),
                    ("go test", "go.mod"),
                    ("go build", "go.mod"),
                    ("rustfmt", "Cargo.toml"),
                ),
                "compiled_systems",
                "rust",
                ("linter", "type_checker", "test_runner", "build_tool"),
            ),
            (
                "java_and_csharp",
                ("pom.xml", "src/App/App.csproj"),
                (
                    ("google-java-format", "pom.xml"),
                    ("checkstyle", "pom.xml"),
                    ("javac", "pom.xml"),
                    ("junit", "pom.xml"),
                    ("maven", "pom.xml"),
                    ("dotnet format", "src/App/App.csproj"),
                ),
                "enterprise_oop",
                "csharp",
                ("linter", "type_checker", "test_runner", "build_tool"),
            ),
        )
        for name, paths, tools, family, incomplete_language, missing_categories in cross_family_cases:
            with self.subTest(cross_family_isolation=name):
                profile = select_code_quality_profile(
                    make_inventory(paths=paths, tools=tools)
                )
                stack = stack_by_family(profile, family)
                self.assertIn(incomplete_language, stack.languages)
                for category in missing_categories:
                    self.assertIn(
                        f"{family}:{incomplete_language}:{category}",
                        profile.gaps,
                    )
                assert_conservative(profile)

        type_error_cases = (
            ("wrong_root", lambda: select_code_quality_profile(None)),
            (
                "paths_not_tuple",
                lambda: select_code_quality_profile(ProjectInventory([], (), ())),
            ),
            (
                "path_not_string",
                lambda: select_code_quality_profile(ProjectInventory((1,), (), ())),
            ),
            (
                "tool_nested_type",
                lambda: select_code_quality_profile(
                    ProjectInventory((), (DeclaredToolSignal(1, "tools.conf"),), ())
                ),
            ),
            (
                "command_nested_type",
                lambda: select_code_quality_profile(
                    ProjectInventory(
                        (),
                        (),
                        (ProjectCommandSignal("check", 1, "README.md"),),
                    )
                ),
            ),
        )
        for name, action in type_error_cases:
            with self.subTest(type_error=name):
                with self.assertRaises(TypeError):
                    action()

        value_error_cases = (
            (
                "empty_path",
                lambda: select_code_quality_profile(ProjectInventory(("",), (), ())),
            ),
            (
                "whitespace_tool_name",
                lambda: select_code_quality_profile(
                    ProjectInventory(
                        ("pyproject.toml",),
                        (DeclaredToolSignal("  ", "pyproject.toml"),),
                        (),
                    )
                ),
            ),
            (
                "empty_command",
                lambda: select_code_quality_profile(
                    ProjectInventory(
                        (),
                        (),
                        (ProjectCommandSignal("check", "", "README.md"),),
                    )
                ),
            ),
            (
                "absolute_path",
                lambda: select_code_quality_profile(ProjectInventory(("/tmp/pom.xml",), (), ())),
            ),
            (
                "drive_path",
                lambda: select_code_quality_profile(
                    ProjectInventory((r"C:\repo\pyproject.toml",), (), ())
                ),
            ),
            (
                "parent_traversal",
                lambda: select_code_quality_profile(
                    ProjectInventory(("../pyproject.toml",), (), ())
                ),
            ),
            (
                "nul_path",
                lambda: select_code_quality_profile(
                    ProjectInventory(("pyproject.toml\0",), (), ())
                ),
            ),
            (
                "traversing_signal_source",
                lambda: select_code_quality_profile(
                    ProjectInventory(
                        ("pyproject.toml",),
                        (DeclaredToolSignal("black", "../pyproject.toml"),),
                        (),
                    )
                ),
            ),
            (
                "conflicting_duplicate_project_command",
                lambda: select_code_quality_profile(
                    ProjectInventory(
                        (),
                        (),
                        (
                            ProjectCommandSignal("check", "pytest", "README.md"),
                            ProjectCommandSignal("check", "ruff check .", "README.md"),
                        ),
                    )
                ),
            ),
        )
        for name, action in value_error_cases:
            with self.subTest(value_error=name):
                with self.assertRaises(ValueError):
                    action()

        with self.subTest(boundary="source_purity"):
            selector_path = SCRIPTS / "product_agent_os" / "code_quality_selector.py"
            selector_source = selector_path.read_text(encoding="utf-8")
            selector_tree = ast.parse(selector_source)
            imported_modules = {
                alias.name.split(".", 1)[0]
                for node in ast.walk(selector_tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            imported_modules.update(
                node.module.split(".", 1)[0]
                for node in ast.walk(selector_tree)
                if isinstance(node, ast.ImportFrom) and node.module
            )
            self.assertTrue({"subprocess", "os"}.isdisjoint(imported_modules))
            self.assertNotRegex(selector_source, r"\bos\.system\s*\(")
            self.assertNotRegex(
                selector_source,
                r"(?:^|\n)\s*(?:from|import)\s+[^\n]*discovery",
            )
            self.assertNotRegex(selector_source, r"\b_?discover[a-z0-9_]*\s*\(")

        with self.subTest(boundary="installer_like_project_command_is_inert"):
            supplied_command = "pip install example-package"
            installer_profile = select_code_quality_profile(
                make_inventory(
                    paths=("pyproject.toml",),
                    commands=(("bootstrap_hint", supplied_command, "README.md"),),
                )
            )
            self.assertEqual(len(installer_profile.project_utilities), 1)
            utility = installer_profile.project_utilities[0]
            self.assertEqual(utility.proposed_command, supplied_command)
            self.assertEqual(utility.status, "present_unverified")
            self.assertNotIn(
                supplied_command,
                tuple(
                    command
                    for stack in installer_profile.stack_profiles
                    for category in stack.categories
                    for tool in category.tools
                    for command in tool.proposed_commands
                ),
            )
            assert_conservative(installer_profile)

    def test_selector_preserves_tool_utility_and_nested_manifest_evidence(self):
        def stack(profile, family):
            return next(item for item in profile.stack_profiles if item.family == family)

        mismatches = []
        known_tool_only = select_code_quality_profile(
            ProjectInventory(
                paths=(),
                declared_tools=(DeclaredToolSignal("ruff", "quality.toml"),),
                project_commands=(),
            )
        )
        python_stack = stack(known_tool_only, "python")
        if known_tool_only.inventory_status != "present_unverified":
            mismatches.append(
                f"known_tool_only: inventory_status={known_tool_only.inventory_status!r}"
            )
        if python_stack.status != "present_unverified":
            mismatches.append(f"known_tool_only: status={python_stack.status!r}")
        if python_stack.languages != ("python",):
            mismatches.append(
                f"known_tool_only: languages={python_stack.languages!r}"
            )
        known_tools = tuple(
            tool.name for category in python_stack.categories for tool in category.tools
        )
        if "ruff" not in known_tools:
            mismatches.append(f"known_tool_only: tools={known_tools!r}")

        utility_only = select_code_quality_profile(
            ProjectInventory(
                paths=(),
                declared_tools=(),
                project_commands=(
                    ProjectCommandSignal(
                        "repo_check",
                        "python tools/check_repo.py",
                        "README.md",
                    ),
                ),
            )
        )
        if utility_only.inventory_status != "present_unverified":
            mismatches.append(
                f"utility_only: status={utility_only.inventory_status!r}"
            )
        utility_names = tuple(
            utility.name for utility in utility_only.project_utilities
        )
        if utility_names != ("repo_check",):
            mismatches.append(f"utility_only: utilities={utility_names!r}")
        non_inert_stacks = tuple(
            stack_profile.family
            for stack_profile in utility_only.stack_profiles
            if stack_profile.status != "not_applicable"
        )
        if non_inert_stacks:
            mismatches.append(
                f"utility_only: non_not_applicable_stacks={non_inert_stacks!r}"
            )

        nested_monorepo = select_code_quality_profile(
            ProjectInventory(
                paths=("services/api/pyproject.toml", "apps/web/package.json"),
                declared_tools=(),
                project_commands=(),
            )
        )
        nested_expectations = (
            ("python", "services/api/pyproject.toml"),
            ("javascript_typescript", "apps/web/package.json"),
        )
        for family, marker in nested_expectations:
            family_profile = stack(nested_monorepo, family)
            if family_profile.status != "present_unverified":
                mismatches.append(
                    f"nested_monorepo:{family}: status={family_profile.status!r}"
                )
            if family_profile.marker_evidence != (marker,):
                mismatches.append(
                    f"nested_monorepo:{family}: markers={family_profile.marker_evidence!r}"
                )

        self.assertEqual(mismatches, [])

    def test_profiles_report_actual_language_subsets_and_strategy_missing_gaps(self):
        from product_agent_os.test_strategy_selector import (
            ChangeRisk,
            TestStrategyRequest,
            select_test_strategy,
        )

        cases = (
            ("javascript", "package.json", "javascript_typescript", "typescript"),
            ("typescript", "tsconfig.json", "javascript_typescript", "javascript"),
            ("go", "go.mod", "compiled_systems", "rust"),
            ("rust", "Cargo.toml", "compiled_systems", "go"),
            ("java", "pom.xml", "enterprise_oop", "csharp"),
            ("csharp", "src/App/App.csproj", "enterprise_oop", "java"),
        )
        mismatches = []
        for language, marker, family, missing_language in cases:
            profile = select_code_quality_profile(
                ProjectInventory((marker,), (), ())
            )
            family_profile = next(
                item for item in profile.stack_profiles if item.family == family
            )
            if family_profile.languages != (language,):
                mismatches.append(
                    f"{marker}: languages={family_profile.languages!r}, expected={(language,)!r}"
                )

            risk_id = f"risk-{language}-must-not-imply-{missing_language}"
            strategy = select_test_strategy(
                TestStrategyRequest(
                    profile=profile,
                    change_mode="configuration",
                    executable_test_seam=True,
                    test_seam_reason="",
                    risks=(
                        ChangeRisk(
                            risk_id=risk_id,
                            kind="pure_logic",
                            description="a sibling language must not be inferred",
                            protected_invariants=("language evidence stays factual",),
                            languages=(missing_language,),
                        ),
                    ),
                    comment_signals=(),
                )
            )
            expected_gap = (
                f"profile_language_missing:{risk_id}:{missing_language}"
            )
            if expected_gap not in strategy.gaps:
                mismatches.append(f"{marker}: missing gap {expected_gap}")

        self.assertEqual(mismatches, [])

    def test_strategy_rejects_every_non_string_public_field_before_serialization(self):
        from product_agent_os.test_strategy_selector import (
            ChangeRisk,
            CommentSignal,
            TestStrategyRequest,
            quality_strategy_as_dict,
            select_test_strategy,
        )

        profile = select_code_quality_profile(ProjectInventory(("pyproject.toml",), (), ()))
        risk = ChangeRisk(
            risk_id="risk-valid",
            kind="pure_logic",
            description="selection can change",
            protected_invariants=("selection remains deterministic",),
            languages=("python",),
        )
        comment = CommentSignal(
            risk_id=risk.risk_id,
            reason="invariant",
            detail="document the invariant boundary",
        )

        def request(*, mode="refactor", seam=True, seam_reason="", risks=(risk,), comments=()):
            return TestStrategyRequest(
                profile=profile,
                change_mode=mode,
                executable_test_seam=seam,
                test_seam_reason=seam_reason,
                risks=risks,
                comment_signals=comments,
            )

        invalid_cases = (
            ("change_mode", request(mode=1)),
            ("test_seam_reason", request(seam=False, seam_reason=1)),
            ("risk_id", request(risks=(replace(risk, risk_id=1),))),
            ("risk_kind", request(risks=(replace(risk, kind=1),))),
            ("risk_description", request(risks=(replace(risk, description=1),))),
            (
                "protected_invariant",
                request(risks=(replace(risk, protected_invariants=(1,)),)),
            ),
            ("risk_language", request(risks=(replace(risk, languages=(1,)),))),
            (
                "comment_risk_id",
                request(comments=(replace(comment, risk_id=1),)),
            ),
            (
                "comment_reason",
                request(comments=(replace(comment, reason=1),)),
            ),
            (
                "comment_detail",
                request(comments=(replace(comment, detail=1),)),
            ),
        )
        mismatches = []
        for field_name, invalid_request in invalid_cases:
            try:
                result = select_test_strategy(invalid_request)
            except TypeError:
                continue
            except Exception as exc:  # exact public exception class is the contract
                mismatches.append(
                    f"{field_name}: {type(exc).__name__}, expected TypeError"
                )
            else:
                payload = quality_strategy_as_dict(result)
                mismatches.append(
                    f"{field_name}: accepted and serialized {payload!r}"
                )

        self.assertEqual(mismatches, [])

        valid_payload = quality_strategy_as_dict(
            select_test_strategy(request(comments=(comment,)))
        )
        serialized_reason_and_id_values = [
            valid_payload["test_first_decision"]["reason"],
            *valid_payload["test_first_decision"]["risk_ids"],
            *(
                risk_id
                for decision in valid_payload["test_decisions"]
                for risk_id in decision["risk_ids"]
            ),
            *valid_payload["comment_decision"]["risk_ids"],
            *valid_payload["comment_decision"]["reasons"],
            *valid_payload["performance_decision"]["risk_ids"],
        ]
        self.assertTrue(
            all(isinstance(value, str) for value in serialized_reason_and_id_values)
        )

    def test_public_code_quality_profile_is_conservative_and_side_effect_free(self):
        profile_path = TEMPLATE_ROOT / "artifact-templates" / "code-quality-profile.md"
        self.assertTrue(
            profile_path.is_file(),
            "canonical public profile template is missing: "
            "plugins/product-agent-os/assets/templates/artifact-templates/"
            "code-quality-profile.md",
        )

        text = profile_path.read_text(encoding="utf-8")
        lower_text = text.lower()
        required_headings = (
            "# code quality profile",
            "## stack profiles",
            "## existing project-native tools",
            "## project utilities",
            "## gaps",
            "## evidence ceiling",
        )
        required_fields = (
            "schema_version",
            "inventory_status",
            "proposed_commands_not_run",
            "installation_performed: false",
            "commands_executed: false",
            "present_unverified",
            "evidence_ceiling",
        )
        for heading in required_headings:
            with self.subTest(heading=heading):
                self.assertIn(heading, lower_text)
        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, lower_text)

        table_rows = [line.lower() for line in text.splitlines() if line.startswith("|")]
        self.assertTrue(
            any(
                all(
                    column in row
                    for column in ("family", "languages", "status", "marker_evidence")
                )
                for row in table_rows
            ),
            "stack profiles must be an explicit evidence table",
        )
        self.assertTrue(
            any(
                all(
                    column in row
                    for column in (
                        "family",
                        "category",
                        "name",
                        "status",
                        "sources",
                        "proposed_commands_not_run",
                    )
                )
                for row in table_rows
            ),
            "existing project-native tools must remain inspectable and unexecuted",
        )
        self.assertTrue(
            any(
                all(
                    column in row
                    for column in ("name", "status", "source", "proposed_command")
                )
                for row in table_rows
            ),
            "project utilities must be represented as inert profile data",
        )

        self.assertNotIn("present_verified", lower_text)
        self.assertNotIn("threshold", lower_text)
        self.assertNotIn("quality_score", lower_text)
        self.assertNotIn("universal_score", lower_text)
        self.assertIsNone(
            re.search(
                r"\b(?:pip|pipx|uv|poetry|npm|pnpm|yarn|cargo|dotnet|mvn|gradle)\s+install\b",
                lower_text,
            ),
            "the public profile must not suggest installing a tool",
        )

    def test_mixed_inventory_yields_stable_conservative_profile(self):
        paths = ("pyproject.toml", "package.json", "Cargo.toml", "pom.xml")
        declared_tools = (
            DeclaredToolSignal(name="black", source="pyproject.toml"),
            DeclaredToolSignal(name="eslint", source="package.json"),
            DeclaredToolSignal(name="clippy", source="Cargo.toml"),
            DeclaredToolSignal(name="checkstyle", source="pom.xml"),
        )
        project_commands = (
            ProjectCommandSignal(
                name="repo_check",
                command="python tools/check_repo.py",
                source="README.md",
            ),
        )
        inventory = ProjectInventory(
            paths=paths,
            declared_tools=declared_tools,
            project_commands=project_commands,
        )
        permuted_inventory = ProjectInventory(
            paths=tuple(reversed(paths)),
            declared_tools=tuple(reversed(declared_tools)),
            project_commands=tuple(reversed(project_commands)),
        )

        profile = select_code_quality_profile(inventory)
        profile_dict = code_quality_profile_as_dict(profile)
        permuted_dict = code_quality_profile_as_dict(
            select_code_quality_profile(permuted_inventory)
        )

        expected_fields = {
            DeclaredToolSignal: ("name", "source"),
            ProjectCommandSignal: ("name", "command", "source"),
            ProjectInventory: ("paths", "declared_tools", "project_commands"),
            ToolEvidence: ("name", "status", "sources", "proposed_commands"),
            CategoryProfile: ("category", "status", "tools", "reason"),
            StackProfile: (
                "family",
                "languages",
                "status",
                "marker_evidence",
                "categories",
            ),
            ProjectUtilityProfile: ("name", "status", "source", "proposed_command"),
            CodeQualityProfile: (
                "schema_version",
                "inventory_status",
                "stack_profiles",
                "project_utilities",
                "gaps",
                "evidence_ceiling",
            ),
        }
        for data_type, field_names in expected_fields.items():
            with self.subTest(data_type=data_type.__name__):
                self.assertTrue(is_dataclass(data_type))
                self.assertEqual(tuple(item.name for item in fields(data_type)), field_names)

        expected_families = (
            "python",
            "javascript_typescript",
            "compiled_systems",
            "enterprise_oop",
        )
        expected_categories = (
            "formatter",
            "linter",
            "type_checker",
            "test_runner",
            "build_tool",
        )
        self.assertIsInstance(profile, CodeQualityProfile)
        self.assertEqual(profile.schema_version, "code_quality_profile_v1")
        self.assertEqual(profile.inventory_status, "present_unverified")
        self.assertEqual(
            tuple(stack.family for stack in profile.stack_profiles), expected_families
        )

        detected_tool_names = set()
        missing_category_count = 0
        frozen_instances = [inventory, *declared_tools, *project_commands, profile]
        for stack in profile.stack_profiles:
            self.assertEqual(stack.status, "present_unverified")
            self.assertEqual(
                tuple(category.category for category in stack.categories),
                expected_categories,
            )
            frozen_instances.append(stack)
            for category in stack.categories:
                frozen_instances.append(category)
                if category.tools:
                    self.assertEqual(category.status, "present_unverified")
                else:
                    self.assertEqual(category.status, "applicable_missing")
                    missing_category_count += 1
                for tool in category.tools:
                    self.assertEqual(tool.status, "present_unverified")
                    detected_tool_names.add(tool.name)
                    frozen_instances.append(tool)

        self.assertGreater(missing_category_count, 0)
        self.assertEqual(detected_tool_names, {tool.name for tool in declared_tools})
        self.assertNotIn("present_verified", json.dumps(profile_dict, sort_keys=True))

        self.assertEqual(len(profile.project_utilities), 1)
        utility = profile.project_utilities[0]
        self.assertEqual(
            (
                utility.name,
                utility.status,
                utility.source,
                utility.proposed_command,
            ),
            (
                "repo_check",
                "present_unverified",
                "README.md",
                "python tools/check_repo.py",
            ),
        )
        frozen_instances.append(utility)

        for instance in frozen_instances:
            with self.subTest(frozen_instance=type(instance).__name__):
                first_field = fields(instance)[0].name
                with self.assertRaises(FrozenInstanceError):
                    setattr(instance, first_field, getattr(instance, first_field))

        self.assertEqual(profile_dict, permuted_dict)
        self.assertEqual(
            tuple(profile_dict),
            (
                "schema_version",
                "inventory_status",
                "stack_profiles",
                "project_utilities",
                "gaps",
                "evidence_ceiling",
            ),
        )
        self.assertEqual(
            tuple(profile_dict["stack_profiles"][0]),
            ("family", "languages", "status", "marker_evidence", "categories"),
        )
        self.assertEqual(
            tuple(profile_dict["stack_profiles"][0]["categories"][0]),
            ("category", "status", "tools", "reason"),
        )
        self.assertEqual(
            tuple(profile_dict["project_utilities"][0]),
            ("name", "status", "source", "proposed_command"),
        )


if __name__ == "__main__":
    unittest.main()
