import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_graph_analysis import build_project_graph_analysis  # noqa: E402


class ProjectGraphAnalysisTest(unittest.TestCase):
    def test_analysis_report_surfaces_hotspots_ambiguous_edges_and_agent_questions_without_source_bodies(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "app").mkdir(parents=True)
            (workspace / "other").mkdir()
            (workspace / "frontend").mkdir()
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "other" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "other" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            (workspace / "app" / "main.py").write_text(
                "from other.worker import run\n\n"
                "def main():\n"
                "    unknown_dynamic()\n"
                "    return run()\n",
                encoding="utf-8",
            )
            (workspace / "frontend" / "widget.ts").write_text("export const widget = 1;\n", encoding="utf-8")

            graph = build_project_code_graph(workspace)
            report = build_project_graph_analysis(graph)
            serialized = json.dumps(report, sort_keys=True)

            self.assertEqual(report["schema_version"], 1)
            self.assertEqual(report["write_policy"], "read_only")
            self.assertTrue(report["hotspots"])
            self.assertTrue(report["god_nodes"])
            self.assertTrue(report["ambiguous_edge_inventory"])
            self.assertTrue(
                any(
                    item.get("source") == "function:app.main.main" and item.get("call_name") == "unknown_dynamic"
                    for item in report["ambiguous_edge_inventory"]
                ),
                report["ambiguous_edge_inventory"],
            )
            self.assertTrue(report["surprising_cross_module_links"])
            self.assertNotIn("typescript", report["unsupported_language_summary"])
            self.assertGreaterEqual(report["partial_language_summary"]["typescript"], 1)
            self.assertTrue(report["suggested_agent_questions"])
            self.assertNotIn("unknown_dynamic()", serialized)
            self.assertNotIn(str(workspace), serialized)

    def test_analysis_report_is_bounded_for_large_graphs(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {
                "scan_id": "scan-test",
                "language_support_summary": {"python": "supported"},
                "python_scanner": {"unresolved_calls": [{"source": f"function:m{i}", "call": "dynamic"} for i in range(50)]},
            },
            "nodes": [
                {"id": f"function:m{index}", "type": "function", "label": f"m{index}", "status": "current", "language": "python"}
                for index in range(100)
            ],
            "edges": [
                {
                    "id": f"edge:{index}",
                    "type": "calls",
                    "source": "function:m0",
                    "target": f"function:m{index}",
                    "confidence": "inferred",
                    "status": "current",
                }
                for index in range(1, 100)
            ],
            "observations": [],
        }

        report = build_project_graph_analysis(graph, max_items=10)

        self.assertLessEqual(len(report["hotspots"]), 10)
        self.assertLessEqual(len(report["ambiguous_edge_inventory"]), 10)
        self.assertTrue(report["budget"]["truncated"])


if __name__ == "__main__":
    unittest.main()
