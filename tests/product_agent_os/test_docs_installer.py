"""Installer contracts; independent of documentation/site edits."""
from tests.product_agent_os.docs_test_support import *

class DocsInstallerContractTest(unittest.TestCase):
    """Exercise installer branching with all external commands replaced by a recorder."""

    def run_installer(self, *arguments, fail_install=False):
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            self.skipTest("PowerShell is required for the installer contract")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tools").mkdir()
            (root / "wheels").mkdir()
            (root / "requirements.txt").write_text("example-package==1.0\n", encoding="utf-8")
            source = (ROOT / "tools/docs_install.ps1").read_text(encoding="utf-8")
            # Replace only the subprocess boundary; keep parameters and control flow intact.
            start = source.index("function Invoke-Checked {")
            end = source.index("\nif (-not $Install)", start)
            stub = '''function Invoke-Checked {
    param([string]$FilePath, [Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments)
    @{file=$FilePath; arguments=@($Arguments)} | ConvertTo-Json -Compress | Add-Content (Join-Path $RepoRoot 'calls.jsonl')
    if (FAIL_INSTALL -and $Arguments -contains 'install') { throw 'No matching distribution found in offline wheelhouse' }
}
'''.replace("FAIL_INSTALL", "$true" if fail_install else "$false")
            script = root / "tools/docs_install.ps1"
            script.write_text(source[:start] + stub + source[end:], encoding="utf-8-sig")
            args = [str(root / "wheels") if a == "WHEELS" else a for a in arguments]
            result = subprocess.run([shell, "-NoProfile", "-File", str(script), *args],
                                    capture_output=True, text=True, timeout=30)
            log = root / "calls.jsonl"
            calls = [json.loads(line) for line in log.read_text(encoding="utf-8-sig").splitlines()] if log.exists() else []
            return result, calls

    def test_offline_install_never_calls_package_index(self):
        for extra in ([], ["-AllowNetwork"]):
            with self.subTest(extra=extra):
                result, calls = self.run_installer("-Install", "-OfflineWheelhouse", "WHEELS", *extra)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(calls[0]["arguments"][:2], ["-m", "venv"])
                installs = [c["arguments"] for c in calls if "pip" in c["arguments"]]
                self.assertTrue(installs)
                for args in installs:
                    self.assertIn("--no-index", args)
                    self.assertIn("--find-links", args)
                self.assertNotIn("--upgrade-deps", calls[0]["arguments"])

    def test_install_requires_source_and_plan_has_no_commands(self):
        result, calls = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, [])
        result, calls = self.run_installer("-Install")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("explicit source", result.stderr)
        self.assertEqual(calls, [])

    def test_missing_wheelhouse_fails_before_bootstrap(self):
        result, calls = self.run_installer("-Install", "-OfflineWheelhouse", "missing-g5-wheelhouse")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Offline wheelhouse directory not found", result.stderr)
        self.assertEqual(calls, [])

    def test_readme_mcp_example_matches_package(self):
        readme = PLUGIN_README.read_text(encoding="utf-8")
        section = readme.split("### Bundled Context7 MCP", 1)[1]
        example = re.search(r"```json\n(.*?)\n```", section, re.S)
        self.assertIsNotNone(example)
        self.assertEqual(json.loads(example.group(1)), json.loads(
            (ROOT / "plugins/product-agent-os/.mcp.json").read_text(encoding="utf-8")))

    def test_online_upgrade_and_offline_failure_do_not_fallback(self):
        result, calls = self.run_installer("-Install", "-AllowNetwork")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(any("--upgrade" in c["arguments"] for c in calls))
        result, calls = self.run_installer("-Install", "-OfflineWheelhouse", "WHEELS", fail_install=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("offline wheelhouse", result.stderr)
        self.assertEqual(len([c for c in calls if "install" in c["arguments"]]), 1)
        self.assertFalse(any("mkdocs" in c["arguments"] for c in calls))

