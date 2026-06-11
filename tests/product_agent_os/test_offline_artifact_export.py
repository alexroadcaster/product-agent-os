import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.offline_artifact_export import (  # noqa: E402
    OfflineArtifactExportError,
    build_html_export_contract,
    write_html_export,
)


class OfflineArtifactExportTest(unittest.TestCase):
    def test_default_export_destination_is_project_scoped_and_approval_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            shutil.copytree(FIXTURES / "empty-repo", workspace)

            contract = build_html_export_contract(
                workspace,
                artifact_id="project-cockpit",
                default_relative_path=".codex/product-agent-os/project-cockpit.html",
            )

            self.assertEqual(contract["destination_scope"], "project_default")
            self.assertTrue(Path(contract["destination"]).is_relative_to(workspace.resolve()))
            self.assertEqual(contract["final_destination_policy"], "project_scoped_or_explicit_user_path")
            self.assertIn("explicit approval required", " ".join(contract["approval_required"]))

    def test_write_requires_approval_and_rejects_unrequested_external_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            external = Path(tmp) / "outside" / "report.html"
            workspace.mkdir()

            with self.assertRaises(OfflineArtifactExportError):
                write_html_export(
                    workspace,
                    artifact_id="report",
                    default_relative_path=".codex/eval-reports/report.html",
                    html_text="<!doctype html>\n",
                    requested_path=external,
                    approval_ref="owner-approved",
                )

            result = write_html_export(
                workspace,
                artifact_id="report",
                default_relative_path=".codex/eval-reports/report.html",
                html_text="<!doctype html>\n",
                requested_path=external,
                explicit_path_requested=True,
                approval_ref="owner-approved",
            )

            self.assertEqual(result["destination_scope"], "explicit_external_path")
            self.assertTrue(external.exists())


if __name__ == "__main__":
    unittest.main()
