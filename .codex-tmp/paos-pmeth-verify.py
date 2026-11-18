from pathlib import Path
import collections
import json
import re
import subprocess

base = Path('docs/planning/user-project-methodologies-2026-11-15')
json_path, json_mirror = (base.with_suffix(s) for s in ('.json', '.en.json'))
assert json_path.read_bytes() == json_mirror.read_bytes()
plan = json.loads(json_path.read_bytes())
before = json.loads(subprocess.check_output(['git', 'show', f'HEAD:{json_path.as_posix()}']))
current_tasks = {t['id']: t for t in plan['tasks']}
baseline_tasks = {t['id']: t for t in before['tasks']}
assert current_tasks.keys() == baseline_tasks.keys()
assert plan['source_snapshot'] == before['source_snapshot']
assert plan['legacy_reference'] == before['legacy_reference']
for key, t in current_tasks.items():
    old = baseline_tasks[key]
    for field in ('title', 'title_en', 'status', 'priority', 'implementation_at', 'execution_authority'):
        assert t[field] == old[field], (key, field)
    assert [a['id'] for a in t['acceptance_criteria']] == [a['id'] for a in old['acceptance_criteria']]

def walk(parent, stack=()):
    assert parent not in stack
    result = set()
    for dep in current_tasks[parent]['depends_on']:
        result |= {dep} | walk(dep, (*stack, parent))
    return result

for key, t in current_tasks.items():
    walk(key)
    assert set(t['blocks']) == {k for k, o in current_tasks.items() if key in o['depends_on']}
    assert all(dep not in walk(other) for dep in t['depends_on'] for other in t['depends_on'])
    assert all(ref.startswith('PAOS-FUNC-') or ref == 'UI-12' for ref in t['external_refs']), t['external_refs']
    restored = plan['planning_revision']['before']['changed_dependencies'].get(key, t['depends_on'])
    assert restored == baseline_tasks[key]['depends_on'], (key, restored)

for suffix, lang in (('.md', 'ru'), ('.en.md', 'en')):
    file = base.with_suffix(suffix)
    text = file.read_text(encoding='utf-8')
    code = chr(96)
    cards = re.split(rf'(?m)^### Task {code}([^{code}]+){code}\n', text)
    sections = dict(zip(cards[1::2], cards[2::2], strict=True))
    assert sections.keys() == current_tasks.keys()
    for key, t in current_tasks.items():
        block = sections[key]
        title = t['title_en' if lang == 'en' else 'title']
        assert f'- Task name: {title}\n' in block
        assert f'- Status: {t["status"]}\n' in block
        assert f'- Priority: {t["priority"]}\n' in block
        for label, field in (('Depends on', 'depends_on'), ('Blocks', 'blocks')):
            value = ', '.join(t[field]) or ('None.' if lang == 'en' else 'Нет.')
            assert f'- {label}: {value}\n' in block, (key, field)
        index_deps = ', '.join(t['depends_on']) or '—'
        assert re.search(rf'(?m)^\| {key} \|.*\| {re.escape(index_deps)} \|$', cards[0]), key
        for ac in t['acceptance_criteria']:
            assert f'  - **{ac["id"]}**: {ac[lang]}\n' in block, ac['id']

milestone = plan['planning_revision']['read_only_milestone']
assert set(milestone['required_tasks']) == walk(milestone['terminal_task']) | {milestone['terminal_task']}
assert len(walk('PAOS-PMETH-20')) == 8
edges = sum(len(t['depends_on']) for t in current_tasks.values())
ac_count = sum(len(t['acceptance_criteria']) for t in current_tasks.values())
priorities = collections.Counter(t['priority'] for t in current_tasks.values())
print(f'ok: B {len(current_tasks)} tasks; {ac_count} AC; {edges} irredundant reciprocal edges; priorities {dict(priorities)}; RU/EN parity, history and identical JSON; 8 Web prerequisites and 10 milestone cards.')
