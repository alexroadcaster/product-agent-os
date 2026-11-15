"""Source documentation checks; built site and historical receipts are opt-in.

Use tools/check_docs.py --paths ... for an ordinary changed-document task.
Site: python -m unittest tests.product_agent_os.site_checks
Archive: python -m unittest tests.product_agent_os.docs_archive_checks
"""
import importlib.util
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]


class ProductAgentOsDocsTest(unittest.TestCase):
    def test_control_plane_sources_are_readable_and_have_titles(self):
        for name in ('AGENTS.md', 'REQUIREMENTS.md', 'PLAN.md', 'TEST.md', 'EVALS.md', 'RUNLOG.md'):
            with self.subTest(document=name):
                text = (ROOT / name).read_text(encoding='utf-8-sig')
                self.assertTrue(text.lstrip().startswith('# '))
                self.assertNotIn('\ufffd', text)
                self.assertNotIn('\x00', text)

    def test_current_workflow_references_resolve_inside_project(self):
        config = tomllib.loads((ROOT / '.codex/config.toml').read_text(encoding='utf-8'))
        for name, relative in config['workflows'].items():
            with self.subTest(workflow=name):
                path = (ROOT / relative).resolve()
                self.assertTrue(path.is_relative_to(ROOT.resolve()))
                self.assertTrue(path.is_file(), relative)

    def test_document_sources_have_status_and_resolvable_links(self):
        spec = importlib.util.spec_from_file_location('source_docs_check', ROOT / 'tools/check_docs.py')
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        checker.check_source_status()
        checker.check_internal_links()
