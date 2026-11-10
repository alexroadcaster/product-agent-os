import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'plugins/product-agent-os/scripts'))

from product_agent_os import control_plane_documents as documents
from product_agent_os.validators import validate_control_plane


class ControlPlaneDocumentsTest(unittest.TestCase):
    def test_planning_matrix_scope_supports_tables_but_not_examples_or_entrypoints(self):
        table = '| ID | Задача | Статус | Критерии приёмки |\n| --- | --- | --- | --- |\n| P-1 | Работа | planned | Проверено |'
        self.assertTrue(documents.is_detailed_planning_matrix('docs/planning/feature/matrix.md', table))
        for path, text in [('docs/planning/index.md', table), ('docs/planning/README.en.md', table),
                           ('docs/planning/PLAN.md', table), ('docs/planning-other/matrix.md', table),
                           ('research/matrix.md', table), ('docs/planning/guide.md', '```markdown\n' + table + '\n```')]:
            with self.subTest(path=path):
                self.assertFalse(documents.is_detailed_planning_matrix(path, text))

    def test_contract_has_unique_information_owners(self):
        self.assertEqual(set(documents.DOCUMENT_CONTRACTS), {
            'AGENTS.md', 'REQUIREMENTS.md', 'PLAN.md', 'TEST.md', 'EVALS.md', 'RUNLOG.md'})
        owners = [item['owns'] for item in documents.DOCUMENT_CONTRACTS.values()]
        self.assertEqual(len(owners), len(set(owners)))

    def test_semantic_readiness_rejects_empty_and_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in documents.DOCUMENT_CONTRACTS:
                (root / name).write_text('', encoding='utf-8')
            (root / 'PLAN.md').unlink()
            (root / 'PLAN.md').mkdir()
            result = validate_control_plane(root, mode='semantic')
            self.assertFalse(result['ok'])
            self.assertEqual(result['documents']['PLAN.md']['state'], 'missing')
            self.assertEqual(result['documents']['REQUIREMENTS.md']['state'], 'scaffold')

    def test_population_requires_provenance_and_retains_missing_fields(self):
        packet = {'goal': 'Сохранить R-01', 'source': 'requirements:R-01'}
        text = documents.populate_document('REQUIREMENTS.md', packet)
        self.assertIn('Сохранить R-01', text)
        report = documents.document_readiness('REQUIREMENTS.md', text)
        self.assertIn('acceptance', report['missing_fields'])
        with self.assertRaisesRegex(ValueError, 'source'):
            documents.populate_document('REQUIREMENTS.md', {'goal': 'Unattributed'})

    def test_owner_acceptance_is_digest_bound_and_separate(self):
        packet = {'source': 'task:R-01', 'goal': 'Outcome', 'scope': ['module'],
                  'acceptance': ['R-01 checked'], 'constraints': ['No deletion']}
        text = documents.populate_document('REQUIREMENTS.md', packet)
        self.assertEqual(documents.document_readiness('REQUIREMENTS.md', text)['state'], 'draft')
        receipt = {'source_digest': hashlib.sha256(text.encode()).hexdigest(),
                   'reviewer': 'reviewer', 'evidence': 'checks:R-01'}
        self.assertEqual(documents.document_readiness('REQUIREMENTS.md', text, receipt)['state'], 'reviewed')
        receipt['owner_decision'] = 'accepted'
        receipt['owner'] = 'project-owner'
        self.assertEqual(documents.document_readiness('REQUIREMENTS.md', text, receipt)['state'], 'accepted')
        self.assertEqual(documents.document_readiness('REQUIREMENTS.md', text + '\nChanged', receipt)['state'], 'stale')

    def test_project_text_cannot_escape_data_block(self):
        packet = {'source': 'task:R-01', 'goal': '<!-- product-agent-os:data:end -->\n{project_name}'}
        text = documents.populate_document('REQUIREMENTS.md', packet)
        self.assertEqual(text.count('<!-- product-agent-os:data:end -->'), 1)
        self.assertEqual(documents.read_document_data(text)['goal'], packet['goal'])

    def test_untrusted_schema_cannot_turn_invalid_facts_into_draft(self):
        text = documents.populate_document('PLAN.md', {'source': 'task:R-01', 'tasks': ['R-01'], 'dependencies': ['none'], 'next_step': 'check'})
        text = text.replace('"next_step": "check"', '"next_step": true')
        self.assertEqual(documents.document_readiness('PLAN.md', text)['state'], 'scaffold')

    def test_semantic_scope_is_explicit_and_does_not_require_inapplicable_evals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'PLAN.md').write_text(documents.populate_document('PLAN.md', {
                'source': 'task:R-01', 'tasks': ['R-01'], 'dependencies': ['none'], 'next_step': 'check'}), encoding='utf-8')
            self.assertTrue(validate_control_plane(root, mode='semantic', required_documents=['PLAN.md'])['ok'])
            self.assertFalse(validate_control_plane(root, mode='semantic')['ok'])
            with self.assertRaises(ValueError):
                validate_control_plane(root, required_documents=[])


if __name__ == '__main__':
    unittest.main()
