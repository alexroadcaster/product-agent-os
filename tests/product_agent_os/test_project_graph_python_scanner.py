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
from product_agent_os.project_graph_adapters import available_graph_adapters  # noqa: E402
from product_agent_os.project_graph_ontology import default_ontology  # noqa: E402
from product_agent_os.project_graph_queries import query_project_graph  # noqa: E402


class ProjectGraphPythonScannerTest(unittest.TestCase):
    def test_python_package_modules_classes_functions_and_methods_have_stable_spans(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            _write_python_workspace(workspace)

            graph = build_project_code_graph(workspace)
            nodes = {node["id"]: node for node in graph["nodes"]}
            edges = {(edge["type"], edge["source"], edge["target"]) for edge in graph["edges"]}

            for expected_id in [
                "package:app",
                "module:app.main",
                "module:app.worker",
                "class:app.main.Controller",
                "function:app.main.main",
                "method:app.main.Controller.handle",
                "function:app.worker.run",
            ]:
                with self.subTest(expected_id=expected_id):
                    self.assertIn(expected_id, nodes)
                    self.assertEqual(nodes[expected_id]["language"], "python")
                    self.assertEqual(nodes[expected_id]["status"], "current")
                    self.assertTrue(nodes[expected_id]["source_spans"])
                    self.assertLessEqual(
                        nodes[expected_id]["source_spans"][0]["start_line"],
                        nodes[expected_id]["source_spans"][0]["end_line"],
                    )

            self.assertIn(("contains", "package:app", "module:app.main"), edges)
            self.assertIn(("contains", "module:app.main", "class:app.main.Controller"), edges)
            self.assertIn(("contains", "module:app.main", "function:app.main.main"), edges)
            self.assertIn(("contains", "class:app.main.Controller", "method:app.main.Controller.handle"), edges)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_python_imports_calls_and_test_links_are_confidence_labelled(self):
        graph = build_project_code_graph(FIXTURES / "project-code-graph-minimal-python")
        nodes = {node["id"]: node for node in graph["nodes"]}
        edge_index = {(edge["type"], edge["source"], edge["target"]): edge for edge in graph["edges"]}

        self.assertIn("module:app.main", nodes)
        self.assertIn("function:app.worker.run", nodes)
        self.assertIn("function:tests.test_worker.test_run", nodes)

        import_edge = edge_index[("imports", "module:app.main", "function:app.worker.run")]
        call_edge = edge_index[("calls", "function:app.main.main", "function:app.worker.run")]
        test_edge = edge_index[("tests", "function:tests.test_worker.test_run", "function:app.worker.run")]

        self.assertEqual(import_edge["confidence"], "verified")
        self.assertEqual(call_edge["confidence"], "inferred")
        self.assertEqual(test_edge["confidence"], "inferred")
        self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_dotted_absolute_import_calls_resolve_when_single_candidate_exists(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            (workspace / "consumer.py").write_text(
                "import app.worker\n\n"
                "def main():\n"
                "    return app.worker.run()\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            edge_index = {(edge["type"], edge["source"], edge["target"]): edge for edge in graph["edges"]}

            self.assertIn(("imports", "module:consumer", "module:app.worker"), edge_index)
            self.assertIn(("calls", "function:consumer.main", "function:app.worker.run"), edge_index)
            self.assertEqual(
                edge_index[("calls", "function:consumer.main", "function:app.worker.run")]["confidence"],
                "inferred",
            )
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_fixture_and_eval_fixture_files_link_to_imported_implementation_targets(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "app").mkdir(parents=True)
            (workspace / "fixtures").mkdir()
            (workspace / "eval-fixtures").mkdir()
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            (workspace / "fixtures" / "worker_fixture.py").write_text(
                "from app.worker import run\n\n"
                "def sample_run():\n"
                "    return run()\n",
                encoding="utf-8",
            )
            (workspace / "eval-fixtures" / "worker_eval.py").write_text(
                "from app.worker import run\n\n"
                "def replay_case():\n"
                "    return run()\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            nodes = {node["id"]: node for node in graph["nodes"]}
            edge_index = {(edge["type"], edge["source"], edge["target"]) for edge in graph["edges"]}

            self.assertEqual(nodes["file:fixtures/worker_fixture.py"]["type"], "fixture")
            self.assertEqual(nodes["file:eval-fixtures/worker_eval.py"]["type"], "fixture")
            self.assertIn(("tests", "function:fixtures.worker_fixture.sample_run", "function:app.worker.run"), edge_index)
            self.assertIn(("tests", "function:eval-fixtures.worker_eval.replay_case", "function:app.worker.run"), edge_index)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_ambiguous_python_calls_are_reported_without_guessing_verified_edges(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "app.py").write_text(
                "def execute(callback):\n"
                "    callback()\n"
                "    return missing_symbol()\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            calls = [edge for edge in graph["edges"] if edge["type"] == "calls"]
            unresolved = graph["metadata"]["python_scanner"]["unresolved_calls"]
            serialized = json.dumps(graph, sort_keys=True)

            self.assertEqual(calls, [])
            self.assertEqual({item["name"] for item in unresolved}, {"callback", "missing_symbol"})
            self.assertNotIn("callback()", serialized)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_missing_imported_symbol_does_not_fall_back_to_module_call(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            (workspace / "consumer.py").write_text(
                "from app.worker import missing\n\n"
                "def main():\n"
                "    return missing()\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            edge_index = {(edge["type"], edge["source"], edge["target"]) for edge in graph["edges"]}
            unresolved = graph["metadata"]["python_scanner"]["unresolved_calls"]

            self.assertNotIn(("calls", "function:consumer.main", "module:app.worker"), edge_index)
            self.assertTrue(any(item["name"] == "missing" for item in unresolved))
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_generated_typescript_files_stay_file_only_with_adapter_boundary(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "web").mkdir(parents=True)
            (workspace / "web" / "app.generated.ts").write_text("export const value = 1;\n", encoding="utf-8")
            (workspace / "app.py").write_text("print('supported')\n", encoding="utf-8")

            graph = build_project_code_graph(workspace)
            nodes = {node["id"]: node for node in graph["nodes"]}

            self.assertIn("python_ast", available_graph_adapters())
            self.assertIn("typescript_javascript_stdlib", available_graph_adapters())
            self.assertIn("unsupported_file", available_graph_adapters())
            self.assertEqual(nodes["file:web/app.generated.ts"]["language"], "typescript")
            self.assertEqual(nodes["file:web/app.generated.ts"]["status"], "generated")
            self.assertEqual(graph["metadata"]["adapter_summary"]["typescript"], "typescript_javascript_stdlib")
            self.assertNotIn("module:web.app.generated", nodes)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_typescript_exports_imports_and_calls_are_entity_level_without_external_parser(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "web").mkdir(parents=True)
            (workspace / "web" / "apiClient.ts").write_text(
                "export function fetchUser(id: string) {\n"
                "  return { id };\n"
                "}\n",
                encoding="utf-8",
            )
            (workspace / "web" / "UserCard.tsx").write_text(
                "import { fetchUser } from './apiClient';\n\n"
                "export function UserCard() {\n"
                "  const user = fetchUser('42');\n"
                "  return <section>{user.id}</section>;\n"
                "}\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            nodes = {node["id"]: node for node in graph["nodes"]}
            edge_index = {(edge["type"], edge["source"], edge["target"]): edge for edge in graph["edges"]}
            serialized = json.dumps(graph, sort_keys=True)

            self.assertIn("typescript_javascript_stdlib", available_graph_adapters())
            for expected_id in [
                "module:web.apiClient",
                "module:web.UserCard",
                "function:web.apiClient.fetchUser",
                "function:web.UserCard.UserCard",
            ]:
                with self.subTest(expected_id=expected_id):
                    self.assertIn(expected_id, nodes)
                    self.assertEqual(nodes[expected_id]["language"], "typescript")
                    self.assertEqual(nodes[expected_id]["status"], "current")
                    self.assertTrue(nodes[expected_id]["source_spans"])

            self.assertEqual(graph["metadata"]["adapter_summary"]["typescript"], "typescript_javascript_stdlib")
            self.assertEqual(graph["metadata"]["typescript_javascript_scanner"]["parser_dependency"], "stdlib_regex_no_external_dependency")
            self.assertIn(("imports", "module:web.UserCard", "function:web.apiClient.fetchUser"), edge_index)
            self.assertIn(("calls", "function:web.UserCard.UserCard", "function:web.apiClient.fetchUser"), edge_index)
            self.assertNotIn("return <section>", serialized)
            self.assertNotIn(str(workspace), serialized)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_typescript_framework_terms_remain_metadata_not_node_types(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "page.tsx").write_text(
                "export function useUser() {\n"
                "  return { id: '42' };\n"
                "}\n\n"
                "export function UserPage() {\n"
                "  const user = useUser();\n"
                "  return <main>{user.id}</main>;\n"
                "}\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            node_types = {node["type"] for node in graph["nodes"]}

            self.assertLessEqual(node_types, set(default_ontology()["node_types"]))
            self.assertNotIn("component", node_types)
            self.assertNotIn("hook", node_types)
            self.assertNotIn("api_route", node_types)
            self.assertIn(
                "framework semantics remain unsupported",
                graph["metadata"]["typescript_javascript_scanner"]["unsupported_syntax_policy"],
            )
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_typescript_framework_semantics_are_metadata_hints_without_runtime_claims(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            (workspace / "src").mkdir(parents=True)
            (workspace / "app" / "api" / "users").mkdir(parents=True)
            (workspace / "electron").mkdir()
            (workspace / "src" / "App.tsx").write_text(
                "import React from 'react';\n\n"
                "export function useUser() {\n"
                "  return { id: '42' };\n"
                "}\n\n"
                "export function App() {\n"
                "  const user = useUser();\n"
                "  return <main>{user.id}</main>;\n"
                "}\n",
                encoding="utf-8",
            )
            (workspace / "app" / "api" / "users" / "route.ts").write_text(
                "export async function GET() {\n"
                "  return Response.json([]);\n"
                "}\n",
                encoding="utf-8",
            )
            (workspace / "vite.config.ts").write_text(
                "import { defineConfig } from 'vite';\n"
                "export default defineConfig({});\n",
                encoding="utf-8",
            )
            (workspace / "electron" / "main.ts").write_text(
                "import { app, BrowserWindow } from 'electron';\n"
                "app.whenReady().then(() => new BrowserWindow());\n",
                encoding="utf-8",
            )
            (workspace / "src" / "desktop.ts").write_text(
                "import { invoke } from '@tauri-apps/api/core';\n"
                "export async function ping() {\n"
                "  return invoke('ping');\n"
                "}\n",
                encoding="utf-8",
            )
            (workspace / "src" / "usefullyNamed.ts").write_text(
                "export function usefullyNamed() {\n"
                "  return true;\n"
                "}\n",
                encoding="utf-8",
            )
            (workspace / "src" / "notRoute.ts").write_text(
                "export async function GET() {\n"
                "  return [];\n"
                "}\n",
                encoding="utf-8",
            )
            (workspace / "src" / "windowFactory.ts").write_text(
                "export function makeWindow() {\n"
                "  return 'BrowserWindow';\n"
                "}\n",
                encoding="utf-8",
            )
            (workspace / "src" / "viteNotes.ts").write_text(
                "// vite is mentioned in a comment, not a build config.\n"
                "export function note() {\n"
                "  return 'vite';\n"
                "}\n",
                encoding="utf-8",
            )

            graph = build_project_code_graph(workspace)
            packet = query_project_graph(
                graph,
                {"query": "agent_reading_packet", "node_id": "function:src.App.App", "max_results": 5},
            )
            scanner = graph["metadata"]["typescript_javascript_scanner"]
            semantics = scanner["framework_semantics"]
            semantic_index = {
                (item["relative_path"], item["semantic_type"], item.get("symbol_id", "")): item
                for item in semantics
            }
            node_types = {node["type"] for node in graph["nodes"]}
            serialized = json.dumps(graph, sort_keys=True).lower()

            self.assertLessEqual(node_types, set(default_ontology()["node_types"]))
            self.assertNotIn("component", node_types)
            self.assertNotIn("hook", node_types)
            self.assertNotIn("api_route", node_types)
            self.assertIn(("src/App.tsx", "component", "function:src.App.App"), semantic_index)
            self.assertIn(("src/App.tsx", "hook", "function:src.App.useUser"), semantic_index)
            self.assertIn(("app/api/users/route.ts", "api_route", "function:app.api.users.route.GET"), semantic_index)
            self.assertIn(("vite.config.ts", "build_config", "module:vite.config"), semantic_index)
            self.assertIn(("electron/main.ts", "native_shell_entrypoint", "module:electron.main"), semantic_index)
            self.assertIn(("src/desktop.ts", "native_bridge_api", "function:src.desktop.ping"), semantic_index)
            self.assertFalse(any(item["relative_path"] == "src/usefullyNamed.ts" for item in semantics))
            self.assertFalse(any(item["relative_path"] == "src/notRoute.ts" for item in semantics))
            self.assertFalse(any(item["relative_path"] == "src/windowFactory.ts" for item in semantics))
            self.assertFalse(any(item["relative_path"] == "src/viteNotes.ts" for item in semantics))
            self.assertGreaterEqual(scanner["framework_semantic_count"], 6)
            self.assertTrue(scanner["unsupported_framework_inventory"])
            self.assertTrue(packet["framework_semantics"])
            self.assertIn("framework_runtime_behavior", packet["unsupported_claims"])
            self.assertEqual(packet["framework_semantics"][0]["source_boundary"], "graph_metadata_only_raw_source_excluded")
            for item in semantics:
                with self.subTest(item=item):
                    self.assertEqual(item["confidence"], "inferred")
                    self.assertTrue(item["source_read_required"])
                    self.assertEqual(item["source_boundary"], "graph_metadata_only_raw_source_excluded")
                    self.assertIn("runtime_behavior", item["unsupported_claims"])
            self.assertNotIn("runtime route verified", serialized)
            self.assertNotIn("browser verified", serialized)
            self.assertNotIn(str(workspace).lower(), serialized)
            self.assertTrue(graph["validation"]["ok"], graph["validation"])

    def test_product_agent_os_scripts_smoke_scan_has_symbols_imports_and_calls(self):
        graph = build_project_code_graph(ROOT / "plugins" / "product-agent-os" / "scripts")
        nodes = {node["id"] for node in graph["nodes"]}
        edges = graph["edges"]

        self.assertIn("module:product_agent_os.project_code_graph", nodes)
        self.assertIn("function:product_agent_os.project_code_graph.build_project_code_graph", nodes)
        self.assertIn("function:product_agent_os.project_graph_manifest.collect_project_files", nodes)
        self.assertGreater(graph["metadata"]["python_scanner"]["module_count"], 10)
        self.assertGreater(graph["metadata"]["python_scanner"]["import_edge_count"], 10)
        self.assertGreater(graph["metadata"]["python_scanner"]["call_edge_count"], 10)
        self.assertTrue(
            any(
                edge["type"] == "imports"
                and edge["source"] == "module:product_agent_os.project_code_graph"
                and edge["target"] == "function:product_agent_os.project_graph_manifest.collect_project_files"
                for edge in edges
            )
        )
        self.assertTrue(graph["validation"]["ok"], graph["validation"])


def _write_python_workspace(workspace: Path) -> None:
    (workspace / "app").mkdir(parents=True)
    (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
    (workspace / "app" / "worker.py").write_text(
        "def run():\n"
        "    return 'ok'\n",
        encoding="utf-8",
    )
    (workspace / "app" / "main.py").write_text(
        "from app.worker import run\n\n"
        "class Controller:\n"
        "    def handle(self):\n"
        "        return run()\n\n"
        "def main():\n"
        "    return run()\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
