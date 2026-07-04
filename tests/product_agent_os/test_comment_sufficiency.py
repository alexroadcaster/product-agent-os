import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.comment_sufficiency import analyze_paths, main  # noqa: E402


class CommentSufficiencyAdvisoryTest(unittest.TestCase):
    def test_v3_runner_required_symbols_have_docstrings_or_intent_comments(self):
        warnings = analyze_paths(
            [
                ROOT / ".codex" / "product-agent-os" / "b45-manual-pilot" / "v3_reference_runner.py",
                ROOT / ".codex" / "product-agent-os" / "b45-manual-pilot" / "v3_js_runner.mjs",
            ],
            root=ROOT,
        )

        self.assertEqual([], [warning.as_dict() for warning in warnings])

    def test_typescript_and_modern_javascript_forms_are_analyzed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ts_path = root / "pipeline.ts"
            tsx_path = root / "policy.tsx"
            js_path = root / "redactor.js"
            ts_path.write_text(
                "export async function normalizeEvent(value: unknown): Promise<unknown> {\n"
                "  return value;\n"
                "}\n",
                encoding="utf-8",
            )
            tsx_path.write_text(
                "export const evaluateAccess = async (value: unknown): Promise<boolean> => {\n"
                "  return Boolean(value);\n"
                "};\n",
                encoding="utf-8",
            )
            js_path.write_text(
                "class Redactor {\n"
                "  async redact(value) {\n"
                "    return value;\n"
                "  }\n"
                "}\n",
                encoding="utf-8",
            )

            warnings = analyze_paths([ts_path, tsx_path, js_path], root=root)

        self.assertEqual({"evaluateAccess", "normalizeEvent", "redact"}, {warning.symbol for warning in warnings})
        self.assertEqual({"javascript"}, {warning.language for warning in warnings})
        self.assertEqual({"pipeline.ts", "policy.tsx", "redactor.js"}, {warning.path for warning in warnings})

    def test_warning_path_outside_root_is_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            outside_path = Path(tmp) / "outside.js"
            root = Path(tmp) / "workspace"
            root.mkdir()
            outside_path.write_text(
                "function evaluateAccess(value) {\n"
                "  return Boolean(value);\n"
                "}\n",
                encoding="utf-8",
            )

            warnings = analyze_paths([outside_path], root=root, use_default_excludes=False)

        self.assertEqual(1, len(warnings))
        self.assertEqual("<outside-root>/outside.js", warnings[0].path)
        self.assertNotIn(str(outside_path.parent), warnings[0].path)

    def test_missing_complex_python_docstring_is_advisory_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "complex_case.py"
            path.write_text(
                "\n".join(
                    [
                        "def complex_case(value):",
                        "    total = 0",
                        "    for item in value:",
                        "        if item:",
                        "            total += 1",
                        "        elif item == 0:",
                        "            total -= 1",
                        "    try:",
                        "        if total > 10 and value:",
                        "            return total",
                        "    except TypeError:",
                        "        return -1",
                        "    while total < 0:",
                        "        total += 1",
                        "    return total",
                    ]
                ),
                encoding="utf-8",
            )

            warnings = analyze_paths([path], root=Path(tmp))

        self.assertEqual(1, len(warnings))
        self.assertEqual("advisory", warnings[0].severity)

    def test_comment_not_needed_reason_suppresses_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "complex_case.py"
            path.write_text(
                "\n".join(
                    [
                        "# comment_not_needed_reason: local parser helper covered by focused tests.",
                        "def complex_case(value):",
                        "    total = 0",
                        "    for item in value:",
                        "        if item:",
                        "            total += 1",
                        "        elif item == 0:",
                        "            total -= 1",
                        "    try:",
                        "        if total > 10 and value:",
                        "            return total",
                        "    except TypeError:",
                        "        return -1",
                        "    while total < 0:",
                        "        total += 1",
                        "    return total",
                    ]
                ),
                encoding="utf-8",
            )

            warnings = analyze_paths([path], root=Path(tmp))

        self.assertEqual([], warnings)

    def test_default_scan_excludes_tests_and_generated_specs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            test_path = root / "tests" / "test_complex_case.py"
            spec_path = root / "docs" / "superpowers" / "specs" / "generated_case.py"
            test_path.parent.mkdir(parents=True)
            spec_path.parent.mkdir(parents=True)
            source = "\n".join(
                [
                    "def complex_case(value):",
                    "    total = 0",
                    "    for item in value:",
                    "        if item:",
                    "            total += 1",
                    "        elif item == 0:",
                    "            total -= 1",
                    "    try:",
                    "        if total > 10 and value:",
                    "            return total",
                    "    except TypeError:",
                    "        return -1",
                    "    while total < 0:",
                    "        total += 1",
                    "    return total",
                ]
            )
            test_path.write_text(source, encoding="utf-8")
            spec_path.write_text(source, encoding="utf-8")

            warnings = analyze_paths([test_path, spec_path], root=root)
            included_warnings = analyze_paths([test_path], root=root, include_tests=True)

        self.assertEqual([], warnings)
        self.assertEqual(1, len(included_warnings))

    def test_warning_caps_reduce_broad_advisory_noise(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "legacy_module.py"
            blocks = []
            for index in range(4):
                blocks.extend(
                    [
                        f"def complex_case_{index}(value):",
                        "    total = 0",
                        "    for item in value:",
                        "        if item:",
                        "            total += 1",
                        "        elif item == 0:",
                        "            total -= 1",
                        "    try:",
                        "        if total > 10 and value:",
                        "            return total",
                        "    except TypeError:",
                        "        return -1",
                        "    while total < 0:",
                        "        total += 1",
                        "    return total",
                        "",
                    ]
                )
            path.write_text("\n".join(blocks), encoding="utf-8")

            warnings = analyze_paths([path], root=root, max_warnings_per_file=2, max_warnings=1)

        self.assertEqual(1, len(warnings))
        self.assertEqual(3, warnings[0].suppressed_count)

    def test_cli_returns_zero_with_warning_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "complex_case.mjs"
            path.write_text(
                "\n".join(
                    [
                        "function complexCase(value) {",
                        "  let total = 0;",
                        "  for (const item of value) {",
                        "    if (item && total < 3) { total += 1; }",
                        "    else if (item === 0) { total -= 1; }",
                        "  }",
                        "  while (total < 0) { total += 1; }",
                        "  try {",
                        "    if (total > 10 || value.length > 5) { return total; }",
                        "  } catch (error) {",
                        "    return -1;",
                        "  }",
                        "  return total;",
                        "}",
                    ]
                ),
                encoding="utf-8",
            )
            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main([str(path), "--root", tmp])

        payload = json.loads(stdout.getvalue())
        self.assertEqual(0, exit_code)
        self.assertFalse(payload["blocking"])
        self.assertEqual(1, payload["warning_count"])
        self.assertEqual(0, payload["suppressed_warning_count"])
        self.assertEqual("advisory", payload["warnings"][0]["severity"])

    def test_cli_rejects_zero_warning_cap(self):
        stderr = StringIO()
        with redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as raised:
                main(["complex_case.py", "--max-warnings", "0"])

        self.assertEqual(2, raised.exception.code)
        self.assertIn("--max-warnings must be positive", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
