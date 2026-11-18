from pathlib import Path
import json
import re

root = Path.cwd()
base = root / 'docs/planning/user-project-methodologies-2026-11-15'
source, mirror = (base.with_suffix(s) for s in ('.json', '.en.json'))
assert source.read_bytes() == mirror.read_bytes()
payload = json.loads(source.read_bytes())
tasks = {int(t['id'][-2:]): t for t in payload['tasks']}
assert len(tasks) == 26 and all(t['status'] == 'planned' for t in tasks.values())

def tid(n):
    return f'PAOS-PMETH-{n:02}'

dag = {12: [11, 16], 15: [7, 13], 16: [6, 15], 17: [6, 15], 18: [17, 19], 19: [7], 20: [19],
       21: [16, 18, 20], 23: [9, 12, 14, 21, 26], 26: [20]}
previous = {tid(n): list(t['depends_on']) for n, t in tasks.items()}
for n, deps in dag.items():
    tasks[n]['depends_on'] = list(map(tid, deps))

def ancestors(n, stack=()):
    assert n not in stack
    acc = set()
    for key in tasks[n]['depends_on']:
        item = int(key[-2:])
        acc |= {item} | ancestors(item, (*stack, n))
    return acc

for t in tasks.values():
    implied = set().union(*(ancestors(int(d[-2:])) for d in t['depends_on']))
    t['depends_on'] = [d for d in t['depends_on'] if int(d[-2:]) not in implied]
for t in tasks.values():
    t['blocks'] = [other['id'] for other in tasks.values() if t['id'] in other['depends_on']]
edges = sum(len(t['depends_on']) for t in tasks.values())
previous = {key: value for key, value in previous.items() if tasks[int(key[-2:])]['depends_on'] != value}

early = {1, 2, 3, 4, 5, 7, 19, 20, 22, 26}
assert ancestors(26) | {26} == early and len(ancestors(20)) == 8
assert ancestors(25) | {25} == set(tasks)

def ac(n, i, ru, en):
    criterion = tasks[n]['acceptance_criteria'][i - 1]
    assert criterion['id'] == f'{tid(n)}-AC{i:02}'
    criterion.update(ru=ru, en=en)

ac(1, 1,
   'Карта reuse/extend/missing прослеживает CLI intake → discovery/audit/synthesis/task routing и Project Analysis → Python bridge → Sources/Teams & Tasks; для записи отдельно G9/F13. У каждого звена указан фактический вход, владелец и существующие тесты.',
   'Trace CLI intake through discovery/audit/synthesis/task routing, Project Analysis through its Python bridge to Sources/Teams & Tasks, and G9/F13 separately for writes. Identify the real entry point, owner and existing tests at each edge.')
ac(1, 2,
   'Зафиксированы два существующих обхода discovery/audit, их фильтры и пример разного покрытия; используется существующая инвентаризация. Detection, observed projection, proposal и execution различаются.',
   'Record the two existing discovery/audit traversals, their filters and a coverage difference. Reuse existing inventories and distinguish detection, observed projection, proposals and execution.')
ac(2, 2,
   'Один нормализованный intent и применимые AC доходят до audit/route. Приоритет task_context и intent_hint явно определён; конфликтный, смешанный или ошибочный ввод отклоняется либо даёт явный gap. Проверены desktop/Python adapter input и CLI intake на эквивалентных bug/docs; parity результата в рабочем HTTP path проверяет PMETH-19, staging — PMETH-16. Repository-only audit сохранён.',
   'Pass one normalized intent and applicable AC to audit and routing. Define precedence between task_context and intent_hint and reject conflicting, mixed or malformed input or expose an explicit gap. Verify desktop/Python adapter input and CLI intake with equivalent bug/docs tasks. PMETH-19 verifies parity on the real HTTP path and PMETH-16 verifies staging. Preserve repository-only audit.')
ac(3, 3,
   'Missing evidence даёт вопрос/gap/present_unverified. В read-only пути пользователь уточняет вход и пересчитывает совет без записи. Durable override с причиной и областью применения закреплён за PMETH-18/21 и сохраняет обязательные проверки.',
   'Missing evidence yields a question, gap or present_unverified. In the read-only path users refine input and recompute advice without a write. PMETH-18/21 own durable overrides with rationale and scope and preserve mandatory checks.')
ac(4, 1,
   'Выбран один schema owner и минимальные Python/TypeScript adapters к существующим контрактам. Project-only facts и task-scoped advice различаются; project/task identity, source/task revisions и evidence refs проверяются на границе.',
   'Choose a single schema owner and minimal Python/TypeScript adapters over existing contracts. Distinguish project-only facts from task-scoped advice and validate project/task identity, source/task revisions and evidence references at the boundary.')
ac(5, 1,
   'Небольшая задача получает concise scope/AC в существующей задаче или read-only проекции без генерации файла. Сложная получает требования/non-goals/invariants и сценарии через существующего владельца.',
   'Give a small task concise scope/AC in the existing task or read-only projection without generating files. Route complex requirements, non-goals, invariants and scenarios to the existing owner.')
ac(5, 3,
   'Существующие user-authored требования и их владелец сохраняются. Read-only путь показывает следующий шаг текстом/ссылкой. Staged proposal/diff и применение принадлежат PMETH-16.',
   'Preserve user-authored requirements and their owner. The read-only path shows the next step as text or a link. PMETH-16 owns staged proposals, diffs and application.')
ac(7, 1,
   'Read-only маршрут показывает следующий тест для backend bug и source check для docs-only. Synthetic fixture подтверждает один regression check с observable intended RED, minimal GREEN и scoped refactor disposition. Команда, revision и expected/actual сохранены в имеющемся evidence без записи в целевой проект.',
   'Show the next test for a backend bug and a source check for docs-only in the read-only path. Substantiate one regression check on a synthetic fixture with intended observable RED, minimal GREEN and scoped refactor disposition. Capture command, revision and expected/actual in existing evidence without writing to the target.')
ac(8, 1,
   'Изменяемый journey определяет цель, шаги, данные, interaction/error/empty/loading/dirty states и accessibility. Для существенного или неясного journey фиксируются гипотеза о проблеме и наблюдение с представительным пользователем либо evidence gap. Backend-only получает not_applicable.',
   'Define the goal, steps, data, interaction/error/empty/loading/dirty states and accessibility for changed journeys. Record a problem hypothesis and representative user observation or evidence gap for substantial or uncertain journeys. Backend-only is not_applicable.')
ac(10, 3,
   'Предложение начинается со страниц и подтверждённого coupling. Public APIs и нижние layers/slices появляются при подтверждённой потребности. Backend/Python и native получают применимую архитектурную политику.',
   'Start with pages and demonstrated coupling. Introduce public APIs and lower layers/slices where a need is demonstrated. Apply the relevant architecture policy to backend, Python and native targets.')
ac(11, 1,
   'FSD rules используют наблюдаемые рёбра F14 для JS/TS/TSX и привязаны к source revision. Покрытие TSImportType, reexports, tsconfig aliases/extends и literal dynamic imports проверяется явно.',
   'Evaluate FSD rules over observed F14 edges for JS/TS/TSX and bind results to the source revision. Explicitly check coverage of TSImportType, re-exports, tsconfig aliases/extends and literal dynamic imports.')
ac(11, 2,
   'Unsupported syntax/alias/symlink/out-of-scope source и CLI без доступного адаптера дают partial/unknown с coverage и объяснением. Частичный graph и folder signals не дают present_verified.',
   'Unsupported syntax, aliases, symlinks, out-of-scope source and CLI without an available adapter yield partial/unknown with coverage and an explanation. Partial graphs and folder signals cannot yield present_verified.')
ac(11, 4,
   'Переиспользованы F14 code-index, parser/resolver и fixtures. F30 остаётся import-only reference. Проверены meaningful parser cases, циклы и no-source-mutation hashes без обязательной установки.',
   'Reuse F14 code-index, its parser/resolver and fixtures. Keep F30 as an import-only reference. Verify meaningful parser cases, cycles and no-source-mutation hashes without requiring installation.')
ac(12, 2,
   'Сначала граница и один page pilot с public API/import ratchet. Вынос в shared/entities оправдан подтверждённым повторным использованием. Следующие checkpoints зависят от принятия предыдущих; возможна остановка на пилоте.',
   'Start with a boundary and one page pilot with a public API/import ratchet. Extract to shared/entities where reuse is demonstrated. Later checkpoints require adoption of the previous one, and the pilot may be the stopping point.')
ac(12, 4,
   'Read-only scan может вернуть proposal в памяти. Staged diff использует PMETH-16 writer после выбора FSD-пути. Target apply и hook activation требуют отдельной authority.',
   'A read-only scan can return a proposal in memory. A staged diff uses the PMETH-16 writer once the FSD path is selected. Target apply and hook activation require separate authority.')
ac(15, 1,
   'Один DAG использует methodology_synthesis и formation_plan. Canonical name и alias одного существующего файла дают один артефакт и одного владельца с обоими основаниями.',
   'Build one DAG over methodology_synthesis and formation_plan. The canonical name and alias of one existing file produce one artifact and one owner with both reasons.')
ac(15, 2,
   'Dependencies отражают фактические prerequisites. PMETH-08/09 и PMETH-10–12 входят только в Design/FSD ветки, PMETH-14 добавляет skills по потребности. Компактная bug/docs рекомендация доступна через PMETH-19/20 без delivery DAG.',
   'Record actual prerequisites. PMETH-08/09 and PMETH-10–12 apply only to Design/FSD branches and PMETH-14 adds skills as needed. Compact bug/docs advice is available through PMETH-19/20 without the delivery DAG.')
ac(16, 1,
   'Infrastructure bundle использует G9 formation/dry-run/stage/manifest/merge, допустимый single-document proposal использует F13 document apply. Вид операции выбирает одного writer; stage вне target, запись требует точную authority.',
   'Use G9 formation/dry-run/stage/manifest/merge for infrastructure bundles and F13 document apply for eligible single-document proposals. Each operation kind selects one writer, the stage stays outside the target and writes require exact authority.')
ac(16, 2,
   'Существующий preview показывает owned paths, user-file handling, method/AC links, side effects и writer. Unmarked AGENTS/config/hooks сохраняются; apply доступен только у своего маршрута.',
   'Use the existing preview to show owned paths, user-file handling, method/AC links, side effects and writer. Preserve unmarked AGENTS/config/hooks and expose apply only through its own route.')
ac(16, 3,
   'Preview/apply связаны точным digest, project/task, revision и operation ID. Drift, wrong root/project, traversal/symlink и stale approval отклоняются; recovery сохраняет edits и не повторяет эффект с unknown outcome.',
   'Bind preview/apply to an exact digest, project/task, revision and operation ID. Reject drift, wrong root/project, traversal/symlinks and stale approvals. Preserve edits in recovery and prevent replay of effects with unknown outcomes.')
ac(17, 1,
   'Requirement → stable AC ID → scenario/check → receipt → verdict имеет owner, revision/environment и применимость. В synthetic задаче manual acceptance сохраняется для двух AC, technical evidence засчитывается только у AC с привязанным receipt нужной revision. Accepted gap остаётся отдельным.',
   'Trace requirement through stable AC ID, scenario/check and receipt to a verdict with owner, revision/environment and applicability. Preserve manual acceptance for two ACs in a synthetic task. Technical evidence counts only for the AC with a bound receipt at the correct revision. Keep accepted gaps distinct.')
ac(17, 2,
   'Переиспользованы task_routing input_digest/check_observations и существующие receipts/acceptTask. Caller-reported results, detection, generated files и test count не дают technical passed; missing/stale/failed/partial видны.',
   'Reuse task_routing input_digest/check_observations and existing receipts/acceptTask. Caller-reported results, detection, generated files and test counts cannot produce technical passed. Keep missing/stale/failed/partial visible.')
ac(17, 4,
   'CLI pilot связывает применимые методы с checks на одном fixture revision. Technical, manual/human и release acceptance различаются. Visual/FSD/target-apply evidence требуется для соответствующих claims PMETH-23.',
   'The CLI pilot links applicable methods to checks on one fixture revision, separating technical, manual/human and release acceptance. Visual, FSD and target-apply evidence supports corresponding PMETH-23 claims.')
ac(18, 1,
   'Project facts, task advice, persisted decision и criterion evidence имеют canonical owners в scans, задачах/ссылках и evidence. Новый durable record оправдан только подтверждённым пробелом, чтение PMETH-19 не требует миграции.',
   'Use scans, tasks/links and evidence as canonical owners for project facts, task advice, persisted decisions and criterion evidence. Add durable records only for proven gaps. PMETH-19 reads require no migration.')
ac(18, 2,
   'Version/revision/CAS, history, project isolation и explicit unknown поддержаны. Override хранит причину, область, автора и revisions, сохраняя обязательные проверки. Older clients/newer schema не теряют данные.',
   'Support version/revision/CAS, history, project isolation and explicit unknown. Store override reason, scope, actor and revisions while retaining mandatory checks. Preserve data across older clients and newer schemas.')
ac(19, 1,
   'Guarded Project Analysis HTTP → Python bridge возвращает task-scoped advice отдельно от project facts. Эквивалентная нормализованная bug/docs задача даёт те же решения и причины в CLI. Ответ другого project/task/revision или неподдержанной версии отклоняется.',
   'The guarded Project Analysis HTTP path through its Python bridge returns task-scoped advice separately from project facts. Equivalent normalized bug/docs tasks yield the same decisions and reasons in CLI. Reject wrong project/task/revision and unsupported schema responses.')
ac(19, 2,
   'Read-only запрос использует существующие session/origin/CSRF/project guards с input bounds и cancellation, без target write и нового durable store. PMETH-16/21 владеют mutating route и проверками его полномочий.',
   'Use existing session/origin/CSRF/project guards with input bounds and cancellation for reads, without target writes or a new durable store. PMETH-16/21 own the mutating route and its authority checks.')
ac(19, 3,
   'Receipt показывает intended path/selector, partial/ready/warnings и причину. После analysis → schema/code_database открытие advice сохраняет последнюю релевантную стадию analysis нужной revision либо объясняет следующий шаг. Bridge failure виден без маскировки fallback.',
   'Expose intended path/selector, partial/ready/warnings and the reason. After analysis then schema/code_database, opening advice retains the last relevant analysis stage for the required revision or explains the next step. Surface bridge failures without masking fallbacks.')
ac(20, 1,
   'Project facts видны в Sources, task advice и следующий проверяемый шаг — в существующем Teams & Tasks flow. Согласованы минимальные placement/states. Видны причина, глубина и required/optional/not_applicable.',
   'Show project facts in Sources and task advice and the next verifiable step in the existing Teams & Tasks flow. Agree on minimal placement and states, and show rationale, depth and required/optional/not_applicable.')
ac(20, 2,
   'Показаны source/coverage/unknown, scope, permissions и причины остановки. Сценарий понимания проверяет, может ли человек без подсказки объяснить совет, назвать следующий шаг и отличить просмотр от применения. Результат или evidence gap записан по PMETH-22.',
   'Show source/coverage/unknown, scope, permissions and stop reasons. Check whether a person can explain the advice, identify the next step and distinguish viewing from applying without prompting. Record the observation or evidence gap under PMETH-22.')
ac(20, 3,
   'Проверены loading/empty/error/stale/partial и applicable permission-required, RU/EN, themes и keyboard/focus. Partial показывает доступные факты и предупреждения, недоступный backend не подменяется fixture success. PMETH-21/23 проверяют конфликт и apply для записи.',
   'Verify loading/empty/error/stale/partial and applicable permission-required, RU/EN, themes and keyboard/focus. Partial shows available facts and warnings, and backend unavailability is never replaced by fixture success. PMETH-21/23 verify conflict and apply for writes.')
ac(20, 4,
   'Synthetic browser проходит PMETH-19 API для backend bug и docs-only, включая wrong project/task, partial и смену latest scan stage. Target и durable methodology state не меняются. Persisted override/audit принадлежат PMETH-18/21.',
   'Exercise the PMETH-19 API from a synthetic browser for backend bug and docs-only, including wrong project/task, partial output and latest scan stage changes. Preserve the target and durable methodology state. PMETH-18/21 own persisted override and audit.')
ac(21, 3,
   'Audit сохраняет минимальные records с redaction, owner и временем. Manual override/disposition видимы в существующей задаче, partial/failed attempts сохранены. Preview/apply показывают digest/revision, diff, conflict и authority state.',
   'Preserve minimal audit records with redaction, owner and time. Show manual overrides/dispositions in the existing task and preserve partial/failed attempts. Preview/apply shows digest/revision, diff, conflict and authority state.')
ac(22, 1,
   'Первый baseline до изменения policy берёт backend bug и docs-only в одном проекте. Для каждого заранее заданы AC, следующий тест или source link, основания и gaps. Native, AI/RAG и три frontend профиля добавляются до своих candidate checks.',
   'Capture the first baseline for backend bug and docs-only in one project before policy changes. Set AC, the next test or source link, reasons and gaps in advance. Add native, AI/RAG and three frontend profiles before their candidate checks.')
ac(22, 2,
   'Ранние негативы покрывают конфликтный/неполный intent, missing tests, stale/partial, wrong project/task/revision и отсутствие target writes. В соответствующих ветках добавить misleading folders, alias unknown, stale spec, forged success, prompt injection, dirty files, denied writes и unavailable tools.',
   'Early negatives cover conflicting/incomplete intent, missing tests, stale/partial output, wrong project/task/revision and absence of target writes. Add misleading folders, unknown aliases, stale specs, forged success, prompt injection, dirty files, denied writes and unavailable tools in applicable branches.')
ac(22, 3,
   'Baseline results и failures сохранены; setup failure не продуктовый RED. Владелец до пилота задаёт sample, пороги верного самостоятельного выбора, времени до первого проверяемого шага, лишних шагов и отмен рекомендации.',
   'Preserve baseline results and failures; setup failure is not product RED. Before the pilot the owner sets sample and thresholds for independent correct choices, time to first verifiable step, unnecessary steps and recommendation cancellations.')
ac(23, 1,
   'Повторён ранний read-only CLI/Web путь. Для заявленных write сценариев на current source пройдены scan → selection → staged plan → authorized fixture apply/build/check → evidence/verdict. Проверены reload override/disposition и stale verdict после смены AC revision.',
   'Repeat the early read-only CLI/Web path. For claimed write scenarios on current source verify scan, selection, staged plan, authorized fixture apply/build/check and evidence/verdict. Verify override/disposition reload and a stale verdict after an AC revision change.')
ac(23, 2,
   'Подходящий frontend pilot проверяет Design states и incremental FSD, модульный frontend сохраняет структуру. Backend/CLI обходятся без FSD gates; AI quality остаётся eval/gap без скрытого provider call. Дополнительные проверки соответствуют заявленным профилям.',
   'Verify Design states and incremental FSD on a suitable frontend pilot, and preserve existing modular structure. Backend/CLI paths omit FSD gates and AI quality stays eval/gap with no hidden provider call. Apply additional checks for claimed profiles.')
ac(24, 2,
   'По PMETH-22 порогам измерены самостоятельный верный выбор, время до первого проверяемого шага, лишние шаги, отмены и причины, accepted outcomes, defects/reopens, repair effort, owner interventions, elapsed и доступные token/cost. Отсутствующие метрики остаются unavailable.',
   'Use PMETH-22 thresholds to measure independent correct choices, time to first verifiable step, unnecessary steps, cancellations and reasons, accepted outcomes, defects/reopens, repair effort, owner interventions, elapsed and available token/cost. Mark missing measures unavailable.')
ac(25, 1,
   'Owner-reviewed go/bounded_go/hold/no-go называет поддержанные профили, evidence и residual gaps; RU/EN PMETH-26 дополняются для подтверждённых расширений PMETH-23. Ранняя приёмка read-only фиксируется отдельно.',
   'The owner-reviewed go/bounded_go/hold/no-go names supported profiles, evidence and residual gaps. Extend PMETH-26 RU/EN guidance for PMETH-23-confirmed expansions. Record early read-only acceptance separately.')
ac(26, 1,
   'RU/EN показывают проверенный ранний bug/docs CLI+Web путь, входы, основания, scope, source, следующий шаг и ограничения. Примеры подтверждены PMETH-22/19/20.',
   'RU/EN guidance shows the verified early bug/docs CLI+Web path, inputs, reasons, scope, sources, next step and limits. Support examples with PMETH-22/19/20.')
ac(26, 2,
   'Есть short route, различие intended RED и setup failure, понятный partial/unknown и safe next action. Override/apply и Design/FSD помечены как будущие до PMETH-23 и PMETH-25.',
   'Explain the short route, intended RED versus setup failure, partial/unknown and a safe next action. Mark override/apply and Design/FSD as future until PMETH-23 and PMETH-25.')

plugin = 'plugins/product-agent-os/scripts/'
engine = plugin + 'product_agent_os/'
local = 'apps/local-service/src/'
paths = {
    1: [local+'project-analysis/bridge.py', local+'http/application.mts'],
    2: [plugin+'codex_runtime_runner/cli.py', plugin+'run_methodology_audit.py', local+'project-analysis/bridge.py'],
    4: ['packages/contracts/project-analysis.ts', 'packages/contracts/issues/task-profile.ts'],
    5: [engine+'control_plane_documents.py', engine+'project_formation.py'],
    6: [engine+'project_formation.py'],
    7: [engine+'test_strategy_selector.py', 'tests/product_agent_os/test_codex_runtime_runner_cli.py'],
    8: [engine+'methodology_audit.py'],
    11: [local+'code-index/service.mts', local+'code-index/lexical.mts', 'tests/web/graph-imports.test.mts'],
    12: [engine+'project_formation.py'],
    14: [engine+'plugin_components.py'],
    15: [engine+'project_formation.py'],
    16: [engine+'project_formation.py', 'packages/contracts/artifacts/document-apply.ts'],
    17: [engine+'task_routing.py', local+'tasks/user-commands.mts', local+'workflows/guards.mts'],
    18: [local+'project-scans/service.mts', 'packages/contracts/issues/task-profile.ts'],
    19: [local+'project-analysis/bridge.py', local+'project-analysis/service.mts', local+'project-scans/service.mts', 'packages/contracts/project-analysis.ts', 'tests/web/project-analysis-api.test.mts'],
    20: ['apps/web/src/features/projects/project-analysis.css', 'tests/web/project-analysis-api.test.mts'],
    22: ['tests/product_agent_os/test_codex_runtime_runner_cli.py', 'tests/web/project-analysis-api.test.mts'],
}
for n, files in paths.items():
    assert all((root/file).is_file() for file in files), (n, [file for file in files if not (root/file).is_file()])
    tasks[n]['work_locations'] = list(dict.fromkeys(tasks[n]['work_locations'] + files))
for n, refs in {11: [14, 30], 16: [13], 17: [2], 18: [2, 28, 29], 19: [27], 20: [23, 27], 22: [23]}.items():
    tasks[n]['external_refs'] = sorted(set(tasks[n]['external_refs'] + [f'PAOS-FUNC-{i:02}' for i in refs]))
payload['planning_revision'] = {
    'date': '2026-11-18',
    'review': 'research/methodology-plan-review-2026-11-18.md',
    'before': {'edge_count': 54, 'changed_dependencies': previous, 'first_web_transitive_prerequisites': 20},
    'after': {'edge_count': edges, 'first_web_transitive_prerequisites': 8},
    'read_only_milestone': {'required_tasks': sorted(map(tid, early)), 'terminal_task': tid(26), 'scenarios': ['backend_bug', 'docs_only']},
    'responsibility_moves': {
        'PMETH-03/20 persisted override': ['PAOS-PMETH-18-AC02', 'PAOS-PMETH-21-AC03', 'PAOS-PMETH-23-AC01'],
        'PMETH-05 staged requirements and PMETH-19 apply': ['PAOS-PMETH-16-AC01', 'PAOS-PMETH-16-AC02', 'PAOS-PMETH-16-AC03'],
        'PMETH-26 broad documentation': ['PAOS-PMETH-25-AC01'],
    },
}

outcomes = {
    19: ('Read-only task advice через существующий Project Analysis API, CLI parity, partial/last relevant stage и negative receipts.',
         'Read-only task advice through the existing Project Analysis API, CLI parity, partial/last relevant stage and negative receipts.'),
    20: ('Read-only bug/docs flow в Sources и Teams & Tasks, synthetic browser и результат проверки понимания либо явный gap.',
         'Read-only bug/docs flow in Sources and Teams & Tasks, synthetic browser evidence and a comprehension observation or explicit gap.'),
    26: ('Проверенные RU/EN примеры раннего CLI+Web пути в существующей документации.',
         'Verified RU/EN examples of the early CLI+Web path in existing guidance.'),
}

def field(block, name, fn):
    out, count = re.subn(rf'^- {name}: (.+)$', lambda m: f'- {name}: {fn(m[1])}', block, count=1, flags=re.M)
    assert count == 1, name
    return out

def revise(s, lang):
    code = chr(96)
    seq = '01 → 02 → 22 → 03 → 04 → 05 → 07 → 19 → 20 → 26'
    l = ('ru', 'en').index(lang)
    date = ('Дата: 15.11.2026. Schema version:', 'Date: 2026-11-15. Schema version:')[l]
    edited = ('Дата создания: 15.11.2026. Редакция: 18.11.2026. Schema version:', 'Created: 2026-11-15. Revised: 2026-11-18. Schema version:')[l]
    assert date in s
    s = s.replace(date, edited, 1)
    web = ('| Web/local service | Прямой methodology-specific owner в проверенных Web/local-service/contracts keyword scopes не установлен этим чтением | PMETH-01 определяет reuse/bridge/gap; PMETH-18–21 доводят выбранный путь до приложения. Отрицательный keyword search не доказывает полное отсутствие интеграции |',
           '| Web/local service | Inspection did not establish a direct methodology-specific owner in searched Web/local-service/contracts keyword scopes | PMETH-01 establishes reuse/bridge/gaps and PMETH-18–21 connect the chosen path; negative keyword search does not prove complete absence |')[l]
    observed = ('| Web/local service | Project Analysis включает guarded HTTP route, Node service, Python bridge и project scan records. Проекция сейчас ориентирована на проект, task-scoped advice остаётся пробелом | PMETH-19/20 расширяют существующий read-only путь; PMETH-18/21 добавляют сохраняемое решение и recovery при необходимости |',
                '| Web/local service | Project Analysis already has a guarded HTTP route, Node service, Python bridge and project scan records. Current projection is project-level, and task-scoped advice is the gap | PMETH-19/20 extend the existing read-only path; PMETH-18/21 add persisted decisions and recovery where needed |')[l]
    assert web in s
    s = s.replace(web, observed, 1)
    lines = {
        'B1': ('Компактные Spec/TDD для bug/docs; drift и Design подключаются по профилю', 'Compact Spec/TDD for bug/docs; add drift and Design by profile'),
        'B3': ('Выбранный delivery plan, отдельные ветки записи и технических доказательств', 'Selected delivery plan, separate write and technical evidence paths'),
        'B4': ('19/20 дают ранний read-only путь; 18/21 добавляют durable decisions и recovery', '19/20 deliver the early read-only path; 18/21 add durable decisions and recovery'),
        'B5': ('26 завершает ранний путь документацией; 23/24/25 проверяют расширение, пользу и rollout', '26 documents the early path; 23/24/25 verify expansions, measure usefulness and decide rollout'),
    }
    for name, desc in lines.items():
        s, count = re.subn(rf'(?m)^(\| {name}\.[^|]+\|[^|]+\| )([^|]+)( \|)$', lambda m: m[1] + desc[l] + m[3], s, count=1)
        assert count == 1, name
    start = ('Старт: PMETH-01', 'Start PMETH-01')[l]
    intro = (
        f'**Первый принимаемый результат — read-only CLI+Web.** Жёсткие зависимости: PMETH {seq}. В одном disposable проекте backend bug и docs-only дают одинаковые выводы CLI/Web, основание и следующий проверяемый шаг. PMETH-26 закрепляет проверенные RU/EN примеры. '
        'Для приёмки нужны наблюдаемые CLI/HTTP/browser проверки и отрицательные случаи, результат проверки понимания или явный gap. PMETH-06, PMETH-08–18 и PMETH-21/23–25 за пределами prerequisites этапа.\n\n'
        f'**Расширенный путь.** PMETH-15 связывает выбранные slices. PMETH-16 добавляет применение, PMETH-17 — technical evidence, PMETH-18/21 — сохранение решения и восстановление. PMETH-23 проверяет заявленные профили, PMETH-24 оценивает пользу, PMETH-25 принимает решение о расширении. '
        f'Design/FSD gates относятся к соответствующим профилям. JSON содержит {edges} активных рёбер. {code}planning_revision{code} фиксирует исходный граф из 54 рёбер и перенос write/override/документации. Основание — [исследование 18.11.2026](../../research/methodology-plan-review-2026-11-18.md).'
    ) if lang == 'ru' else (
        f'**First accepted outcome: read-only CLI+Web.** Hard prerequisites: PMETH {seq}. In one disposable project, backend bug and docs-only give matching CLI/Web decisions, reasons and the next verifiable step. PMETH-26 captures verified RU/EN examples. '
        'Acceptance requires observed CLI/HTTP/browser checks and negatives, plus a comprehension observation or explicit gap. PMETH-06, PMETH-08–18 and PMETH-21/23–25 are outside this milestone’s prerequisites.\n\n'
        f'**Extended route.** PMETH-15 connects selected slices. PMETH-16 adds apply, PMETH-17 adds technical evidence, and PMETH-18/21 add persisted decisions and recovery. PMETH-23 qualifies claimed profiles, PMETH-24 measures usefulness and PMETH-25 decides expansion. '
        f'Design/FSD gates apply to their corresponding profiles. JSON has {edges} active edges. {code}planning_revision{code} records the initial 54-edge graph and shifts of write, override and documentation responsibility. See the [2026-11-18 review](../../research/methodology-plan-review-2026-11-18.md).'
    )
    s, count = re.subn(rf'(?m)^{re.escape(start)}[^\n]*$', lambda _: intro, s, count=1)
    assert count == 1
    history = [('## Проверка подготовки этой редакции', '## Историческая проверка редакции от 15.11.2026'),
               ('## Verification of this planning revision', '## Historical verification of the 2026-11-15 revision')][l]
    s = s.replace(*history, 1)
    for n, t in tasks.items():
        deps, blocks = (', '.join(t[k]) for k in ('depends_on', 'blocks'))
        none = ('Нет.', 'None.')[l]
        pattern = rf'(?m)^(\| {t["id"]} \|[^\n]*\| )([^|]*)( \|)$'
        s, count = re.subn(pattern, lambda m: m[1] + (deps or '—') + m[3], s, count=1)
        assert count == 1, t['id']
        start = s.index(f'### Task {code}{t["id"]}{code}')
        end = s.find('\n### Task ', start + 1)
        end = len(s) if end == -1 else end
        block = field(s[start:end], 'Depends on', lambda _: deps or none)
        block = field(block, 'Blocks', lambda _: blocks or none)
        if t['external_refs']:
            block = field(block, 'External references', lambda _: ', '.join(t['external_refs']))
        for crit in t['acceptance_criteria']:
            pattern = rf'(?m)^(  - \*\*{crit["id"]}\*\*: ).+$'
            block, count = re.subn(pattern, lambda m: m[1] + crit[lang], block, count=1)
            assert count == 1, crit['id']
        if n in paths:
            extra = (' Модули и проверки для переиспользования: ', ' Modules and checks to reuse: ')[l]
            extra += ', '.join(f'{code}{p}{code}' for p in paths[n]) + '.'
            block = field(block, 'Scope', lambda old: old + extra)
        if n in outcomes:
            for label in ('Expected result', 'Output artifacts'):
                block = field(block, label, lambda _: outcomes[n][l])
        s = s[:start] + block + s[end:]
    return s

updated = {}
for suffix, lang in (('.md', 'ru'), ('.en.md', 'en')):
    f = base.with_suffix(suffix)
    original = f.read_bytes()
    newline = '\r\n' if b'\r\n' in original else '\n'
    updated[f] = revise(original.decode('utf-8').replace('\r\n', '\n'), lang).replace('\n', newline).encode()
updated[source] = updated[mirror] = (json.dumps(payload, indent=2, ensure_ascii=False) + '\n').encode()
for f, output in updated.items():
    f.write_bytes(output)
print(f'B: {len(tasks)} tasks, {sum(len(t["acceptance_criteria"]) for t in tasks.values())} AC, {edges} edges. Web prerequisites: {len(ancestors(20))}. Early milestone: {len(early)} tasks.')
