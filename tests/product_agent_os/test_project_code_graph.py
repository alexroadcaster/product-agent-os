import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import (  # noqa: E402
    PROJECT_GRAPH_TARGET,
    build_project_code_graph,
    build_synthetic_project_graph_from_fixture,
    build_synthetic_project_graph,
    graph_to_jsonl,
)


class ProjectCodeGraphTest(unittest.TestCase):
    def test_build_project_code_graph_is_read_only_redacted_and_file_level_for_batch_13(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "app").mkdir()
            (workspace / "app" / "main.py").write_text(
                "API_TOKEN=abc123\n\ndef run():\n    return 'ok'\n",
                encoding="utf-8",
            )
            (workspace / "README.md").write_text("# Demo\n\nSee app/main.py.\n", encoding="utf-8")
            before = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*"))

            graph = build_project_code_graph(workspace)

            after = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*"))
            serialized = json.dumps(graph, sort_keys=True)
            self.assertEqual(after, before)
            self.assertEqual(graph["schema_version"], 1)
            self.assertEqual(graph["write_policy"], "read_only")
            self.assertEqual(graph["artifact_targets"]["json"], PROJECT_GRAPH_TARGET)
            self.assertEqual(graph["metadata"]["source_boundary"], "raw_source_bodies_excluded")
            self.assertNotIn("API_TOKEN=abc123", serialized)
            self.assertNotIn(str(workspace), serialized)
            self.assertIn("file:app/main.py", {node["id"] for node in graph["nodes"]})
            self.assertIn("file:README.md", {node["id"] for node in graph["nodes"]})
            self.assertTrue(any(edge["type"] == "contains" for edge in graph["edges"]))
            for node in graph["nodes"]:
                self.assertNotIn("raw_source", node)
                self.assertIsInstance(node.get("observation_ids"), list)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_edge_ids_do_not_collide_for_similar_file_names(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "a-b.py").write_text("print('dash')\n", encoding="utf-8")
            (workspace / "a_b.py").write_text("print('underscore')\n", encoding="utf-8")

            graph = build_project_code_graph(workspace)

            edge_ids = [edge["id"] for edge in graph["edges"]]
            self.assertEqual(len(edge_ids), len(set(edge_ids)))
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_large_file_line_count_is_capped_without_loading_full_source_body(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "large.py").write_text("x = 1\n" * 20_000, encoding="utf-8")

            graph = build_project_code_graph(workspace)
            large = next(node for node in graph["nodes"] if node.get("path") == "large.py")

            self.assertEqual(large["source_spans"][0]["end_line"], 10_000)
            self.assertEqual(graph["metadata"]["line_count_policy"], "capped_at_10000")
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_graph_to_jsonl_emits_bounded_records_without_source_bodies(self):
        graph = build_project_code_graph(FIXTURES / "project-code-graph-minimal-python")

        lines = graph_to_jsonl(graph).splitlines()

        self.assertTrue(lines)
        self.assertTrue(all(json.loads(line)["record_kind"] in {"metadata", "node", "edge", "observation"} for line in lines))
        self.assertNotIn("def main", "\n".join(lines))

    def test_graph_artifact_records_temporal_delta_when_previous_graph_is_supplied(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "keep.py").write_text("print('keep')\n", encoding="utf-8")
            (workspace / "remove.py").write_text("print('remove')\n", encoding="utf-8")
            first = build_project_code_graph(workspace)
            (workspace / "remove.py").unlink()

            second = build_project_code_graph(workspace, previous_graph=first)

            delta = second["metadata"]["temporal_delta"]
            self.assertEqual(delta["status"], "changed")
            self.assertTrue(delta["invalidated_edges"])
            self.assertTrue(all(item["status"] == "invalidated" for item in delta["invalidated_edges"]))

    def test_docs_heavy_fixture_produces_markdown_and_mkdocs_file_level_nodes(self):
        graph = build_project_code_graph(FIXTURES / "project-code-graph-docs-heavy")

        node_paths = {node.get("path") for node in graph["nodes"]}
        self.assertIn("docs/index.md", node_paths)
        self.assertIn("docs/architecture.md", node_paths)
        self.assertIn("mkdocs.yml", node_paths)
        self.assertEqual(graph["metadata"]["language_support_summary"]["markdown"], "structured_overlay_supported")
        self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_imported_skill_pack_prefix_is_excluded_and_reported_in_scope_policy(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "frontend").mkdir()
            (workspace / "frontend" / "app.ts").write_text("export const app = true;\n", encoding="utf-8")
            imported = workspace / "antigravity-awesome-skills-main" / "skills" / "loki-mode"
            imported.mkdir(parents=True)
            (imported / "SKILL.md").write_text("# Imported Skill\n", encoding="utf-8")
            (imported / "benchmarks.jsonl").write_text("{}\n" * 20, encoding="utf-8")

            graph = build_project_code_graph(workspace)

            node_paths = {node.get("path") for node in graph["nodes"]}
            self.assertIn("frontend/app.ts", node_paths)
            self.assertFalse(any(str(path).startswith("antigravity-awesome-skills-main/") for path in node_paths))
            scope_policy = graph["metadata"]["scope_policy"]
            self.assertIn("antigravity-awesome-skills-main", scope_policy["excluded_prefixes"])
            self.assertEqual(scope_policy["status"], "excluded_prefixes_reported")
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_synthetic_scale_graph_keeps_prompt_payload_bounded_for_1k_5k_10k_cases(self):
        for node_count in [1_000, 5_000, 10_000]:
            with self.subTest(node_count=node_count):
                graph = build_synthetic_project_graph(node_count=node_count)

                self.assertEqual(graph["metadata"]["node_count"], node_count)
                self.assertLessEqual(len(graph["nodes"]), 250)
                self.assertEqual(graph["metadata"]["omitted_node_count"], node_count - len(graph["nodes"]))
                self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_scale_fixture_dirs_drive_bounded_synthetic_graphs(self):
        for fixture_name, node_count in [
            ("project-code-graph-scale-1k", 1_000),
            ("project-code-graph-scale-5k", 5_000),
            ("project-code-graph-scale-10k", 10_000),
        ]:
            with self.subTest(fixture_name=fixture_name):
                graph = build_synthetic_project_graph_from_fixture(FIXTURES / fixture_name)

                self.assertEqual(graph["metadata"]["node_count"], node_count)
                self.assertLessEqual(len(graph["nodes"]), 250)
                self.assertTrue(graph["validation"]["ok"], graph["validation"])


if __name__ == "__main__":
    unittest.main()
