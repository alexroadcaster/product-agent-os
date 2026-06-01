import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_graph_chunking import build_structured_chunks  # noqa: E402


class ProjectGraphOverlaysTest(unittest.TestCase):
    def test_markdown_contract_schema_and_diagram_overlays_create_structured_nodes(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "README.md").write_text(
                "# Service Overview\n\n"
                "See [OpenAPI](openapi.yaml) and the flow below.\n\n"
                "```mermaid\n"
                "graph TD\n"
                "  A[Client] --> B[API]\n"
                "```\n",
                encoding="utf-8",
            )
            (workspace / "openapi.yaml").write_text(
                "openapi: 3.0.0\n"
                "info:\n"
                "  title: Demo API\n"
                "paths:\n"
                "  /items:\n"
                "    get:\n"
                "      operationId: listItems\n",
                encoding="utf-8",
            )
            (workspace / "asyncapi.yaml").write_text(
                "asyncapi: 2.6.0\n"
                "channels:\n"
                "  demo.created:\n"
                "    publish:\n"
                "      message:\n"
                "        name: DemoCreated\n",
                encoding="utf-8",
            )
            (workspace / "schema.dbml").write_text(
                "Table users {\n"
                "  id integer [primary key]\n"
                "}\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            nodes = {node["id"]: node for node in graph["nodes"]}
            edges = {(edge["type"], edge["source"], edge["target"]) for edge in graph["edges"]}
            serialized = json.dumps(graph, sort_keys=True)

            for expected_id in [
                "chunk:README.md:heading:service-overview",
                "diagram:README.md:mermaid:1",
                "chunk:openapi.yaml:operation:listItems",
                "chunk:asyncapi.yaml:channel:demo.created",
                "chunk:schema.dbml:table:users",
            ]:
                with self.subTest(expected_id=expected_id):
                    self.assertIn(expected_id, nodes)
                    self.assertTrue(nodes[expected_id]["source_spans"])
                    self.assertNotIn("Client] --> B", serialized)

            self.assertIn(("contains", "file:README.md", "chunk:README.md:heading:service-overview"), edges)
            self.assertIn(("contains", "file:README.md", "diagram:README.md:mermaid:1"), edges)
            self.assertIn(("references", "chunk:README.md:heading:service-overview", "file:openapi.yaml"), edges)
            self.assertEqual(graph["metadata"]["structured_overlay_summary"]["openapi_operations"], 1)
            self.assertEqual(graph["metadata"]["structured_overlay_summary"]["asyncapi_channels"], 1)
            self.assertEqual(graph["metadata"]["structured_overlay_summary"]["dbml_tables"], 1)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_structured_chunks_are_bounded_and_exclude_raw_source(self):
        chunks = build_structured_chunks(
            "README.md",
            "# Title\n\n"
            "[Local](C:\\Users\\person\\private.md)\n\n"
            "Paragraph that should not be copied as a raw source body.\n\n"
            "## Next\n",
            fingerprint="sha256:" + "a" * 64,
            max_chunks=1,
        )

        self.assertEqual(len(chunks["nodes"]), 1)
        self.assertTrue(chunks["truncated"])
        self.assertEqual(chunks["omitted_count"], 1)
        self.assertNotIn("Paragraph that should not be copied", json.dumps(chunks, sort_keys=True))
        self.assertNotIn("C:/Users", json.dumps(chunks, sort_keys=True))

    def test_source_derived_labels_and_secret_like_unresolved_calls_are_redacted(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "README.md").write_text(
                "# PASSWORD = abc123\n# C:\\Users\\person\\private-project\n",
                encoding="utf-8",
            )
            (workspace / "app.py").write_text(
                "def main():\n"
                "    return TOKEN_ABC123_SECRET()\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            serialized = json.dumps(graph, sort_keys=True)

            self.assertNotIn("PASSWORD = abc123", serialized)
            self.assertNotIn("C:/Users", serialized)
            self.assertNotIn("private-project", serialized)
            self.assertNotIn("TOKEN_ABC123_SECRET", serialized)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_duplicate_structural_nodes_and_repeated_calls_are_not_silently_lost(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "README.md").write_text("# Repeat\n\n# Repeat\n", encoding="utf-8")
            (workspace / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            (workspace / "main.py").write_text(
                "from worker import run\n\n"
                "def main():\n"
                "    run()\n"
                "    run()\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            node_ids = {node["id"] for node in graph["nodes"]}
            call_edges = [
                edge
                for edge in graph["edges"]
                if edge["type"] == "calls"
                and edge["source"] == "function:main.main"
                and edge["target"] == "function:worker.run"
            ]

            self.assertIn("chunk:README.md:heading:repeat", node_ids)
            self.assertIn("chunk:README.md:heading:repeat-2", node_ids)
            self.assertEqual(len(call_edges), 2)
            self.assertEqual(len({edge["id"] for edge in call_edges}), 2)
            self.assertEqual(graph["metadata"]["dedupe_summary"]["dropped_nodes"], 0)
            self.assertEqual(graph["metadata"]["dedupe_summary"]["dropped_edges"], 0)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_standalone_plantuml_windows_links_aliases_and_worktree_partition(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "docs" / "api").mkdir(parents=True)
            (workspace / "nested").mkdir()
            (workspace / "docs" / "index.md").write_text("[API](api.md)\n[API V1](api\\v1.md)\n", encoding="utf-8")
            (workspace / "docs" / "api.md").write_text("# API\n", encoding="utf-8")
            (workspace / "docs" / "api" / "v1.md").write_text("# API V1\n", encoding="utf-8")
            (workspace / "diagram.puml").write_text("@startuml\nAlice -> Bob\n@enduml\n", encoding="utf-8")
            (workspace / "nested" / "openapi.yaml").write_text(
                "openapi: 3.0.0\ninfo:\n  title: Nested\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            nodes = {node["id"]: node for node in graph["nodes"]}
            edges = {(edge["type"], edge["source"], edge["target"]) for edge in graph["edges"]}
            aliases = graph["metadata"]["alias_ledger"]["aliases"]
            partitions = {partition["scope"] for partition in graph["metadata"]["partitions"]}

            self.assertIn("diagram:diagram.puml:plantuml:1", nodes)
            self.assertIn(("references", "chunk:docs/index.md:key:api", "file:docs/api.md"), edges)
            self.assertIn(("references", "chunk:docs/index.md:key:api", "file:docs/api/v1.md"), edges)
            self.assertTrue(any(alias["canonical_id"] == "file:nested/openapi.yaml" for alias in aliases))
            self.assertIn("worktree", partitions)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_partitions_aliases_and_readiness_summary_are_bounded(self):
        graph = build_project_code_graph(FIXTURES / "project-code-graph-mixed-docs-contracts")
        metadata = graph["metadata"]

        self.assertIn("workspace", {partition["scope"] for partition in metadata["partitions"]})
        self.assertIn("docs", {partition["scope"] for partition in metadata["partitions"]})
        self.assertIn("contracts", {partition["scope"] for partition in metadata["partitions"]})
        self.assertLessEqual(len(metadata["alias_ledger"]["aliases"]), 100)
        self.assertTrue(
            any(alias["canonical_id"] == "file:openapi.yaml" for alias in metadata["alias_ledger"]["aliases"])
        )
        self.assertIn("methodology_gates", metadata["readiness_summary"])
        self.assertIn("accepted_gaps", metadata["readiness_summary"])
        self.assertLessEqual(len(metadata["readiness_summary"]["methodology_gates"]), 20)
        self.assertTrue(graph["validation"]["ok"], graph["validation"])


if __name__ == "__main__":
    unittest.main()
