# Packaging и closure

Source status: `official + experiment`

## Назначение

Эта страница фиксирует packaging, documentation closure и owner handoff для Product-Agent OS. Closure делает систему понятной, проверяемой и готовой к approval-bound real testing, но сам по себе не запускает live execution.

Closure packet описывает обновленные source docs, packaging/install smoke definition, required verification, generated `site/` rebuild rule и approval packet для следующего execution step.

## Source-of-truth boundary

канонический источник:

- checked-in Product-Agent OS source docs;
- accepted implementation plan и docs closure scope;
- source registry и control-plane artifacts после their separate owner-approved/docs-maintainer slice;
- текущий command evidence из docs tests, `tools/check_docs.py`, strict MkDocs, optional full closure и packaging/install smoke;
- explicit owner approval packets для any later live/browser/provider/canonical/git action.

не является каноническим источником:

- generated `site/` pages через themselves;
- packaging/install smoke как release или publish approval;
- plugin-cache contents без checked-in source comparison;
- staged evidence без owner review;
- planning matrix presence без implementation и verification evidence.

## Входы

Closure consumes:

- modernization loop docs и metrics-report boundary;
- project code graph, cockpit, static search, backend gate, semantic retrieval, deterministic proposal и extension-closure docs;
- governance/runtime/provider/review/mutation/audit/real-testing-readiness/runtime-QA evidence;
- accepted docs closure scope;
- plugin README install и packaging guidance;
- MkDocs navigation/docs-check requirements из Builder/Tester slice;
- known gaps: docs-maintainer plugin-cache gap и Mermaid external asset gap когда still unresolved.

## Выходы и артефакты

Expected closure outputs:

- обновленные docs pages для Product-Agent OS source docs;
- source registry/backlog/control-plane sync из owning docs-maintainer slice;
- updated docs contract tests и `tools/check_docs.py` из owning Builder/Tester slice;
- regenerated `site/` using regular MkDocs `site_dir`;
- packaging/install smoke evidence packet;
- approval packet draft для real testing execution;
- explicit list из actions не performed без approval.

Эта worker page covers только docs packet. Она не обновляет navigation, tests, registry, README, `site/`, git state или plugin distribution.

## Packaging And Install Smoke

Packaging/install smoke является только evidence. Это следует answer:

- plugin manifest exists и points к expected bundled skills/MCP metadata;
- checked-in `docs-maintainer` guidance является available, или docs-maintainer plugin-cache gap является recorded;
- local install path или marketplace candidate может быть inspected без publishing;
- staged templates и scripts остаются package-readable;
- нет secrets, credentials или private data являются bundled;
- plugin hooks и automations остаются inactive пока explicitly approved;
- install smoke result records command, environment, output summary, gaps и residual risk.

Install smoke не публикует plugin, писать к external systems, create marketplace release, upload artifacts, activate hooks, create automations или approve real testing execution.

## Workflow и cadence

Closure verification order является fixed:

1. Исходные docs.
2. Source registry.
3. Docs contract tests.
4. `python tools\check_docs.py`.
5. Strict MkDocs build.
6. Опциональная полная closure.
7. Packaging/install smoke.
8. Approval-bound handoff packet.

Этот generated documentation site должен быть rebuilt с regular MkDocs `site_dir`:

```powershell
python -m mkdocs build --strict
```

Using только disposable `--site-dir` является не enough когда closure explicitly требует `site/` refresh.

## Обязательная проверка

Minimum closure evidence:

- focused docs contract test result для new pages, required source status и safety boundaries;
- `python tools\check_docs.py`;
- strict MkDocs build в `site/`;
- `git diff --check`;
- packaging/install smoke packet;
- explicit approval-bound handoff packet.

Опциональная полная closure когда risk или scope requires:

- full unittest с long timeout;
- fixture eval;
- transcript eval;
- Codex compatibility validation;
- reviewer pass поверх generated `site/`, long-line IA и accepted gaps.

Не заявляйте, что closure complete, пока текущий запуск не имеет matching command evidence или явно не фиксирует, какая verification не запускалась.

## Approval-Bound Handoff

Real testing execution остается approval-bound. Этот handoff packet следует list separate approval surfaces:

- `approved_local_runtime_launch`;
- `actual_browser_automation_smoke`;
- `approved_provider_api_pilot`;
- `approved_canonical_mutation_pilot`;
- `explicit_git_release_pr_action`.

Каждая surface требует owner, approved target, data policy, redaction/cache/budget boundary где relevant, rollback/disable path, ожидаемые доказательства, residual risk и stop condition.

Real testing может старт только после governance, runtime contract, audit/observability, target consent, QA/performance/stabilization и packaging/docs closure evidence являются current.

## Действия без approval не выполняются

Packaging и closure work не perform these actions без separate explicit owner approval:

- нет live server launch;
- нет browser automation;
- нет provider calls;
- нет live external model/API calls;
- нет canonical graph mutation;
- нет plugin publication;
- нет external write;
- нет package registry или marketplace upload;
- нет hook activation;
- нет active schedules, automations или GitHub Actions creation;
- нет `git add`, commit, push или PR;
- нет real testing execution.

## Риски And Failure Modes

- Трактовка packaging smoke как publish approval может create unauthorized release.
- Rebuilding disposable site но не `site/` leaves stale generated docs.
- Missing docs registry/control-plane sync может make source-backed claims drift.
- Plugin-cache mismatch может hide missing checked-in skills, especially `docs-maintainer`.
- Mermaid external asset dependency может break offline documentation expectations.
- Real testing может accidentally старт live execution если approval surfaces являются bundled together instead из separated.

## Next Action

After docs и packaging evidence являются current, next safe artifact является approval packet draft. Real testing execution, provider/API calls, canonical mutation и git release/PR actions остаются blocked пока their separate approvals exist.

## Актуальный маршрут и evidence

Package, install, hook trust и runtime activation проверяются отдельно. Portable/legacy formats описаны в [technical guide](technical.md); текущий пакет не мигрирован. Docs closure использует [обновлённый checklist](../playbooks/docs-update.md).
