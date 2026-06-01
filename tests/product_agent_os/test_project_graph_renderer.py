import json
import shutil
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.merge_infrastructure import build_merge_plan  # noqa: E402
from product_agent_os.offline_artifact_safety import GENERATED_VIEW_ONLY_TEXT  # noqa: E402
from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_graph_analysis import build_project_graph_analysis  # noqa: E402
from product_agent_os.project_graph_queries import query_project_graph  # noqa: E402
from product_agent_os.project_graph_renderer import (  # noqa: E402
    PROJECT_COCKPIT_HTML_TARGET,
    PROJECT_COCKPIT_JSON_TARGET,
    render_project_graph_cockpit,
    render_project_graph_cockpit_plan,
    stage_project_graph_cockpit,
    validate_project_graph_cockpit_manifest,
)
from product_agent_os.stage_manifest import MANIFEST_NAME  # noqa: E402


class ProjectGraphRendererTest(unittest.TestCase):
    def test_renderer_outputs_offline_eight_page_cockpit_graph_controls_and_safe_json(self):
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

            result = render_project_graph_cockpit(
                graph,
                analysis=analysis,
                query_packets=[trace],
                selected_node_id="function:app.main.main",
            )
            html = result["html"]
            lower = html.lower()
            payload = json.loads(result["json"])

            self.assertTrue(lower.startswith("<!doctype html>"))
            self.assertIn('<meta name="viewport"', lower)
            self.assertNotIn("http://", lower)
            self.assertNotIn("https://", lower)
            self.assertNotIn("<script src=", lower)
            self.assertNotIn("fetch(", lower)
            self.assertNotIn("contenteditable", lower)
            self.assertIn('id="page-overview"', html)
            self.assertIn('id="page-project-map"', html)
            self.assertIn('id="page-code-intelligence"', html)
            self.assertIn('id="section-code-flow"', html)
            self.assertIn('id="graph-canvas-fallback"', html)
            self.assertIn('id="selected-node-evidence"', html)
            self.assertIn('data-filter="node_type"', html)
            self.assertIn('data-filter="edge_type"', html)
            self.assertIn('data-filter="confidence"', html)
            self.assertIn('data-filter="artifact"', html)
            self.assertIn('data-filter="partition"', html)
            self.assertIn('data-command="fit"', html)
            self.assertIn("command === 'fit'", html)
            self.assertIn("command === 'isolate'", html)
            self.assertIn("command === 'expand'", html)
            self.assertIn('data-command="copy"', html)
            self.assertIn('<script type="application/json" id="project-cockpit-data">', html)
            self.assertIn(GENERATED_VIEW_ONLY_TEXT, html)
            self.assertIn("@media", html)
            self.assertEqual(result["validation"]["errors"], [])
            self.assertEqual(payload["schema_version"], 1)
            self.assertIn("visual_projection", payload)
            self.assertIn("visual qa checks", " ".join(result["validation"]["checks"]).lower())
            self.assertNotIn("return 'ok'", html + result["json"])
            self.assertNotIn(str(workspace), html + result["json"])

    def test_renderer_preserves_active_page_and_section_anchor(self):
        with TemporaryDirectory() as tmp:
            workspace = _write_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)

            result = render_project_graph_cockpit(
                graph,
                active_page="code-intelligence",
                section_anchor="code-flow",
            )
            payload = json.loads(result["json"])

            self.assertIn('href="#page-code-intelligence" aria-current="page"', result["html"])
            self.assertEqual(payload["cockpit"]["active_page"], "code-intelligence")
            self.assertEqual(payload["cockpit"]["section_anchor"], "code-flow")

    def test_renderer_escapes_embedded_json_and_redacts_secrets_paths_and_external_urls(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {
                "scan_id": "scan-render",
                "node_count": 1,
                "edge_count": 0,
                "external_doc": "https://example.invalid/api",
                "local_path": "C:\\Users\\person\\repo",
            },
            "nodes": [
                {
                    "id": "file:unsafe.py",
                    "type": "module",
                    "label": "</script><script>alert('x')</script>",
                    "status": "current",
                    "language": "python",
                    "path": "unsafe.py",
                    "token_hint": "TOKEN=fixture-secret",
                }
            ],
            "edges": [],
        }

        result = render_project_graph_cockpit(graph)
        rendered = result["html"] + result["json"]

        self.assertNotIn("</script><script", rendered)
        self.assertNotIn("fixture-secret", rendered)
        self.assertNotIn("C:\\Users\\person", rendered)
        self.assertNotIn("https://example.invalid", rendered)
        self.assertEqual(result["validation"]["errors"], [])

    def test_renderer_strips_unsafe_paths_from_cockpit_code_flow_and_analysis_payload(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {"scan_id": "scan-paths", "node_count": 4, "edge_count": 2},
            "nodes": [
                {"id": "file:posix", "type": "module", "label": "Posix", "path": "/home/alex/repo/private.py"},
                {"id": "file:windows", "type": "module", "label": "Windows", "path": "D:\\repo\\secret.py"},
                {"id": "file:traversal", "type": "module", "label": "Traversal", "path": "../private.py"},
                {"id": "file:url", "type": "module", "label": "Url", "path": "https://example.invalid/source.py"},
            ],
            "edges": [
                {
                    "id": "edge:path-1",
                    "source": "file:posix",
                    "target": "file:windows",
                    "type": "imports",
                    "confidence": "verified",
                    "status": "current",
                },
                {
                    "id": "edge:path-2",
                    "source": "file:traversal",
                    "target": "file:url",
                    "type": "references",
                    "confidence": "inferred",
                    "status": "current",
                },
            ],
        }
        analysis = {
            "graph_ref": {"scan_id": "scan-paths", "node_count": 4, "edge_count": 2},
            "hotspots": [
                {
                    "id": "file:posix",
                    "path": "/tmp/private.py",
                    "raw_source": "SECRET_VALUE",
                    "note": "https://example.invalid/private",
                    "degree": 99,
                }
            ],
            "ambiguous_edge_inventory": [
                {"source": "/Users/alex/project/app.py", "call_name": "load_secret", "status": "ambiguous"}
            ],
            "suggested_agent_questions": [
                {"id": "q", "text": "Review /home/alex/private.py before editing?", "source": "analysis"}
            ],
            "budget": {"max_items": 20, "debug_path": "D:\\repo\\debug.py"},
        }

        result = render_project_graph_cockpit(graph, analysis=analysis)
        rendered = result["json"] + result["html"]

        for forbidden in [
            "/home/alex",
            "/tmp/private.py",
            "/Users/alex",
            "D:\\repo",
            "../private.py",
            "https://example.invalid",
            "SECRET_VALUE",
            "debug_path",
        ]:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, rendered)
        payload = json.loads(result["json"])
        code_paths = [
            item["source"]["path"]
            for item in payload["cockpit"]["code_flow"]["module_flows"]
            if item.get("source")
        ]
        self.assertTrue(all(path == "" for path in code_paths))

    def test_stage_cockpit_is_explicit_opt_in_manifest_bound_and_preserves_existing_targets(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "project-code-graph-minimal-python", workspace)
            graph = build_project_code_graph(workspace)

            dry_run = render_project_graph_cockpit_plan(workspace, graph)
            staged = stage_project_graph_cockpit(workspace, stage_root, graph)
            merge_plan = build_merge_plan(workspace, stage_root)

            self.assertEqual(dry_run["rendered_artifacts"]["mode"], "dry-run")
            self.assertEqual(staged["rendered_artifacts"]["mode"], "stage")
            self.assertTrue((stage_root / PROJECT_COCKPIT_HTML_TARGET).exists())
            self.assertTrue((stage_root / PROJECT_COCKPIT_JSON_TARGET).exists())
            self.assertTrue((stage_root / MANIFEST_NAME).exists())
            self.assertFalse((workspace / PROJECT_COCKPIT_HTML_TARGET).exists())
            self.assertFalse((workspace / PROJECT_COCKPIT_JSON_TARGET).exists())
            self.assertEqual(validate_project_graph_cockpit_manifest(stage_root), [])
            self.assertEqual(merge_plan["status"], "needs_approval")

            existing_html = workspace / PROJECT_COCKPIT_HTML_TARGET
            existing_json = workspace / PROJECT_COCKPIT_JSON_TARGET
            existing_html.parent.mkdir(parents=True, exist_ok=True)
            existing_html.write_text("<!doctype html>\n<title>User graph</title>\n", encoding="utf-8")
            existing_json.write_text('{"user": true}\n', encoding="utf-8")
            stage_root_existing = Path(tmp) / "stage-existing"

            companion = stage_project_graph_cockpit(workspace, stage_root_existing, graph)
            by_target = {item["target_path"]: item for item in companion["rendered_artifacts"]["files"]}

            self.assertEqual(by_target[PROJECT_COCKPIT_HTML_TARGET]["action"], "leave_unchanged")
            self.assertEqual(by_target[PROJECT_COCKPIT_JSON_TARGET]["action"], "leave_unchanged")
            self.assertIn("_proposals", by_target[PROJECT_COCKPIT_HTML_TARGET]["staged_path"])
            self.assertEqual(existing_html.read_text(encoding="utf-8"), "<!doctype html>\n<title>User graph</title>\n")
            self.assertEqual(existing_json.read_text(encoding="utf-8"), '{"user": true}\n')

    def test_cockpit_manifest_validation_rejects_tampered_extra_targets_and_escaping_paths(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "project-code-graph-minimal-python", workspace)
            graph = build_project_code_graph(workspace)
            stage_project_graph_cockpit(workspace, stage_root, graph)
            manifest_path = stage_root / MANIFEST_NAME
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

            manifest["files"].append(
                {
                    "target_path": "AGENTS.md",
                    "action": "create",
                    "staged_path": PROJECT_COCKPIT_HTML_TARGET,
                    "write_policy": "staged_only",
                    "managed_section": "",
                    "digest": manifest["files"][0]["digest"],
                }
            )
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

            errors = validate_project_graph_cockpit_manifest(stage_root)

            self.assertTrue(any("unexpected target" in error for error in errors))

            manifest["files"].pop()
            manifest["files"][0]["staged_path"] = "../escape.html"
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

            errors = validate_project_graph_cockpit_manifest(stage_root)
            self.assertTrue(any("escapes stage root" in error for error in errors))


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
    return workspace


if __name__ == "__main__":
    unittest.main()
