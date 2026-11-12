# Product-Agent OS Web — workflow, sessions, agents и skills, 2026-11-12

Source status: user-authorized local implementation; implementation, technical verification and docs/status synchronization completed. Closure ceiling: implemented_locally_verified_app_active for the selected eleven tasks.

## Scope и baseline

Очередь: PAOS-0036 → 0009 → 0010 → 0011 → 0012 → 0013 → 0014 → 0015 → 0016 → 0017 → 0018. Источники: [полные карточки](product-agent-os-web-task-manager-plan-2026-11-09.md), [machine matrix](product-agent-os-web-task-manager-task-group-2026-11-09.json), [PRD §§13–14](product-agent-os-web-prd-2026-11-05.md), screen specification S08–S16/S25–S26. Предыдущие десять M2 tasks и M1/PAOS-0046 сохраняют собственные receipts. Не входят PAOS-0019, остальные задачи, M3 execution chains, release/commercial/human acceptance.

Baseline `.tmp/paos-m2b/baseline/manifest.json`: 191 source/control-plane files, сохранён 2026-11-12T05:29:18.594691Z. Предыдущий dirty work не очищается. Откат только своих hunks поверх этой baseline; Git history не меняется. Перед новым scope прежняя terminal closure сохранена в собственном marker как previous_scope_closure. Первоначальные read/hash/partial marker calls были отклонены hook до bootstrap; включение полного reporting context разрешило штатный exact-marker bootstrap. Hooks/config/permissions не ослаблялись. Brief digest идентифицирует ASCII scope/schema, не доказывает полноту видимого пакета или approval.

## Acceptance, методы и ownership

Root — evidence/docs/integration owner; максимум два delegated agents и один source writer. Независимая discovery/architecture выполняется read-only; запись передаётся builder/корневому агенту последовательно. Role presence не является runtime activation.

| Task | Given / When / Then — публичный сценарий и отрицательный случай | Evidence owner |
| --- | --- | --- |
| PAOS-0036 | Versioned workflow draft → validate/preview/publish/migrate → новые задачи используют выбранную версию, старый run pin неизменен; invalid graph/stale preview/active migration отвергаются, rollback не удаляет историю | Root + workflow builder |
| PAOS-0009 | Несколько страниц доступных session records → paging с concurrent insert → без потерь/дублей в bounded snapshot; archived/fork/subagent и unavailable coverage видимы | Root |
| PAOS-0010 | Длинный transcript → открыть message ID → стабильный порядок и anchor; автор/task/file/fork/agent различимы, нет first-page-only ограничения | Root |
| PAOS-0011 | Секретный synthetic canary и другой проект → store/search/transcript → редакция, project isolation, truncation/retention показаны, hidden reasoning не запрашивается | Root |
| PAOS-0012 | Source/managed agent versions → каталог/профиль → source/proposed/effective/observed loaded различимы, task/run/session navigation корректна | Root |
| PAOS-0013 | Agent proposal с base revision → diff/validate/apply/archive/restore → immutable version/history; stale apply отклоняется, active run не меняется | Root |
| PAOS-0014 | Описание create/update/delete → target resolution/structured proposal → editable draft и diff; ambiguous target требует уточнения, unavailable model не подменяется silent provider fallback | Root |
| PAOS-0015 | Scoped run/assignment telemetry → выбранный период → unique started runs/outcomes с denominator/source/coverage, неизвестные duration/token/cost остаются null | Root |
| PAOS-0016 | Project/global/vendor discovery → skill profile → origin/scope/hash/effective version/dependencies/agents, недоступные scopes явно unavailable | Root |
| PAOS-0017 | Project-owned skill draft → preview/apply/rollback/archive → versioned content; vendor original не меняется, delete dependencies видимы | Root |
| PAOS-0018 | Local source path / discovery query → preview candidate → containment/resources/metadata/origin/license проверены до apply; поиск не выполняет установку | Root |

Spec-DD использует уже принятые карточки/PRD; Design-DD сохраняет существующие theme/locales/layout и показывает loading/empty/error/conflict/unavailable/unsaved/preview states. TDD: один реальный поведенческий RED, минимальный GREEN, scoped regression; missing module/export не выдаётся за RED. Integration/E2E покрывают отдельные wiring и journey риски. FSD/Storybook/новая дизайн-система не требуются для расширения существующих feature slices. Product hypothesis/release measurement/telemetry promotion не заявляются: это выполнение принятого functional scope. Agent metrics — локальная наблюдаемость с периодом/denominator, не новая внешняя analytics.

## Архитектура, домены и code-change contract

Bounded contexts остаются внутри существующего local service и SQLite Worker: workflow definition/version/migration, session/message/coverage, project agent/skill asset/proposal/version и наблюдённый run pin. PRD §§13–14 задаёт словарь; typed contracts → authenticated project API → feature UI → SQLite transaction/runtime ownership. Definition/publish не равны run/recipe execution. Source file, proposed draft, PAOS effective version и observed loaded runtime version — разные состояния. Project-owned apply не разрешает global/vendor mutation, permission escalation или live provider.

- **existing_capability:** LocalStore/settings/evidence, idempotent write receipts, SQL authority/revision guards, project binding, read-only catalog scanner, message journal/FTS, snapshots, App pull channel, draft registry и themes/locales переиспользуются. Offset pagination и metadata-only catalogs не удовлетворяют полным карточкам.
- **smallest_safe_patch:** новые domain contracts/services и feature panels с точечным подключением к http/application, client/App, Worker и runtime gateways; без второй БД, второго auth client/runner, глобального refactor или автоматически активируемых hooks.
- **invariants:** version pins immutable для уже идущего run; publish не мигрирует старые задачи; migration требует preview/revision и безопасной остановки; native approvals/criteria/dependency/terminal guards сохраняются; no silent loss, no cross-project leakage, no secret/raw-private-log persistence.
- **dependency_decision:** no_new_dependency; стандартные Node SQLite/FS/crypto и установленные React/TypeScript. Новая parser/runtime dependency не добавляется без доказанной необходимости и отдельной authority.
- **risk_selected_tests:** pure contract → real SQLite transaction → authenticated Request/Response → built browser → требуемый actual App/native путь. Fixture/model stand-in не выдаётся за model generation/host activation.
- **comment_decision:** документировать transaction, snapshot, CAS, loaded/proposed/effective, untrusted source и filesystem ownership boundaries; очевидный синтаксис не комментировать.
- **performance_applicability:** keyset/snapshot paging и bounded reads/DOM pages; ресурсный предел и partial coverage видимы. Новые performance SLO не объявляются измеренными без workload evidence.
- **evidence_and_gaps:** implementation proceeds по точному owning scope; source-dependent methods не объявляются verified до checks. Tool/runtime setup failures сохраняются отдельно от feature RED. Root close невозможен при missing required gates.

## Проверки и внешние границы

Запланированы `node --test tests/web/*.test.mts`, focused suites для новых contracts/services, `npm run check:web-m1`, `npm run build:web`; synthetic built browser journeys, relevant native/App pins/negative cases. Plugin route использует TEST.md: full unittest, fixture/transcript evals, compatibility; docs после sync — docs/lifecycle/templates/hooks, checker, matrix validator, diff. Требуемый strict MkDocs определяется только фактическими nav/diagram/config/site изменениями.

Context7 official Node `/nodejs/node/v26.0.0`: DatabaseSync/prepared statements сверены; это справка API, не доказательство atomic behavior нашего кода. React/Node версии берутся из lock/install. Provider/model endpoints, реальные credentials/OS entries, installation, global configuration/policy, Git и publication не вызываются. Bounded disposable loopback/browser/native checks разрешены standing owner authorization; pairing/lease material остаётся в памяти и не входит в отчёты/URL.

## Docs impact и текущий handoff

Root обновит только выбранные11 полных cards и matching JSON после verification; остальные45 cards/objects, все estimates/order/groups сохраняются. REQUIREMENTS/PLAN/TEST/RUNLOG обновляются компактно, detailed evidence остаётся здесь и в results packet. EVALS/AGENTS/prod_test — no_change_needed пока не изменены rubrics/instructions/Batch39 evidence. Source registry RU/EN синхронизируется с новыми factual claims. Research matrix не делится из-за размера.

Current state: selected11 cards and matching JSON marked implemented after technical verification; all required docs/status gates completed.

## Решения discovery и workflow integration

Read-only architect `/root/m2b_workflows` выявил точные дополнительные seams: `commands/domain-tools.mts`, `tasks/user-commands.mts` и `runtime/codex/coordinator.ts` также зависели от fixed status IDs. Ownership передан builder `/root/m2b_workflow_builder` вместе с Worker/TaskManager/gateways/contracts. Сам architect не редактировал исходники по ограничению своего профиля. Explorer `/root/m2b_catalog_discovery` и backend planner подтвердили metadata-only catalogs, offset pagination и недостаточную общую persisted-message redaction; эти ограничения не названы выполненными функциями.

Выбраны произвольные state IDs с одной из восьми host semantic categories. Strict M1 decoder сохраняется; M2 category-aware guards проверяются на pinned definition, native approvals не берутся из пользовательского workflow. Published versions immutable; task selection explicit → issue-type mapping → project default; существующие задачи меняются только reviewed migration. Migration digest связывает registry/board revision и полный matching task cohort/revisions, а не клиентский произвольный список. Definitions recipes остаются bounded metadata M2; M3 не исполняется. Неизвестные skill references требуют trusted resolver и не считаются validated.

Compatibility risk: старый M2 reader schema2 способен открыть новые records, но не понимает workflow refs/custom state guards. Поэтому применяется отдельный lazy semantic capability stamp schema3/`paos-m2b-v1` при первом workflow/team write; canonical SQL1/2 checksums сохраняются. До завершения соответствующих tests это implementation decision, не доказанная совместимость. Полный local profile archive должен сохранять новые definitions/assets/resources; отдельный tasks-only JSON не выдаётся за полный workflow/asset archive.

## Наблюдаемые общие проверки до финальной интеграции

| Команда | Current-run receipt и предел |
| --- | --- |
| `python -B -m unittest discover -s tests -p 'test_*.py' -q` | **1450 tests,527.507s,OK,skip1,exit0**, `.tmp/paos-m2b/full-unittest.log`; workspace TEMP/TMP `.tmp/paos-m2b/python-temp`. До final TS/UI/docs integration; Python implementation не менялась. |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` | **91 fixtures**, все expected_checks true,exit0; `.tmp/paos-m2b/fixture-eval.log`. |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` | **26/26**,exit0; `.tmp/paos-m2b/transcript-eval.log`. |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | exit0, compatible local structure; `.tmp/paos-m2b/codex-compatibility.log`; не host activation. |

Среда подтверждена: Node v26.5.0, npm12.0.1; установленный Codex binary SHA-256 `edfdd48f8b458af0906e507b4cb05217b326c3d6e515e9f024e05e3b8d650f70` совпадает с прежним binary pin. Adapter source pin после implementation требует новой проверки; прежний native receipt не считается новым. Установленные Playwright core/Chromium доступны, Browser plugin not available, поэтому acceptance использует существующий Playwright runner без установки. React skill и frontend-testing-debugging прочитаны; Context7 official React `/reactjs/react.dev` подтвердил Effect cleanup/ignore для stale responses. Третий Context7 docs query остаётся для реальной библиотечной неопределённости.

## Реализация и публичные контракты

PAOS-0036: workflow drafts, state/category/actor/required-field/guard validation, immutable publication, default/type/explicit assignment, archive, rollback и reviewed cohort migration используют существующий Task Manager command serializer и atomic SQLite writer. `packages/contracts/workflows/` содержит browser-safe semantic helpers. S25/S26 подключены в Settings; Tasks editor/board/manual lifecycle и Execution selector понимают custom state IDs. Publish не переписывает tasks/runs; recipe execution остаётся fixed M1, пользовательские recipes — только проверенные M2 metadata. Migrating terminal prerequisites обратно в nonterminal атомарно помечает dependents/parents для review, не стирая Done/evidence.

PAOS-0009–0011: `/projects/:id/sessions/catalog`, `/sessions/search`, `/sessions/:session/transcript` дают stable snapshot cursors и message anchors. Frozen membership/values живут в service memory до15 минут, ограничены 100 snapshots/64MiB total/32MiB per snapshot; restart/expiry возвращает typed stale. Available rows ограничены100000, превышение отвергается явно. UI показывает coverage, retention, counts, unavailable host/fork capability, полную доступную историю и escaped Markdown. Поиск и public legacy reads разделены поproject; known credential forms редактируются до storage/FTS/claim и на чтении. Hidden reasoning metadata исключается; обычный user text не фильтруется по словам. Политика не гарантирует распознавания всех секретов.

PAOS-0012–0018: `/team/catalog` возвращает metadata, `/team/assets/:id` — полный scoped profile/history. Managed PAOS versions отделены от native loadedVersion=null; фактические run pins доступны отдельно. Proposal preview/diff/CAS/idempotent apply/create/update/archive/delete/restore проходят один authoritative writer. Diff показывает effective content, name, description, dependencies, resource manifest, source и availability. Restore нормализует historical effective payload до проверки graph/dependencies/digest. Existing run pins immutable; resource blobs сохраняются для historical restore. Source copy/import проверяет registered project root identity, linked ancestors, symlink/hardlink, containment, path/content/size limits и текущий hash; origin/license видны до Apply. Копируется полный bounded resource tree, binary bytes сохраняются; source original не меняется. Managed bundle download является staging export, не native installation. Local discovery доступен, remote discovery явно unavailable; глобальные/native assets не изменяются.

`/team/generation` использует подключённый App-consumer только в planning binding, purpose `team_proposal`, selected target/context и strict JSON result. Create/update/delete даёт editable draft и отдельный Apply; неоднозначная/невыбранная existing target требует clarification. Provider fallback отсутствует. `/team/metrics?from&to` показывает unique observed starts/outcomes/accepted tasks и denominator/source/coverage; unavailable duration/token/cost остаются null. Skill reverse-agent links и agent→specific run→task/session navigation реализованы; `/team/runs/:id` — allowlisted read-only summary без lease/prompt/full instructions.

Lazy schema3/`paos-m2b-v1` активируется только workflow/team write. SQL1/2 checksums сохранены; сохранённые реальные prior `databaseCompatibility` и `migrate` отклоняют schema3. Backup/restore сохраняет workflow/assets/resources и создаёт inactive profile. Уже открытый произвольный старый SQL writer не объявляется ретроактивно остановленным.

## Текущие receipts и границы доказательств

| Gate | Observed result |
| --- | --- |
| `npm run test:web-m1` | **375/375**, fail0/skip0,9432.3939ms; `.tmp/paos-m2b/web-full-final.log`. Native link fixtures используют process-local lowercase workspace TEMP/TMP. |
| `npm run check:web-m1` | Passed for service/contracts; frontend strict check дополнительно выполнен build. |
| `npm run build:web` | Passed,49 modules; `.tmp/paos-m2b/ui-build-final.log`, установленные dependencies, без install. |
| Native focused backend/review |79/79 initial;84/84 после repair,skip0; `.tmp/paos-m2b/backend-review-round1-native-green.log`. |
| Built browser |**51 checks**, `.tmp/paos-m2b/browser-evidence-GaVuT4/result.json`:120messages/anchor110/permalink reload,55-session frozen paging с concurrent insert,redaction,workflow publish/custom task/cancel/migration/rollback,agent versions,full skill copy/binary download/edit retention,lostACK→navigation→401→re-pair→same-key retry,specific run→task/session, RU/EN/light/dark/mobile geometry. Screenshots inspected by root. |
| Actual App + native |**49 checks**, `.tmp/paos-m2b/actual-app-evidence-JOkK0N/m2-app-result.json`:3 genuine planning jobs create/update/delete→editable proposals; UI explicit create/update Apply, delete remains draft;1 genuine App execution with pinned actual-custom@1 + agentv2 during future workflow/profile publication, PAOS domain approval, exact wx file bytes/sum30/correlated report, separate explicit synthetic UI Done. Consumer observed completed and exit0. |
| Exact manifest/native | Final adapter `57575e07e1732345770439c60aed09fb2008f7173a6ab6c0252293951e85ceb7`; candidate and default loader each3modes passed, credential/model operations0, native stop and fixture cleanup. `.tmp/paos-m2b/native-candidate-4.log`, `native-default-final.log`; Node/Codex binary and lock pins unchanged. |
| Independent source review | `/root/m2b_review`, separate reused context,2 repair passes;7 findings confirmed_fixed, final source_review_passed. Reviewer did not run runtime tests. Root verifies final tests/browser/App and adds explicit self-review below. |

Root self-review found false-positive redacted flags on messages lacking optional fields, reproduced RED then GREEN, and fixed permalink Refresh reopening a prior anchor. New run-summary route has public HTTP404 RED then safe allowlist GREEN; current full375 includes both regressions. Frontend build initially found name/strict type mismatches; corrected before browser, those failures are retained. First browser managed Chromium launch failed at OS boundary; authorized native run used an unchanged disposable-profile runner. Fixture key/seed/selector errors are setup failures, not feature RED.

Review repairs: restore effective dependency/cycle validation; metadata/resource diff; resource/source retention in UI edit; source root replacement identity; custom Done metrics; reverse skill-agent links; lostACK/auth retry envelope; read-only run navigation. Source hashes, exact individual checks, RED refs and9 failed browser/App receipts are preserved in [machine results](product-agent-os-web-m2b-results-2026-11-12.json). Actual run1 failed closed on adapter drift after a new route; run2 native execution succeeded but final assertion expected a synthetic `TOKEN=` value correctly redacted by policy. Final run3 used noncredential `CORRELATION=` and cold-started final source;49 checks passed. Failed receipts were not rewritten as success.

No real credentials, existing OS entries, provider/model API clients, installation, global policy, Git/history/publication or canonical target data were used. App host identity remains attested rather than cryptographic; model/principal/quota/entitlement and whole-App sandbox are not established. Technical synthetic UI decisions do not equal owner human/commercial/release acceptance. No M3 recipe execution, broad performance/WCAG or full host-history claim.

## Control-plane и closure mapping

Selected11 tasks map to their existing complete MD cards and JSON objects only. Other45 cards, estimates,12 groups and execution order are preserved. Aggregate M2 status after this cohort:21/26 technical implemented; PAOS-0019/0020/0021/0022/0027 remain planned. Previous M1/PAOS-0046/first10M2 receipts stay authoritative for their own scope.

REQUIREMENTS/PLAN/TEST/RUNLOG: update_required→updated through reviewed section proposal/recovery; detailed evidence remains here/results. `apps/web/README.md` updated with operator API/capability boundaries. Source registry RU/EN updated. Root README no_change_needed: plugin mission/operator routing unchanged; EVALS/AGENTS/prod_test no_change_needed: rubrics/durable instructions/Batch39 ledger unchanged. MkDocs strict N/A: no MkDocs nav/config/diagram/extension/search/site output changed; generated site freshness is not claimed.

Final docs gates:251 tests in44.128s OK; docs checker,56-card matrix validator,both hook validators and diff--check exit0. Reviewed4-section proposal applied with recovery journal; manual matrix MD/JSON apply used exact-before CAS and retained before/after recovery. All45 other cards/JSON records,56 estimates,12 groups/order unchanged; protected baseline files unchanged. Root byte sizes: REQUIREMENTS39274, PLAN28449, TEST31621, RUNLOG24979, all below40000. Full root site freshness is not claimed. Rollback only owned hunks/files relative to191-file baseline; never remove schema3 row to force an old reader. Restore compatible backup into inactive profile for prior runtime. No destructive Git rollback.

Final current-pointer recheck:113 docs/task-plan tests in19.504s OK after evidence/header sync; final checker and diff exit0. Root verified49 source hashes against current files, both final browser/App receipt source hashes, cleanup, selected task statuses and unchanged45 other cards/JSON records. Completion time is cohort wall time only; per-task durations remain null.
