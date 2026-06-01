import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_graph_manifest import collect_project_files  # noqa: E402


class ProjectGraphSafetyTest(unittest.TestCase):
    def test_graph_artifact_excludes_raw_source_absolute_paths_and_secret_like_values(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "config.py").write_text(
                "PASSWORD = 'abc123'\nLOCAL = r'C:\\Users\\person\\repo'\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            serialized = json.dumps(graph, sort_keys=True)

            self.assertNotIn("PASSWORD = 'abc123'", serialized)
            self.assertNotIn("C:\\Users\\person\\repo", serialized)
            self.assertNotIn(str(workspace), serialized)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])
            self.assertEqual(graph["metadata"]["source_boundary"], "raw_source_bodies_excluded")

    def test_generated_and_low_value_files_are_classified_without_false_completeness(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "src").mkdir(parents=True)
            (workspace / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
            (workspace / "src" / "client.generated.py").write_text("print('generated')\n", encoding="utf-8")
            (workspace / "README.md").write_text("# Demo\n", encoding="utf-8")

            files = collect_project_files(workspace)
            graph = build_project_code_graph(workspace)
            by_path = {item["relative_path"]: item for item in files}
            generated_node = next(node for node in graph["nodes"] if node.get("path") == "src/client.generated.py")

            self.assertTrue(by_path["src/client.generated.py"]["generated"])
            self.assertEqual(generated_node["status"], "generated")
            self.assertEqual(graph["metadata"]["language_support_summary"]["python"], "supported")
            self.assertIn("markdown", graph["metadata"]["language_support_summary"])


if __name__ == "__main__":
    unittest.main()
