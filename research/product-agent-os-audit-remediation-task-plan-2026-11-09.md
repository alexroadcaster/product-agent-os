# Product-Agent OS — задачи и группы исправлений по полному аудиту

Source status: project-local planning artifact, 09.11.2026; составлен по сохранённому аудиту и текущим owning plans. Статус документа: `G1/G2/G3/G4/G5 implemented_locally_verified`; G6 — partially_verified: T30–T33 локально выполнены; T34/HOST-01/HOST-02 остаются открытыми; GAP-06: три local pilots passed, needs_user_acceptance, без HOST-01 dependency. Сохранение карточек не означает выполнение, promotion или разрешение на перечисленные внешние действия.

Document ID: `PAOS-AUDIT-REMEDIATION-2026-11-09`. Authoring task: `PAOS-AUDIT-TASK-MATRIX-2026-11-09`. Часовой пояс: `Europe/Moscow`.

## Назначение и источники

В документе **7 групп и 34 карточки**: 18 задач по F01–F18, пять существующих B45-CQRR-T30–T34, три этапа host/usefulness и восемь задач G7 по качеству реализации. Для каждой группы и задачи указаны ID, название, описание, техническое и продуктовое значение, затрагиваемые файлы и критерии приёмки. Поля task_matrix_plan_v1 сохраняют совместимость с существующим validator; русский текст рядом с каноническим именем поля поясняет его назначение. G7 добавлена как planned; открытые gates и статусы G6 сохранены.

- [Полный аудит 09.11.2026](product-agent-os-full-audit-2026-11-09.md): F01–F18 и границы evidence.
- [Последующее исправление lifecycle по чатам](product-agent-os-session-lifecycle-fix-2026-11-09.md): выполненные session isolation и exact marker bootstrap.
- [Ordinary/GAP implementation plan](product-agent-os-ordinary-route-implementation-plan-2026-11-05.md): ORD, GAP-03 M06, GAP-05 и GAP-06.
- [Canonical B45 task group](../docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json): ID, названия, dependencies и acceptance T30–T34.
- [PLAN.md](../PLAN.md), [TEST.md](../TEST.md), [EVALS.md](../EVALS.md), [RUNLOG.md](../RUNLOG.md): текущие owning pointers и обязательные verification routes.

## Что не выполнять повторно

- T23–T29 и ORD-01–ORD-06 уже реализованы локально. Новая задача их переиспользует; обнаруженная регрессия требует конкретного evidence и ограниченного исправления.
- Session-bound markers, host-envelope identity, own/foreign/mixed marker bootstrap и Windows case handling реализованы отдельным lifecycle slice. F06 теперь относится к оставшимся command/patch classification defects; F18 — к новому ограниченному authoring contract.
- Существующий GAP-05 create-only grant не считается сломанным лишь потому, что не умеет Update File; его расширение требует явного нового контракта.
- PAOS-AUD-F01–F18 — ID новых corrective slices, связанные с соответствующим F в аудите 09.11.2026; они не подменяют старые одинаково названные findings других исследований.
- T30–T34 и PAOS-GAP-06 здесь представлены для общего порядка работ. Их source-owned machine status и canonical acceptance остаются в исходных артефактах. PAOS-AUD-HOST-01/02 адресуют оставшиеся verification этапы существующих GAP gates, не создают второй status registry.
- Planned в карточке означает, что описанный остаточный объём не выполнен этим планом; он не отменяет ранее выполненные части parent задачи.

## Матрица групп

| ID | Группа | Карточки | Основной результат |
| --- | --- | --- | --- |
| PAOS-AUD-G1 | Надёжные hooks, rules и установка | PAOS-AUD-F06, PAOS-AUD-F12, PAOS-AUD-F11, PAOS-AUD-F07, PAOS-AUD-F18 | Согласованные active/package contracts, точные границы записи и корректные staging/merge paths. |
| PAOS-AUD-G2 | Совместимость package и диагностика host | PAOS-AUD-F01, PAOS-AUD-F02, PAOS-AUD-F04 | Один источник диагностики package schema и surface capabilities без нового doctor framework. |
| PAOS-AUD-G3 | Достоверные evidence и текущие статусы | PAOS-AUD-F03, PAOS-AUD-F08, PAOS-AUD-F16 | Устранение ложноположительных и ложных missing-сигналов без нового status registry. |
| PAOS-AUD-G4 | Простой ordinary route и компактные инструкции | PAOS-AUD-F05, PAOS-AUD-F09, PAOS-AUD-F10, PAOS-AUD-F15 | Минимальный task context, совместимость callers, меньшая нагрузка инструкций и повторных scans. |
| PAOS-AUD-G5 | Документация, offline tooling и актуальный site | PAOS-AUD-F13, PAOS-AUD-F14, PAOS-AUD-F17 | Воспроизводимый offline command contract и согласованный source/build output. |
| PAOS-AUD-G6 | Проверка GPT-6, host activation и пользовательской пользы | B45-CQRR-T30, B45-CQRR-T31, B45-CQRR-T32, B45-CQRR-T33, B45-CQRR-T34, PAOS-AUD-HOST-01, PAOS-AUD-HOST-02, PAOS-GAP-06 | Раздельные воспроизводимые evidence для конфигурации, активации, качества и acceptance. |
| PAOS-AUD-G7 | Качество реализации, архитектурная простота и достаточная проверка | PAOS-AUD-G7-T01–T08 | Минимальное полное решение, risk-based checks, доказательный review, безопасные guards и отдельная сравнительная оценка. |

## Порядок, зависимости и ускорение

G7 — планируемое продолжение по анализу Ponytail и аналогов. Его локальные задачи не зависят от завершения G6 целиком; T34, HOST-01/HOST-02 и owner acceptance сохраняют свои gates. Порядок G7: T01 → T02/T03/T05/T06 → T07 → T08; T04 — независимый ранний fix.

1. G1 и G2 — первые local corrective slices. G3 можно вести независимо по core files; shared control-plane обновляется последовательно.
2. В G1 не объединять все guard changes в один неразличимый diff: F06 → F18; generated hooks F12 проверяется на согласованном контракте. F07 и F11 независимы и не требуют настоящих ACL/rules activation для code-level проверки.
3. В G2 F01 и F02 можно подготовить независимо; F04 использует оба результата. Отдельный doctor framework не создаётся.
4. G4: F10 → F09; intake F05 можно вести независимо, incremental report scenario требует F18; измерения F15 допустимы раньше, правка — только при подтверждённой пользе. Не смешивать skill shortening, model switch и compact-contract intervention в одном eval treatment.
5. T30 и T31 можно готовить до завершения local fixes по независимым файлам. Canonical dependency graph: T29 → T30; T27/T29 → T31; T25/T30/T31 → T32; T24/T28/T29/T30/T31/T32 → T33; T33 → T34. G4 freeze — дополнительное условие воспроизводимости выбранного окружения, не скрытая правка canonical B45 dependencies.
6. Документация следует за поведением в каждом slice. Финальный local site build G5 после стабилизации G1–G4; новые host/eval receipts затем добавляются малой адресной синхронизацией.
7. AUD-HOST-01 после финального package/skills; AUD-HOST-02 после финальных hooks/definitions. Изменившийся source/hash вновь открывает относящийся к нему activation gate.
8. GAP-06 начинается с одного pilot в рамках ранее запланированного набора 3–5 задач. Один удачный кейс не закрывает весь набор; T34 не является обязательным условием обычной проверки полезности.

Возможность независимой работы означает допустимое разделение ownership, а не запуск subagents по этому документу. Минимальный состав — один исполнитель. При будущей разрешённой параллельной работе разные владельцы не редактируют один файл одновременно; hooks/lifecycle tests, compatibility module, canonical skills, README и root pointers имеют одного writer на текущий slice.

## Общие границы реализации и проверки

- Все пути ниже workspace-relative. Существующие paths проверены при authoring. Отсутствующие файлы T30–T34 явно помечены `proposed new` и пока не создаются. Directory scope требует точного file manifest до начала соответствующего slice.
- Scope каждой будущей реализации — названные файлы и относящиеся к ней tests. При изменении source-backed claims синхронизируются затронутые RU/EN пары и оба registry. Общие PLAN/TEST/EVALS/REQUIREMENTS/RUNLOG pointers меняет один writer только по применимому control-plane-sync trigger; старый исторический ledger не переписывается.
- Новые behavior/bug fixes: observable RED → минимальный GREEN → scoped refactor. Behavior-neutral документация и форматирование — static checks. Relevant regression, fixture/transcript и compatibility gates выбираются по TEST.md; не повторять неизменные проверки без причины.
- Локальные contract tests, schema validation и generated artifact не доказывают actual host loading, trust, model selection или product acceptance. Для таких claims нужны отдельные receipts выбранного проверенного состояния.
- Указанные роли — будущая ownership recommendation. Они не означают запущенных subagents. Skill выбирать по конкретному подэтапу; canonical Product-Agent OS skills брать из repository, не смешивать с installed cache.
- Исходный authoring запрос разрешал сохранить план, но не выполнять его implementation, provider/model/reviewer calls, cache/global edits, target apply, ACL/trust/rules activation, browser/server, Git или publication. Запросы 09.11.2026 разрешили локальную реализацию G1, G2, G3 и G4; для остальных групп требуется соответствующий implementation request; конкретные внешние границы сохраняются.
- Rollback будущего slice: отменить только его собственные изменения относительно снятого baseline, сохранив чужие hunks и историческое evidence. Для ACL/target/trust заранее нужен отдельный rollback route.
- Оценки длительности не зафиксированы: нет достаточного measured baseline. Не подменять расписание выдуманными сроками; после первого slice оценить фактический объём.

## Проверка этого документа

Authoring не меняет реализацию. Текущие результаты validator, docs checks и scope review записываются ниже после фактического запуска; будущие проверки в карточках — критерии, а не уже полученное evidence.

Verification status: `plan_static_verified`; только качество и полнота документа, не реализация карточек.

| Выполненная проверка 09.11.2026 | Результат |
| --- | --- |
| `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-audit-remediation-task-plan-2026-11-09.md` | Exit 0; ok=true; errors=[]; task_matrix_plan_v1. После уточнения dependencies финальный текст также проверен той же validate_task_matrix_text в memory-only checker: errors=[] |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q` | Exit 0; 100 tests, 3.476 s, OK. Последующие правки затрагивают только этот research plan, не implementation/docs fixtures |
| `python -B tools/check_docs.py` | Exit 0; OK: documentation structure checks passed |
| `git diff --check` | Exit 0. Новый untracked Markdown дополнительно проверен на trailing whitespace напрямую |
| Memory-only Python integrity checker через `python -B -` | Exit 0: 6 групп, 26 уникальных карточек, F01–F18 полностью покрыты, семь запрошенных полей присутствуют, все task statuses planned, exact T30–T34 titles сохранены, existing/proposed paths и relative links валидны, UTF-8 без replacement characters |
| `git diff --name-only` и `git ls-files --others --exclude-standard` | Существующие tracked файлы не изменены; добавлены только этот Markdown и собственный session marker authoring задачи |

Self-review: новые corrective slices отделены от уже выполненных session isolation/ORD/T23–T29; existing T30–T34 и GAP-06 не получили второй machine status. Убраны искусственные hard dependencies: generated path F12 и intake F05 можно исправлять независимо, общие host/authoring gates остаются для соответствующих сценариев. Внешние действия и новые файлы помечены явно. Independent reviewer не запускался.

Граница доказательства: не запускались implementation задач, full runtime suite, fresh host, live model/reviewer, browser, site build или публикация. В этом authoring они не нужны; все будущие acceptance gates остаются открытыми.

## Control-plane sync для сохранения плана

- REQUIREMENTS.md, TEST.md, EVALS.md, prod_test.md: not_applicable — продуктовые требования, обязательные gates, thresholds и историческое evidence этим authoring не изменяются.
- PLAN.md и RUNLOG.md: handoff_required — компактная ссылка на этот отдельный план и выбор первого execution slice нужны при запуске реализации; текущая authority ограничена новым файлом и служебным marker.
- Registry RU/EN: not_applicable для этого research plan — новые official behavior claims не добавляются; источник findings остаётся аудит. Обновления registry включены в соответствующие будущие slices.
- Site/navigation/diagrams: not_applicable для authoring; план не включён в site и не содержит claim о свежей сборке.
- Overflow/refactor: not_applicable. Исторические артефакты, machine status и прочие файлы сохранены.

## PAOS-AUD-G4 — execution evidence 09.11.2026

Status: `implemented_locally_verified`; F05/F09/F10/F15. Можно переходить к G5. Start: 11:30:07 UTC после preflight. Один исполнитель, zero delegation, self_review. Baseline git status: только собственный lifecycle marker dirty; G1–G3 и параллельная Web-документация уже находились в текущем checkout. История не менялась.

### Scope и решения

- F05: existing `task_routing.py` общий adapter `--task`, `--change-mode`, repeated `--changed-path` / `--acceptance`, optional `--task-id`, `--risk-level`. Missing risk=unknown; поведенческие invariants/checks/state остаются в rich `--task-context`. Partial/mixed/unsafe input rejected без fallback. Оба public callers: `codex_runtime_runner/cli.py`, `render_infrastructure.py`; explicit/legacy receipt также в `infrastructure.py`. Legacy default сохранён решением compatibility: автоматическое угадывание task scope из prompt не заменяет checked contract. Existing selectors/state/routes/templates не переписаны. Пустой ordinary stage создаёт manifest directory после gates; target не меняется.
- F10/F09 manifest: все 12 canonical `plugins/product-agent-os/skills/*/SKILL.md`; существующие `references/complexity-routing.md`, `references/source-policy.md`, `references/handoff-contract.md`; `tests/AGENTS.md`; профильные `test_lifecycle_skills.py`, `test_validators.py`; связанный contract consumer `test_infrastructure_templates.py`. Фактически test_validators.py не менялся, его checks переиспользованы. `agent-team-designer` пишет только явно порученные local team/handoff artifacts; dispatch/config activation не разрешены. Completion skeptic и прочие assurance roles read-only. Instruction precedence отделена от factual authority. Relevant unchanged evidence можно переиспользовать с исходной provenance.
- F09: 93 conditional domain sections перенесены без смысловых правок в role-specific sections существующего complexity reference. Entry points содержат triggers, authority, inputs/outputs, stop/verification и индекс applicability. Mixed work читает все затронутые subsections; unknown требует inspection. Role-specific contract reader в `validators.py` и его callers в `test_lifecycle_skills.py` / `run_fixture_eval.py` проверяют сохранённые gates, не загружают skills в host. Metadata всех 12 skills byte-identical; implicit invocation/cache не менялись. Новых refs/framework нет.
- F15: только `discovery.py` извлекает чистый scope detector и переиспользует frozenset текущего inventory внутри одного вызова. Публичный scope API по-прежнему сканирует свежие данные. Methodology/first-run inventories имеют другие exclusions; их не объединяли. Нового cross-call cache, БД или module framework нет.
- Tests: `test_codex_runtime_runner_cli.py`, `test_methodology_audit.py`, `test_lifecycle_skills.py`; existing renderer/state/validator tests. Read-only fixture work и ignored measurements под `.docs-tools/reports/paos-aud-g4/`; TEMP/TMP под `tmp` и `eval-tmp`, Python -B/PYTHONDONTWRITEBYTECODE=1.

### Проверки и failed attempts

| Command / check | Observed result |
| --- | --- |
| Three new intake tests | RED exit 1: 3 tests, 4 errors; flags/helper/fallback receipt отсутствовали |
| `python -B -m unittest tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_infrastructure_renderer -v` | Первый GREEN attempt: 77 tests, 2 errors; empty ordinary stage не создавал manifest directory. Исправлено и включено в passing combined run |
| `test_discovery_reuses_inventory_for_scope_without_stale_cross_call_cache` | RED exit 1: scan count 2 != 1; затем GREEN в combined run, включая fresh second call after filesystem change |
| Runtime modules выше плюс `tests.product_agent_os.test_methodology_audit` | Exit 0: 134 tests, 28.223 s (`runtime-green.log`) |
| Conditional role-section reader | RED import error; первая implementation выявила CRLF regex mismatch. Normalization исправлена; final role isolation/missing section checks pass |
| `python -B -m unittest tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_validators -v` | Exit 0: 95 tests, 2.498 s (`skills-final.log`) |
| `skill-creator/scripts/quick_validate.py` validate_skill on each canonical skill, PYTHONUTF8=1 | 12/12 valid, exit 0; metadata unchanged |
| `measure_scans.py baseline/after` | Первый measurement attempt: sandbox TEMP PermissionError (setup failure). Повтор с workspace TEMP: exit 0; baseline до discovery change сохранён. Five-run timings и exact outputs в JSON |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` | Attempt 1 exit 1: typo в readiness reader, исправлен. Attempt 2 exit 1: 82/91 из-за оставшихся f-string readers; подключены к role-specific reader, assertions сохранены. Final exit 0: 91/91 (`fixtures-verified.log`) |
| `python -B -m unittest discover -s tests -p "test_*.py" -v` | Initial exit 1: 1326 tests, 469.721 s, failures=9, skipped=1; старые fixture readers и один template test consumer. Исправлены до final. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0 (`full-final.log`) |
| `python -B -m unittest tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_infrastructure_renderer tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_validators tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0: 253 tests, 34.476 s (`final-focused.log`), включает docs и empty explicit task-context regression |
| `python -B -m unittest tests.product_agent_os.test_infrastructure_templates -v` | Exit 0: 95 tests, 1.399 s; backend assertions сохранены, reader следует relocation |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py`; `validate_codex_compatibility.py` | Каждый exit 0; transcripts 26/26; compatibility local structure only, host not_verified |
| `validate_agents.py .codex/agents`; `validate_hooks.py .codex/hooks.json`; `validate_hooks.py plugins/product-agent-os/assets/templates/hooks` | Каждый exit 0; 15 active agents, errors/config_errors=[]; hooks errors=[]; activation не выполнялась |
| `python -B tools/check_docs.py`; `validate_task_state_consistency.py`; `validate_task_matrix.py` с этим plan | Exit 0; structure passed; validators ok=true/errors=[] |
| `git diff --check` | Initial: один trailing blank line в complexity reference; удалён. Final exit 0 |
| Self-review empty explicit file argument | RED exit 1: `--task-context ""` ошибочно выбирал legacy. Проверка None вместо truthiness исправляет отказ; final focused passed |

### Измерения и claim ceiling

Fixed synthetic workspace: 304 files, 300 source files в 10 directories; один environment, пять discovery samples. Calls `_relative_files`: 2 → 1. Median discovery: 114.448 ms → 103.959 ms (~9.2% в этом локальном fixture). Полный discovery output до/после equal. Методологический scan отдельно сохранён; это не обещание универсального ускорения.

На том же fixture legacy renderer предлагает 209 artifacts, explicit ordinary — 0, questions=[] в обоих. Timing diagnostic: legacy 593.0/588.5 ms до/после; ordinary 127.6/118.3 ms. Снижение questions не заявляется, baseline уже нулевой. CLI-to-stage RU/EN/no-builder test не создаёт task.json и сохраняет target bytes.

93 moved section bodies сравнены с baseline; все совпали. Entrypoint raw UTF-8 bytes: 292137 → 194355. Ниже реально прочитанные deterministic measurement read sets: SKILL.md + указанные shared refs + selected conditional subsection bodies. Это source-loading simulation, не fresh-host/model token/latency/quality evidence.

| Read set | Before bytes | After bytes | Reduction |
| --- | --- | --- | --- |
| ordinary-doc-plan: implementation-planner + Docs Tooling Selector + source-policy | 42401 | 29541 | 30.33% |
| backend-review: risk-reviewer + Backend + Quality Testing/Evals + source-policy | 34927 | 24137 | 30.89% |
| security-ai-review: risk-reviewer + Security + LLM/AI/RAG + Quality + source-policy | 34927 | 25458 | 27.11% |
| team-handoff: agent-team-designer + Codex Agentic Workflow + source-policy + handoff-contract | 26947 | 26863 | 0.31% |

No claim that every skill or path shrinks equally. All-domain reads can cost more due to the index; applicability remains the selector. Local typical/edge/adversarial contract comparisons preserve role ownership, missing evidence, approvals, unsafe paths and conditional domain gates. Live behavioral comparison/fresh-session discovery belongs to G6, not this source-level check. Model/effort and B45 treatment не менялись.

Rollback: только G4 hunks. Snapshot baseline и file hashes в ignored reports. B42/B45 source JSON, G1–G3, installed cache, global instructions, trust, hooks/rules и Git history не меняются.


### Closure, sync и provenance

Final closure checks после записи статусов: docs unittest exit 0, 100 tests, 3.511 s (`docs-final.log`); check_docs, task matrix, task-state consistency и git diff --check — каждый exit 0. Source/test hashes совпадают с verified manifest; current projection содержит 43 tasks без issues.

Self-review: context_mode=self_review; tester_verdict=closed_allowed для local scope. Проверены public caller compatibility, fail-closed intake, source/read-only boundaries, unchanged metadata, role-scoped references и snapshot lifetime. Blocking findings исправлены. Source bodies 93/93 preserved; текущая projection обновляется после owning-plan write.

Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG updated; CLI/architecture/current-state RU/EN и registry RU/EN updated. prod_test.md not_applicable (Batch 39 не затронут); handoffs none; overflow not_required (<50 KiB roots). Strict MkDocs not_applicable: nav/Mermaid/extensions/site не менялись. Generated site freshness не заявляется.

Measured interval 11:30:07–11:58:37 UTC: 28 мин 30 с; preflight и final evidence checks после checkpoint не включены. Model/reasoning inherited, subagents=0; token/tool telemetry unavailable. Skills: skill-creator прочитан; Python advisory skills ранее прочитаны.

SHA-256 проверенного source/test manifest (raw bytes); source bodies и metadata имеют отдельное baseline сравнение:

| Path | SHA-256 |
| --- | --- |
| `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py` | `a7ce19682281a554894d8c15d45dbb8d1cdf6cb7cb86019d387797e771c382e2` |
| `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | `38311ab28a2b80f9fd61f73c6b39c9b38bae1e139c5e32044e5260aec16aa6e8` |
| `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py` | `b9c8c4a211c5c042148ec9fd0034943b67d577498b8b346bcc51c646b8a58326` |
| `plugins/product-agent-os/scripts/product_agent_os/task_routing.py` | `bcf5740677a3651558643f8d259b744faff0fd916c5090d622de5328e439e097` |
| `plugins/product-agent-os/scripts/product_agent_os/validators.py` | `9fa8cf833a99f1188d00b24b18a5cdf18fdf305627501f145d109e7a3e888deb` |
| `plugins/product-agent-os/scripts/render_infrastructure.py` | `7238888560086dcf97bbcfb0000b2c6a469366bb2d969de33dd57603dc6687a5` |
| `plugins/product-agent-os/scripts/run_fixture_eval.py` | `34216b5ddc01dd64abf2c2e29e53c0671c812d9064b95552276f42658eff0bc2` |
| `plugins/product-agent-os/skills/agent-team-designer/SKILL.md` | `8767197ce0ef37475a24dfc9daa5614ba259ce4dd9fd4437389242342031658e` |
| `plugins/product-agent-os/skills/automation-promoter/SKILL.md` | `01911c2074257c5318dee54fb3b914cf30281f97cbab4fdc257106fdf5393838` |
| `plugins/product-agent-os/skills/completion-skeptic/SKILL.md` | `3f88af990e13b8cb51c2cf320579fdca550b321fbc153ae195b7bee38711f9c8` |
| `plugins/product-agent-os/skills/docs-maintainer/SKILL.md` | `7871f1d7a1df5f794cace515248b82973d7410834cd70f62cbf6c3c2ba91f1fa` |
| `plugins/product-agent-os/skills/implementation-planner/SKILL.md` | `e6e846e712e9988f6dccb8336e2580ef760fa83225c01edcb5a2b4ab2832c151` |
| `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md` | `d132400fd3ee5117a43dc885c82a63929ed2da196c714c30ec3f78bde12ffd98` |
| `plugins/product-agent-os/skills/pr-release-operator/SKILL.md` | `538eee5bffbdaa07e57dbea8ee69c9dd6f740a0568559900ad747de034cafc27` |
| `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md` | `de0ddc5ac698a5f23e1dcf86c8f7d68d6a649054405129bca97209561f2cf7e8` |
| `plugins/product-agent-os/skills/references/complexity-routing.md` | `cb8fe7a0fd0435385726f19727d2650c79e56a05de0a3d4202b024fc43fa0cb2` |
| `plugins/product-agent-os/skills/references/handoff-contract.md` | `fa7529e299eea52b329d0cfec64810ce8642a92e5a00889b50210d740d9fffe6` |
| `plugins/product-agent-os/skills/references/lifecycle-states.md` | `649cb4d7ba706ee6c7fe88a2cd8640daab5c011c51c04a92d0097c70cfa21cd8` |
| `plugins/product-agent-os/skills/references/source-policy.md` | `c31766c27ba09fa0a2ad7ce1798482177be9e5d22d93bea075f7fd45f85b8e35` |
| `plugins/product-agent-os/skills/requirements-author/SKILL.md` | `50c13a4f52ed81f0d6bfa459620b48f13619312827c92c3f35c5bb45bf1b1e82` |
| `plugins/product-agent-os/skills/risk-reviewer/SKILL.md` | `6a3e6d8ff4f5c6796a154d842e3632a3efcb553e0432cfdd0207ec03487f902b` |
| `plugins/product-agent-os/skills/test-eval-designer/SKILL.md` | `0d969a53d66e33fe14fab1501896ec7f33299b2bf405ead63018a513c6c6df19` |
| `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md` | `cca08a7300df6c2a1fc6d55513dda1ffeb2e21c0fd6d0319a8f90a59713b5187` |
| `tests/AGENTS.md` | `305aced71d08747c36eeb0c0fe8659e349d2fb19e60c6b538b785c9512a01005` |
| `tests/product_agent_os/test_codex_runtime_runner_cli.py` | `0ae558423c1b4e90b49c80bed04120d24617a1ecc60e984f80dd505bd5351177` |
| `tests/product_agent_os/test_infrastructure_templates.py` | `b3441d7c35b1ef187100f43af1de1c2ae15371d3bea13c5a2d242a957bb87879` |
| `tests/product_agent_os/test_lifecycle_skills.py` | `ee777fbf3a7dcec93e1427d6a3d8e704ae551c2fccc3f1c743619d45b68ed6cd` |
| `tests/product_agent_os/test_methodology_audit.py` | `b11b58305b1f411e1434f5a3237a475963e7918f84271b4e51d894d450e8caa4` |

## PAOS-AUD-G3 — execution evidence 09.11.2026

Status: `implemented_locally_verified`; F03/F08/F16. Start: 10:19:14 UTC (после preflight). Готов переход к G4.
Один исполнитель, self_review, zero delegation; Python advisory skills ранее прочитаны.
Scope: три owning modules и профильные tests; связанный read-only caller `render_status_dashboard.py` и UTC timestamps двух synthetic predicates в `run_fixture_eval.py`; current-state и self-learning docs RU/EN; registry RU/EN; пять root control-plane files и этот план. Baseline — dirty G1/G2 плюс параллельная Web-документация. Чужие изменения сохранены. Git/provider/host/cache/permission mutations не разрешены.

### Исправления и критерии

- F03: ISO и DD.MM.YYYY после RU/EN labels; строгая calendar validation; missing/invalid/future/stale/date_present_not_verified. Undated source prose не является датой. Несколько дат используют наиболее раннюю, future/invalid не скрываются. Registry resolution — один локальный hop внутри workspace только в canonical registry RU/EN, bounded read, exact heading/table-ID anchor; broken/unsafe refs видны. Claim classes эвристические; project/historical/mention не равны official behavior, claim_supported всегда not_verified. Exact-host URL и secret checks сохранены.
- F08: zero owner labels → insufficient_evidence; owner_sentiment и owner_label_counts отдельно от denominator/coverage и record validity. Negative labels могут быть owner_label_supported, но не positive sentiment. Missing/empty/wholly rejected public summary сохраняет эту семантику. Invalid JSON types в ledger отклоняются без traceback и без копирования rejected payload. Manual-only/candidate-only неизменны.
- F16: один PLAN current pointer содержит только owning paths и SHA-256 revisions. B42/B45 machine JSON сохраняются. Newer dated execution_evidence outranks historical status; equal-date contradictions и duplicate ownership → conflict; invalid/future/unknown/stale revision → unknown. Task/run/verification/acceptance раздельны; prose acceptance criteria не превращаются в acceptance. Markdown task matrices и existing JSON task groups поддерживаются bounded resolver. Existing dashboard CLI wired к workspace pointer; no-pointer B37 deferred route сохранён. Недатированное/naive/future verification evidence не считается current.

### RED/GREEN и текущие gates

Логи: ignored `.docs-tools/reports/paos-aud-g3/`; TEMP/TMP внутри `tmp`, Python `-B`, PYTHONDONTWRITEBYTECODE=1. Все fixtures synthetic; не actual host acceptance.

| Command / check | Result |
| --- | --- |
| `python -B -m unittest tests.product_agent_os.test_source_policy tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_self_learning_extensions -v` | RED exit 1: 46 tests, failures=4/errors=2. GREEN exit 0: 46 tests, 3.997 s |
| `python -B -m unittest tests.product_agent_os.test_status_snapshot -v` | RED exit 1: 14 tests, failure=1/errors=4. GREEN exit 0: 14 tests, 0.060 s |
| `test_source_policy.SourcePolicyTest.test_russian_dotted_dates_and_undated_source_prose` | RED exit 1: invalid вместо date_present_not_verified; затем включён в passing focused suite |
| `python -B -m unittest tests.product_agent_os.test_source_policy tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_self_learning_extensions tests.product_agent_os.test_status_snapshot tests.product_agent_os.test_status_dashboard -v` | Exit 0; 75 tests, 7.362 s (`focused.log`) |
| Final status integration module | Exit 0; 16 tests, 0.141 s (`status-integration.log`); actual `_snapshot_for_workspace` wiring и byte-for-byte synthetic workspace preservation |
| `python -B -m unittest discover -s tests -v` | Exit 0; 1320 tests, 725.771 s, OK (skipped=1); `full.log`. Запущен до последней ownership/UTC правки; final focused и final fixture отдельно проверяют эти изменения |
| Final five-module focused command выше | Exit 0; 78 tests, 6.538 s (`final-focused.log`); scope-prefix ownership regression включена |
| `test_pointer_scope_preserves_canonical_owner_over_planning_cross_reference` | RED exit 1, затем GREEN в final focused; PAOS-AUD-* scope исключает B45 cross-reference cards, не реальные конфликты |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` | Первый exit 1: 90/91; два stale predicates имели naive timestamps. Сохранены assertions, синтетическим датам указан UTC. Повторный `fixtures-final.log`: 91/91 ok=true, JSON результат проверен отдельным assert (exit 0); исходный CLI exit повторного запуска не сохранён после compaction |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` | Exit 0; 26/26 (`transcripts.log`) |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | Exit 0; local_structure_only_not_host_or_distribution_readiness (`compatibility.json`) |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0; 100 tests, 3.890 s (`docs.log`); closure rerun recorded below |
| `python -B tools/check_docs.py`; `validate_task_state_consistency.py`; hooks validators `.codex/hooks.json`, `.codex/hooks`; `git diff --check` | Exit 0; source state errors=[]; hook errors=[]; финальный closure check ниже |

### Scan delta на одном наборе 310 docs до documentation sync

`validate_source_policy('.', as_of=date(2026,11,9))` read-only baseline: needs_review; 188 registry review rows, 151 missing official hints, 310 missing dates, zero secrets. После parser fix: needs_review; 133 review rows, 89 missing official hints, 281 missing + 29 date_present_not_verified, zero secrets. Убраны 55 review rows, новых нет. Examples: project architecture/first-run/evidence-boundary diagrams перестали требовать official behavior evidence только за project contract. 29 распознанных дат не означают semantic verification. Оставшиеся 133 findings — реальная очередь ручного разбора, а не автоматически подтверждённые defects; G3 не исправляет массово source claims. JSON baseline/after сохраняют file-level provenance; документационная синхронизация после сравнения записывается отдельно.

Self-review: context_mode=self_review; tester_verdict=closed_allowed для локального scope. Проверены unsafe paths, bounded reads, stale revisions без fallback, conflicting ownership, отсутствие labels, RU/EN parity и сохранность истории. Нет открытого blocking finding. Rollback: только G3 hunks; сохранить B42/B45 bytes, G1/G2 и Web work. Source-state pointer invalidation требует повторного review и pin, не auto-refresh. Semantic source verification, fresh host и promotion остаются вне локального claim ceiling. Strict MkDocs not_applicable: навигация, Mermaid, extensions и site не меняются.


### Финальная сверка G3

- Final source scan после docs sync: 310 docs, needs_review, 133 review rows, 281 missing dates + 29 date_present_not_verified, zero secrets. Matched baseline delta выше не объявляется semantic audit.
- Current pointer: 43 tasks, 3 revision-pinned sources, no ownership conflicts; audit source scope PAOS-AUD-*. B42/B45 bytes сверяются с pre-slice SHA-256; T23–T29 сохранены.
- Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG updated по соответствующим scope/sequence/checks/evals/handoff triggers; registry и current-state/self-learning RU/EN updated. prod_test.md not_applicable (Batch 39 не затронут); handoffs none; overflow not_required, root budget 50 KiB. Strict MkDocs not_applicable: nav/Mermaid/extensions/site не менялись.
- Model/reasoning inherited; provider/token/tool-count telemetry unavailable. Subagents=0; один восстановленный compacted handoff в G3. Local tests не доказывают fresh-host loading или product acceptance.


### Closure checks и provenance

Final closure docs: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` — exit 0, 100 tests, 4.065 s (`docs-final.log`). `python -B tools/check_docs.py`, `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-audit-remediation-task-plan-2026-11-09.md`, `python -B plugins/product-agent-os/scripts/validate_task_state_consistency.py` и `git diff --check` — exit 0; validators errors=[]. Revision projection after closure: 43 tasks, 3 sources, issues=[]; F03/F08/F16 implemented, B45-T30 planned, B42-S2-M04 implemented from newer receipt. Root UTF-8 budgets <50 KiB; largest REQUIREMENTS.md 48010 bytes.

Measured interval: 10:19:14–10:47:28 UTC, 28 мин 14 с; preflight до start и заключительная запись evidence после checkpoint не включены. Final source scan unchanged: 133 review rows; семантический разбор остаётся отдельной работой.

SHA-256 связывает code/tests с проверенным local состоянием. Full suite начал импорт до последнего scope-prefix test и UTC fixture correction; final focused/fixture покрывают эти дельты. Source revision owning plan закрепляется в PLAN.md после записи этого evidence.

| File | SHA-256 |
| --- | --- |
| `plugins/product-agent-os/scripts/product_agent_os/source_policy.py` | `6ba02af321a592cc59666179b9b9111bed660a4a2be24b48dca1f41c7e68dd00` |
| `plugins/product-agent-os/scripts/product_agent_os/self_learning_feedback.py` | `1f0936316930475379341e635da9608cfa623c46d62559257095b3631386bcf5` |
| `plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py` | `0a3ea0049ab34e50f4599d57908694e8731925d173503ee34a09b2a82c772a11` |
| `plugins/product-agent-os/scripts/render_status_dashboard.py` | `5cbd426fec36ae49f15430e5392b4e2f0f439df50e123c0c72ad73901cf84304` |
| `plugins/product-agent-os/scripts/run_fixture_eval.py` | `8e74c99346c320ad9335dad105a54b77eeb22abb0bdbaa12be7d41db3432f489` |
| `tests/product_agent_os/test_source_policy.py` | `faa97e18c29445f1b6f74f6d30f62c994ce36a979dd35c28c0bc4dc37f6df5a4` |
| `tests/product_agent_os/test_self_learning_state.py` | `237667633f7b2b9038e64237010b8c900dc3cae3abc7475c6b0ddfb0777f4cbc` |
| `tests/product_agent_os/test_self_learning_extensions.py` | `84f37167864361a00c7eeb7a881ea655362dc608884c6abe5992596f19776580` |
| `tests/product_agent_os/test_status_snapshot.py` | `35bb009f88f26a875c0f3d1e78379906de42dc61458bc0807d30db87ac1943ce` |

## PAOS-AUD-G2 — execution evidence 09.11.2026

Status: `implemented_locally_verified`; F01/F02/F04 closed for local scope. Готов переход к G3. Один исполнитель, zero delegation, self_review.
Измеряемый интервал: 09:57:07–10:17:15 UTC, 20 мин 8 с. До него выполнены preflight и официальный source check; время этих действий в интервал не входит. Model/reasoning наследуются; provider/token/tool-count telemetry недоступна. Subagents=0; один восстановленный compacted handoff; Python skills ранее прочитаны, OpenAI Docs прочитан для G2.
Baseline: dirty G1 implementation и параллельные Web-документы сохранены. Scope — файлы карточек, связанные `test_plugin_structure.py`, README, compatibility RU/EN, models RU/EN, registry RU/EN и root control-plane. Новый framework, model migration и изменение T23–T29 не выполняются.

### Реализация и source decisions

- F01: существующий Codex compatibility manifest сохранён; `.mcp.json` использует `mcpServers`. TOML-only startup timeout не переносится в bounded plugin JSON subset. Duplicate keys, transport mixtures и unknown options требуют review; portable root/inline OpenAI precedence не меняется. Контакты/URLs с неподтверждённым владельцем удалены. Required author/developerName содержат явный `Unverified local publisher` sentinel. Publisher, listing URLs, distribution icons и release review остаются gated; это не полный submission validator.
- F02: support и observation разделены. Native plugin documented в App/CLI, unsupported в IDE; standalone skills documented отдельно. Caller observation для unsupported вызывает conflict, а не promotion. Unknown surface не наследует CLI/App support.
- F04: read-only diagnostics принимает до 16 KiB JSON с allowlisted non-secret полями; duplicate/malformed input отклоняется, значения вне allowlist не печатаются. Surface/version, configured/observed model, trust и account access разделены. Только Terra/CLI имеет documented minimum 0.159.0. Optional explicit cache directory сравнивается по manifests/MCP/SKILL.md; это bounded component provenance, не полный package/runtime digest. Cache writes, provider calls, subprocess host discovery, model/effort changes отсутствуют.
- Primary sources fetched 09.11.2026: [Build plugins](https://developers.openai.com/plugins/build/plugins), [submission metadata](https://developers.openai.com/plugins/deploy/submission), [plugin surfaces](https://learn.chatgpt.com/docs/plugins#use-plugins-from-a-supported-surface), [standalone skills](https://learn.chatgpt.com/docs/build-skills), [models](https://learn.chatgpt.com/docs/models). Sources/claims indexed in both registries. Historical model catalog facts dated 03.11.2026 не объявляются заново проверенными.

### Проверки текущего запуска

Логи: ignored `.docs-tools/reports/paos-aud-g2/`. TEMP/TMP направлены в ignored `tmp`/`eval-tmp`; `PYTHONDONTWRITEBYTECODE=1`, Python `-B`. Это локальные synthetic/deterministic checks, не host receipts.

| Command / check | Observed result |
| --- | --- |
| `python -B -m unittest tests.product_agent_os.test_codex_compatibility -v` до implementation | RED: 11 tests; failures=2, errors=9. Package needs_review вместо compatible; смешанный transport ошибочно accepted; новый observations/cache API отсутствует. Shell wrapper вернул 0 после Get-Content, поэтому этот exit не является успехом unittest. `red.log` сохраняет FAILED |
| Та же focused command после implementation | Exit 0; 11 tests, 1.438 s, OK (`green.log`) |
| `python -B -m unittest tests.product_agent_os.test_codex_compatibility tests.product_agent_os.test_plugin_structure -v` | Exit 0; 21 tests, 1.839 s, OK (`focused.log`) |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` | Exit 0; 26/26, failed=0 (`transcripts.log`) |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | Exit 0; compatible, local_structure_only_not_host_or_distribution_readiness; distribution gated; surface unknown, model not_verified, trust unknown, cache_not_provided (`compatibility.json`) |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` | Exit 0; 91 fixtures (`fixtures.log`) |
| `python -B -m unittest tests.product_agent_os.test_codex_compatibility.CodexCompatibilityTest.test_cache_junction_is_not_followed -v` | RED exit 1; observed вместо needs_review. После Windows junction guard входит в passing final suites |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Первый запуск exit 1, 100 tests, один README phrase assertion. Сохранена точная фраза поверхностей с корректным разграничением native/standalone; final combined docs suite passed. После control-plane closure: exit 0, 100 tests, 3.566 s, OK (`docs-final.log`) |
| `python -B -m unittest tests.product_agent_os.test_codex_compatibility tests.product_agent_os.test_plugin_structure tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0; 122 tests, 10.234 s (`final-focused.log`), включает junction и docs regression |
| `python -B -m unittest tests.product_agent_os.test_codex_compatibility tests.product_agent_os.test_plugin_structure -v` после readability refactor и surface scope label | Exit 0; 22 tests, 2.796 s (`final-contracts.log`) |
| `python -B plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks.json`; `.codex/hooks`; `plugins/product-agent-os/assets/templates/hooks` | Каждый exit 0, ok=true, errors=[]; hooks не менялись в G2 |
| `python -B tools/check_docs.py` | Exit 0; documentation structure checks passed |
| `git diff --check` | Exit 0; в отличие от раннего G1, чужие Web EOF ошибки к этому моменту отсутствуют. G2 их не исправляла |
| `python -B -m unittest discover -s tests -p 'test_*.py' -v` | Exit 0; 1305 tests, 748.949 s, OK (skipped=1: non-Windows guard only), `full.log` |
| Final `validate_task_matrix.py` на этом плане; `tools/check_docs.py`; `git -c core.safecrlf=false diff --check`; `validate_codex_compatibility.py`; memory-only integrity checker | Все exit 0; matrix errors=[], docs OK, diff clean, compatible; 26 statuses, только восемь G1/G2 задач implemented, семь конечных source hashes совпадают; UTF-8 и root budgets OK |

Self-review: `context_mode=self_review`; separate reviewer не запускался. Проверены precedence, отсутствие MCP/subprocess/provider execution, output allowlist, IDE conflict, model/trust claim ceiling, bounded cache traversal, сохранение T23–T29 и Git/host boundary. Найден и исправлен Windows junction case; final diff не расширяет model policy или approval authority. Cache comparison не является race-proof authorization mechanism и не заменяет полный package receipt.

### Control-plane sync G2

- REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG: update_required → updated; scope, sequence G3, проверки, claim ceilings и handoff синхронизированы.
- Registry RU/EN, compatibility RU/EN, models RU/EN и README: updated с актуальными primary sources и локальными diagnostic contracts.
- `prod_test.md`: not_applicable — Batch 39 evidence не меняется. T23–T29 и canonical T30–T34 machine status не изменены.
- Overflow/refactor: not_applicable; все пять root files менее 50 KiB. Handoffs required: none внутри G2; G6/owner gates остаются открытыми по исходному acceptance.
- Strict MkDocs/site/navigation/diagrams: not_applicable — изменены только prose/source/control-plane, сайт не пересобирался и его freshness не заявляется.
- Review: self_review, tester_verdict=closed_allowed для локальной группы; closure_level=implemented_locally_verified. Не host/product/release readiness.

### Привязка к проверенному source state

Full discovery стартовал до финального junction guard и readability refactor. Финальные 122 tests покрывают junction/docs repair, затем 22 affected contracts проверены после последнего refactor; full-suite result не выдаётся за повторный запуск всех tests на последней версии. Fixture/transcript behavior последним refactor не меняется. SHA-256 конечных implementation/test файлов:

| File | SHA-256 |
| --- | --- |
| `plugins/product-agent-os/.mcp.json` | `14b1ca834d9867a3f382a7ebbf7d2f149e1b7ac0d2ae9deef5cdc030e670a546` |
| `plugins/product-agent-os/.codex-plugin/plugin.json` | `b3f07a4a2e6ba8a96b27ecfbd3b2065e94676f8d88dafd18a6e33e04bd1fd693` |
| `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py` | `e58c19c216b863f15ecfe30b93655ac2180d9df0d8f2c09aa0756024fb819d7f` |
| `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py` | `dacb7b39f2b1905b89d72aa26a00bb05477f18d8f821841fc1ed195e4008788e` |
| `plugins/product-agent-os/scripts/validate_codex_compatibility.py` | `9ab5e67a3fb5359efa5ad82158f48a0b650cf8bebda0efd24f52aeccd7863265` |
| `tests/product_agent_os/test_codex_compatibility.py` | `ff483c80a22392779320d6e8d48a4388ce910228e49b78e0013d0527786afb3b` |
| `tests/product_agent_os/test_plugin_structure.py` | `d988222e1182cf681e6c67bc0494713320aba8ce21ab09212a4281c72387bc89` |

Lifecycle preflight: две неверные формы собственного нового marker (status `implementation_in_progress`, затем missing updated_at) отклонены hook. Исправлен только own-session marker на `in_progress` с updated_at и сохранённым prior_closure G1. Compound bootstrap rejected; применён exact patch. Это process evidence, не новая activation проверка.

Rollback: отменить только G2 hunks относительно G1 baseline; сохранить чужие Web/G1 изменения и исторические receipts. `prod_test.md`, model pins/effort, installed cache, global config и host trust не изменяются. G6/AUD-HOST-01 владеет actual host receipts; distribution требует подтверждённых owner данных и отдельного разрешения.

## G5 execution evidence — 2026-11-09

Status: `implemented_locally_verified`; F13/F14/F17. Один исполнитель, zero delegation,
context_mode=self_review. Baseline worktree был clean; Git history не изменялась.
Current-run reports: `.docs-tools/reports/paos-aud-g5/`; render inputs:
`output/playwright/paos-aud-g5/`. Подробные source/build hashes: `verified-source-hashes.json`.

| Gate / команда | Наблюдение текущего run |
| --- | --- |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs.DocsInstallerContractTest -v` | RED: 3 tests, 2 failures — offline pip upgrade без --no-index; GREEN: 3/3, затем расширено до 5 regression cases в docs suite |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | 105 tests passed, exit 0; post-build/control-plane rerun: 18.137 s, docs-final.log |
| `python -B tools/check_docs.py` | exit 0, documentation structure checks passed |
| README renderer `--help`, полный пример `--dry-run ... --risk-level low` | exit 0; JSON корректен; context/safety gaps не превращаются в permission или activation |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | exit 0; local structure only, MCP не запускался |
| `.venv-docs/Scripts/python.exe -m mkdocs build --strict` | exit 0; 28.16 s; существующие project-local dependencies, без установки |
| `tools/fix_site_i18n_links.ps1 -SiteDir site` | final retry: updated_files=2, без ошибки; до retry два временно заблокированных Windows HTML |
| `python -B .docs-tools/reports/paos-aud-g5/check-site.py` | 368 HTML; 220 nav routes; missing files/routes/anchors/search routes = 0; 310 search pages |
| `python -B .docs-tools/reports/paos-aud-g5/run_render.py` | installed Chromium headless shell 1223; local Mermaid 10.9.6; 93/93 parse/render with nonzero SVG dimensions; browser exit 0 |
| `git -c core.safecrlf=false diff --check` | exit 0 |

F13: offline branch использует --no-index/--find-links, не обновляет pip; bootstrap
использует venv/bundled ensurepip без --upgrade-deps. Offline побеждает AllowNetwork.
Missing directory отклоняется до bootstrap, ошибка install останавливает путь без
network fallback. Stub заменяет только subprocess boundary: фактическая установка
не выполнялась, глобальная среда не менялась. Online upgrade остаётся explicit.

F14: первый экран README содержит explicit skill invocation, ordinary inline intake,
support/observation matrix и current-state pointer. MCP example совпадает с .mcp.json;
startup_timeout_sec удалён из JSON. Archive receipts/counts сохранены в details, с явной
датированной областью применимости. Publisher и distribution остаются gated.

F17 semantic review: current-state RU/EN совпадают по G1–G5 scope, pointer semantics,
source-policy/feedback limits и next G6; hooks RU/EN совпадают по session selector,
legacy prohibition, trust и explicit activation boundary; models RU/EN совпадают по
G2 diagnostics/cache scope и отсутствию host proof. Hooks/models sources уже согласованы
в G1/G2, повторная редактура не нужна; новая сборка включает их. Registry обновлён
парно. 10 English-original plans сохраняют исключение из translation inventory.
Diagrams/mkdocs.yml/vendor assets не изменены; 93 navigation diagrams проверены заново.

Failures/recovery: первоначальный README dry-run упал на sandbox TEMP cleanup;
повтор с workspace TEMP/TMP прошёл. Shell Chrome dump не дал DOM; обычные Chrome/Edge
и sandbox headless завершались до render. Разрешённый local headless run вне shell
sandbox прошёл с browser sandbox сохранённым, отдельным workspace profile и DNS
blocking; зависимости/серверы не устанавливались. Это render evidence, не host activation.
Два mapped-file errors при i18n исправлены повтором; окончательная проверка всех links
и anchors прошла. Неуспешные попытки не считаются acceptance.

Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG updated; prod_test.md
not_applicable (Batch 39 вне scope); AGENTS/config/hooks not_applicable. Root size
budget проверен docs suite. B42/B45 canonical source hashes сохраняются. Rollback:
вернуть только G5 source hunks, затем пересобрать local site; не менять trust/cache.
Full plugin unittest/fixture/transcript и live behavioral eval: not_applicable для
изменения installer/docs; G4 evidence остаётся прежним run, не объявляется новым.
Следующий slice — G6; owner acceptance, actual installation, fresh-host loading,
model quality, publication и production readiness не подтверждены этим run.

Task-matrix self-review: evidence перенесено перед карточками, чтобы parser не включал его в соседнюю F15 card; исходный placement дал unresolved-placeholder diagnostic. Final validator result — task-matrix-final.json.

## G6 current-project pilots — 2026-11-09

G6 partially_verified: три синтетических пилота выполнены из текущего проекта в host-target/pilots; все проверки passed, результаты needs_user_acceptance. По разрешению владельца HOST-01 больше не блокирует эти пилоты. Fresh-session activation HOST-01/HOST-02 остаётся отдельной открытой задачей; T34 no-go. Owner feedback/acceptance null; manual_only сохраняется.

Результаты и команды: [pilot-results](../docs/superpowers/specs/paos-aud-g6-pilot-results.json). Baseline bug: 64 вместо 8; final 1/4/8/8 и bounded large attempt passed. Config info/7; native encoder /, space, empty passed и SHA-256 unchanged. Исторические HOST receipts ниже не являются текущим pilot status.

## G6 refined HOST execution — 2026-11-09

G6 partially_verified: уточнённый HOST-пакет разрешён и применён — два cache-файла и 210 target files проверены readback. Свежая целевая сессия не запустилась: App API не задаёт произвольный cwd, elevated CLI остановлен auto-review, sandbox CLI не может открыть локальное состояние. Нужен штатный запуск пользователем существующего host-target в Codex App, без повторного разрешения. Пилоты not_run; acceptance null; T34 no-go.

[Current receipt](../docs/superpowers/specs/paos-aud-g6-refined-host-execution.json). Cache backup и target rollback manifest сохранены. Первая попытка apply отклонена из-за неверного типа значения blocking_hooks; поле исправлено на PreToolUse, затем apply exit 0 и 210/210 byte readback. Повторный полный unittest не нужен: runtime sources после предыдущего проверенного fix не менялись. Docs checks — refined-docs.log; check_docs/matrix/state/diff — refined-checks.log. Исторические blockers ниже не переименованы в успех; HOST/GAP tasks остаются blocked.

## G6 approved execution — 2026-11-09

Final local verification: full unittest 1342 tests, 796.146 s, exit 1 (one obsolete expected file count 209→210; one expected platform skip). Corrected exact regression rerun: 1 test, 58.423 s, exit 0. Focused 108 and docs/lifecycle 112 passed; fixtures 91/91, transcripts 26/26; docs/matrix/state/hook/diff gates passed. Full suite was not rerun after the count-only test correction. Final docs refresh is in approved-docs-final.log.

G6 partially_verified: все три пакета разрешены владельцем. Cache: 185 файлов обновлены с backup/readback; после локального handler fix новый diff из двух файлов ожидает review. T34: approved/unconsumed, no-go до tools/context isolation; 0 primary/reviewer calls. HOST-01 invocation не подтверждён. HOST-02: handler пропуск исправлен локально, target activation не доказана. Три пилота not_run из-за host dependency; owner acceptance отсутствует.

Owning evidence: [approved execution](../docs/superpowers/specs/paos-aud-g6-approved-execution.json),
[T34 results](../docs/superpowers/specs/batch45-code-quality-eval-results.json) и
[no-go decision](../docs/superpowers/specs/batch45-code-quality-promotion-decision.json).
Два owner-approved verification chats имеют независимые IDs и собственные markers:
`01a1c072-9005-7d22-bc0b-f832e57bbcb1`, `01a1c072-b0d8-7732-822c-af95aa89a639`.
Их наблюдения не заменяют полный positive/negative generated-target acceptance.

CLI `--version`, `login status`, `exec --help` — exit 0: 0.167.0, ChatGPT login.
`debug prompt-input` сначала exit 1 (Access denied к служебным путям), после approved
escalation exit 0: обнаружен ambient project context. Raw prompt не сохранён;
receipt хранит только хеш/размер/булевы признаки. Frozen readiness/design/context hashes совпали.
Заданный design требует tools=[] и отсутствия ambient skills/hooks/AGENTS;
поддержанный exact transport с доказанной изоляцией не подтверждён. Никакие guards
не отключались и no-tool prompt не выдан за пустую tool schema.
Official reference: [configuration controls](https://learn.chatgpt.com/docs/config-file/config-reference).
Это локальный preflight gap, не утверждение, что будущие версии CLI не могут поддержать такой режим.

Проверки continuation: docs suite, check_docs.py, task-matrix/state consistency и
git diff --check; точные результаты — approved-*.log в reports. Полный local suite
1341/91/26 выше относится к предыдущему запуску, после нового handler fix полный gate повторно запущен (approved-full.log).
HOST-02 выявил отсутствующий staged comment advisory handler. Регистрация исправлена;
runtime formatting сохранён без неоднозначного template marker, active/template parity соблюдена.
RED: missing-handler assertion; GREEN: 108 focused tests; dry-run/stage exit 0,
все шесть handlers присутствуют. [Repair receipt](../docs/superpowers/specs/paos-aud-g6-handler-repair.json).
После fix cache отличается двумя файлами: [точный preview](../docs/superpowers/specs/paos-aud-g6-cache-repair-preview.json).
Исходный host пакет требует stop при source drift; новые байты не установлены,
trust не обновлялся. Source hashes из двух свежих чатов относятся к состоянию до fix.
Контрольные планы, RU/EN current-state/registry и B44 followup синхронизированы.
prod_test.md: not_applicable. Site не пересобирался. Cache backup сохранён; rollback
только reviewed changed rows. Ни T34, ни HOST/GAP parent не объявлены завершёнными.

## G6 execution evidence — 2026-11-09 (historical local phase)

Status: `partially_verified`; audit не закрыт целиком. T30–T33 implemented locally;
T34/HOST-01/HOST-02/GAP-06 — blocked_pending_exact_authority_or_owner_acceptance.
Canonical B45 evidence: `B45-CQRR-A07`, `docs/superpowers/specs/batch45-code-quality-local-readiness.json`.
Один исполнитель, zero delegation, context_mode=self_review; worktree при старте clean.

| Gate | Current-run observation |
| --- | --- |
| Reviewer RED/GREEN | Первоначальный missing-API smoke был setup error, не RED. Затем 7 intended assertion failures для leaks/invalid pairs; GREEN 4 tests, позже rubric assertion добавлен в full suite |
| Versioned schema RED/GREEN | Новый CQ03 no-op сначала quarantined; additive schema и explicit evaluator no-change contract прошли, legacy schema сохраняется |
| `python -B -m unittest` focused modules | 50 tests passed, 11.969 s; reviewer/corpus/design/metrics/behavior/promotion/model-output |
| Corpus replay | 12 input outcomes, 12 reference passes и 12 seeded oracle failures; Python/JavaScript/SQLite/PowerShell, 7 risk classes; no model outputs |
| `python -B -m unittest discover -s tests -p 'test_*.py' -v` | 1341 tests, 1581.125 s, OK (skipped=1), exit 0 |
| Task-state follow-up | A07 metadata support RED/GREEN; all 7 lifecycle tests passed after full-suite import; unknown IDs remain rejected |
| Docs tests | 105 passed; final sync rerun recorded in `.docs-tools/reports/paos-aud-g6/docs-final.log` |
| Fixture / transcript eval | 91/91 and 26/26, exit 0 |
| Compatibility / hook validators | exit 0, local structure only; explicit cache observation reports drift |
| Source/build hygiene | check_docs.py and git diff --check passed; final pointer/matrix/docs checks recorded after synchronization |

T30 uses closed allowlisted blinded packets, random opaque IDs, patch-bound deterministic
receipts and a hash-bound reviewer response. Labels/self-scores are excluded; text leaks
fail closed. Critical/high findings override scores. Receipt authentication and actual
reviewer independence require separate execution evidence; no live reviewer ran.
T31 source/check/reference/seeded files are synthetic, hashes frozen before any generation.
Scoped privacy scan and manual authored-content review found no secrets/private data.
T32 changes only the compact pre-edit instruction; both arms use proposed gpt-6.1-sol/medium,
same runner/timeout/tools/corpus. Compiler checks source hashes and exposes only intent,
acceptance and input source; no oracle or ambient skills/hooks. T33 is local readiness,
not behavioral promotion. Performance oracle counts equality work, not elapsed speedup.

HOST-01: read-only cache comparison found drift; full preview lists 185 add/replace rows,
0 extras. No cache write. Preview: `docs/superpowers/specs/paos-aud-g6-host-approval-preview.json`;
exact per-file digests: `.docs-tools/reports/paos-aud-g6/cache-file-preview.json`.
Observed current-session terminal-marker denial is not fresh-host evidence. Client version,
actual selected skill, trust and observed model remain unverified; two fresh chats and
disposable generated-target activation remain open. Exact report-grant hash requires fresh
session IDs and a separately reviewed definition; no blanket trust permission is inferred.

Automatic approval review rejected `codex --version; codex exec --help` as a potential
separate autonomous-agent launch outside the declared scope. It was not executed or
retried indirectly. The separate bounded CLI scope is included in the pending packet.

T34 approval packet was prepared only after local preflight passed:
`docs/superpowers/specs/batch45-code-quality-eval-approval-packet.json`. Proposed cap:
24 primary + 12 independent reviewer calls, 180 s/call; existing Codex allowance only,
no separately billed API. Missing cost/usage evidence keeps no-go. Approval is absent,
not consumed; no results or promotion-decision success is fabricated.
Pilot proposal: `docs/superpowers/specs/paos-aud-g6-pilot-proposal.json`; three bounded
synthetic bug/config/no-new-code targets. Owner approval and feedback are missing.
Pilot inputs were separated from the held-out corpus before any model outputs;
T34 is not a dependency of this owner pilot.

Control-plane sync: five root files and RU/EN current-state/registry updated; ordinary
and lifecycle owning plans receive scoped handoff. B44 gets a pending proposal pointer,
not new acceptance. prod_test.md not_applicable: no B39 production evidence created.
Root site remains the G5 build; G6 source updates are not claimed as a new site build.
Rollback only G6 files/hunks; restore prior owning pointers after review. No Git actions,
dependency installation, cache/trust changes, live calls or publication performed.

## PAOS-AUD-G1 — execution evidence 09.11.2026

Scope: пять карточек G1, точный file manifest соответствует Scope карточек, двум связанным F12 callers и
общему docs/control-plane scope. Один исполнитель, self_review; subagents не запускались.
Baseline: чистое рабочее дерево. Runtime/model/provider, trust, ACL и target changes
не разрешаются этой записью. Host acceptance остаётся AUD-HOST-02/G6.

### RED и исправления

- F06: новый test_read_classification_rejects_compound_and_unknown_writes — exit 1,
  пять failures; после исправления exit 0. Попытка добавить инертный пример опасной
  команды в patch первоначально заблокирована действующим hook — текущий evidence
  false deny. После исправления source классификации test_patch_prose_is_not_an_executable_command
  проверяет отдельно данные и настоящее исполнение. Source mirror синхронизирован;
  это не fresh-host activation receipt.
- F12: expected discovery path исправлен в tests до реализации. Первый запуск
  merge suite: 35 setup errors из-за sandbox TEMP; это не RED. После workspace TEMP
  test_unapproved_hooks_json_remains_companion_only_and_not_written — exit 1,
  approved_targets mismatch. После mapping fix все 35 merge tests — exit 0.
- F11: native `codex execpolicy check --rules .rules -- rg --files` — exit 1,
  invalid not_match. После первого исправления обнаружен второй parser defect:
  unquoted Windows backslashes в match examples. Исправлены примеры и семантика.
  Итог: rg --files → prompt; rg --replace value → no matched rules;
  python create_task_plan.py new --output ../outside.md → prompt;
  icacls example /remove:d S-1-5-21-123 → forbidden; все четыре checks exit 0.
  Команды-аргументы не исполнялись. CLI сообщил предупреждения о недоступном
  user-level arg0 TEMP; policy JSON получен. Proposal не установлен/не активирован.
  Выбор: не оставлять широкие allow, которые не ограничивают trailing arguments.
- F07: новый repair contract test — exit 1, отсутствует _acl_text/API; GREEN:
  exact target/SID/digest, backup/restore, foreign DENY preservation по формируемым
  командам, drift/reparse denial. Реальные ACL mutation не запускались.
- F18: authoring scenario — exit 1, отсутствует отдельный API; builder test — exit 1,
  отсутствует build_report_authoring_call. GREEN: v2 opt-in, create и два update,
  stale digest, path/session/marker mismatch, expiry, terminal, aliases/reparse,
  mixed patch rejection. Legacy v1 suite сохранён. CAS preflight не является
  атомарной записью: один writer обязателен; race после hook return — явный предел.

### Промежуточные проверки

- `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_infrastructure_templates -q`: 132 tests, exit 1, три failures (старый active mirror, ограниченный Select-Object pipeline, template placeholder regex). Исправлены parity, bounded pipeline и digest regex.
- Пять affected modules: 183 tests, 13.604 s, OK (skipped=1), exit 0.
- После дополнительных negative/rollback tests четыре изменённых modules: 89 tests, 12.465 s, OK (skipped=1), exit 0.
- Все Python проверки используют `PYTHONDONTWRITEBYTECODE=1`, `TEMP=TMP=<workspace>/.codex-tmp/paos-aud-g1`; реальные target files и ACL не меняются.

### Финальные проверки

- Native rules parser, три validate_hooks targets, transcript eval 26/26,
  check_docs.py — exit 0.
- validate_codex_compatibility.py — exit 1, needs_review:
  legacy_flat_mcp_requires_schema_review. Это существующий G2/F01 contract gap;
  G1 не меняет MCP package и не объявляет совместимость доказанной.
- task matrix сначала отклонён: appended evidence попало в последнюю task card
  и было распознано как unresolved placeholder. Evidence перемещено перед
  карточками; повторный validator — exit 0, errors=[].
- Dry-run и staging CLI на existing-codex-config fixture — exit 0 оба;
  manifest и staged .codex/hooks.json существуют, nested mirror отсутствует.
- Self-review добавил F06 regression для tool metadata/unknown tool: RED exit 1,
  executable text содержал workdir/justification; исправлено извлечение payload.
- Финальный affected rerun сначала: 185 tests, failures=2, errors=1, skipped=1.
  Windows TEMP cleanup sharing violation воспроизводимость не подтверждена;
  изолирован TEMP для concurrent checks. Две contract регрессии исправлены:
  legacy command envelope без tool_name и слово Python null-value в rendered
  template, ошибочно распознаваемое старым placeholder assertion.
- Первый fixture eval упал с UnboundLocalError; full discovery остановлен после
  повторных fixture errors. Причина F12: два fixture exercise callers ещё
  использовали старый hooks path. Дополнительный необходимый file scope:
  plugins/product-agent-os/scripts/run_fixture_eval.py и
  tests/product_agent_os/test_infrastructure_renderer.py. Исправлены только
  expected paths/callers, error handling и другие gates не ослаблялись.
- После исправлений paths: fixture eval — exit 0, 91/91 passed.
- Affected suite после изоляции TEMP: 216 tests, 40.024 s, OK (skipped=1), exit 0.
  Промежуточный запуск 216 tests имел только Windows cleanup WinError 32;
  новый TEMP: .docs-tools/reports/paos-aud-g1/tmp, ignored directory.
- `icacls /?` (read-only help) и Microsoft official reference подтверждают
  /inheritance:d (copies ACEs), /remove:d *SID, DACL /save и /restore;
  owner/SACL/integrity labels snapshot не сохраняет и helper не меняет.
- `python -B -m unittest discover -s tests -p 'test_*.py' -v`: 1297 tests,
  532.640 s, OK (skipped=1), exit 0. Единственный skip — non-Windows guard на Windows.
  Этот прогон стартовал до последнего alias-hardening F12; его evidence не
  подменяет последующий focused retest изменённого merge module.
- Финальный self-review F12: ./, case, separator и trailing-dot aliases discovery
  path обходили специальный hook gate (4 RED failures). Добавлен canonical-path
  rejection. После изменения `python -B -m unittest
  tests.product_agent_os.test_merge_infrastructure
  tests.product_agent_os.test_infrastructure_renderer -q`: 67 tests,
  16.645 s, OK, exit 0. Неизменённые другие modules повторно не запускались.
- `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v`:
  100 tests, 4.415 s, OK, exit 0; итоговый status-only docs gate записан ниже.
- Финальные validate_hooks: active definition, active scripts и packaged hooks —
  exit 0 каждый. AST/parity hook/workflow — PASS. .codex/hooks.json,
  .codex/hooks/hooks.json и .codex/config.toml совпадают с baseline HEAD
  с нормализацией line endings. Root site не пересобирался и freshness не заявлена.

### Acceptance mapping и self-review

| Task | Локальный результат | Evidence | Отдельная граница |
| --- | --- | --- | --- |
| F06 | Целая bounded command, metadata separation, unknown mutation scope, inert patch prose | Lifecycle positive/negative suite; active/package parity | Не универсальный shell parser; native sandbox/approval сохраняются |
| F12 | Один discovery path, manifest/config agreement, existing file preservation, synthetic apply/rollback, alias denial | Dry-run/stage CLI; 36 merge и 31 renderer tests | Trust/real target apply не выполнялись |
| F11 | Valid native parser; no broad allow; proposal retained | Четыре execpolicy decisions выше | Discovery rules не устанавливались |
| F07 | Explicit single target/SID, digest, DACL backup/restore, preservation and reparse guards | 9 Windows permissions tests, включая один platform skip; mocked icacls | Реальные ACL и rollback acceptance отдельно |
| F18 | Pinned v2 authoring, previous digest, exact session/path, full-file update, legacy v1 preserved | Lifecycle и builder/validator regressions | Preflight не атомарен; exclusive writer; host gate G6 |

Review context: self_review; tester_verdict=closed_allowed только для local G1.
Blocking local findings после исправлений отсутствуют. Independent reviewer не
запускался. Existing MCP compatibility gap остаётся G2/F01. Поведенческие thresholds
LLM не менялись; live model/provider calls не требовались и не запускались.
Откат: отменить только перечисленные G1 hunks, сохранив чужой session marker и
параллельные .hallmark/прочие artifacts. Own session marker — служебная запись,
не доказательство hook activation.



### Финальный status-only closure check

После обновления пяти карточек: validate_task_matrix.py — exit 0, errors=[];
check_docs.py — exit 0; docs unittest — 100 tests, 3.118 s, OK, exit 0.
Проверены 5 implemented / 21 planned, размеры пяти root файлов меньше 50 KB,
UTF-8 без replacement characters, AST изменённых Python и parity mirrors.
Global `git diff --check` — exit 2 из-за new blank line at EOF в параллельно
изменённых Web architecture/M1-wireframes/PRD research docs (вне G1). Они не
правились. `git diff --check --` с точным manifest из 30 G1-owned files — exit 0.
Это явное разделение scope, не успешный global check и не waiver G1 gate.
Чужой lifecycle marker, .hallmark и прочие параллельные изменения сохранены.

### Проверенное source state

SHA-256 exact file bytes; active/package parity подтверждена отдельно.

| File | SHA-256 |
| --- | --- |
| `.codex/hooks/pre_tool_use_policy.py` | `cd78b4f34db916c622f17dfa8e275f97e30143525caaf60b25a13b416d23326b` |
| `.codex/workflows/task-plan-lifecycle.md` | `962e90330c7a6e5838252eb8f866c111742d3fc65a164e991ab8f020c149e741` |
| `.rules` | `0613c81e78076f22c4597e5b209b425f3370e00c569128cb05e764890f409d4f` |
| `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py` | `01140b699c8379e1d2dd379855f7230a575a4a8038100e01a1947edb80c58b3d` |
| `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py` | `2343e407678ca325b49fdaf088d88fbe7471d8bd06b132af16b0f478c33d5ecb` |
| `plugins/product-agent-os/scripts/product_agent_os/task_plan_lifecycle.py` | `182ee6132e5508544198567c929a53c8850666062235a7c369f237286ceb885a` |
| `plugins/product-agent-os/scripts/product_agent_os/validators.py` | `0add6b2bb429bf12867ea4cfa83087c5eab1f918c330e556c2d9e5f3600e2ed2` |
| `plugins/product-agent-os/scripts/product_agent_os/templates.py` | `05dd4f9754b7826efbe90ff165464d4d72db6c45b5f7ffd7381ec77aa3ce36bc` |
| `plugins/product-agent-os/assets/templates/config/config.toml` | `68673ae1a9941a1424b8b9536204657e3d84a5aa1c7a397233eba7abcb9ef5c0` |

Локальные сырые outputs сохранены под ignored `.docs-tools/reports/paos-aud-g1/`;
ранние и integrated logs перенесены из собственного TEMP в `initial-and-integrated-runs/`.
Durable receipt — этот план; raw logs не являются вторым status registry.

### Control-plane sync

REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG: update_required и обновлены по scope, sequencing,
verification, failure classes и handoff. prod_test.md: not_applicable (Batch 39 не
затронут). Registry RU/EN и runtime docs RU/EN синхронизированы; workflow mirrors
согласованы. Site/navigation/diagrams: not_applicable; build/activation не заявлены.
Overflow: все пять root файлов меньше 50 KB; перераспределение не требуется. Handoff: G2 после local gates, G6 для
host acceptance; иных обязательных local handoffs нет.


## PAOS-AUD-G1 — Надёжные hooks, rules и установка

- **ID:** `PAOS-AUD-G1`
- **Execution status:** `implemented_locally_verified`; пять local acceptance contracts закрыты. Next group: G2; host acceptance остаётся G6.
- **Название группы:** Надёжные hooks, rules и установка
- **Описание группы:** Закрыть оставшиеся ошибки классификации действий и generated onboarding; ограничить ACL repair и добавить безопасное последовательное ведение отчёта. Сохранить уже реализованную session isolation.
- **Техническое значение (для проекта):** Согласованные active/package contracts, точные границы записи и корректные staging/merge paths.
- **Продуктовое значение (для пользователя):** Меньше ложных блокировок и повторных согласований без ослабления защиты пользовательских файлов.
- **Затрагиваемые файлы:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py`; `.rules`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** Все пять карточек имеют локальные positive/negative evidence; active/package mirrors согласованы; нет автоматической активации hooks/rules или изменения рабочих ACL. Host acceptance закрывается отдельно в G6.
- **Зависимости и порядок:** Начинать первой. F06 перед F18; F12 можно исправлять независимо по своим файлам, integrated host probe после итоговых hooks. ACL и rules — независимые ограниченные изменения.
- **Предлагаемая ответственность:** plugin-runtime-builder; assurance — security-privacy-supply-chain-reviewer.

### Task `PAOS-AUD-F06`

- ID: `PAOS-AUD-F06`
- Task: **Название задачи:** Исправить оставшиеся ошибки классификации команд и patch
- Short description: **Описание задачи:** Различать executable command, аргументы и содержимое patch. Не признавать всю составную команду read-only по начальному префиксу; неизвестные формы направлять в ограниченную проверку. Сохранить текущий session-bound selector, exact bootstrap, sandbox и approvals; не писать универсальный shell interpreter.
- Technical value: **Техническое значение (для проекта):** Устранение false allow и false deny в PreToolUse без расширения полномочий.
- Product value: **Продуктовое значение (для пользователя):** Обычные чтения и документационные примеры не блокируются ошибочно, а потенциальные записи проверяются последовательно.
- Scope: **Затрагиваемые файлы:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `tests/product_agent_os/test_lifecycle_hooks.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Инертные cases: чистое чтение разрешено; составная read/write строка не классифицируется как чистое чтение; неизвестная запись не получает allow через отсутствие match. 2) Упоминание опасной команды как данных в обычном Markdown не трактуется как её выполнение; реальные destructive/path/secret проверки сохранены. 3) Регрессии own/foreign/mixed marker, Windows case handling и session isolation проходят; active/package файлы совпадают.
- Group: PAOS-AUD-G1
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию PAOS-AUD-G1.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 12:47
- Depends on: Нет новых обязательных задач этого плана. PAOS-SESSION-LIFECYCLE-2026-11-09 — использовать, не переделывать.
- Blocks: PAOS-AUD-F18, PAOS-AUD-HOST-02; для F05 только incremental report scenario.
- Source: F06; последующий session-lifecycle repair уже закрыл exact marker bootstrap и изоляцию чатов.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Устранение false allow и false deny в PreToolUse без расширения полномочий. Missing host/product gates остаются открытыми.
- Verification gates: RED/GREEN в test_lifecycle_hooks; validate_hooks.py для active/package definitions; AST/parity; свежий host отдельно AUD-HOST-02. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; изменение definition/trust и host probe не входит в локальное исправление. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Local G1 закрыта; следующий маршрут G2, host acceptance отдельно G6.

#### Completion Report

- status: implemented
- what was done: Исправлены whole-command classification, metadata extraction, conservative unknown route и patch destination/data separation; session isolation сохранена.
- files touched / work locations: .codex/hooks/pre_tool_use_policy.py; packaged mirror; test_lifecycle_hooks.py
- technical value delivered: False allow/deny устранены в заявленных local cases.
- product value delivered: Чтения и Markdown examples не требуют ложного mutation approval.
- actual implementation date and time: 09-11-2026 12:47
- verification evidence: Lifecycle suite, full 1297, final source parity; RED/GREEN в execution evidence.
- residual risks: Local verification only; host/trust и реальные ACL не доказаны. MCP gap принадлежит G2. Подробные limits — execution evidence.
- follow-up: Перейти к G2; AUD-HOST-02 и real ACL acceptance остаются отдельными разрешёнными сценариями.


### Task `PAOS-AUD-F12`

- ID: `PAOS-AUD-F12`
- Task: **Название задачи:** Согласовать generated hooks config и безопасный merge
- Short description: **Описание задачи:** Исправить mapping в templates/merge на discovered .codex/hooks.json; согласовать manifest и generated config. Сохранить существующие user-authored hooks. Явно разделить staging, approved apply и фактическую активацию.
- Technical value: **Техническое значение (для проекта):** Устранение несовпадения generated filesystem layout с контрактом загрузки.
- Product value: **Продуктовое значение (для пользователя):** Установка не создаёт видимость включённого hook, который host не загрузит.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`; `plugins/product-agent-os/assets/templates/config/config.toml`; `tests/product_agent_os/test_merge_infrastructure.py`; `tests/product_agent_os/test_infrastructure_templates.py`; связанные callers `plugins/product-agent-os/scripts/run_fixture_eval.py` и `tests/product_agent_os/test_infrastructure_renderer.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Dry-run, staging manifest и config указывают один правильный путь; mirror не считается discovery config. 2) Existing unmarked config не перезаписывается; approved merge/rollback проверены на synthetic workspace. 3) Тест проверяет реальный expected discovery path; результат установки не объявляет trust/activation доказанными.
- Group: PAOS-AUD-G1
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию PAOS-AUD-G1.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 12:47
- Depends on: Нет жёсткой local code зависимости; integration/host probe выполняется после итогового F06.
- Blocks: PAOS-AUD-HOST-02
- Source: F12
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Устранение несовпадения generated filesystem layout с контрактом загрузки. Missing host/product gates остаются открытыми.
- Verification gates: Focused infrastructure/merge tests и dry-run на synthetic fixtures; actual target activation отдельно AUD-HOST-02. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; apply в реальный target и trust требуют своей точной authority. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Local G1 закрыта; следующий маршрут G2, host acceptance отдельно G6.

#### Completion Report

- status: implemented
- what was done: Generated hook definition перенесён в .codex/hooks.json; merge approval/rollback и alias rejection согласованы; обновлены renderer/eval callers.
- files touched / work locations: templates.py; merge_infrastructure.py; template config.toml; run_fixture_eval.py; test_merge_infrastructure.py; test_infrastructure_templates.py; test_infrastructure_renderer.py
- technical value delivered: Manifest/config/merge используют один discovery path с отдельным activation gate.
- product value delivered: Установка сохраняет существующие hooks и явно отделяет staging от активации.
- actual implementation date and time: 09-11-2026 12:47
- verification evidence: Dry-run/staging exit 0; full 1297; final 67 merge/renderer tests after alias fix; fixture 91/91.
- residual risks: Local verification only; host/trust и реальные ACL не доказаны. MCP gap принадлежит G2. Подробные limits — execution evidence.
- follow-up: Перейти к G2; AUD-HOST-02 и real ACL acceptance остаются отдельными разрешёнными сценариями.


### Task `PAOS-AUD-F11`

- ID: `PAOS-AUD-F11`
- Task: **Название задачи:** Исправить семантику и статус rules-файла
- Short description: **Описание задачи:** Устранить использование not_match как исключения; выбрать узкие patterns и корректные проверочные примеры. Отдельно определить, остаётся ли файл proposal или переносится в discovery path по разрешённой активации. Не активировать широкие allow путём простого перемещения.
- Technical value: **Техническое значение (для проекта):** Native parser принимает политику, а разрешения соответствуют проверяемому контракту.
- Product value: **Продуктовое значение (для пользователя):** Пользователь понимает, какие команды реально разрешены и активна ли эта политика.
- Scope: **Затрагиваемые файлы:** `.rules`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) codex execpolicy check принимает файл и даёт ожидаемые решения для positive/negative cases. 2) Patterns не расширяют прежнюю заявленную authority; потенциально опасные варианты не получают широкое allow. 3) Фактический loading status указан отдельно; путь .codex/rules/default.rules не создаётся без отдельного решения об активации.
- Group: PAOS-AUD-G1
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию PAOS-AUD-G1.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 12:47
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: F11
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Native parser принимает политику, а разрешения соответствуют проверяемому контракту. Missing host/product gates остаются открытыми.
- Verification gates: Native execpolicy parser/check на фиксированных inert arguments; docs checks. Исполнение разрешённых команд не требуется. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; relocation/activation rules — отдельная граница разрешения. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: security-privacy-supply-chain-reviewer для read-only review; plugin-runtime-builder для правки; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Local G1 закрыта; следующий маршрут G2, host acceptance отдельно G6.

#### Completion Report

- status: implemented
- what was done: Исправлены not_match semantics и Windows path examples; broad allow заменены review decisions; .rules оставлен proposal.
- files touched / work locations: .rules; docs/runtime/worktrees-hooks-rules.md и .en.md; registry RU/EN
- technical value delivered: Native parser принимает proposal, опасные trailing arguments не получают broad allow.
- product value delivered: Loading status и необходимость review обозначены явно.
- actual implementation date and time: 09-11-2026 12:47
- verification evidence: Четыре codex execpolicy check: exit 0; prompt/no-match/prompt/forbidden; docs tests/checker.
- residual risks: Local verification only; host/trust и реальные ACL не доказаны. MCP gap принадлежит G2. Подробные limits — execution evidence.
- follow-up: Перейти к G2; AUD-HOST-02 и real ACL acceptance остаются отдельными разрешёнными сценариями.


### Task `PAOS-AUD-F07`

- ID: `PAOS-AUD-F07`
- Task: **Название задачи:** Исключить широкий ACL repair из onboarding
- Short description: **Описание задачи:** Убрать normal-onboarding рекомендацию broad ACL repair. Если helper остаётся доступным как repair tool, ограничить target/SID, запретить неоднозначные reparse paths, добавить preview, ACL snapshot/restore и привязку apply к согласованному plan digest.
- Technical value: **Техническое значение (для проекта):** Сохранение системных и проектных deny ACE; обратимый и ограниченный ремонт permissions.
- Product value: **Продуктовое значение (для пользователя):** Настройка Product-Agent OS не снимает пользовательские ограничения доступа и не требует опасного универсального исправления.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py`; `plugins/product-agent-os/scripts/prepare_windows_codex_permissions.py`; `tests/product_agent_os/test_windows_codex_permissions.py`; `plugins/product-agent-os/README.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Default/help/onboarding не предлагают broad apply; dry-run не меняет ACL. 2) Посторонние DENY SID не удаляются; unexpected target, digest drift и reparse ambiguity останавливают apply. 3) Backup/restore и формирование команд проверены через существующий mock/stub слой; настоящий ACL acceptance явно остаётся отдельным разрешённым сценарием.
- Group: PAOS-AUD-G1
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию PAOS-AUD-G1.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 12:47
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: F07
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Сохранение системных и проектных deny ACE; обратимый и ограниченный ремонт permissions. Missing host/product gates остаются открытыми.
- Verification gates: test_windows_codex_permissions: command contract, SID/path allowlist, digest mismatch, rollback preservation. Без реального icacls apply. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; реальные ACL/permissions изменения требуют точных target, owner и rollback. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; независимая проверка security-privacy-supply-chain-reviewer; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Local G1 закрыта; следующий маршрут G2, host acceptance отдельно G6.

#### Completion Report

- status: implemented
- what was done: Broad onboarding apply заменён single-target/SID repair с plan digest, DACL snapshot/restore, reparse/drift rejection и rollback при сбое.
- files touched / work locations: windows_codex_permissions.py; prepare_windows_codex_permissions.py; test_windows_codex_permissions.py; plugin README.md
- technical value delivered: Посторонние DENY SID не удаляются; операции ограничены reviewed plan.
- product value delivered: Обычный onboarding остаётся диагностическим; repair имеет preview и путь восстановления.
- actual implementation date and time: 09-11-2026 12:47
- verification evidence: Permissions mock tests в affected 216 и full 1297; default no-apply, selected SID, drift, reparse, restore failure tests; native help readback.
- residual risks: Local verification only; host/trust и реальные ACL не доказаны. MCP gap принадлежит G2. Подробные limits — execution evidence.
- follow-up: Перейти к G2; AUD-HOST-02 и real ACL acceptance остаются отдельными разрешёнными сценариями.


### Task `PAOS-AUD-F18`

- ID: `PAOS-AUD-F18`
- Task: **Название задачи:** Добавить ограниченное последовательное authoring одного отчёта
- Short description: **Описание задачи:** Спроектировать отдельный opt-in report-authoring scope на один exact Markdown path: create/update, expected previous digest, срок действия, session ownership и terminal handling. Определить честное отображение этого work type в lifecycle schema. Существующий create-only grant не расширять неявно.
- Technical value: **Техническое значение (для проекта):** Поддержка incremental research без общего разрешения на запись и без маскировки документации под runtime implementation.
- Product value: **Продуктовое значение (для пользователя):** Наблюдения сохраняются по мере работы без повторной ручной разблокировки каждой записи.
- Scope: **Затрагиваемые файлы:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/scripts/product_agent_os/task_plan_lifecycle.py`; `plugins/product-agent-os/scripts/product_agent_os/validators.py`; `.codex/workflows/task-plan-lifecycle.md`; `plugins/product-agent-os/assets/templates/workflows/task-plan-lifecycle.md`; `tests/product_agent_os/test_lifecycle_hooks.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Несколько последовательных обновлений своего exact report проходят при совпадении digest и действующем scope. 2) Чужой marker/path, stale digest, expired grant, terminal state, symlink/alias и mixed patch отклоняются. 3) Legacy create-only поведение сохранено; новая authoring authority явно выражена и не меняет sandbox/trust. 4) Конкурирующее изменение отчёта даёт conflict, а не silent overwrite; host behavior закрывается отдельно.
- Group: PAOS-AUD-G1
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию PAOS-AUD-G1.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 12:47
- Depends on: PAOS-AUD-F06
- Blocks: PAOS-AUD-HOST-02; для F05 только incremental report scenario.
- Source: F18; GAP-05 create-only grant; session isolation уже реализована.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Поддержка incremental research без общего разрешения на запись и без маскировки документации под runtime implementation. Missing host/product gates остаются открытыми.
- Verification gates: Contract design + focused lifecycle/validators tests с RED/GREEN; source parity; после итоговых hashes AUD-HOST-02. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; изменение opt-in grant не даёт права активировать его в hook definition. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: lifecycle-orchestrator; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Local G1 закрыта; следующий маршрут G2, host acceptance отдельно G6.

#### Completion Report

- status: implemented
- what was done: Добавлен отдельный opt-in work_type report_authoring, v2 grant/session/expiry, previous-digest conflict check и whole-report create/update builder; v1 сохранён.
- files touched / work locations: active/package pre_tool_use_policy.py и workflow; task_plan_lifecycle.py; validators.py; lifecycle/task-plan tests
- technical value delivered: Последовательные записи одного отчёта ограничены exact path, grant и session.
- product value delivered: Можно накапливать отчёт без общего mutation scope и без переоформления grant на каждую версию.
- actual implementation date and time: 09-11-2026 12:47
- verification evidence: Create + two updates, stale digest, foreign path/session/marker, expiry, terminal, alias/reparse/mixed denial; affected 216; full 1297.
- residual risks: Local verification only; host/trust и реальные ACL не доказаны. MCP gap принадлежит G2. Подробные limits — execution evidence.
- follow-up: Перейти к G2; AUD-HOST-02 и real ACL acceptance остаются отдельными разрешёнными сценариями.

## PAOS-AUD-G2 — Совместимость package и диагностика host

- **ID:** `PAOS-AUD-G2`
- **Статус:** `implemented_locally_verified`; F01/F02/F04 выполнены, следующий G3.
- **Название группы:** Совместимость package и диагностика host
- **Описание группы:** Исправить MCP declaration, capability matrix и расширить существующий compatibility report наблюдаемыми данными host/model/provenance.
- **Техническое значение (для проекта):** Один источник диагностики package schema и surface capabilities без нового doctor framework.
- **Продуктовое значение (для пользователя):** Пользователь видит, что доступно, что не поддерживается и что ещё не проверено.
- **Затрагиваемые файлы:** `plugins/product-agent-os/.mcp.json`; `plugins/product-agent-os/.codex-plugin/plugin.json`; `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`; `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `plugins/product-agent-os/scripts/validate_codex_compatibility.py`; `tests/product_agent_os/test_codex_compatibility.py`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** Поддерживаемый локальный package проходит compatibility check; unsupported и not_verified различены; version/model/cache/trust не получают вымышленных значений.
- **Зависимости и порядок:** Можно вести независимо от G1 при отдельном владельце. F01 и F02 перед F04. Выход используется G5/G6.
- **Предлагаемая ответственность:** plugin-runtime-builder.


### Task `PAOS-AUD-F01`

- ID: `PAOS-AUD-F01`
- Task: **Название задачи:** Исправить MCP declaration и distribution metadata
- Short description: **Описание задачи:** Исправить flat .mcp.json в рамках поддерживаемого текущего manifest format; проверить resolver precedence. Проверить placeholder publisher/URLs: использовать только подтверждённые данные владельца, иначе явно оставить distribution gate открытым.
- Technical value: **Техническое значение (для проекта):** Совместимый package без необязательной wholesale migration на portable format.
- Product value: **Продуктовое значение (для пользователя):** Пакет устанавливается по понятному контракту и не вводит в заблуждение относительно издателя.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/.mcp.json`; `plugins/product-agent-os/.codex-plugin/plugin.json`; `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`; `tests/product_agent_os/test_codex_compatibility.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Текущий package проходит локальный compatibility check по MCP shape; malformed/ambiguous fixtures остаются rejected/needs_review. 2) Legacy manifest сохраняется, если нет отдельного требования переносимости; не смешиваются два независимых manifest authority. 3) Publisher/URLs проверены или distribution остаётся явно gated; MCP server не запускается проверкой структуры.
- Group: PAOS-AUD-G2
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию G2 с проверками; внешние boundaries сохранены.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:16
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F04, PAOS-AUD-F14, PAOS-AUD-HOST-01
- Source: F01
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Совместимый package без необязательной wholesale migration на portable format. Missing host/product gates остаются открытыми.
- Verification gates: validate_codex_compatibility.py; existing component/compatibility fixtures; JSON syntax и resolver regression. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; неизвестные identity/URL не выдумывать; publication и MCP execution вне scope. Rollback — по общим правилам.
- Complexity: low
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Реализованные scope files; G2 execution evidence и SHA-256 в этом плане.
- Next step: G3; actual host acceptance и distribution gates отдельно.

#### Completion Report

- status: implemented
- what was done: Исправлен MCP wrapper; rejected duplicate/ambiguous/unknown inputs; сохранён portable precedence. Неподтверждённые publisher/URLs заменены явным gated status.
- files touched / work locations: plugins/product-agent-os/.mcp.json; .codex-plugin/plugin.json; scripts/product_agent_os/plugin_components.py; tests/product_agent_os/test_codex_compatibility.py; test_plugin_structure.py; shared docs/control-plane.
- technical value delivered: Поддерживаемая локальная структура без смешения authority.
- product value delivered: Понятный package contract без ложной атрибуции издателю.
- actual implementation date and time: 09-11-2026 13:16
- verification evidence: G2 execution evidence выше: RED; full 1305 OK (1 platform skip), 748.949 s, exit 0; final focused 122 OK, final contracts 22 OK; fixtures 91, transcript 26/26; compatibility exit 0; docs/hooks passed. Source state provenance и hashes сохранены.
- residual risks: Distribution publisher/URLs/icons gated; host activation/trust/account access и full package receipts не доказаны. T30–T34/G6 остаются source-owned.
- follow-up: Переход к G3. Для actual host evidence — AUD-HOST-01/G6; publication и model promotion требуют своих gates.

### Task `PAOS-AUD-F02`

- ID: `PAOS-AUD-F02`
- Task: **Название задачи:** Разделить поддержку и проверенность host capabilities
- Short description: **Описание задачи:** В существующей capability matrix разделить documented support, unsupported и observed/not_verified для Codex App, CLI и IDE extension; различать native plugin и standalone skills.
- Technical value: **Техническое значение (для проекта):** Типизированный capability contract без смешения невозможного и ещё не протестированного.
- Product value: **Продуктовое значение (для пользователя):** Пользователь не тратит время на попытку включить неподдерживаемую функцию.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `tests/product_agent_os/test_codex_compatibility.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) App/CLI/IDE получают документированные разные capabilities; unsupported не заменяется requires_host_receipt. 2) Host receipt не может повысить documented unsupported до supported без обновления source-backed contract. 3) Local structure scope и отсутствие активационного доказательства сохранены.
- Group: PAOS-AUD-G2
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию G2 с проверками; внешние boundaries сохранены.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:16
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F04, PAOS-AUD-F14, PAOS-AUD-HOST-01
- Source: F02
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Типизированный capability contract без смешения невозможного и ещё не протестированного. Missing host/product gates остаются открытыми.
- Verification gates: Focused compatibility tests: surface/component matrix, unknown surface, unsupported versus unverified; актуальные official sources при реализации. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; capability facts сверить заново на дату реализации. Rollback — по общим правилам.
- Complexity: low
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Реализованные scope files; G2 execution evidence и SHA-256 в этом плане.
- Next step: G3; actual host acceptance и distribution gates отдельно.

#### Completion Report

- status: implemented
- what was done: Разделены documented support и observation; IDE native plugin unsupported; receipt conflict не повышает capability; standalone skills отдельно.
- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py; tests/product_agent_os/test_codex_compatibility.py; shared docs/control-plane.
- technical value delivered: Раздельный capability contract для App/CLI/IDE.
- product value delivered: Неподдерживаемая функция не предлагается как ожидающая активации.
- actual implementation date and time: 09-11-2026 13:16
- verification evidence: G2 execution evidence выше: RED; full 1305 OK (1 platform skip), 748.949 s, exit 0; final focused 122 OK, final contracts 22 OK; fixtures 91, transcript 26/26; compatibility exit 0; docs/hooks passed. Source state provenance и hashes сохранены.
- residual risks: Distribution publisher/URLs/icons gated; host activation/trust/account access и full package receipts не доказаны. T30–T34/G6 остаются source-owned.
- follow-up: Переход к G3. Для actual host evidence — AUD-HOST-01/G6; publication и model promotion требуют своих gates.

### Task `PAOS-AUD-F04`

- ID: `PAOS-AUD-F04`
- Task: **Название задачи:** Дополнить диагностику GPT-6 и provenance без promotion claims
- Short description: **Описание задачи:** Расширить существующий compatibility report сведениями client version/surface, configured versus observed model, canonical/cache provenance и trust unknown/observed. Клиентский minimum проверять только для конкретной documented surface. Не менять model pins или effort.
- Technical value: **Техническое значение (для проекта):** Один наблюдаемый compatibility contract связывает конфигурацию с доступным evidence.
- Product value: **Продуктовое значение (для пользователя):** Видно, почему выбранная модель или skill пока не подтверждены в текущем окружении.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `plugins/product-agent-os/scripts/validate_codex_compatibility.py`; `tests/product_agent_os/test_codex_compatibility.py`; `docs/codex/models-and-reasoning.md`; `docs/codex/models-and-reasoning.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Missing/old/unknown version, недоступный model receipt, source/cache drift и unknown trust отражаются явно. 2) Установленный CLI не выдаётся за проверенную версию App или доступность аккаунта. 3) Нет provider вызовов, cache writes, автоматического повышения effort или promotion по одному model ID. 4) Read-only inputs/report редактируют только allowlisted non-secret данные; baseline T23–T29 сохранён.
- Group: PAOS-AUD-G2
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию G2 с проверками; внешние boundaries сохранены.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:16
- Depends on: PAOS-AUD-F01, PAOS-AUD-F02
- Blocks: PAOS-AUD-F14, PAOS-AUD-HOST-01
- Source: F04 — локальная диагностика; качество treatment остаётся в B45-CQRR-T30–T34.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Один наблюдаемый compatibility contract связывает конфигурацию с доступным evidence. Missing host/product gates остаются открытыми.
- Verification gates: Focused version/capability/provenance fixtures и read-only CLI output; actual host receipt — AUD-HOST-01. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; диагностика не требует credential use или изменения active profiles. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Реализованные scope files; G2 execution evidence и SHA-256 в этом плане.
- Next step: G3; actual host acceptance и distribution gates отдельно.

#### Completion Report

- status: implemented
- what was done: Добавлены bounded allowlisted observations и explicit cache read-only comparison, version/model/trust diagnostics; CLI minimum применяется только Terra/CLI. Symlink/junction rejected; model pins/effort сохранены.
- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py; scripts/validate_codex_compatibility.py; tests/product_agent_os/test_codex_compatibility.py; docs/codex/models-and-reasoning.md и .en.md; shared docs/control-plane.
- technical value delivered: Configured/observed и canonical/cache evidence раздельны, unknown явно отображён.
- product value delivered: Видны причины отсутствия подтверждения модели, trust и выбранного skill source.
- actual implementation date and time: 09-11-2026 13:16
- verification evidence: G2 execution evidence выше: RED; full 1305 OK (1 platform skip), 748.949 s, exit 0; final focused 122 OK, final contracts 22 OK; fixtures 91, transcript 26/26; compatibility exit 0; docs/hooks passed. Source state provenance и hashes сохранены.
- residual risks: Distribution publisher/URLs/icons gated; host activation/trust/account access и full package receipts не доказаны. T30–T34/G6 остаются source-owned.
- follow-up: Переход к G3. Для actual host evidence — AUD-HOST-01/G6; publication и model promotion требуют своих gates.

## PAOS-AUD-G3 — Достоверные evidence и текущие статусы

- **ID:** `PAOS-AUD-G3`
- **Название группы:** Достоверные evidence и текущие статусы
- **Описание группы:** Исправить freshness parser, пустой feedback и precedence текущего состояния относительно исторических receipts.
- **Техническое значение (для проекта):** Устранение ложноположительных и ложных missing-сигналов без нового status registry.
- **Продуктовое значение (для пользователя):** Понятно, что действительно проверено и какие действия ещё нужны; отсутствие данных не выглядит успехом.
- **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`; `plugins/product-agent-os/scripts/product_agent_os/self_learning_feedback.py`; `plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py`; `PLAN.md`; `RUNLOG.md`; `TEST.md`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** Unknown/empty/stale/conflicting cases имеют корректные результаты; текущие projections привязаны к source revision; история сохранена.
- **Зависимости и порядок:** Независима от G1/G2 по core modules. Общие control-plane pointers обновляет один владелец последовательно.
- **Предлагаемая ответственность:** plugin-runtime-builder; feedback — learning-loop-engineer; projections — graph-cockpit-engineer.

### Task `PAOS-AUD-F03`

- ID: `PAOS-AUD-F03`
- Task: **Название задачи:** Исправить freshness и классификацию source evidence
- Short description: **Описание задачи:** Поддержать используемые RU/EN date labels, строгую валидацию календарной даты и ссылки на локальный registry. Разделить official behavior, project contract и historical receipt; не считать простое упоминание Codex behavioral claim.
- Technical value: **Техническое значение (для проекта):** Меньше ложных missing/review результатов; date presence, freshness и semantic support остаются разными измерениями.
- Product value: **Продуктовое значение (для пользователя):** Пользователь видит реальные пробелы источников вместо массового списка ложных предупреждений.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`; `tests/product_agent_os/test_source_policy.py`; `docs/sources/registry.md`; `docs/sources/registry.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Форматы «Проверено YYYY-MM-DD.» и фактические EN формы распознаются; invalid/future/missing/stale cases различены по явной политике. 2) Registry reference разрешается безопасно внутри workspace; broken refs отражены как missing evidence. 3) Project-local и historical claims не получают ложный official verdict; дата/URL не меняют claim_supported на verified без semantic review.
- Group: PAOS-AUD-G3
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию G3 с проверками.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:47
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F17
- Source: F03
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Меньше ложных missing/review результатов; date presence, freshness и semantic support остаются разными измерениями. Missing host/product gates остаются открытыми.
- Verification gates: test_source_policy: formats, dates, registry resolution, claim classes; scan текущих docs с разбором изменения findings, docs checks. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; сохранить exact-host URL и secret protections; не превращать scanner в crawler. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и G3 execution evidence в этом плане.
- Next step: PAOS-AUD-G4; host/promotion gates отдельно.

#### Completion Report

- status: implemented
- what was done: RU/EN dates, strict freshness, bounded registry resolution и heuristic claim classes; URL/date не semantic proof.
- files touched / work locations: source_policy.py; test_source_policy.py; registry RU/EN; shared control-plane и owning plan
- technical value delivered: Убраны ложные date/source gaps при сохранении review boundaries.
- product value delivered: Source report различает отсутствие даты, устаревание и неподтверждённую семантику.
- actual implementation date and time: 09-11-2026 13:47
- verification evidence: G3 execution evidence выше: RED/GREEN, Full unittest: 1320 tests, 725.771 s, OK (skipped=1); final focused 78 tests OK; fixture 91/91; transcript 26/26; compatibility passed (local structure only).
- residual risks: Semantic source support требует ручной проверки; generated state не acceptance. Host/promotion вне scope.
- follow-up: PAOS-AUD-G4; сохранять revision pin и canonical B42/B45 ownership.

### Task `PAOS-AUD-F08`

- ID: `PAOS-AUD-F08`
- Task: **Название задачи:** Исправить положительный сигнал при отсутствии owner feedback
- Short description: **Описание задачи:** При нулевом числе допустимых owner labels возвращать insufficient_evidence. Раздельно учитывать валидность записи, human label count и тональность; public summary должен сохранять эту семантику.
- Technical value: **Техническое значение (для проекта):** Отсутствие evidence перестаёт выглядеть основанием для promotion.
- Product value: **Продуктовое значение (для пользователя):** Система не делает вывод об удовлетворённости пользователя, пока он не дал пригодную обратную связь.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/self_learning_feedback.py`; `tests/product_agent_os/test_self_learning_extensions.py`; `tests/product_agent_os/test_self_learning_state.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Empty ledger, missing ledger и wholly rejected records дают insufficient_evidence и не positive promotion signal. 2) Допустимые positive/negative/mixed labels сохраняют корректные denominator/counts и summary. 3) Candidate-only/manual-only safeguards не меняются; fixtures не содержат реальных персональных данных.
- Group: PAOS-AUD-G3
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию G3 с проверками.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:47
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-GAP-06
- Source: F08
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Отсутствие evidence перестаёт выглядеть основанием для promotion. Missing host/product gates остаются открытыми.
- Verification gates: RED на evaluate_satisfaction([]) и public summary; focused self-learning regression. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; изменение output enum требует проверки существующих consumers. Rollback — по общим правилам.
- Complexity: low
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: learning-loop-engineer; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и G3 execution evidence в этом плане.
- Next step: PAOS-AUD-G4; host/promotion gates отдельно.

#### Completion Report

- status: implemented
- what was done: Zero owner labels дают insufficient_evidence; sentiment/coverage/row validity разделены; malformed ledger безопасно отклоняется.
- files touched / work locations: self_learning_feedback.py; test_self_learning_state.py; test_self_learning_extensions.py; self-learning-loop RU/EN; shared control-plane и owning plan
- technical value delivered: Нет положительного evidence сигнала при пустых/rejected данных.
- product value delivered: Пользователь видит отсутствие feedback без ложного promotion signal.
- actual implementation date and time: 09-11-2026 13:47
- verification evidence: G3 execution evidence выше: RED/GREEN, Full unittest: 1320 tests, 725.771 s, OK (skipped=1); final focused 78 tests OK; fixture 91/91; transcript 26/26; compatibility passed (local structure only).
- residual risks: Semantic source support требует ручной проверки; generated state не acceptance. Host/promotion вне scope.
- follow-up: PAOS-AUD-G4; сохранять revision pin и canonical B42/B45 ownership.

### Task `PAOS-AUD-F16`

- ID: `PAOS-AUD-F16`
- Task: **Название задачи:** Определить precedence текущего статуса и исторических receipts
- Short description: **Описание задачи:** В существующих projections определить source ownership и precedence новых execution evidence. Добавить компактный current pointer с revision, не создавая второй registry. Различать task/run/verification/acceptance; при конфликте показывать conflict/unknown.
- Technical value: **Техническое значение (для проекта):** Воспроизводимое вычисление current state из owning sources вместо выбора первой записи Current.
- Product value: **Продуктовое значение (для пользователя):** Понятно, что уже выполнено, что ждёт проверки и какая задача следующая.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py`; `tests/product_agent_os/test_status_snapshot.py`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Historical planned плюс более новый execution receipt не возвращает выполненную задачу в planned. 2) Current result содержит источник/revision и различает implemented, verified, accepted; ambiguous/conflicting evidence не скрывается. 3) Исторические B42/B45 receipts сохранены; T23–T29 и machine statuses не переписаны из-за новой projection.
- Group: PAOS-AUD-G3
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию G3 с проверками.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 13:47
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F17
- Source: F16
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Воспроизводимое вычисление current state из owning sources вместо выбора первой записи Current. Missing host/product gates остаются открытыми.
- Verification gates: test_status_snapshot с historical/current/conflict cases; validate_task_state_consistency.py; docs checks. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; control-plane файлы общие — изменения только последовательно. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: graph-cockpit-engineer; control-plane writer один; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и G3 execution evidence в этом плане.
- Next step: PAOS-AUD-G4; host/promotion gates отдельно.

#### Completion Report

- status: implemented
- what was done: Revision-pinned PLAN pointer, scoped ownership и precedence dated receipts; task/run/verification/acceptance раздельны; dashboard caller подключён.
- files touched / work locations: status_snapshot.py; render_status_dashboard.py; run_fixture_eval.py; test_status_snapshot.py; PLAN.md; current-state RU/EN; shared control-plane и owning plan
- technical value delivered: Current projection связана с исходником; конфликт и drift не маскируются историей.
- product value delivered: Исторический planned не скрывает более позднее scoped execution evidence.
- actual implementation date and time: 09-11-2026 13:47
- verification evidence: G3 execution evidence выше: RED/GREEN, Full unittest: 1320 tests, 725.771 s, OK (skipped=1); final focused 78 tests OK; fixture 91/91; transcript 26/26; compatibility passed (local structure only).
- residual risks: Semantic source support требует ручной проверки; generated state не acceptance. Host/promotion вне scope.
- follow-up: PAOS-AUD-G4; сохранять revision pin и canonical B42/B45 ownership.

## PAOS-AUD-G4 — Простой ordinary route и компактные инструкции

- **ID:** `PAOS-AUD-G4`
- **Название группы:** Простой ordinary route и компактные инструкции
- **Описание группы:** Упростить вход в существующий ordinary route, убрать повторяющиеся инструкции и только измеренную лишнюю работу модулей.
- **Техническое значение (для проекта):** Минимальный task context, совместимость callers, меньшая нагрузка инструкций и повторных scans.
- **Продуктовое значение (для пользователя):** Меньше лишних вопросов, файлов и времени ожидания для обычной задачи при сохранении high-risk escalation.
- **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/state.py`; `plugins/product-agent-os/skills/`; `tests/AGENTS.md`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** Representative ordinary/edge/adversarial cases сохраняют корректность и границы; сокращение контекста/сканирования измерено; бездоказательный рефакторинг не выполняется.
- **Зависимости и порядок:** Intake F05 независим; изменяемый authoring scenario — после нужных G1 gates. F10 перед или совместно с F09; F15 — измерение сначала. Финальный baseline перед T32.
- **Предлагаемая ответственность:** plugin-runtime-builder; инструкции — lifecycle-orchestrator.

### Task `PAOS-AUD-F05`

- ID: `PAOS-AUD-F05`
- Task: **Название задачи:** Упростить вход в существующий ordinary route
- Short description: **Описание задачи:** Добавить минимальный явный intake/task-context на существующем public entrypoint. Объяснить и диагностировать legacy fallback; проверить callers до возможной смены default. Поддержать RU/EN/no-builder без нового onboarding на каждую задачу.
- Technical value: **Техническое значение (для проекта):** Использование готовых selectors через минимальный контракт вместо полного template registry по умолчанию.
- Product value: **Продуктовое значение (для пользователя):** Обычная задача начинается с небольшого числа нужных действий и не создаёт сотни лишних предложений файлов.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/state.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`; `tests/product_agent_os/test_infrastructure_renderer.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Small ordinary case выбирает согласованный минимальный artifact set; high-risk/unknown case сохраняет escalation. 2) RU/EN проекты и отсутствие builder не вызывают скрытого full onboarding. 3) Legacy callers имеют явный fallback receipt; default меняется только после compatibility regression и отдельного решения в задаче. 4) Нет автоматического target apply или повторной реализации T25–T29.
- Group: PAOS-AUD-G4
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию G4 с проверками.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 14:58
- Depends on: ORD-01–ORD-06 выполнены. Intake можно реализовать независимо; incremental report scenario использует завершённые F06/F18.
- Blocks: PAOS-AUD-F15, PAOS-AUD-F14, PAOS-GAP-06
- Source: F05; ORD-01–ORD-06 и T23–T29 уже реализованы.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Использование готовых selectors через минимальный контракт вместо полного template registry по умолчанию. Missing host/product gates остаются открытыми.
- Verification gates: Existing ORD positive/negative cases, CLI-to-selector-to-staging integration; сравнение artifact count и лишних вопросов с baseline. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; authority и readiness не выводятся только из task context. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и G4 execution evidence в этом плане.
- Next step: PAOS-AUD-G5; host/behavioral gates отдельно в G6.

#### Completion Report

- status: implemented
- what was done: Inline intake и явный fallback receipt в двух public CLIs; rich JSON и selectors сохранены. Empty/partial/mixed/escaping input rejected; empty ordinary stage manifest исправлен.
- files touched / work locations: task_routing.py; codex_runtime_runner/cli.py; infrastructure.py; render_infrastructure.py; test_codex_runtime_runner_cli.py; docs/control-plane и owning plan
- technical value delivered: Explicit ordinary path переиспользует действующие selectors без legacy inference.
- product value delivered: Небольшая docs задача работает без task.json и builder; 0 вместо 209 file proposals.
- actual implementation date and time: 09-11-2026 14:58
- verification evidence: G4 execution evidence выше. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only.
- residual risks: Source-level/local contracts проверены; fresh host discovery и live behavioral evaluation не выполнены, принадлежат G6. No provider/cache/activation/Git actions.
- follow-up: PAOS-AUD-G5; затем G6 host/behavioral gates на зафиксированном source.

### Task `PAOS-AUD-F09`

- ID: `PAOS-AUD-F09`
- Task: **Название задачи:** Сократить повторяющиеся skill instructions
- Short description: **Описание задачи:** Сохранить trigger, authority, inputs, outputs и stop в canonical SKILL.md; общие повторения и длинные conditional процедуры перенести в существующие references. Сначала снять baseline реально прочитанных файлов; не менять implicit invocation или installed cache.
- Technical value: **Техническое значение (для проекта):** Progressive disclosure без повторной загрузки одинаковых политик и искусственного увеличения context budget.
- Product value: **Продуктовое значение (для пользователя):** Меньше задержек и ненужных шагов при сохранении качества и предсказуемости результата.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/skills/`; `tests/product_agent_os/test_lifecycle_skills.py`; `tests/product_agent_os/test_validators.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Все 12 canonical skills сохраняют свои role boundaries и metadata; ссылки на references валидны. 2) Измерено сокращение реально загружаемого контекста на выбранных задачах, включая conditional reference reads. 3) Typical/edge/adversarial cases не теряют authority и необходимые gates; local checks и live behavioral evaluation обозначены отдельно. 4) No implicit enable, cache install или повышение context limit как замена сокращению.
- Group: PAOS-AUD-G4
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию G4 с проверками.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 14:58
- Depends on: PAOS-AUD-F10
- Blocks: PAOS-AUD-HOST-01
- Source: F09
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Progressive disclosure без повторной загрузки одинаковых политик и искусственного увеличения context budget. Missing host/product gates остаются открытыми.
- Verification gates: Skill metadata/links/contract tests, baseline/source digest comparison; behavioral comparison — через отдельный замороженный treatment, не смешивать с B45 compact-contract intervention. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; directory scope означает только 12 canonical skills и непосредственно используемые references; точный file manifest фиксируется до правки. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: lifecycle-orchestrator; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и G4 execution evidence в этом плане.
- Next step: PAOS-AUD-G5; host/behavioral gates отдельно в G6.

#### Completion Report

- status: implemented
- what was done: 93 conditional sections moved verbatim в existing role-specific reference; entrypoints сохраняют triggers/authority/I/O/stop. Metadata 12/12 unchanged; contract readers следуют relocation.
- files touched / work locations: 12 canonical SKILL.md; references/complexity-routing.md; validators.py; run_fixture_eval.py; test_lifecycle_skills.py; test_infrastructure_templates.py; docs/control-plane и owning plan
- technical value delivered: Selected read sets сокращены на 0.31–30.89%; baseline и conditional reads учтены.
- product value delivered: Меньше нерелевантного context при сохранении domain gates и явных gaps.
- actual implementation date and time: 09-11-2026 14:58
- verification evidence: G4 execution evidence выше. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only.
- residual risks: Source-level/local contracts проверены; fresh host discovery и live behavioral evaluation не выполнены, принадлежат G6. No provider/cache/activation/Git actions.
- follow-up: PAOS-AUD-G5; затем G6 host/behavioral gates на зафиксированном source.

### Task `PAOS-AUD-F10`

- ID: `PAOS-AUD-F10`
- Task: **Название задачи:** Устранить дублирование и конфликт instruction authority
- Short description: **Описание задачи:** Заменить устаревший tests/AGENTS.md короткими English test-specific правилами. В canonical skills отделить default read-only роль от явно авторизованной задачи; согласовать использование неизменившегося evidence. Не удалить намеренные role restrictions.
- Technical value: **Техническое значение (для проекта):** Единая иерархия инструкций; factual source authority не смешивается с instruction precedence.
- Product value: **Продуктовое значение (для пользователя):** Меньше противоречащих указаний и повторных запросов уже данного разрешения.
- Scope: **Затрагиваемые файлы:** `tests/AGENTS.md`; `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`; `plugins/product-agent-os/skills/completion-skeptic/SKILL.md`; `plugins/product-agent-os/skills/`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) tests/AGENTS.md на английском, содержит только уместные test-specific инструкции и корректную hierarchy. 2) Общие правила не конфликтуют с действующей root policy; read-only assurance и approval boundaries сохранены. 3) Проверено отсутствие дублирующих противоречий в остальных canonical skills; правятся только найденные случаи. 4) Static correction не объявляется runtime discovery proof; при таком claim нужен fresh-session receipt.
- Group: PAOS-AUD-G4
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию G4 с проверками.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 14:58
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F09
- Source: F10
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Единая иерархия инструкций; factual source authority не смешивается с instruction precedence. Missing host/product gates остаются открытыми.
- Verification gates: Static instruction comparison, skill contract tests; snapshot baseline; source loading проверяется отдельно при необходимости. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; глобальный AGENTS.md и настройки host не входят в scope. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: lifecycle-orchestrator; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и G4 execution evidence в этом плане.
- Next step: PAOS-AUD-G5; host/behavioral gates отдельно в G6.

#### Completion Report

- status: implemented
- what was done: tests/AGENTS.md стал кратким English test-specific файлом. Instruction hierarchy отделена от factual evidence; task-authorized team writing и read-only assurance различены; unchanged evidence сохраняет provenance.
- files touched / work locations: tests/AGENTS.md; 12 canonical SKILL.md; references/source-policy.md; references/handoff-contract.md; docs/control-plane и owning plan
- technical value delivered: tests/AGENTS.md: 8471→1483 bytes; убрано дублирование global rules и запрет на порученные team artifacts.
- product value delivered: Меньше противоречивых инструкций; approval и assurance boundaries сохранены.
- actual implementation date and time: 09-11-2026 14:58
- verification evidence: G4 execution evidence выше. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only.
- residual risks: Source-level/local contracts проверены; fresh host discovery и live behavioral evaluation не выполнены, принадлежат G6. No provider/cache/activation/Git actions.
- follow-up: PAOS-AUD-G5; затем G6 host/behavioral gates на зафиксированном source.

### Task `PAOS-AUD-F15`

- ID: `PAOS-AUD-F15`
- Task: **Название задачи:** Устранить измеренные повторные scans и дублирование модулей
- Short description: **Описание задачи:** На fixed synthetic workspace измерить повторные inventory/scans и стоимость ordinary route. Переиспользовать immutable inventory snapshot и выделять detector/render contracts лишь там, где измерения и callers подтверждают пользу. Размер файлов сам по себе не основание для правки.
- Technical value: **Техническое значение (для проекта):** Снижение повторной работы и связности без новой БД, workflow engine или provider abstraction.
- Product value: **Продуктовое значение (для пользователя):** Быстрее анализ проекта и меньше противоречивых выводов между представлениями.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_metrics.py`; `tests/product_agent_os/test_methodology_audit.py`; `tests/product_agent_os/test_infrastructure_renderer.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) До изменения записан baseline scan counts/runtime/output на одинаковом fixture и окружении. 2) После изменения output contracts и safety boundaries сохранены; уменьшение повторных операций измерено. 3) Если существенного дублирования не подтверждено, задача закрывается accepted_gap с обоснованием без рефакторинга. 4) Выделение нового модуля допускается только после фиксации конкретной границы и собственного test coverage; live semantic/provider claims не добавляются.
- Group: PAOS-AUD-G4
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на полную локальную реализацию G4 с проверками.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 14:58
- Depends on: PAOS-AUD-F05
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: F15
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Снижение повторной работы и связности без новой БД, workflow engine или provider abstraction. Missing host/product gates остаются открытыми.
- Verification gates: Characterization existing tests, deterministic output comparison, bounded repeated timing/scan measurement; расширение file scope только по выявленным callers. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; условная оптимизация, не обязательное переписывание больших модулей. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и G4 execution evidence в этом плане.
- Next step: PAOS-AUD-G5; host/behavioral gates отдельно в G6.

#### Completion Report

- status: implemented
- what was done: Внутри analyze_workspace scope detector использует один immutable inventory snapshot. Public API свежий на каждый вызов; различающиеся methodology/first-run inventories не объединены.
- files touched / work locations: discovery.py; test_methodology_audit.py; docs/control-plane и owning plan
- technical value delivered: Discovery inventory calls 2→1, identical output; median 114.448→103.959 ms на fixed synthetic fixture.
- product value delivered: Меньше повторной работы без нового cache/framework и без потери свежести.
- actual implementation date and time: 09-11-2026 14:58
- verification evidence: G4 execution evidence выше. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only.
- residual risks: Source-level/local contracts проверены; fresh host discovery и live behavioral evaluation не выполнены, принадлежат G6. No provider/cache/activation/Git actions.
- follow-up: PAOS-AUD-G5; затем G6 host/behavioral gates на зафиксированном source.

## PAOS-AUD-G5 — Документация, offline tooling и актуальный site

- **ID:** `PAOS-AUD-G5`
- **Название группы:** Документация, offline tooling и актуальный site
- **Описание группы:** Исправить offline installer, обновить package README и синхронизировать RU/EN, registry и generated site после локальных правок.
- **Техническое значение (для проекта):** Воспроизводимый offline command contract и согласованный source/build output.
- **Продуктовое значение (для пользователя):** Пользователь следует актуальному стартовому маршруту и получает одинаковые инструкции на русском и английском.
- **Затрагиваемые файлы:** `tools/docs_install.ps1`; `plugins/product-agent-os/README.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `site/`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** Offline path не формирует сетевых install-команд; README/examples согласованы; strict build, RU/EN links/anchors и Mermaid check проходят; публикации нет.
- **Зависимости и порядок:** F13 можно раньше. Документацию обновлять вместе с каждой группой; итоговый F14/F17 после G1–G4. После G6 обновлять только новые receipts и затронутые страницы.
- **Предлагаемая ответственность:** docs-maintainer; installer — plugin-runtime-builder.

### Task `PAOS-AUD-F13`

- ID: `PAOS-AUD-F13`
- Task: **Название задачи:** Обеспечить offline contract документационного installer
- Short description: **Описание задачи:** Убрать unconditional pip upgrade до offline branch либо провести весь install через указанный wheelhouse. Проверить формирование команд через stub, сохранив project-local tooling.
- Technical value: **Техническое значение (для проекта):** Offline режим действительно не строит сетевых package-install команд.
- Product value: **Продуктовое значение (для пользователя):** В закрытой сети установка не зависает на неожиданном обращении к package index.
- Scope: **Затрагиваемые файлы:** `tools/docs_install.ps1`; `tests/product_agent_os/test_product_agent_os_docs.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) OfflineWheelhouse path исключает index/network для всех pip вызовов, включая upgrade/bootstrap. 2) Online mode остаётся явным; отсутствие нужного wheel даёт понятную локальную ошибку. 3) Command-contract test не устанавливает зависимости и не меняет глобальную среду.
- Group: PAOS-AUD-G5
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на реализацию G5 с локальными проверками и сборкой.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 15:24
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F17
- Source: F13
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Offline режим действительно не строит сетевых package-install команд. Missing host/product gates остаются открытыми.
- Verification gates: Stubbed installer command inspection + existing docs tests; настоящая установка не требуется для локального command contract. Общие gates — TEST.md и правила выше.
- Risks / approval gates: low; dependency installation вне текущей задачи планирования и отдельно согласуется при необходимости. Rollback — по общим правилам.
- Complexity: low
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: G6; host/behavioral/owner acceptance gates остаются отдельными.

#### Completion Report

- status: implemented
- what was done: Offline pip routing исправлен; online upgrade изолирован, directory/error guards и command-stub regression.
- files touched / work locations: tools/docs_install.ps1; tests/product_agent_os/test_product_agent_os_docs.py; control-plane и owning plan.
- technical value delivered: Проверяемый local contract без скрытой сетевой установки или activation claims.
- product value delivered: Актуальный короткий старт и воспроизводимая локальная документация.
- actual implementation date and time: 09-11-2026 15:24
- verification evidence: G5 execution evidence выше; 105 docs tests, strict build, site integrity и 93 Mermaid renders passed.
- residual risks: Actual install/host activation/publication не выполнялись; generated site не является source of truth.
- follow-up: PAOS-AUD-G6 по его собственным gates.


### Task `PAOS-AUD-F14`

- ID: `PAOS-AUD-F14`
- Task: **Название задачи:** Обновить package README и стартовый маршрут
- Short description: **Описание задачи:** Сделать короткий start path с explicit skill invocation и ordinary task context. Согласовать MCP example, supported surfaces и manifest variants; убрать исторические counts из актуального summary, сохранив ссылки на owning evidence.
- Technical value: **Техническое значение (для проекта):** Package entrypoint соответствует public CLI и текущим compatibility contracts.
- Product value: **Продуктовое значение (для пользователя):** Новый пользователь начинает с рабочего минимального пути и понимает ограничения установки.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/README.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Примеры args/JSON соответствуют реализации и проходят локальные syntax/CLI contract checks. 2) Виден supported/unsupported/not_verified; explicit-only skills вызываются явно; ordinary route не скрыт за full generation. 3) Historical receipts доступны по ссылкам и не выданы за текущий запуск; неизвестные distribution данные не придуманы.
- Group: PAOS-AUD-G5
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на реализацию G5 с локальными проверками и сборкой.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 15:24
- Depends on: PAOS-AUD-F01, PAOS-AUD-F02, PAOS-AUD-F04, PAOS-AUD-F05
- Blocks: PAOS-AUD-F17
- Source: F14
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Package entrypoint соответствует public CLI и текущим compatibility contracts. Missing host/product gates остаются открытыми.
- Verification gates: Docs tests/check_docs, example syntax, локальная проверка CLI help/dry-run; без MCP execution. Общие gates — TEST.md и правила выше.
- Risks / approval gates: low; не заявлять activation на основании source tests. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: docs-maintainer; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: G6; host/behavioral/owner acceptance gates остаются отдельными.

#### Completion Report

- status: implemented
- what was done: Короткий explicit start, ordinary task intake, актуальный MCP JSON и support matrix; archive receipts отделены.
- files touched / work locations: plugins/product-agent-os/README.md; current-state RU/EN; registry RU/EN; control-plane и owning plan.
- technical value delivered: Проверяемый local contract без скрытой сетевой установки или activation claims.
- product value delivered: Актуальный короткий старт и воспроизводимая локальная документация.
- actual implementation date and time: 09-11-2026 15:24
- verification evidence: G5 execution evidence выше; 105 docs tests, strict build, site integrity и 93 Mermaid renders passed.
- residual risks: Actual install/host activation/publication не выполнялись; generated site не является source of truth.
- follow-up: PAOS-AUD-G6 по его собственным gates.


### Task `PAOS-AUD-F17`

- ID: `PAOS-AUD-F17`
- Task: **Название задачи:** Синхронизировать RU/EN и пересобрать локальный site
- Short description: **Описание задачи:** Согласовать изменённые user guides и registry; проверить затронутые Mermaid diagrams. После локальных changes пересобрать site существующими project-local средствами, проверить routes, links, anchors и диаграммы. После host receipts обновлять только новые claims.
- Technical value: **Техническое значение (для проекта):** Generated site воспроизводимо соответствует проверенным source files.
- Product value: **Продуктовое значение (для пользователя):** На русском и английском доступны одинаково актуальные инструкции и рабочая навигация.
- Scope: **Затрагиваемые файлы:** `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`; `docs/codex/models-and-reasoning.md`; `docs/codex/models-and-reasoning.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `docs/diagrams/`; `mkdocs.yml`; `site/`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Ручная semantic parity затронутых RU/EN пар и Source status актуальны; 10 English-original plans не объявляются missing translations. 2) Docs checks и strict MkDocs build проходят; internal routes/links/anchors проверены по generated output. 3) Затронутые Mermaid diagrams успешно разобраны/отрендерены разрешённым инструментом; отсутствие runtime render явно оставляет соответствующий gate открытым. 4) Site receipt связан с source revision; сайт не опубликован; dependencies/automation/hooks не активированы автоматически.
- Group: PAOS-AUD-G5
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на реализацию G5 с локальными проверками и сборкой.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 15:24
- Depends on: PAOS-AUD-F03, PAOS-AUD-F13, PAOS-AUD-F14, PAOS-AUD-F16 Финальная local сборка после всех фактически выполненных G1–G4 изменений, включая F09/F10/F15; host receipts обновляются отдельной малой синхронизацией.
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: F17
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Generated site воспроизводимо соответствует проверенным source files. Missing host/product gates остаются открытыми.
- Verification gates: 100-case docs suite в текущем составе, check_docs, strict MkDocs, generated link/anchor check и Mermaid rendering при точной authority; git diff --check. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; mkdocs.yml/diagrams правятся только если затронуты новой документацией; browser/server/install/publication не следуют из сохранения плана. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: docs-maintainer; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: G6; host/behavioral/owner acceptance gates остаются отдельными.

#### Completion Report

- status: implemented
- what was done: RU/EN semantic review, strict site rebuild, links/anchors/search и 93 Mermaid renders.
- files touched / work locations: current-state RU/EN; registry RU/EN; site/; source hashes и render receipts; control-plane и owning plan.
- technical value delivered: Проверяемый local contract без скрытой сетевой установки или activation claims.
- product value delivered: Актуальный короткий старт и воспроизводимая локальная документация.
- actual implementation date and time: 09-11-2026 15:24
- verification evidence: G5 execution evidence выше; 105 docs tests, strict build, site integrity и 93 Mermaid renders passed.
- residual risks: Actual install/host activation/publication не выполнялись; generated site не является source of truth.
- follow-up: PAOS-AUD-G6 по его собственным gates.


## PAOS-AUD-G6 — Проверка GPT-6, host activation и пользовательской пользы

- **ID:** `PAOS-AUD-G6`
- **Название группы:** Проверка GPT-6, host activation и пользовательской пользы
- **Описание группы:** Продолжить существующие T30–T34 и оставшиеся GAP gates; отдельно доказать local readiness, host behavior, качество treatment и полезность ordinary flow.
- **Техническое значение (для проекта):** Раздельные воспроизводимые evidence для конфигурации, активации, качества и acceptance.
- **Продуктовое значение (для пользователя):** Улучшение оценивается по успешной работе и затратам пользователя, а не по наличию GPT-6 ID или числу тестов.
- **Затрагиваемые файлы:** `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`; `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`; `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; `EVALS.md`; `RUNLOG.md`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** T30–T34 закрываются только по своим canonical gates; fresh-host receipts привязаны к версиям/хешам; pilot имеет owner acceptance; missing evidence сохраняет no-go/partial.
- **Зависимости и порядок:** T30/T31 готовить параллельно локальным fixes по независимым файлам; T32 после стабильного baseline, T33 после T32, T34 только после T33 и exact approval. Host gates после итоговых G1/G2.
- **Предлагаемая ответственность:** Роли существующих T30–T34; host — tester; pilot — product-manager.

### Task `B45-CQRR-T30`

- ID: `B45-CQRR-T30`
- Task: **Название задачи:** Implement an independent blinded reviewer contract
- Short description: **Описание задачи:** Реализовать контракт независимого reviewer для baseline/treatment patches без arm labels и primary self-scores. Reviewer допускается только после valid deterministic pair evidence; critical findings имеют приоритет над средними оценками.
- Technical value: **Техническое значение (для проекта):** Независимая проверка качества отделена от самооценки generating model.
- Product value: **Продуктовое значение (для пользователя):** Ошибки корректности, безопасности и лишняя сложность не скрываются хорошим средним баллом.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/assets/templates/evals/code-quality-reviewer-rubric.json` (proposed new); `plugins/product-agent-os/scripts/codex_runtime_runner/reviewer_contract.py` (proposed new); `tests/product_agent_os/test_batch45_code_quality_reviewer.py` (proposed new); `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Reviewer input не содержит baseline/treatment labels и primary self-scores. 2) Verdict blocked до валидного deterministic pair evidence. 3) Critical correctness/security/data-loss/regression findings перекрывают averages.
- Group: PAOS-AUD-G6
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: Нет новых обязательных задач этого плана. B45-CQRR-T29 — локально выполнена.
- Blocks: B45-CQRR-T32, B45-CQRR-T33
- Source: Существующая B45-CQRR-T30; canonical title/depends_on/acceptance сохранены из task-group JSON. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Независимая проверка качества отделена от самооценки generating model. Missing host/product gates остаются открытыми.
- Verification gates: Blinding, invalid pair gate и critical override tests на synthetic pairs. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; live reviewer call требует отдельного exact approval, локальная реализация его не разрешает. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: architect; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Review exact approval packets; execute only the separately authorized runtime scope.

#### Completion Report

- status: implemented
- what was done: Blinded reviewer module/rubric and negative gates implemented.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 execution evidence above; A07 readiness receipt and current-run logs.
- residual risks: No actual model/reviewer calls, fresh-host activation or owner pilot acceptance.
- follow-up: Exact owner approval; preserve no-go until each remaining gate passes.


### Task `B45-CQRR-T31`

- ID: `B45-CQRR-T31`
- Task: **Название задачи:** Build a representative multi-stack held-out corpus
- Short description: **Описание задачи:** Подготовить 12–16 sanitized/synthetic задач минимум четырёх stack families и пяти risk classes. Включить small change, legacy bug, boundary, unnecessary-abstraction и performance cases, а также решения через reuse/config/delete/no-new-code. Freeze до просмотра treatment outputs.
- Technical value: **Техническое значение (для проекта):** Проверка на репрезентативном отложенном наборе вместо подгонки под внутренние восемь задач.
- Product value: **Продуктовое значение (для пользователя):** Оценка ближе к разным реальным проектам и не поощряет ненужное написание кода.
- Scope: **Затрагиваемые файлы:** `tests/fixtures/product_agent_os/batch45/code-quality-corpus/` (proposed new); `docs/superpowers/specs/batch45-code-quality-heldout-corpus.json` (proposed new); `tests/product_agent_os/test_batch45_code_quality_corpus.py` (proposed new); `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Представлены минимум четыре stack families и пять risk classes; 12–16 задач с проверяемым ожидаемым результатом. 2) Корпус заморожен с hashes до inspection treatment; последующая настройка под результат запрещена. 3) Нет secrets/private source/raw chats/customer data/absolute user paths. 4) Присутствуют случаи правильного отказа от нового кода, reuse, config и deletion.
- Group: PAOS-AUD-G6
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: Нет новых обязательных задач этого плана. B45-CQRR-T27 и T29 — локально выполнены; независима от T30.
- Blocks: B45-CQRR-T32, B45-CQRR-T33
- Source: Существующая B45-CQRR-T31. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Проверка на репрезентативном отложенном наборе вместо подгонки под внутренние восемь задач. Missing host/product gates остаются открытыми.
- Verification gates: Schema, privacy/secret scan, difficulty/risk matrix и hash freeze validation. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; не использовать неразрешённый target source для наполнения корпуса. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: tester; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Review exact approval packets; execute only the separately authorized runtime scope.

#### Completion Report

- status: implemented
- what was done: 12 synthetic tasks frozen; 4 stacks, 7 risk classes; all reference/seeded outcomes verified.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 execution evidence above; A07 readiness receipt and current-run logs.
- residual risks: No actual model/reviewer calls, fresh-host activation or owner pilot acceptance.
- follow-up: Exact owner approval; preserve no-go until each remaining gate passes.


### Task `B45-CQRR-T32`

- ID: `B45-CQRR-T32`
- Task: **Название задачи:** Freeze an isolated treatment and executable prompt contract
- Short description: **Описание задачи:** Зафиксировать exact baseline/treatment prompt/context templates. В первичном сравнении меняется только compact pre-edit contract; reviewer assistance и comment advisory остаются отдельными later factors. Итоговые skill/route changes G4 должны быть одинаковы в обеих arms или исключены из comparison.
- Technical value: **Техническое значение (для проекта):** Причина результата измерима: один фактор вместо одновременной смены модели, effort, prompts и маршрута.
- Product value: **Продуктовое значение (для пользователя):** Решение об улучшении основано на проверяемом эффекте, а не на впечатлении от новой модели.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/assets/templates/evals/code-quality-baseline-prompt.md` (proposed new); `plugins/product-agent-os/assets/templates/evals/code-quality-treatment-prompt.md` (proposed new); `docs/superpowers/specs/batch45-code-quality-eval-design.json` (proposed new); `tests/product_agent_os/test_batch45_code_quality_eval_design.py` (proposed new); `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Baseline/treatment используют одинаковые model, effort, runner, timeout, tools и corpus. 2) Ровно один planned intervention различается; точные templates/context digests воспроизводимы без private raw data. 3) Full research/checklist не вставлен в каждый generation prompt. 4) Изменение model/effort или отдельное skill-shortening treatment требует нового изолированного design, не приписывается этому сравнению.
- Group: PAOS-AUD-G6
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: B45-CQRR-T30, B45-CQRR-T31 B45-CQRR-T25 выполнена; freeze после стабильного baseline затронутых G1–G4. Не объявлять внешнюю sequencing рекомендацию изменением canonical depends_on.
- Blocks: B45-CQRR-T33
- Source: Существующая B45-CQRR-T32. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Причина результата измерима: один фактор вместо одновременной смены модели, effort, prompts и маршрута. Missing host/product gates остаются открытыми.
- Verification gates: Prompt/context diff, digest reproducibility и no-extra-variable contract tests. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; не корректировать prompts после просмотра held-out treatment outputs. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: architect; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Review exact approval packets; execute only the separately authorized runtime scope.

#### Completion Report

- status: implemented
- what was done: Isolated prompts, deterministic compiler and versioned schema frozen; no generation calls.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 execution evidence above; A07 readiness receipt and current-run logs.
- residual risks: No actual model/reviewer calls, fresh-host activation or owner pilot acceptance.
- follow-up: Exact owner approval; preserve no-go until each remaining gate passes.


### Task `B45-CQRR-T33`

- ID: `B45-CQRR-T33`
- Task: **Название задачи:** Run the local promotion-readiness preflight
- Short description: **Описание задачи:** Проверить локальную воспроизводимость executable schema, normalization, deterministic metrics, reviewer gate, frozen corpus и isolated prompt contract. Сохранить readiness evidence до подготовки нового live approval packet.
- Technical value: **Техническое значение (для проекта):** Локальные дефекты контрактов выявлены до затрат на provider/model/reviewer вызовы.
- Product value: **Продуктовое значение (для пользователя):** Меньше бесполезных запусков и более понятное решение о готовности к эксперименту.
- Scope: **Затрагиваемые файлы:** `docs/superpowers/specs/batch45-code-quality-local-readiness.json` (proposed new); `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Все valid fixtures проходят, все invalid дают ожидаемый failure class. 2) Seeded faults обнаруживаются предназначенным тестом/метрикой. 3) Blinding/reviewer gate работают на synthetic pairs; corpus/prompts hashes воспроизводимы. 4) Нет provider/model/reviewer calls; любой обязательный failed/missing gate сохраняет no-go.
- Group: PAOS-AUD-G6
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: B45-CQRR-T30, B45-CQRR-T31, B45-CQRR-T32 B45-CQRR-T24, T28, T29 выполнены.
- Blocks: B45-CQRR-T34
- Source: Существующая B45-CQRR-T33. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Локальные дефекты контрактов выявлены до затрат на provider/model/reviewer вызовы. Missing host/product gates остаются открытыми.
- Verification gates: Focused contract/strategy tests, seeded-fault replay, freeze checks, docs/source registry checks и diff hygiene. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; local readiness не равна behavioral promotion или product acceptance. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: completion-skeptic; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Review exact approval packets; execute only the separately authorized runtime scope.

#### Completion Report

- status: implemented
- what was done: Local preflight passed; A07 readiness receipt saved.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 execution evidence above; A07 readiness receipt and current-run logs.
- residual risks: No actual model/reviewer calls, fresh-host activation or owner pilot acceptance.
- follow-up: Exact owner approval; preserve no-go until each remaining gate passes.


### Task `B45-CQRR-T34`

- ID: `B45-CQRR-T34`
- Task: **Название задачи:** Prepare, execute and decide a new promotion eval only after exact approval
- Short description: **Описание задачи:** После T33 подготовить конкретный reviewable approval packet; только после exact owner approval выполнить frozen same-model comparison. Reviewer вызывается после valid pairs. Решение promotion/no-go основывается на deterministic evidence и независимых findings.
- Technical value: **Техническое значение (для проекта):** Связанные с checked state quality/cost/latency evidence для выбранной GPT-6 конфигурации.
- Product value: **Продуктовое значение (для пользователя):** Продвигается только улучшение с приемлемой корректностью, затратами и временем ответа.
- Scope: **Затрагиваемые файлы:** `docs/superpowers/specs/batch45-code-quality-eval-approval-packet.json` (proposed new); `docs/superpowers/specs/batch45-code-quality-eval-results.json` (proposed new); `docs/superpowers/specs/batch45-code-quality-promotion-decision.json` (proposed new); `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `EVALS.md`; `RUNLOG.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Exact approval задаёт model, effort, call cap, timeout, cost, retention и reviewer policy до вызовов. 2) Все учитываемые pairs schema-valid и имеют deterministic acceptance; reviewer выполнен без unresolved critical findings. 3) Latency/token/cost/performance за frozen tolerance блокируют promotion либо имеют отдельное owner-accepted исключение. 4) При incomplete/invalid/mixed evidence остаётся no-go; raw private outputs не сохраняются. 5) Same-model результат не объявляется доказательством превосходства всей GPT-6 family; model/effort changes сравниваются отдельно.
- Group: PAOS-AUD-G6
- Status: blocked
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: B45-CQRR-T33
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: Существующая B45-CQRR-T34; behavioral часть F04. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Связанные с checked state quality/cost/latency evidence для выбранной GPT-6 конфигурации. Missing host/product gates остаются открытыми.
- Verification gates: Approval preflight, sanitized results validation, independent reviewer evidence, retention/no-unapproved-actions checks, control-plane sync. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; approval_required_not_started; сохранение этого плана не разрешает live calls. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: release-operator; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Resolve recorded runtime/host evidence gap within approved bounds; owner acceptance only after actual pilot results.

#### Completion Report

- status: blocked
- what was done: Owner approved execution; runtime/cache/fresh-host preflight performed, exact observations in approved execution receipt.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 approved execution receipt and approved-*.log; previous A07 remains local-only evidence.
- residual risks: Technical runtime/host gaps remain; pilots not_run; owner acceptance absent.
- follow-up: Resolve observed technical blocker; do not request the already granted packet authority again.


### Task `PAOS-AUD-HOST-01`

- ID: `PAOS-AUD-HOST-01`
- Task: **Название задачи:** Закрыть оставшийся GAP-03 M06: exposure и invocation выбранного host
- Short description: **Описание задачи:** На выбранной поддерживаемой surface проверить canonical/installed source provenance, exposure и явный вызов skill. Записать client/surface, hashes, observed model при доступном receipt. Если нужен cache update, сначала подготовить конкретный preview/rollback и получить точную authority.
- Technical value: **Техническое значение (для проекта):** Связь source package с реально загруженными host компонентами.
- Product value: **Продуктовое значение (для пользователя):** Пользователь знает, что установленные skills соответствуют исправленной версии и вызываются ожидаемым способом.
- Scope: **Затрагиваемые файлы:** `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `TEST.md`; `RUNLOG.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Выбранный host/surface поддерживается; version/source/cache digests и invocation evidence связаны с проверенным состоянием. 2) Configured model отдельно от observed; при отсутствии model receipt поле остаётся not_verified. 3) Explicit-only skill не объявляется implicit; source/cache mismatch имеет явное решение и не скрывается. 4) GAP-03 M06 закрывается только своим evidence; parent статус обновляется в owning плане, а не независимом registry.
- Group: PAOS-AUD-G6
- Status: blocked
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: PAOS-AUD-F01, PAOS-AUD-F02, PAOS-AUD-F04, PAOS-AUD-F09
- Blocks: Fresh-session native exposure claim; не блокирует три одобренных current-project pilots PAOS-GAP-06
- Source: GAP-03 M06; F02/F04/F09. ID — адрес конкретного этапа этого плана, не новая замена parent GAP-03.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Связь source package с реально загруженными host компонентами. Missing host/product gates остаются открытыми.
- Verification gates: Ограниченный fresh-host exposure/invocation receipt; exact commands/target выбираются после host scope, не выдумываются в общем плане. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; installation/cache/trust/provider actions имеют отдельную точную authority. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: tester; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Resolve recorded runtime/host evidence gap within approved bounds; owner acceptance only after actual pilot results.

#### Completion Report

- status: blocked
- what was done: Owner approved execution; runtime/cache/fresh-host preflight performed, exact observations in approved execution receipt.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 approved execution receipt and approved-*.log; previous A07 remains local-only evidence.
- residual risks: Technical runtime/host gaps remain; pilots not_run; owner acceptance absent.
- follow-up: Resolve observed technical blocker; do not request the already granted packet authority again.


### Task `PAOS-AUD-HOST-02`

- ID: `PAOS-AUD-HOST-02`
- Task: **Название задачи:** Закрыть оставшиеся GAP-05 и fresh-host lifecycle gates
- Short description: **Описание задачи:** После финальных source hashes проверить фактическую загрузку hooks, positive/negative сценарии, report-authoring и независимость новых чатов. Отдельно проверить generated target route на точном разрешённом disposable target. Сохранить различие current-host observation и fresh-host evidence.
- Technical value: **Техническое значение (для проекта):** Подтверждение активного исправленного пути и отсутствия маскирующего legacy fallback.
- Product value: **Продуктовое значение (для пользователя):** Новые чаты не мешают друг другу; разрешённый отчёт сохраняется, чужие/выходящие за scope записи блокируются.
- Scope: **Затрагиваемые файлы:** `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`; `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`; `TEST.md`; `RUNLOG.md`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Receipt содержит version, exact definition/source hashes, выбранный config path, trust observation и workspace scope. 2) Fresh positive и безопасный negative probe подтверждены output/absence evidence; filesystem failure не выдан за hook denial. 3) Два новых session-aware чата изолированы; чужой marker и старый shared marker не авторизуют mutation. 4) Generated config действительно загружается; ранее неактивный mirror/legacy route не маскирует результат. 5) Report create/update проходит только в согласованных границах; изменение hashes после проверки вновь открывает затронутый gate.
- Group: PAOS-AUD-G6
- Status: blocked
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 на G6; local implementation authorized, exact live/host/owner gates remain separate.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 16:04
- Depends on: PAOS-AUD-F06, PAOS-AUD-F12, PAOS-AUD-F18 Если активируются rules из F11, effective-policy probe оформляется отдельным ограниченным подпунктом с собственной authority.
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: GAP-05; F06/F12/F18; PAOS-SESSION-LIFECYCLE-2026-11-09. ID — объединённый verification этап, не повторная реализация parent задач.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Подтверждение активного исправленного пути и отсутствия маскирующего legacy fallback. Missing host/product gates остаются открытыми.
- Verification gates: Fresh-host bounded positive/negative receipts и source hashes; synthetic tests повторять только по изменённому контракту. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; actual target writes, hook trust/definitions и fresh-host execution требуют точного разрешения; permission не выводится из plan status. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: tester; security review read-only; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Resolve recorded runtime/host evidence gap within approved bounds; owner acceptance only after actual pilot results.

#### Completion Report

- status: blocked
- what was done: Owner approved execution; runtime/cache/fresh-host preflight performed, exact observations in approved execution receipt.
- files touched / work locations: Named task artifacts; G6 evidence, owning plans and control-plane.
- technical value delivered: Frozen reproducible local contracts and explicit missing runtime evidence.
- product value delivered: Reviewable next action without invented activation, quality or acceptance.
- actual implementation date and time: 09-11-2026 16:04
- verification evidence: G6 approved execution receipt and approved-*.log; previous A07 remains local-only evidence.
- residual risks: Technical runtime/host gaps remain; pilots not_run; owner acceptance absent.
- follow-up: Resolve observed technical blocker; do not request the already granted packet authority again.


### Task `PAOS-GAP-06`

- ID: `PAOS-GAP-06`
- Task: **Название задачи:** Проверить ordinary user outcomes через существующие B39/B44 manual packets
- Short description: **Описание задачи:** Сначала согласовать 3–5 representative задач и конкретные targets: bugfix, docs, legacy, no-new-code, boundary change. Начать с одного bounded ordinary pilot, затем продолжить выбранный набор. Измерять время до полезного результата, лишние вопросы/артефакты, повторные проверки, correctness и owner intervention.
- Technical value: **Техническое значение (для проекта):** Проверка сквозного пользовательского пути после локальных contract gates.
- Product value: **Продуктовое значение (для пользователя):** Подтверждение, что Product-Agent OS действительно уменьшает усилия пользователя и даёт пригодный результат.
- Scope: **Затрагиваемые файлы:** `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; `prod_test.md`; `RUNLOG.md`; `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) До запуска согласованы tasks/targets/allowed actions/rollback и baseline measurements. 2) Есть per-task outcome, owner feedback/acceptance и сохранённые failed cases; один pilot не объявляется закрытием полного representative набора. 3) Выявленные улучшения идут в существующий manual candidate loop; нет automatic promotion/schedules/auto-apply. 4) prod_test.md меняется только если действительно создаётся evidence его B39 family; прочая история не переписывается.
- Group: PAOS-AUD-G6
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Владелец разрешил три пилота из текущего проекта в host-target; HOST-01 dependency снята, activation отдельно.
- Validator target: detailed task blocks
- Date and time of task implementation: 09-11-2026 17:11
- Depends on: ORD-06 и локальные F05/F08 выполнены; HOST-01/HOST-02 и T34 не являются gates этих трёх synthetic local pilots.
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: Существующая PAOS-GAP-06 из ordinary implementation plan; canonical scope сохранён. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Проверка сквозного пользовательского пути после локальных contract gates. Missing host/product gates остаются открытыми.
- Verification gates: Фактические baseline/final checks, source hashes и file inventories в pilot-results; обязательные docs/matrix/state gates; owner feedback отдельно.
- Risks / approval gates: Текущий local pilot scope явно разрешён; owner acceptance pending; fresh-session/provider/browser/Git не входят в этот маршрут. Rollback по initial_source proposal; receipts сохранить.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: product-manager; evidence — learning-loop-engineer; acceptance — пользователь; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Named local task artifacts and G6 evidence; live/host/owner receipts remain pending.
- Next step: Приёмка трёх результатов пользователем; fresh-session activation остаётся самостоятельной открытой задачей.

#### Completion Report

- status: in_progress
- what was done: Три одобренных пилота выполнены в host-target/pilots из текущей сессии; HOST-01 dependency снята по решению владельца.
- files touched / work locations: candidate.py, candidate.json, неизменный candidate.cjs и три receipt.json; pilot proposal/results; owning plans и control-plane.
- technical value delivered: Наблюдаемый bug RED/GREEN; config JSON/invariant checks; no-new-code SHA-256 preservation.
- product value delivered: Три проверяемых результата для owner acceptance, без лишних вопросов в ходе пилотов.
- actual implementation date and time: 09-11-2026 17:11
- verification evidence: docs/superpowers/specs/paos-aud-g6-pilot-results.json; python -B .docs-tools/reports/paos-aud-g6/run_pilots.py baseline и verify, оба exit 0; внутри baseline ожидаемый bug/config assertion exit 1.
- residual risks: needs_user_acceptance; feedback/acceptance null. Synthetic cases не доказывают массовую полезность; fresh-session activation и T34 отдельно открыты.
- follow-up: Пользователь принимает или отклоняет каждый результат; findings остаются manual candidates.

## PAOS-AUD-G7 — Качество реализации, архитектурная простота и достаточная проверка

- **ID:** `PAOS-AUD-G7`
- **Название группы:** Качество реализации, архитектурная простота и достаточная проверка
- **Описание группы:** Внедрить проверяемые улучшения существующих механизмов PAOS по анализу Ponytail и аналогов: полное минимальное решение, границы ответственности, полезные проверки, доказательный review и оценка стоимости следующего изменения.
- **Техническое значение (для проекта):** Уменьшить неявную связанность, дублирование правил и ложные process gates; переиспользовать текущие selectors, inventory, test/eval infrastructure.
- **Продуктовое значение (для пользователя):** Получать пригодный результат с меньшими затратами на лишний код, вопросы, документы и повторные проверки без ухудшения корректности и безопасности.
- **Затрагиваемые файлы:** Exact scope каждой карточки ниже; shared docs/control-plane синхронизируются одним writer. `AGENTS.md`, hooks definitions/trust, installed cache, frozen T34 inputs и чужие workspaces исключены, если поздняя точная authority не изменит границу.
- **Критерии приёмки группы:** T01–T06 имеют применимые current-run contract/regression evidence; T07 имеет frozen separate design; T08 имеет фактические результаты и owner decision. Открытая поведенческая оценка оставляет группу partially_verified. Статические проверки текста не доказывают качество генерации или fresh-session loading.
- **Зависимости и порядок:** T01 → T02/T03/T05/T06 → T07 → T08. T04 — независимый ранний security-sensitive fix; его live activation имеет отдельный HOST-02 gate. Shared files T01/T02/T05 и T03/T07 редактировать последовательно. Незавершённые G6 acceptance/HOST/T34 не создают искусственный общий запрет на локальную G7.
- **Предлагаемая ответственность:** Один исполнитель по умолчанию; named roles ниже описывают ownership, не разрешение автоматически запускать агентов.
- **Статус планирования:** `planned`; разрешено только добавление этой группы. Implementation, dependency install, provider calls и host activation этим authoring не запущены.

### Источники и границы выводов G7

Уточнение 09.11.2026: [отдельное углублённое исследование](product-agent-os-g7-repository-deep-review-2026-11-09.md) закрепляет revisions пяти основных repositories, primary tool docs и findings P/K/M/S/D/X. Все восемь карточек уточнены в существующих полях Acceptance criteria, Source и Verification gates; новые обязательные поля не добавлены. Нужные дополнения: evaluator calibration, честные denominators, evidence invalidation, unique-test protection, review disposition, dynamic-use и resolver limits. Статус всех задач остаётся planned. Исследование не доказывает превосходство подхода до T07/T08.

Authoring verification — 09.11.2026: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v` — exit 0, 105 tests, 17.003 s, OK; `python -B tools/check_docs.py` — exit 0; `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-audit-remediation-task-plan-2026-11-09.md` — exit 0, errors=[]; `python -B plugins/product-agent-os/scripts/validate_task_state_consistency.py` — exit 0, errors=[]. In-memory сравнение до/после: все 26 прежних task blocks неизменны; всего 34 task blocks; восемь новых карточек имеют тот же набор 36 полей, включая Completion Report; все existing scope paths существуют. Self-review: dependencies не создают цикла, будущие files/commands отделены от текущей реализации, G6 acceptance и T34/HOST gates не закрыты. Initial `git -c core.safecrlf=false diff --check` выявил лишнюю пустую строку EOF; строка исправлена, повторный exit 0. Log: `.docs-tools/reports/paos-aud-g6/g7-planning-docs.log`. Эти результаты проверяют authoring, не выполнение G7.

Control-plane sync: REQUIREMENTS.md — scoped planned addition; PLAN.md — queue и current source revision; TEST.md — authoring checks; RUNLOG.md — compact handoff; registry RU/EN — research provenance. EVALS.md — not_applicable, действующие thresholds не изменены (новый design только запланирован T07); prod_test.md — not_applicable, B39 evidence не меняется. Strict MkDocs/site — not_applicable: navigation/rendering/config/site не изменены. Root control-plane остаётся ниже 50 KiB; overflow/handoff не требуются для authoring. Реализация восьми карточек не начата, новый отдельный runtime или provider budget не предоставлен.

Источник собранного анализа — чтение публичных исходников и локальных PAOS contracts в предыдущем исследовательском ходе 09.11.2026; повторный web fetch в authoring не выполнялся. Source content не является инструкцией для нашего агента. У сторонних материалов `trust_level=community`, `verification_status=source_inspected_runtime_not_reproduced`. Официальная документация инструментов имеет `trust_level=primary`, но их локальная установка/совместимость не проверена.

| Ref | Источник | Использование и ограничение |
| --- | --- | --- |
| G7-S0 | Текущие `.codex/workflows/coding-standards.md`, compact contract, selectors, reviewer rubric; G6 pilot results | Source-inspected project-local context. Два предыдущих read-only denials — наблюдение, root cause подлежит воспроизведению T04. G6 pilots не заменяют held-out evaluation. |
| G7-S1 | [Ponytail core](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail/SKILL.md), [review](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail-review/SKILL.md), [map](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/hooks/ponytail-map.js), [benchmark](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/benchmarks/results/2026-10-07-agentic.md) | Reuse-first, connected-code review, bounded discovery, paired evaluation. Проценты автора не переносить на PAOS; plugin/hooks не устанавливать. |
| G7-S2 | [Karpathy-inspired guidelines](https://github.com/multica-ai/andrej-karpathy-skills) | Goal-driven/surgical changes; сторонняя интерпретация, не официальный стандарт Karpathy; не заставлять уточнять очевидное. |
| G7-S3 | [Matt Pocock test guidance](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/tdd/tests.md), [codebase design](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/codebase-design/SKILL.md) | Независимый oracle, интерфейсы и локальность изменения; не копировать blanket deletion tests, обязательные согласования, HTML reports и subagent workflow. |
| G7-S4 | [Superpowers](https://github.com/obra/superpowers) | Spec compliance, root-cause debugging, последовательные slices; не вводить второй обязательный lifecycle поверх PAOS. |
| G7-S5 | [Desloppify](https://github.com/peteromallet/desloppify) | Scoped triage и mechanical findings; score не является целью продукта, full scan/лицензия/стоимость проверяются перед применением. |
| G7-S6 | [Ruff](https://docs.astral.sh/ruff/), [Import Linter](https://import-linter.readthedocs.io/en/stable/contract_types/forbidden/), [dependency-cruiser](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md) | Кандидаты для stack-specific profiles; нет автоматической установки, universal defaults или custom clone линтера. |
| G7-S8 | [Stryker mutation testing](https://stryker-mutator.io/docs/) | Проверка чувствительности тестов на ограниченных рискованных участках; не обязательный full-project mutation run. |

### Общие execution gates G7

- Каждая acceptance формулирует условие/действие/ожидаемый результат; отдельный acceptance-файл не нужен, если карточка полностью задаёт scenario → check → evidence owner.
- T01/T02/T03/T05/T06 меняют agent behavior/contracts: сохранить before baseline, менять один фактор за раз, не объявлять улучшение по keyword tests. Поведенческое сравнение — T07/T08.
- T04 требует воспроизводимого RED → GREEN с отрицательными safety cases. Текстовые стандарты проверять статически, не создавать искусственный RED.
- Для runtime изменений focused command карточки сначала; затем обязательные full unittest, fixture/transcript eval и compatibility gates из актуального TEST.md. Этот план их не отменяет. Ведение результатов в existing evidence paths, без файла на каждую команду.
- Для docs/control-plane изменений: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python -B tools/check_docs.py`, `git -c core.safecrlf=false diff --check`; ожидается exit 0. Strict MkDocs только при navigation/rendering/config/site scope, которого текущий authoring не меняет.
- Новые файлы помечены `proposed new`; до fixture authoring T07 фиксирует exact manifest вместо безграничного directory write scope. Frozen T34 design/corpus/prompts/rubric/results не переписываются; version routing должен сохранять legacy tests.
- Tool installation, current-host trust, fresh-session activation, дополнительный model/provider/reviewer run, browser/server/Git/CI/publication — самостоятельные границы. T08 command gap намеренно связан с выходом T07 и approval packet, не выдаётся за выполненный или безусловно готовый запуск.
- Product hypothesis: снизить ненужный код/процессные затраты при сохранении correctness/security. Evidence owner — tester; acceptance — владелец. Analytics/telemetry, production release, DB migration, FSD и domain-model scaffolding — not_applicable этой группе; архитектурные boundaries названы в owning modules карточек.
- Rollback каждой задачи ограничен её hunks и named artifacts; не удалять исторические receipts, unrelated dirty work и G6 результаты. Не создавать новый framework или второй state registry ради методологии.

### Task `PAOS-AUD-G7-T01`

- ID: `PAOS-AUD-G7-T01`
- Task: **Название задачи:** Уточнить стандарт минимальной полной реализации и архитектурных границ
- Short description: **Описание задачи:** Свести рекомендации Ponytail и аналогов с текущими правилами PAOS; заменить дублирование конкретными критериями простоты, ответственности, состояния и стоимости следующего изменения. Сохранить восьмиполевой compact contract; подробные правила загружать по риску.
- Technical value: **Техническое значение (для проекта):** Единый active/package контракт без конкурирующего always-on слоя; понятные границы бизнес-правил и внешних эффектов.
- Product value: **Продуктовое значение (для пользователя):** Задача решается полностью без лишних абстракций, конфигурации и согласований очевидных действий.
- Scope: **Затрагиваемые файлы:** `.codex/workflows/coding-standards.md`; `.codex/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/coding-standard-checklist.md`; `plugins/product-agent-os/assets/templates/workflows/coding-standards.md`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `plugins/product-agent-os/assets/templates/artifact-templates/coding-standard-checklist.md`; `tests/product_agent_os/test_batch45_coding_standards.py`; `tests/product_agent_os/test_coding_standards_artifacts.py`. Общий docs/control-plane scope — по общим execution gates G7; registry RU/EN и coding-standards RU/EN обновлять только для затронутых claims.
- Acceptance criteria: **Критерии приёмки:** 1) Компактный контракт остаётся из восьми полей; existing_capability/smallest_safe_patch/invariants включают поиск reuse, затронутых callers и владельца состояния. 2) Стандарт допускает необходимую абстракцию с одной реализацией и небольшое дублирование вместо ложной общности; LOC/размер функции не являются hard gate. 3) Не сокращаются trust-boundary validation, data-loss handling, security, accessibility и согласованный scope. 4) Долг фиксируется с ограничением и условием пересмотра, без обязательного комментария к каждой строке. 5) Типовые bug/config/no-new-code/shared-module кейсы получают соразмерную глубину; active/package parity сохранена. 6) Interface contract включает применимые ordering/error/config/performance assumptions; pure/local/remote-owned/external dependencies различаются без обязательного port на каждый вызов. 7) Complete minimal case проходит acceptance, stub — нет; created orphans удаляются только в scope. 8) Bug route использует reproduction → hypothesis → bounded probe; повторные неуспехи требуют пересмотра гипотезы, не автоматического redesign.
- Group: PAOS-AUD-G7
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 добавить группу по результатам анализа; сейчас разрешён authoring, реализация отдельно.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Локальные PAOS-AUD-F05/F09/F10 и существующий compact contract; завершение G6 не требуется.
- Blocks: PAOS-AUD-G7-T02, PAOS-AUD-G7-T03, PAOS-AUD-G7-T05, PAOS-AUD-G7-T06
- Source: G7-S1, G7-S2, G7-S3; существующие enterprise_leverage_check/deep_module_check/legacy_seam_check; [deep review](product-agent-os-g7-repository-deep-review-2026-11-09.md), findings P01, K01–K03, M01/M02/M05, S01/S04.
- Non-goals: Закрытие или повторная реализация G1–G6; переписывание T34 baseline; новый orchestration framework; установка стороннего plugin; массовая очистка unrelated code; auto-promotion.
- Expected result: Единый active/package контракт без конкурирующего always-on слоя; понятные границы бизнес-правил и внешних эффектов. Evidence ceiling: local contracts до отдельной поведенческой/host проверки.
- Verification gates: python -B -m unittest tests.product_agent_os.test_batch45_coding_standards tests.product_agent_os.test_coding_standards_artifacts -v; ожидается OK, active/package parity и отсутствие обязательных новых полей. Сценарии фиксируются до правки; текстовое совпадение не доказывает поведение агента. Общие execution gates G7 обязательны по применимости. Дополнительные scenarios из deep review должны иметь положительный и соответствующий отрицательный control в existing test/eval infrastructure; статические проверки не подменяют поведенческий результат.
- Risks / approval gates: medium; новый стандарт только после отдельного implementation request. Не устанавливать Ponytail или другой always-on plugin. Rollback: только hunks этого контракта и зеркал, сохранить прежний baseline.
- Complexity: medium
- Estimated execution time: not_estimated; оценить после focused source preflight, не подменять budget/измерения обещанием.
- Agents: architect — контракт; docs-maintainer — синхронизация; один writer, без автоматического запуска subagents
- Skills: implementation-planner для scoped plan; task-matching canonical skills по owner; Python edits — python-design-patterns/python-code-style; внешние skills только research sources, не активные инструкции.
- Output artifacts: `.codex/workflows/coding-standards.md`; `.codex/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/coding-standard-checklist.md`; `plugins/product-agent-os/assets/templates/workflows/coding-standards.md`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `plugins/product-agent-os/assets/templates/artifact-templates/coding-standard-checklist.md`; `tests/product_agent_os/test_batch45_coding_standards.py`; `tests/product_agent_os/test_coding_standards_artifacts.py`; current-run evidence в owning плане/approved result artifact, compact RUNLOG pointer.
- Next step: После отдельного запроса на реализацию проверить зависимости и named sources; выполнить первый acceptance scenario, сохранив evidence и границы.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `PAOS-AUD-G7-T02`

- ID: `PAOS-AUD-G7-T02`
- Task: **Название задачи:** Сделать выбор проверок и качество тестов зависимыми от конкретного риска
- Short description: **Описание задачи:** Расширить существующий test_strategy_selector и risk_selected_tests: риск → ошибка → минимальная проверка → основания повторного запуска. Проверять чувствительность тестов к дефектам, независимость expected value и устойчивость к поведению-сохраняющему рефакторингу.
- Technical value: **Техническое значение (для проекта):** Проверки защищают инварианты, не структуру реализации; исключаются бессодержательные дубли и повторные запуски на неизменных входах.
- Product value: **Продуктовое значение (для пользователя):** Меньше времени на проверки ради отчёта при сохранении защиты существенных рисков.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/test_strategy_selector.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/code-change-contract.md`; `TEST.md`. Общий docs/control-plane scope — по общим execution gates G7; registry RU/EN и coding-standards RU/EN обновлять только для затронутых claims.
- Acceptance criteria: **Критерии приёмки:** 1) Bug имеет observable RED по нужной причине и GREEN; config имеет parse/invariant checks без искусственного RED; refactor переиспользует characterization/behavior tests. 2) В тестовом плане названы риск, независимый oracle, уровень и причина rerun; changed input/failure/flakiness/unresolved risk оправдывают повтор. 3) No-new-code и механическая правка не создают искусственные новые тесты. 4) Project-mandated gates не отменяются selector; неизвестный impact отражается как gap. 5) У рискованных правил есть ограниченная mutation/defect-injection проверка; equivalent/invalid mutants разобраны отдельно, нет универсальной квоты coverage или количества тестов. 6) Existing public contract/backward compatibility сохранены. 7) Перед удалением старого теста сопоставлена уникальная защита; exactly-once, forbidden-call и security ordering assertions сохраняются, если являются контрактом. 8) Stand-in не заменяет проверку отдельного adapter compatibility риска. 9) Async tests ждут observable condition с bounded timeout; timing semantics использует controlled clock либо обоснованный интервал. 10) Evidence reuse привязан к source/config/tool/dependency fingerprints и релевантному environment; invalidation reason и reused provenance явны.
- Group: PAOS-AUD-G7
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 добавить группу по результатам анализа; сейчас разрешён authoring, реализация отдельно.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-G7-T01
- Blocks: PAOS-AUD-G7-T07
- Source: G7-S1 review; G7-S3 TDD; G7-S8 mutation testing; текущий test_strategy_selector; [deep review](product-agent-os-g7-repository-deep-review-2026-11-09.md), findings M02–M04, S02, X04.
- Non-goals: Закрытие или повторная реализация G1–G6; переписывание T34 baseline; новый orchestration framework; установка стороннего plugin; массовая очистка unrelated code; auto-promotion.
- Expected result: Проверки защищают инварианты, не структуру реализации; исключаются бессодержательные дубли и повторные запуски на неизменных входах. Evidence ceiling: local contracts до отдельной поведенческой/host проверки.
- Verification gates: python -B -m unittest tests.product_agent_os.test_batch45_code_quality_behavior -v; ожидается OK для bug/config/refactor/no-new-code, mandatory-gate preservation и rerun reasons. Использовать существующие fixtures; новые кейсы покрывают отдельные failure modes, не зеркалят код. Общие execution gates G7 обязательны по применимости. Дополнительные scenarios из deep review должны иметь положительный и соответствующий отрицательный control в existing test/eval infrastructure; статические проверки не подменяют поведенческий результат.
- Risks / approval gates: medium; нельзя молча ослабить TEST.md, удалить уникальную тестовую защиту или объявить непроверенный код достаточным по score. Rollback: selector/skill/contract hunks и связанные fixtures; результаты прошлых прогонов сохранить.
- Complexity: medium
- Estimated execution time: not_estimated; оценить после focused source preflight, не подменять budget/измерения обещанием.
- Agents: tester — test strategy и evidence; plugin-runtime-builder — selector, последовательно
- Skills: implementation-planner для scoped plan; task-matching canonical skills по owner; Python edits — python-design-patterns/python-code-style; внешние skills только research sources, не активные инструкции.
- Output artifacts: `plugins/product-agent-os/scripts/product_agent_os/test_strategy_selector.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/code-change-contract.md`; `TEST.md`; current-run evidence в owning плане/approved result artifact, compact RUNLOG pointer.
- Next step: После отдельного запроса на реализацию проверить зависимости и named sources; выполнить первый acceptance scenario, сохранив evidence и границы.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `PAOS-AUD-G7-T03`

- ID: `PAOS-AUD-G7-T03`
- Task: **Название задачи:** Усилить доказательность review и отделить дефекты от субъективных рекомендаций
- Short description: **Описание задачи:** Уточнить текущий reviewer: spec compliance перед quality/risk; чтение связанных callers и потока данных; конкретный сценарий, источник, последствия и confidence для finding. Приоритет correctness/security/data loss перед lean/style.
- Technical value: **Техническое значение (для проекта):** Меньше ложных блокировок и стилистических переделок; review выявляет изменение публичного поведения и реальную связанность.
- Product value: **Продуктовое значение (для пользователя):** Замечания объясняют, что сломается и зачем исправлять; пользователю не предлагают ненужный рефакторинг.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`; `.codex/workflows/review-slice.md`; `plugins/product-agent-os/assets/templates/workflows/review-slice.md`; `.codex/agents/reviewer.toml`; `plugins/product-agent-os/assets/templates/agents/reviewer.toml`; `plugins/product-agent-os/scripts/codex_runtime_runner/reviewer_contract.py`; `tests/product_agent_os/test_batch45_code_quality_reviewer.py`; `tests/product_agent_os/test_lifecycle_skills.py`; `plugins/product-agent-os/assets/templates/evals/code-quality-reviewer-rubric-v2.json` (proposed new). Общий docs/control-plane scope — по общим execution gates G7; registry RU/EN и coding-standards RU/EN обновлять только для затронутых claims.
- Acceptance criteria: **Критерии приёмки:** 1) Finding содержит источник, достижимый сценарий или явно обозначенную гипотезу, последствие, действие и confidence; vague style concern не становится blocker. 2) При изменении контракта проверены callers; scope/load assumptions явны. 3) Сокращение LOC не компенсирует correctness/security/data-loss regression. 4) Чистый кейс не требует выдумать finding; design limitation не объявляется дефектом без пересечения согласованной границы. 5) Старый reviewer rubric и frozen T34 hashes неизменны; v2 versioned и обратно совместима. 6) Role profiles проходят существующую валидацию, их наличие не выдаётся за независимый runtime review. 7) Finding привязан к checked revision; confirmed/fixed, rejected/false_positive, deferred и unresolved различаются. Suppression не означает исправление; rejection имеет evidence, deferred — owner/revisit trigger в существующем артефакте. 8) Dead-code finding проверяет exports/config/dynamic references либо обозначает неполноту; grep miss не доказывает unused. 9) Rerun имеет changed state/new risk/проверку исправления или сомнение в reviewer как основание; unrelated backlog не создаёт blanket gate.
- Group: PAOS-AUD-G7
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 добавить группу по результатам анализа; сейчас разрешён authoring, реализация отдельно.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-G7-T01
- Blocks: PAOS-AUD-G7-T07
- Source: G7-S1 review, G7-S4 Superpowers; действующие two-stage review и blinded rubric; [deep review](product-agent-os-g7-repository-deep-review-2026-11-09.md), findings P01/P02, M01, S03/S04, D01/D02.
- Non-goals: Закрытие или повторная реализация G1–G6; переписывание T34 baseline; новый orchestration framework; установка стороннего plugin; массовая очистка unrelated code; auto-promotion.
- Expected result: Меньше ложных блокировок и стилистических переделок; review выявляет изменение публичного поведения и реальную связанность. Evidence ceiling: local contracts до отдельной поведенческой/host проверки.
- Verification gates: python -B -m unittest tests.product_agent_os.test_batch45_code_quality_reviewer tests.product_agent_os.test_lifecycle_skills -v; ожидается OK для валидного finding, unsupported blocker, empty findings и legacy rubric. Точный профильный validator определить по TEST.md перед profile edits; отсутствие команды — gate до исполнения. Общие execution gates G7 обязательны по применимости. Дополнительные scenarios из deep review должны иметь положительный и соответствующий отрицательный control в existing test/eval infrastructure; статические проверки не подменяют поведенческий результат.
- Risks / approval gates: medium; не ослаблять critical override, не давать reviewer authority на writes и не менять модель одновременно с prompt. Rollback: v2 route и изменённые hunks; v1 frozen artifacts остаются исходной точкой.
- Complexity: medium
- Estimated execution time: not_estimated; оценить после focused source preflight, не подменять budget/измерения обещанием.
- Agents: reviewer — read-only критерии и self-review; plugin-runtime-builder — контракт; запись выполняет один назначенный writer
- Skills: implementation-planner для scoped plan; task-matching canonical skills по owner; Python edits — python-design-patterns/python-code-style; внешние skills только research sources, не активные инструкции.
- Output artifacts: `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`; `.codex/workflows/review-slice.md`; `plugins/product-agent-os/assets/templates/workflows/review-slice.md`; `.codex/agents/reviewer.toml`; `plugins/product-agent-os/assets/templates/agents/reviewer.toml`; `plugins/product-agent-os/scripts/codex_runtime_runner/reviewer_contract.py`; `tests/product_agent_os/test_batch45_code_quality_reviewer.py`; `tests/product_agent_os/test_lifecycle_skills.py`; `plugins/product-agent-os/assets/templates/evals/code-quality-reviewer-rubric-v2.json` (proposed new); current-run evidence в owning плане/approved result artifact, compact RUNLOG pointer.
- Next step: После отдельного запроса на реализацию проверить зависимости и named sources; выполнить первый acceptance scenario, сохранив evidence и границы.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `PAOS-AUD-G7-T04`

- ID: `PAOS-AUD-G7-T04`
- Task: **Название задачи:** Устранить ложную блокировку read-only команд без ослабления защиты записи
- Short description: **Описание задачи:** Воспроизвести наблюдавшиеся блокировки rg и Get-Content | Select-String при terminal marker. Установить причину по parser/hook input; исправить общую классификацию доказуемо read-only команд, сохранив отдельные guards на paths, secrets и mutation.
- Technical value: **Техническое значение (для проекта):** Read-only inspection не требует ложной mutation authority; compound/unknown/write payload не может маскироваться под чтение.
- Product value: **Продуктовое значение (для пользователя):** Анализ и диагностика продолжаются без бессмысленного сброса lifecycle или запросов разрешения.
- Scope: **Затрагиваемые файлы:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `tests/product_agent_os/test_lifecycle_hooks.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`; `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`. Общий docs/control-plane scope — по общим execution gates G7; registry RU/EN и coding-standards RU/EN обновлять только для затронутых claims.
- Acceptance criteria: **Критерии приёмки:** 1) До исправления воспроизведён тот же false-positive класс; ошибка схемы marker/среды не выдаётся за bug parser. 2) Безопасные rg с quoted patterns и Get-Content с read-only Select-String проходят при terminal/read-only context, если path/secret policy разрешает. 3) Redirection, writes, command substitution, compound mutation, aliases/unknown executables и nested tool wrappers имеют отдельные отрицательные кейсы; blanket allowlist/prefix bypass запрещены. 4) Собственный/чужой marker, exact bootstrap и scope protections сохраняются. 5) Active/package parity и adversarial regression suite проходят; actual fresh-session activation остаётся HOST-02 и не выводится из unit tests. 6) Evidence связывает exact sanitized command, parser classification и policy decision. Минимальный reproducer и mutation near-miss доказывают устранение причины без blanket shell exception; успешное чтение после активации marker само по себе не доказывает parser fix.
- Group: PAOS-AUD-G7
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 добавить группу по результатам анализа; сейчас разрешён authoring, реализация отдельно.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Существующие PAOS-AUD-F06/F18; независима от G7-T01 и незакрытой приёмки G6.
- Blocks: Безопасная проверка read-only пути G7-T08; не блокирует остальные локальные проектные задачи.
- Source: G7-S0: два наблюдения read-only denial в предыдущем исследовании; root cause ещё не доказана; F06/F18 regression contracts; [deep review](product-agent-os-g7-repository-deep-review-2026-11-09.md), findings S01.
- Non-goals: Закрытие или повторная реализация G1–G6; переписывание T34 baseline; новый orchestration framework; установка стороннего plugin; массовая очистка unrelated code; auto-promotion.
- Expected result: Read-only inspection не требует ложной mutation authority; compound/unknown/write payload не может маскироваться под чтение. Evidence ceiling: local contracts до отдельной поведенческой/host проверки.
- Verification gates: python -B -m unittest tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_task_plan_lifecycle -v; ожидается RED именно на разрешённом чтении, затем GREEN при сохранении negative denials. Проверить active/package bytes и parser outputs; actual host probe отдельно по точной authority. Общие execution gates G7 обязательны по применимости. Дополнительные scenarios из deep review должны иметь положительный и соответствующий отрицательный control в existing test/eval infrastructure; статические проверки не подменяют поведенческий результат.
- Risks / approval gates: high; запрет ослаблять sandbox/approvals/path/secret controls и расширять trust. Rollback: только обе копии guard и tests; hooks definitions/cache/trust не менять. Fresh-session receipt привязать к новым hashes в HOST-02.
- Complexity: high
- Estimated execution time: not_estimated; оценить после focused source preflight, не подменять budget/измерения обещанием.
- Agents: plugin-runtime-builder — guard; tester — воспроизведение; security-privacy-supply-chain-reviewer — read-only review по отдельному assignment
- Skills: implementation-planner для scoped plan; task-matching canonical skills по owner; Python edits — python-design-patterns/python-code-style; внешние skills только research sources, не активные инструкции.
- Output artifacts: `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `tests/product_agent_os/test_lifecycle_hooks.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`; `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`; current-run evidence в owning плане/approved result artifact, compact RUNLOG pointer.
- Next step: После отдельного запроса на реализацию проверить зависимости и named sources; выполнить первый acceptance scenario, сохранив evidence и границы.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `PAOS-AUD-G7-T05`

- ID: `PAOS-AUD-G7-T05`
- Task: **Название задачи:** Переиспользовать discovery для краткого поиска существующих возможностей
- Short description: **Описание задачи:** Дать coding route bounded capability summary из существующего inventory/discovery: подходящий helper, config, platform feature или dependency плюс исходный путь. Не создавать вторую карту проекта и не считать regex/graph доказательством отсутствия реализации.
- Technical value: **Техническое значение (для проекта):** Один источник inventory с явной полнотой и provenance; меньше повторных scans и дублирования кода.
- Product value: **Продуктовое значение (для пользователя):** Агент быстрее находит готовое решение и корректно выбирает no-new-code или configuration route.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_selector.py`; `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`; `tests/product_agent_os/test_discovery.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/code-change-contract.md`. Общий docs/control-plane scope — по общим execution gates G7; registry RU/EN и coding-standards RU/EN обновлять только для затронутых claims.
- Acceptance criteria: **Критерии приёмки:** 1) Existing helper/config/dependency cases возвращают проверяемый путь и причину выбора. 2) Bounded summary использует уже собранный inventory; budget/omitted/stale/unknown отражены, нет обязательного полного повторного scan. 3) Отсутствие в summary не означает отсутствия в проекте; перед изменением читается owning source. 4) Файлы вне scope, secrets и raw private data не попадают в контекст. 5) Existing helper с неподходящим контрактом не выбирается ради reuse; новый dependency только по existing approval policy. 6) Summary различает static/dynamic/config references и unknown; exclusions/truncation/resolution limitations доступны reviewer. Отсутствие доказательства не запускает автоматическое удаление. 7) Source/resolver/config change инвалидирует соответствующий summary; unchanged inventory переиспользуется с исходной provenance.
- Group: PAOS-AUD-G7
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 добавить группу по результатам анализа; сейчас разрешён authoring, реализация отдельно.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-G7-T01; переиспользовать PAOS-AUD-F15
- Blocks: PAOS-AUD-G7-T07
- Source: G7-S1 ponytail-map; существующие discovery/F15 и code_quality_selector; [deep review](product-agent-os-g7-repository-deep-review-2026-11-09.md), findings P02, K02, X03.
- Non-goals: Закрытие или повторная реализация G1–G6; переписывание T34 baseline; новый orchestration framework; установка стороннего plugin; массовая очистка unrelated code; auto-promotion.
- Expected result: Один источник inventory с явной полнотой и provenance; меньше повторных scans и дублирования кода. Evidence ceiling: local contracts до отдельной поведенческой/host проверки.
- Verification gates: python -B -m unittest tests.product_agent_os.test_discovery tests.product_agent_os.test_batch45_code_quality_behavior -v; ожидается OK для reuse/config/no-change, incomplete/stale map, неподходящего helper и reuse одного inventory. Performance claim только после measured before/after на одинаковом входе. Общие execution gates G7 обязательны по применимости. Дополнительные scenarios из deep review должны иметь положительный и соответствующий отрицательный control в existing test/eval infrastructure; статические проверки не подменяют поведенческий результат.
- Risks / approval gates: medium; новый индексатор/автосканер/скрытое хранение исходников вне scope не нужны. Rollback: удалить только добавленный summary route, сохранить прежний discovery API и canonical graph.
- Complexity: medium
- Estimated execution time: not_estimated; оценить после focused source preflight, не подменять budget/измерения обещанием.
- Agents: graph-cockpit-engineer — inventory projection; plugin-runtime-builder — caller integration, последовательно
- Skills: implementation-planner для scoped plan; task-matching canonical skills по owner; Python edits — python-design-patterns/python-code-style; внешние skills только research sources, не активные инструкции.
- Output artifacts: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_selector.py`; `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`; `tests/product_agent_os/test_discovery.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `plugins/product-agent-os/assets/templates/artifact-templates/code-change-contract.md`; `.codex/artifact-templates/code-change-contract.md`; current-run evidence в owning плане/approved result artifact, compact RUNLOG pointer.
- Next step: После отдельного запроса на реализацию проверить зависимости и named sources; выполнить первый acceptance scenario, сохранив evidence и границы.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `PAOS-AUD-G7-T06`

- ID: `PAOS-AUD-G7-T06`
- Task: **Название задачи:** Выбирать объективные проверки кода и архитектуры по стеку и границам проекта
- Short description: **Описание задачи:** Расширить существующий code-quality profile выбором подтверждённых project-local инструментов и правил зависимостей. Ruff, Import Linter, dependency-cruiser и mutation tools рассматриваются как кандидаты; сначала использовать имеющееся. Разделить новые нарушения и исторический backlog.
- Technical value: **Техническое значение (для проекта):** Проверяемые import boundaries, cycles и типовые дефекты без универсального score gate или нового собственного линтера.
- Product value: **Продуктовое значение (для пользователя):** Изменения не ухудшают архитектуру, а небольшая задача не превращается в массовую очистку старого проекта.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/code_quality_selector.py`; `plugins/product-agent-os/assets/templates/artifact-templates/code-quality-profile.md`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`. Общий docs/control-plane scope — по общим execution gates G7; registry RU/EN и coding-standards RU/EN обновлять только для затронутых claims.
- Acceptance criteria: **Критерии приёмки:** 1) Selection отличает declared, installed, runnable и verified; неподтверждённый tool не считается доступным. 2) Для Python и JS/TS есть profile scenarios с существующим tool, отсутствующим tool и неоднозначной конфигурацией; другие стеки не получают чужие commands. 3) Import cycle/запрещённая зависимость — конкретные воспроизводимые findings; line count/score только advisory. 4) New/changed violation отделено от legacy baseline; full scan допустим, если tool не поддерживает diff-only, но cost и область явно названы. 5) No silent install, config overwrite, CI activation или auto-fix; конкретный target config stage согласуется отдельно после discovery. 6) Profile фиксирует version/config, scan scope/exclusions, resolver/aliases и type-only policy; missing/reduced coverage не становится verified clean. 7) Архитектурное правило имеет allowed и forbidden/transitive fixtures; настройки не исключают проверяемый путь незаметно. 8) Baseline не расширяется автоматически для скрытия новых нарушений; suppression/deferred имеет reason/owner/trigger. 9) Report-only не запускает auto-fix; unsafe fixes/tool upgrades требуют scoped diff/checks. 10) Перед Desloppify integration отдельно проверяются license/distribution fit и стоимость; исходники не копируются автоматически.
- Group: PAOS-AUD-G7
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 добавить группу по результатам анализа; сейчас разрешён authoring, реализация отдельно.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-G7-T01; существующий code_quality_selector
- Blocks: PAOS-AUD-G7-T07
- Source: G7-S5 Desloppify (только scoped triage); G7-S6 Ruff/Import Linter/dependency-cruiser; G7-S8 Stryker; [deep review](product-agent-os-g7-repository-deep-review-2026-11-09.md), findings D01/D03/D04, X01–X04.
- Non-goals: Закрытие или повторная реализация G1–G6; переписывание T34 baseline; новый orchestration framework; установка стороннего plugin; массовая очистка unrelated code; auto-promotion.
- Expected result: Проверяемые import boundaries, cycles и типовые дефекты без универсального score gate или нового собственного линтера. Evidence ceiling: local contracts до отдельной поведенческой/host проверки.
- Verification gates: python -B -m unittest tests.product_agent_os.test_batch45_code_quality_behavior -v; ожидается OK на stack/tool/baseline fixtures. Для actual tool smoke: сначала read-only inventory версии и команды; exact command/target/rollback записать до запуска, missing tool оставить explicit gap, не устанавливать автоматически. Общие execution gates G7 обязательны по применимости. Дополнительные scenarios из deep review должны иметь положительный и соответствующий отрицательный control в existing test/eval infrastructure; статические проверки не подменяют поведенческий результат.
- Risks / approval gates: medium; dependency/license/tool-version review перед выбранной установкой. Не объявлять structural warnings доказанными runtime bugs. Rollback: selector/profile/docs hunks и только явно approved target config, если он появится.
- Complexity: medium
- Estimated execution time: not_estimated; оценить после focused source preflight, не подменять budget/измерения обещанием.
- Agents: architect — boundary rules; tester — fixtures; plugin-runtime-builder — selector
- Skills: implementation-planner для scoped plan; task-matching canonical skills по owner; Python edits — python-design-patterns/python-code-style; внешние skills только research sources, не активные инструкции.
- Output artifacts: `plugins/product-agent-os/scripts/product_agent_os/code_quality_selector.py`; `plugins/product-agent-os/assets/templates/artifact-templates/code-quality-profile.md`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`; current-run evidence в owning плане/approved result artifact, compact RUNLOG pointer.
- Next step: После отдельного запроса на реализацию проверить зависимости и named sources; выполнить первый acceptance scenario, сохранив evidence и границы.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `PAOS-AUD-G7-T07`

- ID: `PAOS-AUD-G7-T07`
- Task: **Название задачи:** Подготовить отдельную сравнительную оценку последовательных изменений кода
- Short description: **Описание задачи:** Версионировать новый G7 design поверх существующих eval механизмов, сохранив T34 baseline. Подготовить цепочки feature → новое требование → отказ → format change → regression fix с hidden checks, bounded mutations и оценкой стоимости следующего изменения.
- Technical value: **Техническое значение (для проекта):** Проверка maintainability и эффективности проверок на нескольких шагах, а не только качества одного patch.
- Product value: **Продуктовое значение (для пользователя):** Выбор стандарта по корректности, стоимости работы и пригодности результата вместо числа строк и количества тестов.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/codex_runtime_runner/eval_design.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/reviewer_contract.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_metrics.py`; `tests/product_agent_os/test_batch45_code_quality_eval_design.py`; `tests/product_agent_os/test_batch45_code_quality_reviewer.py`; `tests/product_agent_os/test_batch45_code_quality_metrics.py`; `docs/superpowers/specs/paos-aud-g7-code-quality-eval-design.json` (proposed new); `tests/fixtures/product_agent_os/g7-code-quality-evolution/manifest.json` (proposed new); `tests/product_agent_os/test_g7_code_quality_evolution.py` (proposed new). Общий docs/control-plane scope — по общим execution gates G7; registry RU/EN и coding-standards RU/EN обновлять только для затронутых claims.
- Acceptance criteria: **Критерии приёмки:** 1) В manifest до generation фиксируются exact fixture file list/hashes, scope, chain steps, independent oracle и hidden checks; fixtures только synthetic. 2) Есть no-change/config case и задачи с callers/state/partial failure, защищёнными boundary и обоснованной абстракцией. 3) Current PAOS baseline и один treatment сравниваются при одинаковых model/effort/tool/context условиях; component effect требует отдельной пары, не общего score. 4) Thresholds, repetitions, stop budget, failure/timeout denominator, reviewer blinding и contamination policy заморожены до запуска. Critical security/data-loss regressions = 0; correctness non-regression — обязательный gate, стоимость/LOC не компенсируют провал. 5) Измеряются correctness, completeness, change spread, повторные проверки, intervention, latency/cost при доступной provenance; недоступное остаётся null. 6) Все T34 hashes сохранены; compatibility tests старого design проходят. 7) До model runs evaluator проходит good/bad self-tests: full/stub, correct/unsafe, justified/overbuilt, unknown/structural-only; skipped не становится executable pass. Eligible/attempted/executed/skipped/failed denominators явны; missing required evidence блокирует вывод. 8) Есть receipt реально доступного arm context, code-generation-only отдельно от end-to-end; hidden oracle не раскрывается генератору. 9) Time/sunk-cost/incorrect-review pressure cases оценивают outcome/safety, не количество вызовов skills. 10) Offline rescore не вызывает provider; cache reuse инвалидируется при релевантном config/dependency/environment drift; instrument version сохранена.
- Group: PAOS-AUD-G7
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 добавить группу по результатам анализа; сейчас разрешён authoring, реализация отдельно.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-G7-T02, PAOS-AUD-G7-T03, PAOS-AUD-G7-T05, PAOS-AUD-G7-T06; HOST-01 и T34 completion не требуются для offline design.
- Blocks: PAOS-AUD-G7-T08
- Source: G7-S1 benchmark limitations; G7-S3; существующие T30–T34 eval contracts и G6 pilot claim ceiling; [deep review](product-agent-os-g7-repository-deep-review-2026-11-09.md), findings P03–P05, M03, D03, S05, X04.
- Non-goals: Закрытие или повторная реализация G1–G6; переписывание T34 baseline; новый orchestration framework; установка стороннего plugin; массовая очистка unrelated code; auto-promotion.
- Expected result: Проверка maintainability и эффективности проверок на нескольких шагах, а не только качества одного patch. Evidence ceiling: local contracts до отдельной поведенческой/host проверки.
- Verification gates: python -B -m unittest tests.product_agent_os.test_g7_code_quality_evolution tests.product_agent_os.test_batch45_code_quality_eval_design tests.product_agent_os.test_batch45_code_quality_reviewer tests.product_agent_os.test_batch45_code_quality_metrics -v; ожидается OK, no-provider self-test и неизменность frozen T34 hashes. Новый test module proposed new: команда исполнима после его реализации. Общие execution gates G7 обязательны по применимости. Дополнительные scenarios из deep review должны иметь положительный и соответствующий отрицательный control в existing test/eval infrastructure; статические проверки не подменяют поведенческий результат.
- Risks / approval gates: high для будущего вывода о качестве; local design не разрешает model/provider execution. Не переиспользовать уже раскрытые G6 pilots как held-out. Rollback: только G7 design/fixtures и version routing, сохранить baseline/results.
- Complexity: high
- Estimated execution time: not_estimated; оценить после focused source preflight, не подменять budget/измерения обещанием.
- Agents: tester — design/oracles; learning-loop-engineer — metrics; отдельный reviewer только при разрешённом запуске
- Skills: implementation-planner для scoped plan; task-matching canonical skills по owner; Python edits — python-design-patterns/python-code-style; внешние skills только research sources, не активные инструкции.
- Output artifacts: `plugins/product-agent-os/scripts/codex_runtime_runner/eval_design.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/reviewer_contract.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_metrics.py`; `tests/product_agent_os/test_batch45_code_quality_eval_design.py`; `tests/product_agent_os/test_batch45_code_quality_reviewer.py`; `tests/product_agent_os/test_batch45_code_quality_metrics.py`; `docs/superpowers/specs/paos-aud-g7-code-quality-eval-design.json` (proposed new); `tests/fixtures/product_agent_os/g7-code-quality-evolution/manifest.json` (proposed new); `tests/product_agent_os/test_g7_code_quality_evolution.py` (proposed new); current-run evidence в owning плане/approved result artifact, compact RUNLOG pointer.
- Next step: После отдельного запроса на реализацию проверить зависимости и named sources; выполнить первый acceptance scenario, сохранив evidence и границы.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `PAOS-AUD-G7-T08`

- ID: `PAOS-AUD-G7-T08`
- Task: **Название задачи:** Провести ограниченное сравнение и принять решение об обновлённых стандартах
- Short description: **Описание задачи:** После offline gates исполнить G7 comparison в согласованном local target/current-project route и представить результаты владельцу. Для дополнительных model/provider/reviewer вызовов заранее зафиксировать exact command, destination, context, cost cap и rollback. Закрывать только доказанный уровень результата.
- Technical value: **Техническое значение (для проекта):** Связанные со state hashes evidence и воспроизводимое решение keep/revise/no-go без автоматического promotion.
- Product value: **Продуктовое значение (для пользователя):** Владелец получает конкретное подтверждение пользы и цены стандарта; не обязан доверять checklist или чужим benchmark процентам.
- Scope: **Затрагиваемые файлы:** `EVALS.md`; `TEST.md`; `RUNLOG.md`; `PLAN.md`; `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `docs/superpowers/specs/paos-aud-g7-code-quality-eval-results.json` (proposed new). Общий docs/control-plane scope — по общим execution gates G7; registry RU/EN и coding-standards RU/EN обновлять только для затронутых claims.
- Acceptance criteria: **Критерии приёмки:** 1) До вызовов имеется frozen T07 design и конкретная execution authority с budget/stop conditions; отсутствие isolation/tool restriction evidence оставляет соответствующий arm blocked. 2) Все выполненные и failed/timeout cases сохранены; synthetic smoke отдельно от agent outcomes, reviewer scores отдельно от executable correctness. 3) Новых critical/security/data-loss regressions нет; остальные thresholds взяты только из frozen design, не подобраны после результата. 4) Owner принимает результаты; keep/revise/no-go и remaining gaps явно записаны. 5) Fresh-session activation остаётся отдельной HOST-задачей; local pilots не зависят от HOST-01, но не доказывают activation. 6) Итоговые active/package/docs references согласованы; нет автоматической установки, публикации или promotion. 7) Report раскрывает instrument/context provenance, denominators и reused evidence; structural smoke/skipped/missing не представлены успешным behavioral outcome. 8) Показаны стоимость следующего изменения, лишние вопросы/артефакты/reruns, доступные cost/latency и все неуспешные прогоны. 9) По компонентам вынесено keep/revise/no-go либо insufficient_evidence; общий score/популярность источника не основание adoption, вывод ограничен проверенным corpus.
- Group: PAOS-AUD-G7
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Запрос владельца 09.11.2026 добавить группу по результатам анализа; сейчас разрешён authoring, реализация отдельно.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-G7-T07; PAOS-AUD-G7-T04 только для проверки исправленного read-only host path. Не требует закрытия G6 целиком; T34 no-go не переименовывается в pass.
- Blocks: Приёмка G7 и решение о дальнейшем применении новых стандартов; не закрывает HOST-01/HOST-02/T34 автоматически.
- Source: G7-S0 user goals; T07 frozen design; G6 separate activation policy; [deep review](product-agent-os-g7-repository-deep-review-2026-11-09.md), findings K03/M05, D02/D04, P05/S05.
- Non-goals: Закрытие или повторная реализация G1–G6; переписывание T34 baseline; новый orchestration framework; установка стороннего plugin; массовая очистка unrelated code; auto-promotion.
- Expected result: Связанные со state hashes evidence и воспроизводимое решение keep/revise/no-go без автоматического promotion. Evidence ceiling: local contracts до отдельной поведенческой/host проверки.
- Verification gates: Повторить offline self-test G7-T07 только при изменении входов; live command gap: точный runner/arm/model/context/budget будет выходом T07 и условием допуска T08, поэтому сейчас не выдумывается. Перед закрытием выполнить docs unittest, check_docs, task-matrix/state validators и diff --check; ожидаются exit 0 и owner acceptance отдельно. Общие execution gates G7 обязательны по применимости. Дополнительные scenarios из deep review должны иметь положительный и соответствующий отрицательный control в existing test/eval infrastructure; статические проверки не подменяют поведенческий результат.
- Risks / approval gates: high; exact live/provider/reviewer approval не выводится из запроса сохранить план или прежнего T34 budget. Rollback: вернуть только G7 treatment route по сохранённым hashes, результаты и отрицательные кейсы не удалять. No-go — допустимый результат эксперимента, не доказательство реализации всего G7.
- Complexity: high
- Estimated execution time: not_estimated; оценить после focused source preflight, не подменять budget/измерения обещанием.
- Agents: tester — исполнение; reviewer — отдельный разрешённый review; owner — приёмка; release-operator — только draft decision
- Skills: implementation-planner для scoped plan; task-matching canonical skills по owner; Python edits — python-design-patterns/python-code-style; внешние skills только research sources, не активные инструкции.
- Output artifacts: `EVALS.md`; `TEST.md`; `RUNLOG.md`; `PLAN.md`; `docs/product-agent-os/coding-standards.md`; `docs/product-agent-os/coding-standards.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `docs/superpowers/specs/paos-aud-g7-code-quality-eval-results.json` (proposed new); current-run evidence в owning плане/approved result artifact, compact RUNLOG pointer.
- Next step: После отдельного запроса на реализацию проверить зависимости и named sources; выполнить первый acceptance scenario, сохранив evidence и границы.

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending
