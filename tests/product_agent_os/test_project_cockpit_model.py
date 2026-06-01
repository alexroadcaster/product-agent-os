import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_cockpit_model import (  # noqa: E402
    COCKPIT_PAGE_LABELS,
    build_project_cockpit_model,
)
from product_agent_os.project_graph_analysis import build_project_graph_analysis  # noqa: E402
from product_agent_os.project_graph_queries import query_project_graph  # noqa: E402


class ProjectCockpitModelTest(unittest.TestCase):
    def test_cockpit_model_exposes_exactly_eight_pages_and_maps_sections_once(self):
        with TemporaryDirectory() as tmp:
            workspace = _write_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            analysis = build_project_graph_analysis(graph)
            trace = query_project_graph(
                graph,
                {
                    "query": "trace",
                    "node_id": "function:tests.test_worker.test_run",
                    "target_id": "function:app.worker.run",
                    "max_depth": 5,
                },
            )

            model = build_project_cockpit_model(
                graph,
                analysis=analysis,
                query_packets=[trace],
                active_page="code-intelligence",
                section_anchor="code-flow",
            )
            serialized = json.dumps(model, sort_keys=True)

            self.assertEqual(model["schema_version"], 1)
            self.assertEqual(model["write_policy"], "read_only")
            self.assertEqual(model["source_policy"], "generated cockpit is not source of truth")
            self.assertEqual([page["label"] for page in model["pages"]], COCKPIT_PAGE_LABELS)
            self.assertEqual(len(model["pages"]), 8)
            self.assertEqual(model["active_page"], "code-intelligence")
            self.assertEqual(model["section_anchor"], "code-flow")
            self.assertNotIn("code-flow", {page["id"] for page in model["pages"]})

            section_ids = [section["id"] for page in model["pages"] for section in page["sections"]]
            self.assertEqual(len(section_ids), len(set(section_ids)))
            code_page = next(page for page in model["pages"] if page["id"] == "code-intelligence")
            self.assertIn("code-flow", {section["id"] for section in code_page["sections"]})

            for page in model["pages"]:
                self.assertIsInstance(page["role"], str)
                self.assertIsInstance(page["source_links"], list)
                self.assertIsInstance(page["stale_flags"], list)
                self.assertIsInstance(page["graph_packets"], list)
                self.assertIsInstance(page["approval_boundaries"], list)
                self.assertIsInstance(page["action_surfaces"], list)

            self.assertTrue(model["navigation"]["local_section_anchors"])
            self.assertTrue(model["graph_summary"]["node_count"])
            self.assertTrue(model["code_flow"]["module_flows"])
            self.assertIn("graph_packets_are_orientation_evidence_only", serialized)
            self.assertNotIn("return 'ok'", serialized)
            self.assertNotIn(str(workspace), serialized)

    def test_invalid_active_page_and_anchor_fall_back_without_blocking_render(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {"scan_id": "scan-test", "node_count": 0, "edge_count": 0},
            "nodes": [],
            "edges": [],
        }

        model = build_project_cockpit_model(
            graph,
            active_page="missing-page",
            section_anchor="missing-section",
        )

        self.assertEqual(model["active_page"], "overview")
        self.assertEqual(model["section_anchor"], "")
        self.assertIn("active_page_fallback", model["stale_flags"])
        self.assertIn("section_anchor_fallback", model["stale_flags"])


def _write_workspace(workspace: Path) -> Path:
    (workspace / "app").mkdir(parents=True)
    (workspace / "tests").mkdir()
    (workspace / "docs").mkdir()
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
    (workspace / "docs" / "index.md").write_text("# Docs\n\nSee app.worker.\n", encoding="utf-8")
    (workspace / "openapi.yaml").write_text("openapi: 3.0.0\ninfo:\n  title: Demo\n  version: 1.0.0\n", encoding="utf-8")
    return workspace


if __name__ == "__main__":
    unittest.main()
