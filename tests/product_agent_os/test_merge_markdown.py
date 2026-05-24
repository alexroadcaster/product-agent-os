import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
WRAPPER = SCRIPTS / "merge_markdown.py"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.merge_markdown import merge_section  # noqa: E402


def load_wrapper():
    spec = importlib.util.spec_from_file_location("merge_markdown_wrapper", WRAPPER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class MergeMarkdownTest(unittest.TestCase):
    def test_insert_managed_section_preserves_user_content(self):
        original = "# AGENTS.md\n\nUser rule.\n"
        updated = merge_section(original, "product-agent-os", "checks", "- Run tests.\n\n")

        self.assertEqual(
            updated,
            "# AGENTS.md\n\n"
            "User rule.\n\n"
            "<!-- product-agent-os:start checks -->\n"
            "- Run tests.\n"
            "<!-- product-agent-os:end checks -->\n",
        )

    def test_update_existing_managed_section_removes_old_body(self):
        original = (
            "# AGENTS.md\n\n"
            "<!-- product-agent-os:start checks -->\n"
            "- Old check.\n"
            "<!-- product-agent-os:end checks -->\n"
            "\nUser rule.\n"
        )

        updated = merge_section(original, "product-agent-os", "checks", "- New check.")

        self.assertIn("- New check.", updated)
        self.assertNotIn("- Old check.", updated)
        self.assertIn("\nUser rule.\n", updated)

    def test_update_is_idempotent(self):
        original = "# AGENTS.md\n"
        once = merge_section(original, "product-agent-os", "checks", "- Run tests.")
        twice = merge_section(once, "product-agent-os", "checks", "- Run tests.")

        self.assertEqual(once, twice)
        self.assertEqual(once.count("product-agent-os:start checks"), 1)

    def test_update_does_not_replace_other_section_id(self):
        original = (
            "<!-- product-agent-os:start other -->\n"
            "Keep me.\n"
            "<!-- product-agent-os:end other -->\n"
        )

        updated = merge_section(original, "product-agent-os", "checks", "New block.")

        self.assertIn("product-agent-os:start other", updated)
        self.assertIn("Keep me.", updated)
        self.assertIn("product-agent-os:start checks", updated)

    def test_cli_writes_merged_file_and_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            body = Path(tmp) / "body.md"
            target.write_text("# AGENTS.md\n", encoding="utf-8")
            body.write_text("- Run tests.\n\n", encoding="utf-8")

            rc = load_wrapper().main([str(target), "product-agent-os", "checks", str(body)])

            self.assertEqual(rc, 0)
            self.assertIn("product-agent-os:start checks", target.read_text(encoding="utf-8"))

    def test_cli_wrong_arg_count_returns_two_and_usage(self):
        stderr = io.StringIO()

        with redirect_stderr(stderr):
            rc = load_wrapper().main(["only-target"])

        self.assertEqual(rc, 2)
        self.assertIn("usage: merge_markdown.py", stderr.getvalue())

    def test_rejects_body_containing_same_managed_boundary_marker(self):
        original = "# AGENTS.md\n"
        body = "Keep.\n<!-- product-agent-os:start checks -->\nNested.\n"

        with self.assertRaisesRegex(ValueError, "managed boundary marker"):
            merge_section(original, "product-agent-os", "checks", body)

    def test_duplicate_matching_sections_fail_without_writing(self):
        original = (
            "# AGENTS.md\n\n"
            "<!-- product-agent-os:start checks -->\n"
            "First.\n"
            "<!-- product-agent-os:end checks -->\n\n"
            "<!-- product-agent-os:start checks -->\n"
            "Second.\n"
            "<!-- product-agent-os:end checks -->\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            body = Path(tmp) / "body.md"
            target.write_text(original, encoding="utf-8")
            body.write_text("Replacement.\n", encoding="utf-8")
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                rc = load_wrapper().main([str(target), "product-agent-os", "checks", str(body)])

            self.assertNotEqual(rc, 0)
            self.assertIn("duplicate managed section", stderr.getvalue())
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_cli_missing_body_file_returns_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            missing_body = Path(tmp) / "missing.md"
            original = "# AGENTS.md\n"
            target.write_text(original, encoding="utf-8")
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                rc = load_wrapper().main([str(target), "product-agent-os", "checks", str(missing_body)])

            self.assertNotEqual(rc, 0)
            self.assertIn("error:", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_preserves_lf_newline_style(self):
        original = "# AGENTS.md\n\nUser rule.\n"

        updated = merge_section(original, "product-agent-os", "checks", "- Run tests.\n")

        self.assertIn("<!-- product-agent-os:start checks -->\n- Run tests.\n", updated)
        self.assertNotIn("\r\n", updated)

    def test_preserves_crlf_newline_style(self):
        original = "# AGENTS.md\r\n\r\nUser rule.\r\n"

        updated = merge_section(original, "product-agent-os", "checks", "- Run tests.\n")

        self.assertIn("<!-- product-agent-os:start checks -->\r\n- Run tests.\r\n", updated)
        self.assertNotIn("checks -->\n- Run tests.", updated.replace("\r\n", ""))

    def test_cli_invalid_owner_returns_error_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            body = Path(tmp) / "body.md"
            original = "# AGENTS.md\n"
            target.write_text(original, encoding="utf-8")
            body.write_text("Replacement.\n", encoding="utf-8")
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                rc = load_wrapper().main([str(target), "../bad", "checks", str(body)])

            self.assertNotEqual(rc, 0)
            self.assertIn("invalid owner", stderr.getvalue())
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_cli_invalid_section_id_returns_error_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            body = Path(tmp) / "body.md"
            original = "# AGENTS.md\n"
            target.write_text(original, encoding="utf-8")
            body.write_text("Replacement.\n", encoding="utf-8")
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                rc = load_wrapper().main([str(target), "product-agent-os", "bad section", str(body)])

            self.assertNotEqual(rc, 0)
            self.assertIn("invalid section-id", stderr.getvalue())
            self.assertEqual(target.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
