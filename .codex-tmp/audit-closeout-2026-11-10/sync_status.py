import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

root = Path.cwd()
out = root / '.codex-tmp/audit-closeout-2026-11-10'
now = datetime.now(timezone.utc).isoformat()
report = 'research/product-agent-os-audit-closeout-tooling-2026-11-10.md'

def read(path):
    return (root / path).read_bytes().decode('utf-8')

def write(path, text):
    p = root / path
    backup = out / 'before' / path
    if p.exists() and not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(p.read_bytes())
    p.write_bytes(text.encode('utf-8'))

pilot_path = 'docs/superpowers/specs/paos-aud-g6-pilot-results.json'
pilot = json.loads(read(pilot_path))
assert pilot['status'] == 'needs_user_acceptance'
pilot['status'] = 'owner_accepted'
pilot['owner_feedback'] = 'Owner accepted all three synthetic local pilot results; no broader effectiveness claim.'
pilot['owner_acceptance'] = {'decision': 'accepted', 'recorded_at': now,
    'scope': [p['id'] for p in pilot['pilots']],
    'limits': 'T34 and HOST-01/HOST-02 remain open; manual_only and candidate-only unchanged'}
for p in pilot['pilots']:
    p['status'] = 'owner_accepted'
    p['metrics']['owner_feedback'] = 'Result accepted by owner.'
    p['metrics']['owner_acceptance'] = True
write(pilot_path, json.dumps(pilot, ensure_ascii=False, indent=2) + '\n')

summary = ('G6 partially_verified: GAP-06 implemented / owner accepted 10.11.2026; '
           'все три synthetic local pilots приняты владельцем. HOST-01 не является их зависимостью. '
           'T34 no-go и fresh-session activation HOST-01/HOST-02 остаются открытыми отдельно; manual_only сохраняется.')
matrix = 'research/product-agent-os-audit-remediation-task-plan-2026-11-09.md'
ordinary = 'research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md'
for path in [matrix, ordinary]:
    text = read(path)
    start = text.index('### Task `PAOS-GAP-06`')
    end = text.find('\n## ', start + 1)
    if end < 0:
        end = len(text)
    card = text[start:end]
    card = card.replace('- Status: in_progress', '- Status: implemented').replace('- status: in_progress', '- status: implemented')
    card = card.replace('owner acceptance pending', 'owner acceptance получена 10.11.2026')
    card = card.replace('Приёмка трёх результатов пользователем; fresh-session activation остаётся самостоятельной открытой задачей.',
                        'Три результата приняты владельцем 10.11.2026; T34 и fresh-session activation отдельно открыты.')
    card = card.replace('needs_user_acceptance; feedback/acceptance null.', 'Owner accepted all three local pilots 10.11.2026.')
    card = card.replace('Пользователь принимает или отклоняет каждый результат; findings остаются manual candidates.',
                        'Приёмка получена для всех трёх результатов; findings остаются manual candidates, без promotion.')
    card = card.replace('live/host/owner receipts remain pending.', 'owner receipt recorded; live/host receipts remain separate.')
    card = card.replace('Три проверяемых результата для owner acceptance,', 'Три проверенных и принятых владельцем результата,')
    text = text[:start] + card + text[end:]
    if path == matrix:
        text = text.replace('GAP-06: три local pilots passed, needs_user_acceptance, без HOST-01 dependency.',
                            'GAP-06: три local pilots passed / owner accepted 10.11.2026, без HOST-01 dependency.')
        text = re.sub(r'G6 partially_verified: три синтетических пилота[^\r\n]+', summary, text)
        text = text.replace('T34/HOST-01/HOST-02/GAP-06 — blocked_pending_exact_authority_or_owner_acceptance.',
                            'T34 — approved_preflight_blocked / no-go; HOST-01/HOST-02 отдельно открыты; GAP-06 owner accepted 10.11.2026.')
        text = text.replace('Technical runtime/host gaps remain; pilots not_run; owner acceptance absent.',
                            'T34/runtime and fresh-host gaps remain; GAP-06 pilots passed and owner accepted 10.11.2026.')
        text = text.replace('- Статус: in_progress; T01–T13 implemented локально с уточнением docs/planning; T14 owner accepted; G8 closed; needs_user_acceptance до явного решения владельца.',
                            '- Статус: implemented; T01–T13 implemented локально с уточнением docs/planning; T14 owner accepted; G8 closed.')
        text = text.replace('- follow-up: T08 owner acceptance; не расширять выводы на другие стеки или production.',
                            '- follow-up: T08 owner accepted, G7 closed; не расширять выводы на другие стеки или production.')
        text = text.replace('|\r\n\r\n| PAOS-AUD-G9', '|\r\n| PAOS-AUD-G9').replace('|\n\n| PAOS-AUD-G9', '|\n| PAOS-AUD-G9')
    write(path, text)

group_path = 'docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json'
text = read(group_path).replace('T34 remains approval_required_not_started.',
    'T34 remains approved_preflight_blocked; approved scope is unconsumed, tools/context isolation is not attested.')
write(group_path, text)

for path in ['PLAN.md', 'RUNLOG.md', 'REQUIREMENTS.md', 'TEST.md', 'EVALS.md']:
    text = read(path)
    # Compact pointers replace repeated full pilot narrative in control-plane documents.
    text = re.sub(r'G6 partially_verified: три синтетических пилота[^\r\n]+',
        summary + ' [Результаты](docs/superpowers/specs/paos-aud-g6-pilot-results.json).', text)
    if path == 'PLAN.md':
        text = text.replace('Следующая группа — G2; существующий MCP compatibility gap остаётся её F01.',
                            'G2/F01 впоследствии закрыла MCP compatibility gap; текущие остатки — T34 и HOST-01/HOST-02.')
        text = text.replace('следующий slice — G3.', 'G3 впоследствии выполнена.')
        for old, new in [('Следующая группа — G4.', 'G4 впоследствии выполнена.'),
                         ('Следующая группа — G5.', 'G5 впоследствии выполнена.'),
                         ('Следующая группа — G6; её host/behavioral/owner gates остаются отдельными.',
                          'G6 частично выполнена; T34 и host gates остаются отдельными, пилоты приняты.')]:
            text = text.replace(old, new)
        # Rebind only changed sources; other source selectors remain intact.
        for source in [matrix, group_path]:
            digest = hashlib.sha256((root / source).read_bytes()).hexdigest()
            text = re.sub(r'("path": "' + re.escape(source) + r'",\s*"revision": ")sha256:[0-9a-f]+',
                          lambda m: m[1] + 'sha256:' + digest, text)
    write(path, text)

receipt = {'recorded_at': now, 'owner_acceptance': 'GAP-06 all three pilots',
           't34_unchanged_fields': ['status', 'result_status', 'blocker', 'approved_runtime_followup'],
           'evidence_report': report}
(out / 'acceptance.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
print(json.dumps(receipt))
