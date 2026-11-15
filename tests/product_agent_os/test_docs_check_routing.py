"""Changed-document checks must not depend on unrelated sources or a site build."""
import importlib.util
import ast
import io
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('scoped_docs_checker', ROOT / 'tools/check_docs.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class DocsCheckRoutingTest(unittest.TestCase):
    def test_source_collection_excludes_site_archive_and_installer(self):
        suite = unittest.defaultTestLoader.loadTestsFromName('tests.product_agent_os.test_product_agent_os_docs')
        def cases(group):
            for item in group:
                if isinstance(item, unittest.TestSuite):
                    yield from cases(item)
                else:
                    yield item
        collected = list(cases(suite))
        self.assertTrue(collected)
        self.assertTrue(all(type(item).__name__ == 'ProductAgentOsDocsTest' for item in collected))
        for filename in ('test_product_agent_os_docs.py', 'docs_archive_checks.py'):
            tree = ast.parse((ROOT / 'tests/product_agent_os' / filename).read_text(encoding='utf-8'))
            self.assertFalse(any(isinstance(node, ast.Name) and node.id == 'SITE' for node in ast.walk(tree)), filename)
        self.assertTrue((ROOT / 'tests/product_agent_os/site_checks.py').is_file())

    def check_paths(self, root, *paths):
        with mock.patch.object(checker, 'ROOT', root), mock.patch.object(checker, 'DOCS', root / 'docs'), mock.patch('sys.argv', ['check_docs.py', '--paths', *paths]), redirect_stdout(io.StringIO()):
            checker.main()

    def test_report_check_does_not_require_site_or_unrelated_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'report.md').write_text('# Report\n[Evidence](evidence.md)\n', encoding='utf-8')
            (root / 'evidence.md').write_text('# Evidence\n', encoding='utf-8')
            (root / 'docs').mkdir()
            (root / 'docs/broken.md').write_text('[Broken](absent.md)', encoding='utf-8')
            self.check_paths(root, 'report.md')
            self.assertFalse((root / 'site').exists())

    def test_changed_document_broken_link_and_missing_file_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'report.md').write_text('[Evidence](absent.md)', encoding='utf-8')
            for path in ('report.md', 'missing.md', '../outside.md'):
                with self.subTest(path=path), self.assertRaises(SystemExit):
                    self.check_paths(root, path)

    def test_source_status_applies_to_docs_not_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs').mkdir()
            path = root / 'docs/page.md'
            path.write_text('# Page\n', encoding='utf-8')
            with self.assertRaises(SystemExit):
                self.check_paths(root, 'docs/page.md')
            path.write_text('# Page\n\nSource status: local.\n', encoding='utf-8')
            self.check_paths(root, 'docs/page.md')

    def test_reference_links_validate_missing_and_outside_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = root / 'report.md'
            for target in ('missing.md', '../outside.md'):
                with self.subTest(target=target):
                    report.write_text(f'[Evidence][receipt]\n\n[receipt]: {target}\n', encoding='utf-8')
                    with self.assertRaises(SystemExit):
                        self.check_paths(root, 'report.md')
            (root / 'evidence file.md').write_text('# Evidence\n', encoding='utf-8')
            report.write_text('[Evidence][receipt]\n\n[receipt]: <evidence file.md> "Title"\n', encoding='utf-8')
            self.check_paths(root, 'report.md')

    def test_code_examples_and_external_links_are_not_local_file_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'report.md').write_text('# Report\n`[example](missing.md)`\n```md\n[x](missing.md)\n```\n[web](https://example.test)\n', encoding='utf-8')
            self.check_paths(root, 'report.md')
