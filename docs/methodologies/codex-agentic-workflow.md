# Codex / Agentic Workflow

Source status: `official OpenAI + verified methodology + local implementation evidence + tool-assisted + experiment`

Источники: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex customization](https://developers.openai.com/codex/concepts/customization), [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [Codex MCP](https://developers.openai.com/codex/mcp), [Codex hooks](https://developers.openai.com/codex/hooks), [Codex build plugins](https://developers.openai.com/codex/plugins/build), [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex memories](https://developers.openai.com/codex/memories), [Codex workflows](https://developers.openai.com/codex/workflows), [Codex automations](https://developers.openai.com/codex/app/automations), [Save workflows as skills](https://developers.openai.com/codex/use-cases/reusable-codex-skills), [Run verified operations](https://developers.openai.com/codex/use-cases/verified-operations-workflows), [Follow goals in Codex](https://developers.openai.com/codex/use-cases/follow-goals), [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents), [Agents SDK orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration), [Agents SDK guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals), [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/codex-agentic-workflow.md).

## Deep research цель

Codex / Agentic Workflow слой описывает, как большой проект использует Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, memory, sandbox, approvals, MCP, hooks, plugins, Agents SDK и automations без превращения чата в source of truth.

Главный принцип: чат является рабочей поверхностью, но не durable state. Требования, решения, ограничения, evidence, approvals, handoffs и promotion decisions должны жить в `AGENTS.md`, control-plane файлах, task packets, run logs, source registry и staged artifacts.

## Поддержанные факты

- Codex customization layers include `AGENTS.md`, skills, subagents, MCP, hooks, plugins, memory, workflows and automations; they solve different persistence and capability problems.
- Official Codex guidance treats `AGENTS.md` as durable project instructions and memory as recall layer, not source of mandatory project truth.
- Skills package repeatable workflows with trigger, inputs, steps, references/scripts, verification and failure modes.
- Subagents are useful for independent or specialist work, but require fresh-context task packets, ownership boundaries and handoff evidence.
- MCP, hooks, plugins and automations are capability surfaces with permission, trust, data-boundary and side-effect implications.
- Verified operations and goal-following workflows require structured inputs, current evidence, explicit approvals and auditable output.
- Agents SDK concepts such as handoffs, guardrails, tracing and human review are useful for code-owned agent apps, but must stay distinct from Codex App/CLI/IDE runtime workflow guidance.

## Assumptions

- Chat is a work surface, not source of truth; durable state belongs in checked-in artifacts.
- Reusable workflows should be promoted only after manual success, known failure modes and verification evidence.
- Subagents and parallel workers need explicit file/subsystem ownership. Overlap should route to sequential work.
- MCP and hooks should be reviewed as side-effecting capabilities before activation.
- Automations are only for stable recurring workflows with owner, cadence, verification and disable path.
- Model/reasoning policy should be role/risk based, not always maximum reasoning.

## Инструкции применения на проекте

1. Классифицировать задачу до старта: docs, web/front-end, backend, database, API, native/mobile, desktop, AI/eval, security, delivery/release, automation, plugin/skill, PR/review или long-running goal.
2. Начинать с read-only inventory, если задача нетривиальная: `AGENTS.md`, релевантные docs, target files, existing patterns, команды проверки, sandbox/approval constraints.
3. Для long-running/product work использовать control-plane files: `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`.
4. Держать durable project rules в `AGENTS.md`, а не в memory, private chat или повторяемых prompts.
5. Обновлять `AGENTS.md` только после понятной повторяющейся ошибки, recurring PR feedback или устойчивого workflow rule.
6. Использовать skills, когда workflow имеет clear trigger, inputs, outputs, steps, verification и failure modes.
7. Создавать skill только из proven manual workflow: successful run, known failure/risk и проверяемый output.
8. Упаковывать plugin, когда стабильный workflow надо распространять, ставить через marketplace или bundle-ить со skills, MCP, hooks, apps/assets.
9. Считать MCP capability boundary: tools/resources/prompts, trust level, data boundary, side effects, approvals и secrets handling должны быть явными.
10. Считать hooks executable policy: hook event, matcher, command, trust decision, failure behavior и disable path должны быть задокументированы до activation.
11. Использовать subagents только для независимых или specialist задач. Каждый subagent получает fresh-context task packet.
12. Не давать subagents пересекающиеся ownership зоны. Если файлы или contracts пересекаются, использовать sequential work с review checkpoint.
13. Для parallel work использовать worktrees или явный ownership map: owned files, forbidden files, merge path, evidence output.
14. Держать sandbox и approvals tight by default. External writes, GitHub/CI, publishing, production data, network-heavy work, hook activation и MCP side effects требуют explicit approval.
15. Выбирать runtime по задаче: Codex App/IDE для ambiguity и steering, CLI для local engineering, `codex exec` для stable non-interactive jobs, GitHub Action для PR/CI, MCP для external tools, Agents SDK для code-owned agent apps, automation для stable recurring workflows.
16. Задавать model/reasoning policy по риску: stronger reasoning для architecture, review, debugging, security, eval judging, migrations и ambiguous multi-step work; lower reasoning для bounded read-only или mechanical tasks.
17. Использовать memory только как recall layer. Required rules, source policy, acceptance criteria, secrets policy и verification commands должны жить в checked-in docs.
18. Любой completion/readiness claim должен ссылаться на current evidence: commands, checks, artifacts, runtime output, traces, screenshots, evals или explicit gap.
19. Продвигать повторяемые workflows по цепочке: manual thread -> playbook -> skill -> plugin -> automation.
20. Не активировать automation, пока нет manual stability evidence, owner, durable prompt, cadence, environment, verification и disable/rollback path.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| Agentic delivery loop | Любая нетривиальная работа | Discovery -> smallest useful plan -> focused slice -> verification -> risk review -> handoff/release evidence. |
| Control-plane docs-as-state | Long-running или production work | `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` вместо состояния в чате. |
| `AGENTS.md` durable rules | Повторяются team/project conventions | Repo layout, commands, standards, constraints, source policy и done criteria рядом с кодом. |
| Progressive disclosure skills | Workflow повторяется | `SKILL.md` с trigger, inputs, outputs, scripts/references, verification и failure modes. |
| Plugin packaging lifecycle | Workflow нужно распространять | `.codex-plugin/plugin.json`, bundled skills/MCP/hooks/apps/assets, owner, evals, update loop. |
| Fresh-context handoff | Нужен specialist/subagent | Task packet с sources, assumptions, owned files, forbidden files, expected evidence, output schema, stop condition. |
| Ownership-bound parallelism | Можно безопасно параллелить | Непересекающиеся files/subsystems, merge path, evidence output, fallback to sequential. |
| Approval-bound capability governance | Есть side effects или privileged actions | Sandbox, approvals, MCP, hooks, CI, publish, production и external-write boundaries до действия. |
| Evidence-before-completion | Любой done/works/passes claim | Текущие команды, artifacts, runtime evidence, traces/screenshots/evals или explicit gap. |
| Memory hygiene | Контекст повторяется между threads | Memory помогает recall, но mandatory rules и secrets policy живут в checked-in docs. |
| Automation promotion | Workflow стал predictable | Manual success -> skill/playbook -> candidate automation -> first-run review -> active schedule. |
| Agent eval loop | Качество agent behavior важно | Baseline, one focused change, rerun eval, inspect traces/artifacts, log result, threshold. |
| Runtime routing | Есть несколько поверхностей исполнения | Выбор между Codex App, IDE extension, CLI, `codex exec`, GitHub Action, MCP, Agents SDK, automation. |
| Model/reasoning policy | Важен cost/latency/quality tradeoff | Default model/reasoning, escalation, downgrade и budget по role/workflow. |

## Инструменты, артефакты и стандарты документирования

- `AGENTS.md`: durable project rules, source policy, commands, conventions, done criteria.
- `REQUIREMENTS.md`: users, goals, non-goals, constraints, acceptance criteria, source constraints.
- `PLAN.md`: smallest useful plan, ownership, gates, rollback, verification.
- `TEST.md`: unit/integration/runtime/manual/eval checks and commands.
- `EVALS.md`: subjective or long-horizon quality thresholds, datasets, judge criteria.
- `RUNLOG.md`: decisions, command evidence, failures, residual risks, next action.
- `agent-task-packet.md`: fresh-context packet для subagent/parallel worker.
- `handoff-contract.md`: output schema, evidence fields, stop conditions.
- `worktree-ownership.md`: parallel ownership map and merge boundaries.
- `skill-candidate.md`: manual workflow evidence before skill creation.
- `skill-failure-log.md`: trigger misses, missing inputs, unsafe actions, verification failures.
- `plugin-blueprint.md`: users, bundled skills, MCP/hooks/apps, permissions, evals, owner.
- `mcp-permission-review.md`: tools/resources/prompts, trust level, side effects, approval policy.
- `hook-activation-record.md`: hook source, event, command, trust decision, failure behavior.
- `approval-record.md`: external write or privilege escalation approval, scope, rollback.
- `automation-candidate.md`: manual stability evidence, cadence, prompt, environment, verification, disable path.
- `model-reasoning-policy.md`: role/workflow defaults, escalation/downgrade rules, budget.
- `context-memory-policy.md`: что живет в chat, `RUNLOG.md`, `AGENTS.md`, memory и source docs.
- `agent-eval-case.md`: input, expected behavior, trace/evidence, grader, threshold, failure label.
- `release-packet.md`: final evidence, risks, approvals, next action for merge/release.

## Что еще включить в deep research

- Maturity levels: `manual`, `repeatable`, `skill`, `plugin`, `automation`, `managed`.
- Runtime decision matrix: Codex App vs IDE extension vs CLI vs `codex exec` vs GitHub Action vs MCP vs Agents SDK.
- Subagent safety policy: когда параллелить, когда запрещать, когда требовать worktree.
- MCP permission model: read-only resources, side-effecting tools, secrets, trust level, approval policy.
- Hook governance: activation, trust review, deterministic failure behavior, disable path.
- Skill lifecycle: trigger tests, negative trigger tests, missing-input behavior, verification failures, failure log.
- Plugin lifecycle: marketplace, versioning, permissions, bundled components, eval cases, owner/update loop.
- Automation lifecycle: manual prompt test, first-run review, cadence, environment, worktree/local mode, disable/rollback.
- Memory and context policy: что можно запоминать, что нельзя, как не хранить secrets/private context.
- Agent evals: trace-derived datasets, tool-call correctness, handoff correctness, regression thresholds.
- Model/reasoning policy: роль, риск, latency, cost, escalation, downgrade.

## Product-Agent OS routing

- `project-lifecycle-orchestrator` классифицирует task archetype, runtime surface и следующий lifecycle skill.
- `workspace-discovery-auditor` начинает read-only и фиксирует project docs, target files, commands, patterns, risks and sandbox/approval constraints.
- `requirements-author` превращает ambiguous request в users, goals, constraints, acceptance scenarios and source constraints.
- `implementation-planner` блокирует plan-ready status, если нет source of truth, ownership, gates, rollback или verification.
- `agent-team-designer` создает fresh-context packets, role ownership, handoff contracts and stop conditions for subagents/parallel workers.
- `test-eval-designer` определяет current evidence: tests, builds, runtime checks, screenshots, traces, evals, artifacts.
- `risk-reviewer` проверяет approval boundaries, unsupported claims, overlapping edits, security/data/release risks.
- `pr-release-operator` собирает release/merge evidence packet and finish options.
- `learning-loop-maintainer` переносит failures, repeated mistakes and improvement decisions into durable artifacts.
- `automation-promoter` создает только candidate automation до manual stability evidence и explicit approval.

## Candidate readiness gates

- `agentic_scope_classified`: use-case archetype, runtime surface and task type are explicit.
- `source_of_truth_present`: durable artifacts exist; chat is not the only source of truth.
- `control_plane_present`: required `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` exist for multi-slice work.
- `read_only_discovery_complete`: current docs, files, commands, patterns and sandbox/approval context were inspected.
- `approval_boundary_present`: external writes, privileged actions, MCP side effects, hooks, CI, release and production data have owner, approval and rollback/disable path.
- `fresh_context_handoff_present`: any subagent/parallel worker has task packet with sources, assumptions, ownership, forbidden files, expected evidence and stop condition.
- `ownership_split_present`: parallel files/subsystems do not overlap or fallback is sequential.
- `subagent_parallelism_safe`: work is independent enough to justify subagents.
- `skill_promotion_evidence_present`: skill has manual success evidence, trigger, inputs, outputs, verification and failure modes.
- `plugin_boundary_present`: plugin has manifest, components, permissions, evals and owner/update loop.
- `mcp_permission_review_present`: MCP capabilities, trust level, data boundary, side effects and approval policy are documented.
- `hook_activation_approval_present`: hook event, matcher, command, trust decision and failure behavior are documented and approved.
- `automation_manual_stability_present`: automation has manual test evidence, durable prompt, cadence, environment, owner, verification and disable path.
- `model_reasoning_policy_present`: durable roles/workflows have default model/reasoning, escalation/downgrade and budget.
- `memory_policy_present`: memory is recall only; mandatory rules and secrets policy live in checked-in docs.
- `agent_eval_workflow_present`: agent behavior changes have baseline, eval cases, threshold, rerun command and failure labels.
- `agentic_evidence_before_completion`: completion/readiness claim cites current evidence or explicit gap.

## Candidate eval fields

- Agentic scope and runtime surface are classified.
- Source-of-truth artifacts exist and chat is not the only durable state.
- Read-only discovery inspected docs, files, commands and sandbox/approval constraints.
- Approval boundary exists for MCP, hooks, CI, release, external writes and production data.
- Subagent packet includes sources, assumptions, owned files, forbidden files, expected evidence and stop condition.
- Parallel work has non-overlapping ownership or sequential fallback.
- Skill promotion has manual success evidence, trigger, inputs, outputs, verification and failure modes.
- Plugin boundary includes manifest, bundled capabilities, permissions, eval cases and owner/update loop.
- Automation has manual stability evidence, durable prompt, owner, cadence, verification and disable path.
- Completion claim cites current evidence or explicit gap.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Durable rules | `AGENTS.md` | Project rules, commands, source policy and done criteria. |
| Control plane | `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` | Long-running product work state and evidence. |
| Codex runtime config | `config.toml` | Model, reasoning and runtime defaults when project-owned. |
| Handoff | `agent-task-packet.md`, `handoff-contract.md` | Fresh-context subagent work and expected evidence. |
| Skills | `SKILL.md` | Repeatable workflow packaging after manual success. |
| Plugins | `.codex-plugin/plugin.json` | Bundle skills, MCP, hooks, apps/assets and permission expectations. |
| MCP review | `mcp-permission-review.md` | Tool/resource/prompt trust, side effects, secrets and approvals. |
| Hooks | `hooks.json`, `hook-activation-record.md` | Event/matcher/command, trust decision and disable path. |
| Automations | `automation.toml`, `automation-candidate.md` | Stable recurring workflow candidate and manual review evidence. |
| Agent workflow readiness | `agentic-workflow-readiness.md` | Combined gate packet before promotion or orchestration. |

## Проверки

- Workflow starts from classified use-case archetype and selected runtime.
- Source-of-truth artifacts are present and current.
- Read-only discovery inspected project docs, target files, commands and sandbox/approval context.
- Subagent work has task packet, ownership, forbidden files, output schema and stop conditions.
- Parallel work has explicit ownership or uses sequential fallback.
- Skill promotion is backed by manual evidence and failure modes.
- Plugin packaging includes manifest, bundled components, permissions, eval cases and owner/update loop.
- MCP and hooks have capability/trust/approval review before side effects or activation.
- Automation remains candidate-only until manual stability evidence exists.
- Model/reasoning policy is explicit for durable agents/workflows.
- Memory is not used as source of mandatory project truth.
- Final claims cite current evidence.

## Типовые сбои

- Chat contains real requirements while project artifacts stay stale.
- `AGENTS.md` becomes vague, obsolete or filled with one-off instructions.
- Subagents edit overlapping files without ownership.
- Handoffs omit source constraints, assumptions, evidence or stop conditions.
- Skills are created from ideas without successful manual workflow evidence.
- Plugins are packaged before permissions, evals and owner/update loop exist.
- MCP tools are treated as safe even when they expose side effects.
- Hooks are enabled without trust review or failure-mode documentation.
- Automations are scheduled before prompt/tools are stable.
- Memory stores context that should be checked into docs, or contains private/secrets material.
- Completion is claimed from inspection-only evidence.
- Agents SDK concepts are copied into Codex runtime docs without distinguishing runtime layers.

## Unsupported claims not adopted

- "Memory is project source of truth." Memory is recall only; durable rules and evidence belong in files.
- "Subagents are automatically faster." They help only when work is independent and ownership is clear.
- "MCP tools are safe because they are tools." MCP can expose data and side effects and needs trust review.
- "Hooks are just convenience scripts." Hooks are executable policy and need approval, failure behavior and disable path.
- "A repeated workflow should become automation immediately." Automation follows manual stability and first-run review.
- "Agents SDK and Codex runtime are the same layer." Agents SDK is for code-owned agent apps; Codex App/CLI/IDE is the engineering runtime.

## Open questions for future implementation

- Which maturity labels should Product-Agent OS use: `manual`, `repeatable`, `skill`, `plugin`, `automation`, `managed`?
- Should runtime routing be a single decision matrix or split by use-case archetype?
- Which subagent tasks require worktrees by default?
- Should MCP permission review be generated for every MCP config change or only side-effecting capabilities?
- How should skill trigger tests and negative trigger tests be stored?
- Which agent eval cases are enough before promoting a workflow to plugin or automation?
