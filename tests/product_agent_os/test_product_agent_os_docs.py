import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PRODUCT_AGENT_OS = DOCS / "product-agent-os"
MKDOCS = ROOT / "mkdocs.yml"
CHECK_DOCS = ROOT / "tools" / "check_docs.py"
SOURCE_REGISTRY = DOCS / "sources" / "registry.md"
TRACK_BACKLOG = DOCS / "sources" / "product-agent-os-track-8-detailed-backlog.md"
TRACK9_BACKLOG = DOCS / "sources" / "product-agent-os-track-9-backlog.md"


class ProductAgentOsDocsTest(unittest.TestCase):
    def test_t8h_dedicated_docs_pages_exist_with_operating_contracts(self):
        expected_pages = {
            "scenarios.md": [
                "usage_mode",
                "first response",
                "minimum artifacts",
                "approval boundary",
                "verification gates",
                "bug_rescue",
                "greenfield_idea",
                "complex_system_acceleration",
                "release_packaging",
            ],
            "behavioral-evals.md": [
                "behavioral-workflows.json",
                "expected behavior",
                "forbidden behavior",
                "fixture eval",
                "transcript/session eval runner",
                "evidence-before-completion",
                "residual risk",
            ],
            "codex-compatibility.md": [
                "Codex App",
                "CLI",
                "IDE extension",
                ".codex-plugin/plugin.json",
                "skills",
                "MCP",
                "staged hooks",
                "validate_codex_compatibility.py",
                "no standalone Agents SDK",
                "no separate OpenAI API key",
            ],
        }

        for filename, terms in expected_pages.items():
            with self.subTest(filename=filename):
                path = PRODUCT_AGENT_OS / filename
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                self.assertIn("Source status:", text)
                self.assertIn("Inputs", text)
                self.assertIn("Outputs", text)
                self.assertIn("Verification", text)
                self.assertIn("Risks", text)
                for term in terms:
                    self.assertIn(term, text)

    def test_t8h_docs_are_in_nav_and_required_docs_check(self):
        nav = MKDOCS.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")

        for path in [
            "product-agent-os/scenarios.md",
            "product-agent-os/behavioral-evals.md",
            "product-agent-os/codex-compatibility.md",
        ]:
            with self.subTest(path=path):
                self.assertIn(path, nav)
                self.assertIn(path.replace("/", '" / "'), check_docs)

    def test_track9_methodology_intelligence_docs_exist(self):
        path = PRODUCT_AGENT_OS / "methodology-intelligence.md"
        self.assertTrue(path.exists(), path)

        text = path.read_text(encoding="utf-8")
        self.assertIn("Source status:", text)
        self.assertIn("Inputs", text)
        self.assertIn("Outputs", text)
        self.assertIn("Verification", text)
        self.assertIn("Risks", text)

        nav = MKDOCS.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")
        self.assertIn("methodology-intelligence.md", nav)
        self.assertIn('product-agent-os" / "methodology-intelligence.md', check_docs)

    def test_t8h_and_t8gy_source_and_backlog_closure_are_documented(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK_BACKLOG.read_text(encoding="utf-8")

        self.assertIn("Product-Agent OS Track 8 scenario, eval and transcript docs", registry)
        self.assertIn("docs/product-agent-os/scenarios.md", registry)
        self.assertIn("docs/product-agent-os/behavioral-evals.md", registry)
        self.assertIn("docs/product-agent-os/codex-compatibility.md", registry)
        self.assertIn("plugins/product-agent-os/scripts/product_agent_os/discovery.py", registry)
        self.assertIn("plugins/product-agent-os/scripts/run_transcript_eval.py", registry)
        self.assertIn("T8-D", registry)
        self.assertIn("verification_status:", registry)

        self.assertIn("| `done` | `T8-H` system docs and control-plane sync |", backlog)
        self.assertIn("dedicated scenario, behavioral eval and Codex compatibility docs", backlog)
        self.assertIn("| `T8-GY` behavioral workflow evals | `done` |", backlog)
        self.assertIn("deterministic transcript/session runner", backlog)
        self.assertIn("| `T8-D` discovery model | `done` |", backlog)
        self.assertIn("methodology_applicability", backlog)

    def test_track9_backend_docs_and_source_registry_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")

        for expected in [
            "Product-Agent OS Track 9 backend methodology coverage",
            "T9-D7",
            "backend_contract_present",
            "docs/product-agent-os/behavioral-evals.md",
            "plugins/product-agent-os/scripts/product_agent_os/discovery.py",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "backend_contract_present",
            "Backend eval",
            "runtime/failure/observability/security/rollback evidence",
            "owner reviewed test/eval/runtime evidence sufficiency",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "Backend methodology routing",
            "backend-service-overview.md",
            "backend-runtime-behavior.md",
            "runtime/failure evidence",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)

        for expected in [
            "Backend methodology",
            "backend_contract_present",
            "backend_service_boundary_present",
            "owner reviewed test/eval/runtime evidence sufficiency",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

        self.assertIn("T9-D7-M40..M45", backlog)
        self.assertIn("stack-specific backend snippets deferred", backlog)
        self.assertIn("cross-domain semantic sufficiency backlog", backlog)

    def test_track9_api_integrations_docs_and_source_registry_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")

        for expected in [
            "Product-Agent OS Track 9 API & Integrations methodology coverage",
            "T9-D8",
            "api_integrations_contract_present",
            "docs/product-agent-os/behavioral-evals.md",
            "plugins/product-agent-os/scripts/product_agent_os/discovery.py",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "api_integrations_contract_present",
            "API & Integrations eval",
            "Swagger UI is not source of truth",
            "external writes are approval_required",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "API & Integrations methodology routing",
            "api-inventory.md",
            "api-contract-test-matrix.md",
            "external-integration-approval.md",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)

        for expected in [
            "API & Integrations methodology",
            "api_integrations_contract_present",
            "api_contract_source_present",
            "external_write_approval_present",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

        self.assertIn("T9-D8", backlog)
        self.assertIn("API lint tooling", backlog)
        self.assertIn("multi-repository generated clients deferred", backlog)

    def test_track9_database_data_docs_and_source_registry_are_synced(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")

        for expected in [
            "Product-Agent OS Track 9 Database & Data methodology coverage",
            "T9-D9",
            "database_data_contract_present",
            "docs/product-agent-os/behavioral-evals.md",
            "plugins/product-agent-os/scripts/product_agent_os/discovery.py",
            "verification_status:",
        ]:
            with self.subTest(source_registry=expected):
                self.assertIn(expected, registry)

        for expected in [
            "database_data_contract_present",
            "Database & Data eval",
            "schema-only artifact is not safety proof",
            "production access approval_required",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "Database & Data methodology routing",
            "database-inventory.md",
            "database-migration-plan.md",
            "database-production-access-approval.md",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)

        for expected in [
            "Database & Data methodology",
            "database_data_contract_present",
            "database_migration_plan_present",
            "database_production_access_approval_present",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

        self.assertIn("T9-D9", backlog)
        self.assertIn("schema-diff tooling deferred", backlog)
        self.assertIn("runtime/pipeline/RAG signals stay `present_unverified`", backlog)

    def test_track9_llm_ai_rag_docs_and_backlog_are_synced_through_m36(self):
        backlog = TRACK9_BACKLOG.read_text(encoding="utf-8")
        behavioral_evals = (PRODUCT_AGENT_OS / "behavioral-evals.md").read_text(encoding="utf-8")
        scenarios = (PRODUCT_AGENT_OS / "scenarios.md").read_text(encoding="utf-8")
        development_standards = (PRODUCT_AGENT_OS / "development-standards.md").read_text(
            encoding="utf-8"
        )
        readme = (ROOT / "plugins" / "product-agent-os" / "README.md").read_text(encoding="utf-8")

        for expected in [
            "Batch `M20..M29` completed scope",
            "Batch `M30..M36` completed scope",
            "llm_ai_rag_contract_present",
            "renderer file count increased from 142 to 157",
            "diff_signal_policy",
            "AI incident workflow",
        ]:
            with self.subTest(backlog=expected):
                self.assertIn(expected, backlog)

        for expected in [
            "LLM / AI / RAG eval",
            "llm_ai_rag_contract_present",
            "Prompt inspection is not enough",
            "citations alone do not prove grounding",
            "eval tooling selector",
            "AI incident workflow",
        ]:
            with self.subTest(behavioral_evals=expected):
                self.assertIn(expected, behavioral_evals)

        for expected in [
            "LLM / AI / RAG methodology routing",
            "ai-behavior-spec.md",
            "rag-retrieval-config.md",
            "live model calls",
            "agent-handoff-contract.md",
            "filename-only diffs",
        ]:
            with self.subTest(scenarios=expected):
                self.assertIn(expected, scenarios)

        for expected in [
            "LLM / AI / RAG methodology",
            "llm_ai_rag_contract_present",
            "ai-cost-latency-budget.md",
            "live model calls",
            "agent-task-packet.md",
            "eval tooling selector",
        ]:
            with self.subTest(readme=expected):
                self.assertIn(expected, readme)

        self.assertIn("llm_ai_rag_readiness_when_ai_behavior_changes", development_standards)
        self.assertIn("AI/RAG behavior changes record `llm_ai_rag` evidence", development_standards)


if __name__ == "__main__":
    unittest.main()
