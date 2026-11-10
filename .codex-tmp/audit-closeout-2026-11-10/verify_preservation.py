import collections
import hashlib
import json
import re
from pathlib import Path

root = Path.cwd()
out = root / '.codex-tmp/audit-closeout-2026-11-10'
before = out / 'before'
pilot_path = 'docs/superpowers/specs/paos-aud-g6-pilot-results.json'
old = json.loads((before / pilot_path).read_text(encoding='utf-8'))
new = json.loads((root / pilot_path).read_text(encoding='utf-8'))
assert new['status'] == 'owner_accepted' and new['owner_acceptance']['decision'] == 'accepted'
for old_pilot, pilot in zip(old['pilots'], new['pilots'], strict=True):
    assert pilot['status'] == 'owner_accepted' and pilot['metrics']['owner_acceptance'] is True
    pilot['status'] = old_pilot['status']
    for key in ('owner_feedback', 'owner_acceptance'):
        pilot['metrics'][key] = old_pilot['metrics'][key]
for key in ('status', 'owner_feedback', 'owner_acceptance'):
    new[key] = old[key]
assert new == old, 'Pilot execution evidence changed'
group_path = 'docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json'
old = json.loads((before / group_path).read_text(encoding='utf-8'))
new = json.loads((root / group_path).read_text(encoding='utf-8'))
new['source_status'] = old['source_status']
assert new == old, 'Structured T34 evidence or authority changed'
matrix_path = 'research/product-agent-os-audit-remediation-task-plan-2026-11-09.md'
matrix = (root / matrix_path).read_text(encoding='utf-8')
cards = re.findall(r'^### Task `([^`]+)`\n(.*?)(?=^### Task |\Z)', matrix, re.M | re.S)
statuses = {name: re.search(r'^- Status: (\S+)', body, re.M)[1] for name, body in cards}
assert len(statuses) == 65
assert statuses['PAOS-GAP-06'] == 'implemented'
assert {k for k,v in statuses.items() if v != 'implemented'} == {'B45-CQRR-T34','PAOS-AUD-HOST-01','PAOS-AUD-HOST-02'}
old_matrix = (before / matrix_path).read_text(encoding='utf-8')
g9 = '## PAOS-AUD-G9'
assert matrix[matrix.index(g9):] == old_matrix[old_matrix.index(g9):], 'Accepted G9 cards changed'
plan = (root / 'PLAN.md').read_text(encoding='utf-8')
pointer = json.loads(re.search(r'<!-- product-agent-os:current-state:start -->\s*```json\s*(.*?)\s*```', plan, re.S)[1])
for source in pointer['sources']:
    assert source['revision'] == 'sha256:' + hashlib.sha256((root/source['path']).read_bytes()).hexdigest()
assert (root/'.codex/hooks/pre_tool_use_policy.py').read_bytes() == (root/'plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py').read_bytes()
sizes = {name: (root/name).stat().st_size for name in ('AGENTS.md','REQUIREMENTS.md','PLAN.md','TEST.md','EVALS.md','RUNLOG.md')}
assert all(size <= 40000 for size in sizes.values())
result = {'ok':True, 'cards':len(statuses), 'statuses':dict(collections.Counter(statuses.values())),
          'pilot_execution_evidence_unchanged':True,'t34_structured_evidence_unchanged':True,
          'g9_cards_unchanged':True,'source_pins_valid':True,'hook_parity':True,'control_plane_bytes':sizes}
print(json.dumps(result, indent=2))
