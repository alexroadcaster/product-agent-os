from pathlib import Path
import json
import re

base = Path('docs/planning/user-project-methodologies-2026-11-15')
files = [base.with_suffix(s) for s in ('.json', '.en.json')]
p = json.loads(files[0].read_bytes())
tasks = {int(t['id'][-2:]): t for t in p['tasks']}
assert p['planning_revision']['after']['edge_count'] == 37
def ref(n):
    return f'PAOS-PMETH-{n:02}'

previous = p['planning_revision']['before']['changed_dependencies']
previous[ref(9)] = tasks[9]['depends_on']
assert previous[ref(12)] == [ref(6), ref(11)]
tasks[9]['depends_on'] = [ref(8)]
tasks[12]['depends_on'] = [ref(11)]
tasks[23]['depends_on'] = [ref(26)]
for t in tasks.values():
    t['blocks'] = [o['id'] for o in tasks.values() if t['id'] in o['depends_on']]
edges = sum(len(t['depends_on']) for t in tasks.values())
assert edges == 31
p['planning_revision']['after']['edge_count'] = edges
scope_gates = {
    'read_only_bug_docs': [ref(26)],
    'design': [ref(9)],
    'fsd_migration': [ref(12)],
    'skill_tool_routing': [ref(14)],
    'target_write_apply': [ref(16)],
    'criterion_readiness': [ref(17)],
    'durable_override_recovery': [ref(21)],
}
p['profile_qualification'] = {
    'qualification_task': ref(23),
    'rollout_decision_task': ref(25),
    'base_profile': 'read_only_bug_docs',
    'required_tasks_by_claim': scope_gates,
    'broad_rollout_requires_all_claims': True,
    'before_go': 'All tasks required by the claimed profile and their hard prerequisites must have qualifying evidence and disposition. Any unverified claim is excluded and a critical gap blocks the affected profile.',
    'on_profile_expansion': 'Repeat PMETH-23 on the new claimed profile and record evidence revision and scope before PMETH-25 expands rollout.',
}

def ac(n, i, ru, en):
    tasks[n]['acceptance_criteria'][i-1].update(ru=ru, en=en)

ac(12, 3,
   'Proposal описывает ожидаемое сохранение user files, dirty changes и business/API semantics и показывает, как проверить границы legacy imports. На этой стадии исходники сохраняются; фактический перенос проверяется в PMETH-23, если вошёл в scope пилота.',
   'Describe how the proposal preserves user files, dirty changes and business/API semantics, and how to check legacy import boundaries. Preserve target files in this task. PMETH-23 verifies actual code moves when included in the pilot scope.')
ac(12, 4,
   'Готовый read-only proposal доступен в памяти. Staged diff и apply по отдельно выбранному FSD пути используют PMETH-16 writer и проверяются в PMETH-23. Target write и hook activation требуют отдельной authority.',
   'Deliver the read-only proposal in memory. The separately selected FSD path uses the PMETH-16 writer for staged diff and apply, verified in PMETH-23. Target writes and hook activation require separate authority.')
ac(19, 1,
   'Guarded Project Analysis HTTP → Python bridge возвращает task-scoped advice отдельно от project facts. Эквивалентные bug/docs запросы при одинаковых данных и coverage дают те же решения и причины в CLI. Если Web видит только metadata, а CLI прочитал исходники, различие объясняется coverage и partial/unknown. Ответ другого project/task/revision или неподдержанной версии отклоняется.',
   'The guarded Project Analysis HTTP path through its Python bridge returns task-scoped advice separately from project facts. Equivalent bug/docs requests with the same data and coverage yield the same decisions and reasons in CLI. When Web sees only metadata and CLI reads source, explain the difference through coverage and partial/unknown. Reject wrong project/task/revision and unsupported schema responses.')
ac(19, 2,
   'Read-only запрос проверяет session/origin/project scope, input bounds и cancellation. CSRF применяется по HTTP-методу и действующему контракту. Target write и новый durable store не требуются. PMETH-16/21 владеют mutating route и проверками его полномочий.',
   'Check session/origin/project scope, input bounds and cancellation for read-only requests. Apply CSRF according to HTTP method and the existing contract. Reads require no target write or new durable store. PMETH-16/21 own the mutating route and its authority checks.')
ac(22, 1,
   'PMETH-22 закрывает baseline до изменения policy на двух задачах в одном проекте: backend bug и docs-only. Для каждой заранее заданы AC, следующий тест или source link, основания и gaps. Native, AI/RAG и три frontend профиля остаются в общей матрице; baseline для них фиксируют владельцы соответствующих веток до candidate checks и включения.',
   'PMETH-22 completes its baseline before policy changes on two tasks in one project, backend bug and docs-only. Set AC, next test or source link, reasons and gaps in advance. Retain native, AI/RAG and three frontend profiles in the scenario matrix. Branch owners capture their baseline before candidate checks and enabling each profile.')
ac(22, 2,
   'Ранние негативы покрывают конфликтный/неполный intent, missing tests, stale/partial, wrong project/task/revision и отсутствие target writes. В общей матрице помечены дополнительные случаи misleading folders, alias unknown, stale spec, forged success, prompt injection, dirty files, denied writes и unavailable tools; соответствующая ветка проверяет их перед включением.',
   'Early negatives cover conflicting/incomplete intent, missing tests, stale/partial output, wrong project/task/revision and absence of target writes. Keep misleading folders, unknown aliases, stale specs, forged success, prompt injection, dirty files, denied writes and unavailable tools in the shared matrix. The owning branch checks them before enabling.')
ac(23, 2,
   'Подходящий frontend pilot проверяет Design states, FSD migration proposal и incremental FSD. Если заявлен apply, проверены staged diff PMETH-16, compatibility, rollback и сохранность user files. Модульный frontend сохраняет структуру; backend/CLI обходятся без FSD gates, AI quality остаётся eval/gap без скрытого provider call.',
   'Verify Design states, the FSD migration proposal and incremental FSD on a suitable frontend pilot. If apply is claimed, verify the PMETH-16 staged diff, compatibility, rollback and user-file preservation. Preserve existing modular structure, omit FSD gates on backend/CLI paths and keep AI quality as eval/gap with no hidden provider calls.')
ac(23, 1,
   'Базовый профиль повторяет read-only CLI/Web на current source. Для каждого заявленного расширения выполнены задачи и проверки из profile_qualification, включая staged plan → authorized fixture apply/build/check → evidence/verdict для write и reload override, stale verdict после смены AC для соответствующих claims. Расширение профиля повторно проходит PMETH-23 с новой областью и revision.',
   'Repeat the read-only CLI/Web route on current source for the base profile. Meet the tasks and checks in profile_qualification for each claimed expansion, including staged plan, authorized fixture apply/build/check and evidence/verdict for writes, and override reload and stale verdict after AC changes for corresponding claims. Repeat PMETH-23 with the new scope and revision on expansion.')
ac(23, 3,
   'Проверены critical privacy/authority/user-file/isolation/false-ready cases, source/build/harness identity и cleanup по заявленному scope. Critical gap блокирует соответствующий профиль. Broad rollout проходит все ветки и отрицательные случаи, включая реальные approval/recovery/rollback на fixture.',
   'Verify critical privacy/authority/user-file/isolation/false-ready cases, source/build/harness identity and cleanup for the claimed scope. A critical gap blocks the affected profile. Broad rollout exercises all branches and negatives, including real approval/recovery/rollback on a fixture.')
ac(25, 1,
   'Owner-reviewed go/bounded_go/hold/no-go фиксирует scope/revision, evidence и residual gaps. Проверены статусы и evidence задач из profile_qualification для каждого заявленного профиля. Непроверенные профили остаются вне решения; при расширении нужен профильный PMETH-23. RU/EN обновляются только для подтверждённых путей.',
   'Record scope/revision, evidence and residual gaps in the owner-reviewed go/bounded_go/hold/no-go. Check status and evidence of the profile_qualification tasks for each claimed profile. Exclude unverified profiles and repeat profile-specific PMETH-23 before expansion. Update RU/EN guidance for confirmed paths only.')

result12 = ('Read-only migration proposal с reversible page pilot, public APIs, import ratchet и критериями следующего checkpoint.',
            'Read-only migration proposal with a reversible page pilot, public APIs, import ratchet and criteria for the next checkpoint.')
current_snapshot = (
    'Срез исследования от 18.11.2026 по текущему FUNC-владельцу — 33 implemented и F23 awaiting_user_decision. Повторно используются F02 (task/artifact links), F13 (document apply), F14 (code index) и F27–29 (project analysis и связи источников). Статусы описывают матрицу FUNC; новый runtime-прогон этим исследованием не выполнялся. Первичные источники и Context7 проверены 18.11.2026, результаты и ограничения приведены в исследовании.',
    'The 2026-11-18 review of the current FUNC owner recorded 33 implemented and F23 awaiting_user_decision. Reuse F02 (task/artifact links), F13 (document apply), F14 (code index) and F27–29 (project analysis and source links). These are FUNC matrix statuses. This review did not rerun the runtime. The review records primary sources and Context7 findings and limitations checked on 2026-11-18.',
)
out = {}
for suffix, lang, l in (('.md','ru',0), ('.en.md','en',1)):
    f = base.with_suffix(suffix)
    old = f.read_bytes()
    newline = '\r\n' if b'\r\n' in old else '\n'
    s = old.decode().replace('\r\n', '\n')
    s = s.replace('\n| Область |', f'\n{current_snapshot[l]}\n\n| Область |', 1) if not l else s.replace('\n| Area |', f'\n{current_snapshot[l]}\n\n| Area |', 1)
    s = s.replace('37 активных', f'{edges} активных').replace('37 active', f'{edges} active')
    code = chr(96)
    s = s.replace('[исследование 18.11.2026](../../research/methodology-plan-review-2026-11-18.md)', f'{code}research/methodology-plan-review-2026-11-18.md{code}')
    s = s.replace('[2026-11-18 review](../../research/methodology-plan-review-2026-11-18.md)', f'2026-11-18 review in {code}research/methodology-plan-review-2026-11-18.md{code}')
    profile_title = ('## Условные требования перед квалификацией профиля', '## Conditional requirements before profile qualification')[l]
    labels = ('Заявленный путь | Обязательная карточка перед профильным PMETH-23', 'Claimed route | Required task before profile-specific PMETH-23')[l]
    names = (
        ('Базовый read-only bug/docs', 'Design journey', 'Миграция FSD', 'Маршрутизация skills/tools', 'Запись в target', 'Technical readiness по AC', 'Durable override и recovery'),
        ('Base read-only bug/docs', 'Design journey', 'FSD migration', 'Skill/tool routing', 'Target writes', 'Technical readiness by AC', 'Durable override and recovery'),
    )[l]
    table = [f'| {labels} |', '| --- | --- |']
    table.extend(f'| {label} | {", ".join(required)} |' for label, required in zip(names, scope_gates.values(), strict=True))
    after = (
        'Базовая PMETH-23 ждёт PMETH-26. Перед go по каждому дополнительному claim обязательны указанная карточка, её hard prerequisites и профильные E2E с evidence на выбранных scope/revision. Для широкого rollout квалифицируются все строки. PMETH-25 сверяет статусы и evidence по ' + f'{code}profile_qualification{code}' + '; непроверенный claim не включается, critical gap блокирует соответствующий профиль. Расширение требует повторного PMETH-23 по новой области и revision.',
        'Base PMETH-23 depends on PMETH-26. Before go on an additional claim, its listed task, hard prerequisites and profile-specific E2E evidence at the selected scope/revision are mandatory. Broad rollout qualifies every row. PMETH-25 reconciles task status and evidence against ' + f'{code}profile_qualification{code}' + '. Exclude unverified claims, and block an affected profile on a critical gap. Repeat PMETH-23 for the new scope and revision before expansion.',
    )[l]
    marker = ('## Связи с A и действующими планами', '## Links to A and existing plans')[l]
    assert marker in s
    s = s.replace(marker, '\n\n'.join([profile_title, '\n'.join(table), after, marker]), 1)
    s = s.replace('эквивалентных данных и coverage', 'данных и покрытия')
    s = s.replace('backend bug и docs-only дают одинаковые выводы CLI/Web, основание и следующий проверяемый шаг.', 'backend bug и docs-only дают одинаковые выводы CLI/Web при равных данных и покрытии, с основанием и следующим проверяемым шагом.')
    s = s.replace('backend bug and docs-only give matching CLI/Web decisions, reasons and the next verifiable step.', 'backend bug and docs-only give matching CLI/Web decisions with the same data and coverage, as well as reasons and the next verifiable step.')
    for n, t in tasks.items():
        key = t['id']
        deps, blocks = (', '.join(t[k]) for k in ('depends_on','blocks'))
        none = ('Нет.', 'None.')[l]
        s, count = re.subn(rf'(?m)^(\| {key} \|[^\n]*\| )([^|]*)( \|)$', lambda m: m[1] + (deps or '—') + m[3], s, count=1)
        assert count == 1
        code = chr(96)
        a = s.index(f'### Task {code}{key}{code}')
        b = s.find('\n### Task ', a + 1)
        b = len(s) if b == -1 else b
        card = s[a:b]
        for label, value in (('Depends on', deps or none), ('Blocks', blocks or none)):
            card = re.sub(rf'(?m)^- {label}: .+$', lambda m: f'- {label}: {value}', card, count=1)
        for crit in t['acceptance_criteria']:
            card = re.sub(rf'(?m)^(  - \*\*{crit["id"]}\*\*: ).+$', lambda m: m[1]+crit[lang], card, count=1)
        if n == 12:
            for label in ('Output artifacts', 'Expected result'):
                card = re.sub(rf'(?m)^- {label}: .+$', lambda m: f'- {label}: {result12[l]}', card, count=1)
        s = s[:a] + card + s[b:]
    out[f] = s.replace('\n', newline).encode()
serialized = (json.dumps(p, indent=2, ensure_ascii=False) + '\n').encode()
for f in files:
    out[f] = serialized
for f, data in out.items():
    f.write_bytes(data)
