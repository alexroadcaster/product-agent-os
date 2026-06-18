import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_graph_ontology import (  # noqa: E402
    GRAPH_LIMITS,
    default_ontology,
    register_ontology_extension,
    validate_graph_schema,
)
from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402


DECISION_ARTIFACT = ROOT / "docs" / "superpowers" / "specs" / "batch39-s4-graph-depth-s0-ontology-parser-decision.json"


class ProjectGraphOntologyTest(unittest.TestCase):
    def test_default_ontology_defines_batch_13_node_edge_and_status_contract(self):
        ontology = default_ontology()

        self.assertEqual(ontology["schema_version"], 1)
        self.assertIn("workspace", ontology["node_types"])
        self.assertIn("module", ontology["node_types"])
        self.assertIn("test", ontology["node_types"])
        self.assertIn("generated_artifact", ontology["node_types"])
        self.assertIn("contains", ontology["edge_types"])
        self.assertIn("references", ontology["edge_types"])
        self.assertIn("impacts", ontology["edge_types"])
        self.assertIn("verified", ontology["confidence_levels"])
        self.assertIn("inferred", ontology["confidence_levels"])
        self.assertIn("unsupported", ontology["status_values"])
        self.assertEqual(ontology["language_support"]["python"], "supported")
        self.assertEqual(ontology["language_support"]["typescript"], "supported_conservative_stdlib")
        self.assertEqual(ontology["language_support"]["javascript"], "supported_conservative_stdlib")
        self.assertEqual(ontology["language_support"]["unknown"], "file_only")
        self.assertLessEqual(GRAPH_LIMITS["max_nodes"], 10_000)

    def test_graph_depth_decision_artifact_records_ontology_and_parser_boundaries(self):
        payload = json.loads(DECISION_ARTIFACT.read_text(encoding="utf-8"))

        self.assertEqual(payload["artifact_kind"], "batch39_s4_graph_depth_ontology_parser_decision")
        self.assertEqual(payload["status"], "accepted_local_decision_no_new_dependency")
        self.assertEqual(
            payload["task_ids"],
            ["B39-S4-GRAPH-DEPTH-00", "B39-S4-GRAPH-DEPTH-07"],
        )
        self.assertEqual(payload["ontology_decision"]["core_node_types_added"], [])
        self.assertEqual(payload["ontology_decision"]["core_edge_types_added"], [])
        self.assertEqual(payload["ontology_decision"]["schema_migration_required"], False)
        self.assertIn("component", payload["ontology_decision"]["framework_terms_kept_as_metadata"])
        self.assertIn("api_route", payload["ontology_decision"]["framework_terms_kept_as_metadata"])
        self.assertEqual(
            payload["parser_dependency_decision"]["selected_option"],
            "stdlib_regex_no_external_dependency",
        )
        self.assertEqual(payload["parser_dependency_decision"]["dependency_installation_required"], False)
        self.assertEqual(payload["parser_dependency_decision"]["external_parser_dependency_allowed"], False)
        self.assertIn("tree-sitter WASM", payload["parser_dependency_decision"]["deferred_options"])
        self.assertIn("release readiness", " ".join(payload["unsupported_claims"]))

    def test_project_graph_metadata_cites_graph_depth_decision(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "web").mkdir(parents=True)
            (workspace / "web" / "widget.ts").write_text(
                "export function Widget() {\n"
                "  return null;\n"
                "}\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            decision = graph["metadata"]["graph_depth_decision"]

            self.assertEqual(decision["decision_id"], "B39-S4-GD-S0-ONTOLOGY-PARSER-DECISION")
            self.assertEqual(decision["decision_artifact"], "docs/superpowers/specs/batch39-s4-graph-depth-s0-ontology-parser-decision.json")
            self.assertEqual(decision["parser_dependency_policy"], "stdlib_regex_no_external_dependency")
            self.assertEqual(decision["core_node_types_added"], [])
            self.assertEqual(decision["schema_migration_required"], False)
            self.assertEqual(
                graph["metadata"]["language_support_summary"]["typescript"],
                "supported_conservative_stdlib",
            )
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_register_ontology_extension_keeps_core_terms_and_marks_extension(self):
        extended = register_ontology_extension(
            default_ontology(),
            node_types=["service_boundary"],
            edge_types=["publishes"],
        )

        self.assertIn("workspace", extended["node_types"])
        self.assertIn("service_boundary", extended["node_types"])
        self.assertIn("publishes", extended["edge_types"])
        self.assertEqual(extended["extension_status"], "registered")

    def test_validate_graph_schema_accepts_safe_graph_and_rejects_invalid_or_leaky_graph(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {
                "source_boundary": "raw_source_bodies_excluded",
                "generated_view_policy": "html_is_review_only",
            },
            "nodes": [
                {
                    "id": "workspace:demo",
                    "type": "workspace",
                    "label": "demo",
                    "status": "current",
                    "language": "unknown",
                    "observation_ids": ["obs:workspace"],
                },
                {
                    "id": "file:app/main.py",
                    "type": "module",
                    "label": "app/main.py",
                    "status": "current",
                    "language": "python",
                    "path": "app/main.py",
                    "source_spans": [
                        {
                            "relative_path": "app/main.py",
                            "start_line": 1,
                            "end_line": 4,
                            "fingerprint": "sha256:" + "a" * 64,
                        }
                    ],
                    "observation_ids": ["obs:file"],
                },
            ],
            "edges": [
                {
                    "id": "edge:workspace-demo:file-app-main-py",
                    "type": "contains",
                    "source": "workspace:demo",
                    "target": "file:app/main.py",
                    "confidence": "verified",
                    "status": "current",
                    "observation_ids": ["obs:edge"],
                }
            ],
            "observations": [
                {
                    "id": "obs:workspace",
                    "scan_id": "scan-1",
                    "subject_id": "workspace:demo",
                    "relative_path": ".",
                    "span": {"start_line": 1, "end_line": 1},
                    "fingerprint": "sha256:" + "a" * 64,
                    "extractor": "workspace_inventory",
                    "confidence": "verified",
                    "redaction_status": "redacted",
                    "raw_source_status": "excluded",
                },
                {
                    "id": "obs:file",
                    "scan_id": "scan-1",
                    "subject_id": "file:app/main.py",
                    "relative_path": "app/main.py",
                    "span": {"start_line": 1, "end_line": 4},
                    "fingerprint": "sha256:" + "a" * 64,
                    "extractor": "file_inventory",
                    "confidence": "verified",
                    "redaction_status": "redacted",
                    "raw_source_status": "excluded",
                },
                {
                    "id": "obs:edge",
                    "scan_id": "scan-1",
                    "subject_id": "edge:workspace-demo:file-app-main-py",
                    "relative_path": "app/main.py",
                    "span": {"start_line": 1, "end_line": 1},
                    "fingerprint": "sha256:" + "a" * 64,
                    "extractor": "file_inventory",
                    "confidence": "verified",
                    "redaction_status": "redacted",
                    "raw_source_status": "excluded",
                }
            ],
        }

        accepted = validate_graph_schema(graph)
        self.assertTrue(accepted["ok"], accepted)

        leaky = json.loads(json.dumps(graph))
        leaky["nodes"][1]["raw_source"] = "TOKEN=abc123\nprint('secret')"
        rejected = validate_graph_schema(leaky)
        self.assertFalse(rejected["ok"])
        self.assertIn("node.raw_source:forbidden", rejected["errors"])
        self.assertIn("redaction:secret_retained", rejected["errors"])

    def test_validate_graph_schema_requires_observation_contract_and_references(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {
                "source_boundary": "raw_source_bodies_excluded",
                "generated_view_policy": "html_is_review_only",
            },
            "nodes": [
                {
                    "id": "workspace:demo",
                    "type": "workspace",
                    "label": "demo",
                    "status": "current",
                    "language": "unknown",
                    "observation_ids": ["obs:missing"],
                }
            ],
            "edges": [],
            "observations": [
                {
                    "id": "obs:incomplete",
                    "relative_path": "README.md",
                    "span": {"start_line": 1, "end_line": 1},
                    "fingerprint": "sha256:" + "b" * 64,
                }
            ],
        }

        result = validate_graph_schema(graph)

        self.assertFalse(result["ok"])
        self.assertIn("observation.scan_id:required", result["errors"])
        self.assertIn("observation.subject_id:required", result["errors"])
        self.assertIn("observation.extractor:required", result["errors"])
        self.assertIn("observation.confidence:required", result["errors"])
        self.assertIn("observation.redaction_status:required", result["errors"])
        self.assertIn("observation.raw_source_status:must_be_excluded", result["errors"])
        self.assertIn("node.observation_ids:unknown_observation", result["errors"])

    def test_validate_graph_schema_rejects_nested_raw_source_keys(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {
                "source_boundary": "raw_source_bodies_excluded",
                "generated_view_policy": "html_is_review_only",
                "nested": {"content": "def leaked():\n    return True"},
            },
            "nodes": [],
            "edges": [],
            "observations": [],
        }

        result = validate_graph_schema(graph)

        self.assertFalse(result["ok"])
        self.assertIn("metadata.nested.content:forbidden", result["errors"])


if __name__ == "__main__":
    unittest.main()
