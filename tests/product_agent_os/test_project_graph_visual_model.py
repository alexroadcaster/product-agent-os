import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph, build_synthetic_project_graph  # noqa: E402
from product_agent_os.project_graph_visual_model import (  # noqa: E402
    DEFAULT_VISIBLE_NODE_LIMIT,
    HARD_VISIBLE_EDGE_LIMIT,
    HARD_VISIBLE_NODE_LIMIT,
    build_project_graph_visual_model,
)


class ProjectGraphVisualModelTest(unittest.TestCase):
    def test_visual_projection_is_graphology_compatible_source_free_and_local_only(self):
        with TemporaryDirectory() as tmp:
            workspace = _write_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)

            projection = build_project_graph_visual_model(
                graph,
                selected_node_id="function:app.main.main",
                max_nodes=80,
                max_edges=120,
            )
            serialized = json.dumps(projection, sort_keys=True)

            self.assertEqual(projection["schema_version"], 1)
            self.assertEqual(projection["write_policy"], "read_only")
            self.assertTrue(projection["graphology_compatible"])
            self.assertEqual(projection["renderer_policy"]["external_assets"], "forbidden")
            self.assertEqual(projection["renderer_policy"]["sigma_status"], "not_bundled_static_fallback")
            self.assertTrue(projection["nodes"])
            self.assertTrue(projection["edges"])
            self.assertLessEqual(len(projection["nodes"]), 80)
            self.assertLessEqual(len(projection["edges"]), 120)
            self.assertTrue(projection["clusters"])
            self.assertTrue(projection["focused_subgraph"]["selected_node"])

            first_node = projection["nodes"][0]
            self.assertIn("key", first_node)
            self.assertIn("attributes", first_node)
            for field in ["x", "y", "size", "color", "community", "lod_tier", "label_priority", "renderer_hint"]:
                self.assertIn(field, first_node["attributes"])

            first_edge = projection["edges"][0]
            self.assertIn("key", first_edge)
            self.assertIn("source", first_edge)
            self.assertIn("target", first_edge)
            self.assertIn("confidence", first_edge["attributes"])

            self.assertIn("node_type", projection["available_filters"])
            self.assertIn("confidence", projection["available_filters"])
            self.assertIn("text", projection["available_filters"])
            self.assertIn("fit", projection["navigation_commands"])
            self.assertIn("copy", projection["navigation_commands"])
            self.assertNotIn("return 'ok'", serialized)
            self.assertNotIn(str(workspace), serialized)

    def test_large_graph_projection_uses_lod_clusters_and_static_fallback_bounds(self):
        graph = build_synthetic_project_graph(node_count=10_000)

        projection = build_project_graph_visual_model(graph, max_nodes=120, max_edges=150)

        self.assertLessEqual(len(projection["nodes"]), 120)
        self.assertEqual(projection["performance_budget"]["declared_node_count"], 10_000)
        self.assertGreater(projection["performance_budget"]["omitted_node_count"], 0)
        self.assertEqual(projection["render_modes"]["large_graph"], "clustered_static_fallback")
        self.assertTrue(projection["performance_budget"]["large_graph"])
        self.assertTrue(any(node["attributes"]["lod_tier"] >= 1 for node in projection["nodes"]))
        self.assertLessEqual(len(projection["nodes"]), DEFAULT_VISIBLE_NODE_LIMIT)

    def test_visual_projection_clamps_caller_requested_large_limits(self):
        graph = build_synthetic_project_graph(node_count=10_000)

        projection = build_project_graph_visual_model(graph, max_nodes=100_000, max_edges=100_000)
        budget = projection["performance_budget"]

        self.assertEqual(budget["requested_visible_node_limit"], 100_000)
        self.assertEqual(budget["requested_visible_edge_limit"], 100_000)
        self.assertEqual(budget["visible_node_limit"], HARD_VISIBLE_NODE_LIMIT)
        self.assertEqual(budget["visible_edge_limit"], HARD_VISIBLE_EDGE_LIMIT)
        self.assertLessEqual(len(projection["nodes"]), HARD_VISIBLE_NODE_LIMIT)
        self.assertLessEqual(len(projection["edges"]), HARD_VISIBLE_EDGE_LIMIT)

    def test_visual_projection_strips_unsafe_source_like_fields_paths_and_external_urls(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {"scan_id": "scan-unsafe", "node_count": 1, "edge_count": 0},
            "nodes": [
                {
                    "id": "file:unsafe.py",
                    "type": "module",
                    "label": "See https://example.invalid/raw and C:\\Users\\person\\repo",
                    "status": "current",
                    "language": "python",
                    "path": "C:\\Users\\person\\repo\\unsafe.py",
                    "raw_source": "TOKEN=fixture-secret",
                }
            ],
            "edges": [],
        }

        projection = build_project_graph_visual_model(graph)
        serialized = json.dumps(projection, sort_keys=True)

        self.assertNotIn("https://example.invalid", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("fixture-secret", serialized)
        self.assertEqual(projection["nodes"][0]["attributes"]["path"], "")


def _write_workspace(workspace: Path) -> Path:
    (workspace / "app").mkdir(parents=True)
    (workspace / "tests").mkdir()
    (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
    (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
    (workspace / "app" / "main.py").write_text(
        "from app.worker import run\n\n"
        "def main():\n"
        "    return run()\n",
        encoding="utf-8",
    )
    (workspace / "tests" / "test_worker.py").write_text(
        "from app.worker import run\n\n"
        "def test_run():\n"
        "    assert run() == 'ok'\n",
        encoding="utf-8",
    )
    return workspace


if __name__ == "__main__":
    unittest.main()
