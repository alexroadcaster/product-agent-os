"""Compare trusted repository mechanisms; never generate or execute model code."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import types
from pathlib import Path

from codex_runtime_runner.g7_quality_eval import evidence_fingerprint, review_findings, summarize_outcomes, verify_fixture_files
from product_agent_os.code_quality_selector import ProjectInventory, select_code_quality_profile


def run(root: Path) -> dict:
    """Read frozen inputs and compare baseline/current pure functions on identical cases."""
    design_path = root / 'docs/superpowers/specs/paos-aud-g7-code-quality-eval-design.json'
    design = json.loads(design_path.read_text(encoding='utf-8'))
    for relative, expected in design['instrument_hashes'].items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != expected:
            raise ValueError('instrument dependency drift: ' + relative)
    manifest = json.loads((root / design['manifest_path']).read_text(encoding='utf-8'))
    if evidence_fingerprint(manifest) != design['manifest_digest']:
        raise ValueError('manifest drift')
    verify_fixture_files((root / design['manifest_path']).parent, manifest)
    results = []
    for arm in ('baseline', 'treatment'):
        modules = {}
        digests = {}
        for name, relative in design['local_mechanisms'].items():
            if arm == 'baseline':
                source = subprocess.run(['git', 'show', design['baseline_commit'] + ':' + relative],
                                        cwd=root, check=True, capture_output=True).stdout
            else:
                source = (root / relative).read_bytes()
            digest = hashlib.sha256(source).hexdigest()
            if digest != design['source_hashes'][arm][name]:
                raise ValueError('instrument drift: ' + arm + ':' + name)
            module_name = '_g7_' + arm + '_' + name
            module = types.ModuleType(module_name)
            module.__file__ = str(root / relative)
            sys.modules[module_name] = module
            # Only pinned code from this repository, never a candidate supplied by a model.
            exec(compile(source, relative, 'exec'), module.__dict__)
            modules[name] = module
            digests[name] = digest
        outcomes = []
        for case in manifest['local_cases']:
            if case['mechanism'] == 'guard':
                observed = modules['guard']._is_read_only(case['input'])
            else:
                module = modules['strategy']
                profile = select_code_quality_profile(ProjectInventory(('pyproject.toml',), (), ()))
                request = module.TestStrategyRequest(profile, case['input'], True, '',
                    (module.ChangeRisk('logic', 'pure_logic', 'preserve result', ('result',), ('python',)),), ())
                observed = module.select_test_strategy(request).test_first_decision.status
            outcomes.append({'case_id': case['id'], 'status': 'passed' if observed == case['expected'] else 'failed',
                             'observed': observed, 'expected': case['expected']})
        results.append({'arm': arm, 'source_hashes': digests, 'outcomes': outcomes,
                        'summary': summarize_outcomes(outcomes, [c['id'] for c in manifest['local_cases']])})
    return {'schema_version': 'g7_local_comparison_v1', 'design_digest': evidence_fingerprint(design),
            'manifest_digest': evidence_fingerprint(manifest), 'arms': results,
            'empty_review_control_not_run_review': review_findings([], 'a' * 64),
            'instrument_hashes': design['instrument_hashes'],
            'runtime': {'python': sys.version, 'platform': sys.platform},
            'baseline_scope': 'pinned baseline functions with a shared current profile factory, not a full historical runtime',
            'comparison_kind': 'deterministic_repository_mechanisms_not_model_AB',
            'model_calls': 0, 'model_quality_effect': None, 'owner_acceptance': None,
            'limits': ['targeted cases, not general quality estimate', 'hidden oracle isolation for model runs not established',
                       'fresh-session activation separate', 'no performance claim from test timings']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    output = args.output.resolve()
    if output != root / 'docs/superpowers/specs/paos-aud-g7-code-quality-eval-results.json':
        parser.error('output must be the exact G7 results file')
    result = run(root)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('G7 local comparison recorded; model A/B and owner acceptance not implied')
    raise SystemExit(0 if result['arms'][1]['summary']['complete'] else 1)
