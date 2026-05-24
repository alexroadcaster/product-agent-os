# Specification: Product-Agent OS plugin

Source status: `official + experiment`  
Источники: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk), [Codex use cases](https://developers.openai.com/codex/use-cases), [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/).

## Назначение

`product-agent-os` - это production-ready Codex plugin, который превращает текущий workspace пользователя в управляемую среду реализации проекта через Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, hooks, evals и automation candidates.

Plugin должен вести проект от идеи до production-ready результата:

```mermaid
flowchart LR
    A["Idea"] --> B["Discovery"]
    B --> C["Requirements"]
    C --> D["Plan"]
    D --> E["Agent team"]
    E --> F["Build slices"]
    F --> G["Tests and evals"]
    G --> H["Review"]
    H --> I["PR or release packet"]
    I --> J["Learning loop"]
    J --> K["Automation candidates"]
```

Главная цель plugin - не создать набор файлов один раз, а поддерживать lifecycle проекта через проверяемые артефакты, gated changes, role ownership, handoff contracts и evidence. Track 6 расширяет это до engineering standards layer: product hypothesis, architecture boundary, test-first/eval-first verification, docs-as-code, human review, release measurement и learning loop.

## Не цели

- Не заменять human product owner: спорные цели, рискованные approvals и irreversible actions остаются за пользователем.
- Не менять global `~/.codex/config.toml`, глобальные credentials или user-level memory без явного запроса.
- Не запускать все skills подряд. Orchestrator выбирает маршрут по профилю проекта и текущему lifecycle state.
- Не сохранять secrets, tokens, private customer data, raw credentials, private chat logs или PII в generated files, memory, docs, fixtures, examples или run logs.
- Не создавать automation до ручной стабилизации workflow и появления failure log.

## Target users

| Пользователь | Задача | Основной режим |
| --- | --- | --- |
| Solo developer | Быстро структурировать проект и довести feature до PR | `guided-small` |
| Product engineer | Вести full feature с требованиями, планом, тестами, review и release notes | `standard-product` |
| Engineering team | Разделить работу между агентами, worktrees и review gates | `production-team` |
| AI product team | Добавить eval-driven loop, prompt/context policy и regression checks | `ai-product` |
| Enterprise team | Ужесточить approvals, hooks, audit trail и automation promotion | `enterprise-governed` |

## Supported surfaces

| Surface | Поддержка | Использование |
| --- | --- | --- |
| Codex App | primary | Инициализация, long-running project threads, worktrees, artifacts, automations |
| Codex CLI | primary | Local implementation, `codex exec`, project `.codex/config.toml` |
| IDE extension | assisted | Scoped edits and review from editor context |
| Cloud task | optional | Background repo work after setup commands and environment are known |
| GitHub | optional | PR packet, review, CI failure triage, release notes |
| MCP | optional | Context7 docs, Codex MCP, GitHub, Figma, Sentry, Linear, Slack when available |
| Agents SDK | advanced | Programmable Manager pattern with Codex MCP for teams that need orchestration runtime |
| Automation | gated | Only stable recurring workflows with audit artifact and failure log |

## Plugin package

Production package layout:

```text
product-agent-os/
  .codex-plugin/
    plugin.json
  skills/
    project-lifecycle-orchestrator/
    workspace-discovery-auditor/
    requirements-author/
    implementation-planner/
    agent-team-designer/
    test-eval-designer/
    risk-reviewer/
    pr-release-operator/
    learning-loop-maintainer/
    automation-promoter/
  scripts/
    detect_project.py
    merge_markdown.py
    validate_control_plane.py
    validate_agents.py
    validate_hooks.py
    run_fixture_eval.py
  assets/
    templates/
      control-plane/
      agents/
      hooks/
      workflows/
        source-context-pack.md
        worktree-ownership.md
        build-slice.md
        development-standards.md
        documentation-system.md
        first-run-intake.md
        bug-rescue.md
        greenfield-idea-to-plan.md
        complex-system-acceleration.md
        pr-review-readiness.md
        legacy-onboarding.md
        api-migration.md
        ai-eval-regression.md
        native-mobile-feature.md
        desktop-local-first.md
        data-migration.md
        security-sensitive-change.md
        ci-stabilization.md
      artifact-templates/
        adr.md
        architecture-overview.md
        domain-modeling.md
        metric-spec.md
        api-contract-review.md
        component-card.md
        database-dictionary.md
        bug-rescue-report.md
        greenfield-idea-brief.md
        integration-catalog.md
        pr-risk-review.md
        onboarding-map.md
        migration-plan.md
        ai-eval-spec.md
        security-risk-review.md
        ci-stabilization-report.md
        agent-task-packet.md
        behavioral-eval-case.md
        plan-quality-check.md
        codex-compatibility-report.md
      evals/
      pr/
      automations/
    fixtures/
      empty-repo/
      node-app/
      python-app/
      monorepo/
      docs-repo/
      existing-codex-config/
  hooks/
    pre_tool_use_policy.py
    permission_request_summary.py
    post_tool_use_evidence.py
    stop_runlog_reminder.py
  .mcp.json
```

`plugin.json` должен указывать packaged skills, optional MCP config, interface metadata, capabilities и default prompts. Skills используют `agents/openai.yaml` для display metadata, invocation policy и tool dependencies. Для source-sensitive skills default policy: `allow_implicit_invocation: false`.

## Lifecycle state machine

`project-lifecycle-orchestrator` является entrypoint. Он определяет текущее состояние проекта и выбирает следующий skill.

| State | Trigger | Required artifact | Gate before next state |
| --- | --- | --- | --- |
| `uninitialized` | Plugin впервые применен к workspace | `PROJECT_AUDIT.md` или audit section in `RUNLOG.md` | Discovery complete, no write yet |
| `infrastructure_planned` | Audit completed | `INFRASTRUCTURE_PLAN.md` or staged plan section | User approves write scope |
| `requirements_ready` | Goal and constraints clear | `REQUIREMENTS.md` | Acceptance criteria explicit |
| `plan_ready` | Requirements stable | `PLAN.md` | Ownership and verification named |
| `team_ready` | Work needs roles or parallelism | `.codex/agents/*.toml` | Write scopes do not overlap |
| `build_active` | Approved implementation slice | Diff + `RUNLOG.md` entry | Slice verification run |
| `quality_gate` | Build slice completed | `TEST.md`, `EVALS.md`, reports | No blocking failure |
| `review_ready` | Checks pass or failures documented | Review findings | No unresolved blocker |
| `release_ready` | Review complete | PR packet or release packet | Verification evidence included |
| `learning_ready` | Delivery complete | Updated `RUNLOG.md`, skill candidates, automation candidates | Reusable lessons classified |
| `maintenance` | Stable recurring workflow exists | Automation candidate packet | Manual workflow stable |

The orchestrator must never skip from `uninitialized` to `build_active`.

## Complexity profiles

Plugin computes a `ComplexityProfile` during discovery.

```yaml
profile:
  name: "guided-small | standard-product | production-team | ai-product | enterprise-governed | autonomous-maintenance"
  confidence: "high | medium | low"
  drivers:
    repo_size: "small | medium | large"
    stack_count: 1
    service_count: 1
    test_maturity: "none | partial | strong"
    ci_present: true
    external_integrations: []
    risk_level: "low | medium | high"
    team_mode: "solo | team | enterprise"
    autonomy_target: "supervised | assisted | recurring"
    change_surface: "docs | code | production_ops | external_systems"
  recommended_route:
    - "workspace-discovery-auditor"
    - "requirements-author"
    - "implementation-planner"
```

Profile decisions:

| Profile | Creates | Skips by default |
| --- | --- | --- |
| `guided-small` | `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `RUNLOG.md` | Custom agents beyond planner/reviewer, automations |
| `standard-product` | Control-plane files, role cards, basic hooks, eval skeleton | Enterprise rules, programmable runner |
| `production-team` | Worktree strategy, full agent team, strict handoff, PR packet | Autonomous recurring tasks until stable |
| `ai-product` | Prompt/context policy, eval suite, LLM-as-judge rubric, regression logs | External writes without approval |
| `enterprise-governed` | Strict approval policy, forbidden paths, audit evidence, staged config | Global config mutation |
| `autonomous-maintenance` | Automation candidates, recurring run prompts, failure log | New automations without manual success history |

## Initialization behavior

After user invokes the plugin:

1. Read `AGENTS.md`, README, package files, CI config, test config, `.codex/`, `docs/`, git state and current working tree status.
2. Produce read-only `WorkspaceAudit`.
3. Infer complexity profile and `usage_mode`.
4. Return `usage_mode.primary`, `secondary`, `confidence`, route reasons, fallback, minimum artifacts, behavioral eval cases and first-response contract.
5. Ask only blocking clarifying questions. Examples: product goal absent, destructive rewrite requested, ambiguous ownership, missing test command for production profile, or route confidence is low.
6. Propose an `InfrastructurePlan`.
7. Present staged changes with file list and write policy.
8. Wait for explicit approval before writing.

Expected first response shape:

```yaml
workspace_audit:
  status: "ready_for_plan | blocked | needs_user_input"
  detected_stack: []
  existing_control_plane: []
  missing_control_plane: []
  risks: []
complexity_profile:
  name: ""
  confidence: ""
infrastructure_plan:
  create: []
  update: []
  leave_unchanged: []
  requires_approval: []
usage_mode:
  primary: ""
  secondary: []
  confidence: ""
  minimum_artifacts: []
  behavioral_eval_cases: []
questions:
  - ""
next_action: "approve_infrastructure_plan | answer_questions | run_read_only_audit_again"
```

## Track 8 usage-mode implementation status

The plugin must not blur implemented workflows with partial or pending coverage.

| Status | Meaning | Modes |
| --- | --- | --- |
| `done` | Route, workflow template, artifact template or explicit artifact, behavioral eval coverage and verification evidence exist. | `first-run-intake`, `bug_rescue`, `greenfield_idea`, `complex_system_acceleration`, `pr_review`, `legacy_onboarding`, `api_migration`, `ai_eval_regression`, `native_mobile_feature`, `desktop_local_first`, `data_migration`, `security_sensitive_change`, `ci_stabilization`, `release_packaging`. |
| `done methodology gate` | Reusable behavior exists with template, skill, behavioral eval and fixture coverage. | no-placeholder planning, generalized two-stage review, fresh-context handoff, acceptance scenarios, conditional DDD domain modeling, bounded-context-to-architecture traceability, ubiquitous language traceability, conditional FSD structure routing, metric hardening, evidence-before-completion, docs tooling selector with `docs_as_code_impact` statuses, conditional readiness gates with `readiness_statuses`. |
| `done documentation` | Operator-facing docs exist for route selection, eval behavior and Codex-only packaging scope. | `docs/product-agent-os/scenarios.md`, `behavioral-evals.md`, `codex-compatibility.md`. |
| `done eval runner` | Deterministic transcript/session replay exists for synthetic or redacted sessions without external model calls. | `run_transcript_eval.py`, `product_agent_os/transcript_evals.py`, `product-agent-os-synthetic-sessions.json`. |
| `partial` | Some reusable behavior exists, but the full planned contract is not complete. | lifecycle trigger hardening. |

## Generated project files

| File | Owner | Purpose | Update rule |
| --- | --- | --- | --- |
| `AGENTS.md` | Orchestrator + user approval | Durable project rules | Only stable rules that apply across future tasks |
| `REQUIREMENTS.md` | Product Manager role | Goal, users, scope, non-goals, acceptance criteria | When product intent changes |
| `PLAN.md` | Architect role | Decomposition, ownership, sequence, no-placeholder plan quality, risks, rollback | Before implementation and when plan changes |
| `TEST.md` | Tester role | Deterministic checks, manual QA, visual QA | Before quality gate |
| `EVALS.md` | Eval designer role | Subjective checks, LLM-as-judge rubric, thresholds | For AI, UX, docs, long-horizon or subjective outputs |
| `RUNLOG.md` | Orchestrator | Iterations, scores, decisions, evidence, handoff summary | Every meaningful lifecycle step |
| `.codex/config.toml` | Orchestrator + user approval | Project-scoped Codex defaults | Staged; never overwrite blindly |
| `.codex/agents/*.toml` | Agent team designer | Project-scoped custom agents | Generated from role cards and profile |
| `.codex/hooks/*` | Hook author | Deterministic guardrails and evidence capture | Enabled only after validation |
| `.codex/workflows/*.md` | Workflow builder | Reusable task packets | Created from stable routes |
| `.codex/evals/*.json` | Eval designer | Fixture evals and expected behaviors | Updated from failure log |

## System file update policy

Plugin updates system files through merge-safe sections.

Generated sections use stable markers:

```markdown
<!-- product-agent-os:start <section-id> -->
...
<!-- product-agent-os:end <section-id> -->
```

Rules:

- User-authored content outside managed sections is preserved.
- Existing managed sections are updated only after a new plan is shown.
- If a file exists without markers, plugin proposes an append or separate companion file.
- If merge is ambiguous, plugin stops and returns a conflict report.
- Source-backed claims require official source or `experiment` label.

## Context and information overflow policy

Plugin uses layered context.

| Layer | Contents | Loaded when |
| --- | --- | --- |
| Hot | `AGENTS.md`, active `REQUIREMENTS.md`, active `PLAN.md`, current task packet | Every lifecycle step |
| Warm | `TEST.md`, `EVALS.md`, latest `RUNLOG.md` summary, active role cards | Planning, build, review, eval |
| Cold | Archived runlogs, historical eval reports, old decisions, source cards | Only when referenced |
| External | Official docs, Context7, MCP sources | When freshness or library detail matters |

Compaction rules:

- `RUNLOG.md` keeps current best, latest iterations and handoff summary.
- Older iterations move to `docs/runlogs/archive/YYYY-MM-DD-<topic>.md` or `.codex/runlogs/archive/` depending on project convention.
- Raw subagent logs are summarized into evidence, decisions and risks.
- `AGENTS.md` stays concise; long guidance moves to docs or `.codex/workflows/`.
- Skill bodies stay short; long details live in `references/`.
- Memory is never used as citation source; important facts are retrieved or read from checked-in docs.

## Skills

| Skill | Job | Required inputs | Output | Verification |
| --- | --- | --- | --- | --- |
| `project-lifecycle-orchestrator` | Route the lifecycle and enforce gates | User goal, workspace audit, current state | Next action packet | State transition is valid |
| `workspace-discovery-auditor` | Read-only project audit | Workspace path | `WorkspaceAudit` | No writes; detected files exist |
| `requirements-author` | Create/update requirements | Goal, users, constraints | `REQUIREMENTS.md` | Acceptance criteria present |
| `implementation-planner` | Produce executable plan | Requirements, audit | `PLAN.md` | Ownership, tests, rollback named |
| `agent-team-designer` | Generate roles and custom agents | Plan, complexity profile | `.codex/agents/*.toml` | TOML validates |
| `test-eval-designer` | Define tests and evals | Requirements, plan, stack | `TEST.md`, `EVALS.md` | Thresholds and artifacts explicit |
| `risk-reviewer` | Review diff and project risk | Diff, plan, tests | Findings by severity | No unsupported claims |
| `pr-release-operator` | Prepare PR/release packet | Diff, checks, runlog | PR body, release notes, rollback | Evidence included |
| `learning-loop-maintainer` | Capture reusable lessons | Final result, failures | `AGENTS.md` suggestions, skill candidates | Lessons classified |
| `automation-promoter` | Propose recurring runs | Stable workflow, failure log | Automation candidate packet | Manual success history exists |

Each skill must define trigger, boundaries, inputs, outputs, failure modes and final response contract.

Track 3 workflow templates cover task-packet jobs that are not packaged as `SKILL.md` bundles in the current implementation:

- `source-context-pack.md` covers official-source and Context7 research packets.
- `worktree-ownership.md` covers parallel ownership and worktree maps.
- `build-slice.md` covers one approved implementation slice with verification evidence.
- `development-standards.md` covers product hypothesis, architecture boundary, test-first/eval-first verification, bounded agent implementation, review and release measurement.
- `documentation-system.md` covers docs-as-code source-of-truth artifacts for architecture, API, UI, code reference, database and release docs.

Track 7 artifact templates cover methodology outputs that are too concrete to leave as prose-only workflow advice:

- `adr.md` for architecture decision records with context, decision, consequences, verification and rollback.
- `architecture-overview.md` for C4-style system/container notes, quality attributes and architecture risks.
- `domain-modeling.md` for bounded context, ubiquitous language traceability, aggregates, invariants, domain events, context maps and bounded-context-to-architecture traceability.
- `metric-spec.md` for product hypothesis, baseline, North Star or primary value metric, input metric, counter-metric, guardrail metrics, proxy metric risk, privacy classification, retention period, data minimization, owner signoff, Goodhart checks and post-release review.
- `api-contract-review.md` for OpenAPI, AsyncAPI, auth, errors, examples, compatibility and generated docs checks.
- `component-card.md` for UI states, accessibility, public API and Storybook documentation.
- `database-dictionary.md` for table meaning, sensitive fields, retention, migration history and schema verification.

Track 8 completed workflow templates cover scenario-specific first actions:

- `first-run-intake.md` keeps first launch small for empty, broken, existing control-plane and complex system starts: mode, confidence, next smallest action, minimum artifacts, approval boundary and evidence gaps.
- `bug-rescue.md` and `bug-rescue-report.md` enforce reproduction and root-cause evidence before fixes.
- `greenfield-idea-to-plan.md` and `greenfield-idea-brief.md` block scaffold before selected direction and approval.
- `complex-system-acceleration.md` and `integration-catalog.md` force ownership split, release gates and integration risk mapping before parallel work.
- `pr-review-readiness.md` and `pr-risk-review.md` provide read-only changed-file review with spec compliance before quality/risk verdict.
- `review-slice.md`, `RUNLOG.md`, `pr-risk-review.md` and `risk-reviewer` generalize that two-stage review to risky public-contract, migration, security-sensitive, data migration, release packaging and parallel slices.
- `agent-team-designer`, `handoff-contract.md`, `agent-task-packet.md` and `worktree-ownership.md` require fresh-context handoff before subagent or parallel worker execution.
- `acceptance-scenarios.md`, generated `REQUIREMENTS/TEST/EVALS`, `development-standards.md`, `requirements-author`, `implementation-planner`, `test-eval-designer`, `project-readiness.json` and `behavioral-workflows.json` require ATDD/BDD traceability before behavior changes: `requirement -> scenario -> check -> evidence owner`, Given/When/Then or equivalent behavior format, business rule, edge case, non-goal, explicit gap and evidence owner.
- `domain-modeling.md`, `architecture-overview.md`, `project-readiness.json`, `discovery.py`, `implementation-planner` and fixture eval require conditional DDD domain modeling for complex backend/workflow/enterprise/data-heavy/multi-service/multi-context work, plus `bounded_context_architecture_boundary_trace` from every bounded context to an architecture boundary or accepted gap and `ubiquitous_language_traceability` from each domain term to requirement/source plus API/event/contract, UI label, code module or owner; simple CRUD or simple MVP work can mark DDD as not applicable or accepted gap.
- `component-card.md`, `development-standards.md`, `project-readiness.json`, `discovery.py`, `workspace-discovery-auditor` and `implementation-planner` support optional `fsd_structure` for applicable web UI/component work; backend, native, simple CRUD and simple MVP work can mark Feature-Sliced Design as not applicable or accepted gap.
- `metric-spec.md`, `release-packet.md`, generated `REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills and fixture eval require `metric_hardening_when_product_behavior_changes` for product behavior changes; product success claims need counter-metric, guardrail, qualitative review and post-release review evidence, not a single proxy metric.
- `docs-tooling-decision.md`, `documentation-system.md`, generated `PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills, `discovery.py` and fixture eval require `docs_tooling_selector` and `docs_as_code_impact` statuses for stack-aware docs tooling without forced installs or unapproved external activation.
- `project-readiness.json`, generated `AGENTS/PLAN/TEST/EVALS/RUNLOG`, lifecycle skills and fixture eval require conditional readiness gates with `readiness_statuses`, applicability, required evidence, owner and residual risk; detection alone can only support `present_unverified`.
- `legacy-onboarding.md` and `onboarding-map.md` keep old or undocumented repos in read-only orientation with `present_unverified` claims before refactor.
- `api-migration.md` and `migration-plan.md` route HTTP API and event contract changes through OpenAPI/AsyncAPI, consumers, generated clients, backwards compatibility, deprecation, rollout, release impact and owner review gates before implementation or release.
- `ai-eval-regression.md` and `ai-eval-spec.md` route AI/RAG quality regressions through baseline, no-secrets dataset policy, prompt/context, retrieval metrics, judge rubric, threshold, latency, cost, grounding, one-factor-at-a-time change, rerun command, failure examples and residual risk before model, prompt, retrieval, dataset, rubric, or threshold changes.
- `native-mobile-feature.md` routes iOS/Android/native mobile changes through platform assumptions, permissions, offline state, simulator/emulator, device, logs, screenshots, build command, runtime evidence, manual device gap and approval before permission, signing, store or runtime behavior claims.
- `desktop-local-first.md` routes desktop/local-first changes through desktop platform assumptions, filesystem permissions, local data, local DB, indexing, background jobs, privacy, app logs, runtime log check, build command, recovery path, rollback, runtime evidence, manual OS gap and approval before filesystem access, local data, packaging, signing, distribution or runtime behavior claims.
- `data-migration.md` routes schema, backfill, retention and sensitive-data changes through a migration plan, database dictionary, data quality, PII, sensitive fields, rollback, validation, dry run, backup, owner review, production DB boundary and approval before production data access, production DB access or migration execution.
- `security-sensitive-change.md` and `security-risk-review.md` route authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, approval and explicit Codex Security boundaries before implementation or release.
- `ci-stabilization.md` and `ci-stabilization-report.md` route failing or flaky CI through failing job, command, logs, environment, deterministic/flaky classification, failure evidence, isolation plan, local reproduction, rerun evidence, remote CI/GitHub Actions boundary, approval and residual risk before implementation, remote CI mutation, or CI health claims.
- `release-packaging.md` and `release-readiness.md` route package, SDK, plugin, app, desktop, mobile, or open-source release prep through release scope, package metadata, version/SemVer, changelog, build evidence, test evidence, docs evidence, security notes, license notes, artifacts, package registry, owner review, publish approval, tag boundary, rollback and residual risk before publishing, tagging, release creation, artifact upload, or package registry mutation.

These workflow templates may be promoted to skills later only after manual success evidence and failure logs justify that promotion.

## Agent team

Generated custom agents are project-scoped in `.codex/agents/`.

| Agent | Purpose | Default reasoning | Default sandbox |
| --- | --- | --- | --- |
| `product-manager` | Requirements, scope, acceptance criteria | `medium` / `high` | `read-only` |
| `architect` | Decomposition, ownership, risks, rollback | `high` / `xhigh` | `read-only` |
| `explorer` | Read-heavy codebase and docs mapping | `low` / `medium` | `read-only` |
| `builder` | Scoped implementation | `medium` / `high` | `workspace-write` |
| `tester` | Test gaps, verification commands, eval reports | `medium` / `high` | `workspace-write` |
| `reviewer` | Correctness, security, regressions, missing tests | `high` / `xhigh` | `read-only` |
| `docs-maintainer` | Docs, changelog, release notes | `low` / `medium` | `workspace-write` |
| `release-operator` | PR packet, rollout notes, automation candidates | `medium` / `high` | `read-only` by default |

Every role card includes:

```yaml
role: ""
owns: ""
does_not_do: []
inputs: []
outputs: []
model_policy:
  default_model: "project-default"
  reasoning_effort: "low | medium | high | xhigh"
  escalate_when: []
  downgrade_when: []
handoff:
  next_roles: []
  required_fields:
    - "sources_used"
    - "assumptions"
    - "files_touched_or_proposed"
    - "verification_evidence"
    - "open_risks"
stop_conditions: []
```

## Handoff contracts

All agent and skill handoffs use structured payloads.

```yaml
handoff:
  lifecycle_state: ""
  goal: ""
  constraints: []
  allowed_sources: []
  inputs_used: []
  verified_claims: []
  unsupported_claims: []
  files_touched: []
  files_proposed: []
  commands_run: []
  verification_evidence: []
  risks: []
  next_agent_task: ""
  stop_reason: ""
```

If a handoff lacks `goal`, `constraints`, `files_touched/files_proposed`, or `verification_evidence`, the orchestrator rejects it and asks for a corrected handoff.

## Safety and approvals

Default project config proposal:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"
allow_login_shell = false
```

For read-only planning and review:

```toml
approval_policy = "untrusted"
sandbox_mode = "read-only"
allow_login_shell = false
```

Granular approval policy proposal for governed projects:

```toml
approval_policy = { granular = {
  sandbox_approval = true,
  rules = true,
  mcp_elicitations = true,
  request_permissions = false,
  skill_approval = true
} }
```

Approval required for:

- external writes;
- destructive commands;
- permission changes;
- global config changes;
- credential, deployment, billing, database, auth, migration, production operation or source-of-truth update;
- starting automation;
- enabling broad network access.

Forbidden by default:

- storing secrets in docs, prompts, memory, fixtures or examples;
- editing generated/vendor/build artifacts unless explicitly allowed;
- changing global Codex config;
- creating recurring automation without manual stability evidence;
- claiming checks passed without running them in the current lifecycle step.

## Hooks and rules

Plugin provides hook templates, not silent enforcement.

| Hook | Event | Purpose | Blocking |
| --- | --- | --- | --- |
| `session_start_context.py` | `SessionStart` | Summarize active control-plane state | no |
| `pre_tool_use_policy.py` | `PreToolUse` | Detect destructive commands and forbidden paths | yes for high-risk matches |
| `permission_request_summary.py` | `PermissionRequest` | Explain why approval is requested | no |
| `post_tool_use_evidence.py` | `PostToolUse` | Append command evidence to active runlog buffer | no |
| `stop_runlog_reminder.py` | `Stop` | Remind to update `RUNLOG.md` when evidence exists | no by default |

Rules must be narrow, auditable and aligned with sandbox/approvals. Hooks must not store secrets.

## Runtime selection

| Project need | Runtime decision |
| --- | --- |
| First-time project setup | Codex App or CLI interactive |
| One prepared task packet | `codex exec` |
| Large feature | App/CLI with worktree per coherent unit |
| PR review | GitHub integration or Codex review flow |
| Recurring stable check | Codex automation or GitHub Action |
| Programmable multi-agent workflow | Agents SDK + Codex MCP |
| GUI-only task | Computer Use only when no dedicated tool exists |

Runtime choice is stored in `PLAN.md` or `RUNLOG.md`, not hidden in chat.

## Context7 and source policy

The Track 3 `source-context-pack.md` workflow template records Context7 usage for library and official documentation retrieval when current docs are required.

Rules:

- Official status applies only when underlying source is official.
- Context7 results from community repositories are intake material until verified.
- OpenAI product claims prefer official OpenAI docs.
- Source-backed claims update source registry or project source notes.
- Community tricks are stored as insights with `trust_level` and `verification_status`.

## Evals and verification

Plugin has its own eval suite and creates project evals.

Plugin fixture evals:

| Case | Fixture | Expected behavior |
| --- | --- | --- |
| Happy path | `node-app` | Creates control plane, agents, test plan, runlog, no unsafe write |
| Existing files | `existing-codex-config` | Preserves user content and proposes managed sections |
| Missing tests | `empty-repo` | Names test gap and does not invent passing checks |
| Unsafe write | Any fixture | Stages draft and requests approval |
| Monorepo | `monorepo` | Creates nested ownership and avoids overlapping write scopes |
| Source conflict | `docs-repo` | Marks conflict and requests verification |
| Failed verification | `python-app` | Reports failure evidence and does not claim completion |

Project evals:

- deterministic checks: tests, lint, build, docs checks, schema validation;
- LLM-as-judge checks: usefulness, clarity, source fidelity, handoff completeness;
- artifact inspection: screenshots, generated reports, deployment previews, PR body;
- regression checks: previous passing scenarios remain passing.

Stopping rule example:

```yaml
quality_gate:
  deterministic_checks_required: true
  no_blocking_review_findings: true
  llm_judge_average_min: 0.90
  no_unresolved_source_conflicts: true
  rollback_note_required_for_risky_change: true
```

## Automation promotion

`automation-promoter` can only produce an automation candidate when all conditions are true:

- workflow ran manually at least twice or has equivalent fixture evidence;
- inputs and outputs are stable;
- failure modes are known;
- write policy is explicit;
- verification is runnable;
- owner and cadence are named;
- external writes are staged or approval-gated.

Automation candidate packet:

```yaml
automation_candidate:
  name: ""
  purpose: ""
  trigger_or_cadence: ""
  required_inputs: []
  write_policy: "read_only | draft_only | approved_write"
  verification: []
  failure_modes: []
  owner: ""
  rollback_or_disable: ""
```

## Optional Agents SDK runner

For advanced teams, plugin may include a companion runner design under `scripts/agents_sdk_runner/`.

Architecture:

- Manager Agent owns lifecycle state and final output.
- Specialist agents are tools or handoff targets.
- Codex MCP performs workspace work with explicit sandbox and approval policy.
- Guardrails validate handoff completeness, tool boundary, source fidelity and no secret retention.
- Sessions preserve conversation continuity.
- Tracing records tools, handoffs, latency and failures.

This runner is optional because many projects need Codex plugin + skills + `.codex/` config before they need a programmable agent app.

## Failure modes

| Failure | Detection | Required behavior |
| --- | --- | --- |
| Scope too broad | Requirements span unrelated systems | Split into phases and ask for priority |
| Existing project rules conflict | `AGENTS.md` and proposed config disagree | Stop and show conflict |
| Context overflow | Runlog or docs too large | Build context pack and archive old details |
| Agent edits outside ownership | Diff touches unassigned files | Stop or request approval |
| Verification missing | No test/eval command known | Create test gap and avoid success claim |
| Hook false positive | Valid command blocked | Log rule, propose narrower rule |
| Automation too early | No manual success history | Keep as candidate, not active automation |
| Source drift | Official docs changed | Mark freshness risk and refresh source |
| Secret risk | Potential credential detected | Stop, redact, do not store |

## Acceptance criteria

Plugin is production-ready when:

- It can initialize existing and greenfield projects without overwriting user content.
- It produces a clear infrastructure plan before writing.
- It routes skills by lifecycle state and complexity profile.
- It creates valid control-plane files and project-scoped `.codex/` assets.
- It supports full project lifecycle from idea to PR/release packet.
- It logs evidence and decisions in `RUNLOG.md`.
- It handles context overflow through hot/warm/cold context layers and archive policy.
- It enforces approval gates for risky writes.
- It has fixture evals for happy path, existing config, missing tests, unsafe write, monorepo, source conflict and failed verification.
- It does not create active automations without stability evidence.
- It documents residual risks and next action after every run.

## Implementation handoff

Implementation should be split into four build tracks:

1. **Plugin core and contracts** - manifest, schemas, detection scripts, validators, fixture harness.
2. **Lifecycle skills** - orchestrator and each lifecycle stage skill with concise `SKILL.md`, references and output contracts.
3. **Generated project infrastructure** - control-plane templates, `.codex/agents/*.toml`, hooks, workflow packets and eval templates.
4. **Production hardening** - fixture evals, safe merge behavior, source policy checks, automation promotion gates and optional Agents SDK runner.

Each track must have deterministic validation before the plugin is used on real customer projects.
