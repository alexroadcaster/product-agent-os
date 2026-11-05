---
title: "Архив — Product-Agent OS Batch 40 S5: пилотные метрики и закрытие Doubt verifier"
---

# Архив — Product-Agent OS Batch 40 S5: пилотные метрики и закрытие Doubt verifier {#product-agent-os-batch-40-s5-doubt-verifier}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `project-authored implementation evidence`. Этот пакет является source-owned evidence для Batch 40 S5 и не является generated `site/` output.

## Пакет пилотных метрик и закрытия B40-S5

B40-S5 закрывает `B40-DVL-M22..M24` для локального Doubt / verifier loop через детерминированные артефакты `completion_skeptic_manual_pilot_ledger`, `completion_skeptic_scorecard_calibration` и `completion_skeptic_go_no_go_closure`.

Границы:

- pilot scope: `synthetic_local`.
- decision: `manual_only`.
- promotion status: `not_promoted`.
- release posture: `not_ready_for_automation_or_release`.
- реальные project pilots, live server, browser automation, provider/API call, MCP server, Agents SDK runner, canonical graph mutation, external write, hook/automation activation и git action не выполнялись.

## Пилотный Ledger

`completion_skeptic_manual_pilot_ledger` записывает пять строк `synthetic_local`, чтобы выполнить существующий порог `min_sample_size: 5` без заявления, что три примера доказывают продуктовую ценность.

| pilot id | archetype | цель | ожидаемая реакция verifier | attempt/failure/fix/retest |
| --- | --- | --- | --- | --- |
| `synthetic-pilot-1` | `docs_research` | Проверка source-sensitive documentation claims. | Найти unsupported или stale source claims и потребовать fresh evidence либо accepted gap. | attempt/failure/fix/retest recorded. |
| `synthetic-pilot-2` | `code_check` | Проверка code/tool claim до статуса done. | Требовать current command evidence, а не user-claimed command output. | attempt/failure/fix/retest recorded. |
| `synthetic-pilot-3` | `expected_block` | Проверка отказа для approval-bound action. | Блокировать pass/release claims, если нет approval evidence. | attempt/failure/fix/retest recorded. |
| `synthetic-pilot-4` | `docs_research` | Учёт false positive candidate. | Сохранять false positives видимыми без автоматического превращения в rewrites. | attempt/failure/fix/retest recorded. |
| `synthetic-pilot-5` | `code_check` | Повторная проверка evidence sufficiency. | Подтвердить доступные command/source evidence и residual gaps. | attempt/failure/fix/retest recorded. |

Поля ledger:

- `pilot_denominators`: sample size, scenario mix, owner review status и no-unapproved-actions proof.
- `false_pass`: все строки false.
- `false_rewrite`: все строки false.
- `evidence_sufficient`: все строки true для synthetic-local examples.
- `owner_accepted_gap`: один accepted metrics gap для synthetic-only calibration.
- `no_unapproved_actions`: true.

## Калибровка Scorecard

`completion_skeptic_scorecard_calibration` оборачивает существующий scorecard и добавляет numerator/denominator evidence для promotion review:

| metric | numerator | denominator | примечание |
| --- | ---: | ---: | --- |
| `false_pass_rate` | 0 | 5 | Synthetic rows не допускают false pass. |
| `false_rewrite_rate` | 0 | 5 | Gate может предложить revisions, но не unsupported rewrites. |
| `evidence_sufficiency_rate` | 5 | 5 | Synthetic examples содержат sufficient local evidence fields. |
| `missing_check_catch_rate` | 5 | 5 | Missing-check cases отлавливаются. |
| `accepted_gap_rate` | 1 | 5 | Один accepted metrics gap оставляет synthetic scope явным. |
| `user_revision_acceptance_rate` | 5 | 5 | Synthetic revision offers приняты. |
| `revision_usefulness_rate` | 5 | 5 | Synthetic revisions помечены useful только для calibration. |

Решение calibration:

- `decision_status`: `calibrated_with_accepted_metrics_gap`.
- `promotion_policy`: `manual_only_synthetic_calibration_gap`.
- owner review status: `accepted_gap`.

Эта calibration имеет numerator/denominator evidence, но остаётся synthetic. Она не доказывает broad semantic usefulness, real user value, release readiness или automation readiness.

## Go/No-Go

`completion_skeptic_go_no_go_closure` записывает финальное решение Batch 40 S5:

- `decision_status`: `manual_only`.
- `promotion_status`: `not_promoted`.
- implemented rows: `B40-DVL-M22`, `B40-DVL-M23`, `B40-DVL-M24`.
- `rollback_disable_path`: оставить `completion-skeptic` как manual-only; удалить candidate reminder/template references перед любой будущей activation.
- `next_approval_needs`: `exact_owner_approval_for_release_or_automation`, `exact_owner_approval_for_git_stage_commit_push_pr`, `exact_owner_approval_for_real_project_pilots`.

Promotions, заблокированные без точного последующего approval:

- active automation.
- MCP server.
- Agents SDK runner.
- live provider/runtime call.
- browser automation.
- target workspace apply.
- canonical graph mutation.
- git stage/commit/push/PR или public/team release.

## Verification Contract

B40-S5 добавляет focused unit coverage для:

- `build_completion_skeptic_pilot_ledger`.
- `build_completion_skeptic_scorecard_calibration`.
- `build_completion_skeptic_go_no_go_packet`.
- `build_completion_skeptic_metrics_loop_record`.
- fixture checks `completion_skeptic_manual_pilot_ledger_present`, `completion_skeptic_scorecard_calibration_present` и `completion_skeptic_go_no_go_closure_present`.
- docs/control-plane sync для этого packet, registry, Track 10 backlog, Track 10 plan, `RUNLOG.md`, `TEST.md` и `AGENTS.md`.

## Verification Evidence

Текущий run:

- focused B40-S5 code/docs contracts сначала упали на missing S5 helper API и missing source packet; после реализации прошли.
- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`: 78 tests, `OK`.
- `python -m unittest discover -s tests -p "test_*.py" -v`: 871 tests, `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py`: exit `0`, `renderer_file_count: 197`, checks `completion_skeptic_manual_pilot_ledger_present`, `completion_skeptic_scorecard_calibration_present` и `completion_skeptic_go_no_go_closure_present` true.
- `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json`: exit `0`, 26 sessions, 0 failures.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py`: `status: compatible`.
- strict MkDocs build: exit `0`.
- generated-site file-safe cleanup removed absolute `/en/` fallback links from English-original plan pages.
- `python tools\check_docs.py`: `OK`.
- `git diff --check`: exit `0`.

Generated `site/` был rebuilt для S5, потому что новый RU/EN source packet изменил full-site i18n, search и sitemap inventory. Generated `site/` остаётся не source of truth.
