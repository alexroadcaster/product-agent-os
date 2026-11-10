# Technical features and installation

## G8: documents and lossless compaction

The scoped renderer (`--task` or `--task-context`) produces compact documents by purpose. The context field `documents` supplies explicit facts with `source`; `evals_required: true` or an EVALS packet includes the eval document. Full-registry compatibility now requires explicit `--legacy-catalog`; missing context returns a gap. Use `--formation-context` for [unified project formation](project-formation.md).

Information ownership: AGENTS owns durable rules; REQUIREMENTS scope/acceptance; PLAN sequencing; TEST verification; EVALS quality rubrics; RUNLOG current handoff. Schema v1 stores facts in a JSON data block independently of heading language. Unknown fields require explicit migration. `validate_control_plane.py workspace --semantic` distinguishes missing/scaffold/draft. Reviewed/accepted states need a separate digest-bound receipt with reviewer/evidence and owner decision. Legacy structural mode only checks files. A receipt is reported local evidence, not runtime proof or automatic acceptance.

Regenerating a filled managed section preserves the target and offers a companion proposal; bulk merge cannot upgrade that proposal to replacement. Dry-run and stage validate actual proposed bytes. Scaffolds are not ready requirements. Preserve existing canonical document names and explicit mappings instead of renaming files to match a template.

Active-document budget: **40,000 UTF-8 bytes**, warning at 32,000; exactly 40,000 is allowed. Stricter project budgets belong in `[product_agent_os.documents.limits]`, for example `"PLAN.md" = 20000`. Legacy character limits remain deprecated report metadata. History/evidence/generated/dataset exemptions need classification, owner, reason and index; root control-plane documents cannot be exempted; detailed planning matrices follow the exception below.

`compact_control_plane.py propose workspace moves.json --output private-proposal.json` creates a reviewable diff, byte ranges, preservation map and exact before/after bytes. Proposal/journal privacy equals source privacy; do not publish their bodies. `apply workspace private-proposal.json --approve sha256:DIGEST` requires the exact reviewed proposal digest; the command does not grant user authority. `rollback workspace .codex/product-agent-os/compaction/DIGEST.json --approve sha256:DIGEST` restores only matching state. A recovery journal does not provide a cross-file ACID transaction. Callers must exclude external writers; crash recovery requires explicit operator handoff before clearing a stale lock through the recovery API. No automatic history deletion.

`document_navigation.task_plan_moves` proposes complete-card splits, preserving IDs/dependencies and bytes, with source anchor pointers. Oversized individual cards require manual decomposition. `documentation_inventory` reuses docs/index.md, docs/README.md or docs/control-plane/index.md and requests architecture/decisions/API/data/operations/evidence/history only when triggered. Do not generate empty files for completeness.

Mirror/reference checks verify source digests and exact bytes, separating required from optional evidence. Cross-repository references require identity, path, revision, digest and claim boundary; unavailable sources remain unknown. After M1 cutover, SQL task projections are forbidden file-compaction targets; M1 must declare authority/projection paths and freeze stops writes. Fixtures verify this boundary, not a running M1 service.

G8 check receipts and comparison are repository artifact `research/product-agent-os-g8-execution-report.md`; pilot results are `docs/superpowers/specs/paos-aud-g8-control-plane-results.json`. Fresh-session activation and owner acceptance remain separate.


Contract v1: required facts are explicit fields; absent facts remain missing. Inputs are owner-provided source packets, outputs are staged Markdown and readiness diagnostics. Update only the owning document when its facts change.

| Document | Required facts | Update trigger |
| --- | --- | --- |
| AGENTS | rules, boundaries | instruction change |
| REQUIREMENTS | goal, scope, acceptance, constraints | scope change |
| PLAN | tasks, dependencies, next_step | queue change |
| TEST | checks, evidence_limits | verification change |
| EVALS (conditional) | cases, thresholds, claim_limits | eval applicability |
| RUNLOG | result, evidence, risks, next_step | slice outcome |

Use repeated `--document NAME` with semantic validation to match scoped selection. Structural validation without it retains the legacy six-file contract. `check_documents.py workspace manifest.json` accepts `paths`, conditional `signals` and `references`; it reports local links, duplicate paragraphs and provenance without writes. An `offline_bundle` evidence profile binds each required artifact by relative path and digest. This does not prove availability in an unpublished clean Git checkout. Mirror provenance belongs to its companion reference record (canonical source and digest); the mirrored bytes remain identical.


The existing PLAN selector supports up to 32 revision-pinned sources while retaining the former aggregate 16 MiB read ceiling. split_source_references proposes replacement pins without another state owner. Old pins become unknown after a split until explicitly updated.

Detailed task matrices under `docs/planning/` (including subfolders) are exempt from the default size trigger: preserve full cards/tables; size alone does not require compaction. This is active detail, not archive. Recognized forms are detailed cards or tables with identifiers, statuses and acceptance criteria (Russian headers supported); fenced examples are excluded. Index/README and control-plane filenames retain budgets; explicit per-file project limits and content/link/security checks still apply.

Source status: `official + experiment`  
Sources: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [Codex MCP](https://developers.openai.com/codex/mcp), [Codex hooks](https://developers.openai.com/codex/hooks), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk), [Product-Agent OS architecture](architecture.md).

## Quick start

Product-Agent OS is a local Codex plugin package. Use it to stage control-plane artifacts, route product-agent workflows, run deterministic validators and package repeatable methods as skills. Installation does not grant permission to start live systems, call providers, mutate target repositories or publish anything.

Use the [operator command matrix](operator-command-matrix.md) for command authority and [site freshness](residual-follow-up-site-freshness.md) for current build evidence. Historical DOC-M26/DOC-M25 milestones are not the current installation procedure.

## Capability status

| Capability | Status | Boundary |
| --- | --- | --- |
| Plugin manifest | Implemented. | Declares package capabilities only. |
| Lifecycle skills | Implemented. | Recommend and stage work; they do not override approvals. |
| Staged infrastructure renderer | Implemented. | Writes to explicit staging output, not silently into the target workspace. |
| Fixture eval runner | Implemented. | Local deterministic evidence only. |
| Transcript eval runner | Implemented. | Uses synthetic/redacted transcripts and privacy checks. |
| Codex compatibility validator | Implemented. | Checks package shape, not live operational readiness. |
| Graph/cockpit orientation | Staged evidence route. | Generated views are not source of truth. |
| Live runtime/provider/mutation actions | Approval-bound. | Disabled until a specific owner-approved packet exists. |
| Professional Code Authoring | Source contract. | Uses [Professional Code Authoring Standards](coding-standards.md); does not prove real agent behavior or runtime enforcement. |

The cockpit surface groups graph data into reader-facing views: `Project Map`, `Code Intelligence`, `Contracts`, `Quality & Metrics`, `Operations & Risk` and `Proposal Ledger`. The recommended path is graph, guided read order, source files, then tests/evidence. The cockpit and query packets do not prove runtime behavior, browser behavior, source freshness, contract correctness, test pass status or release readiness.

## Operator contract

The operator must keep actions explicit:

- read source files before claims;
- stage proposals before target mutation;
- keep `Source status:` on non-index docs;
- run focused verification after meaningful changes;
- keep live server launch, browser automation, provider/API calls, canonical graph mutation and git actions approval-bound;
- never store secrets, credentials, customer data or raw private chats in docs, prompts, fixtures or templates.

## Package layout

The package lives under `plugins/product-agent-os/` and includes:

- `.codex-plugin/plugin.json` for Codex plugin metadata;
- skills under `skills/`;
- templates and packaged examples under `assets/templates/`;
- eval fixtures under `assets/eval-fixtures/`;
- scripts for rendering, validation and eval execution;
- docs under `docs/product-agent-os/` and `docs/product-agent/`;
- local tests under `tests/product_agent_os/`.

## Bundled MCP

MCP declarations are integration boundaries, not blanket permission. A declared MCP server or tool must still respect sandbox, approvals, source policy, external-system ownership and current verification evidence.

## Packaged skills

Packaged skills cover requirements authoring, implementation planning, test/eval design, risk review, docs maintenance, release packaging and agent team design. Each skill should name trigger, inputs, outputs, verification, failure modes and stop conditions.

## Generated infrastructure

Generated infrastructure is staged-first. Use dry run before staging:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run --legacy-catalog
```

Use staging only with an explicit output directory:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --legacy-catalog --stage <output-dir>
```

The renderer must preserve user-authored files outside managed sections. Existing unmarked `AGENTS.md`, `.codex/config.toml`, hooks, workflows and automation files are user content and should be staged as companion proposals unless an approved merge path exists.

Packaged hooks and automations are examples or candidates. They must not be activated silently.

The generated `.codex/config.toml` includes a `product-agent-os-project` permission profile. The profile keeps `.codex` itself read-only while opening only Product-Agent OS project artifact directories such as `.codex/agents`, `.codex/skills`, `.codex/workflows`, `.codex/artifact-templates`, `.codex/evals`, `.codex/runlogs`, `.codex/automation-candidates`, `.codex/pr`, `.codex/product-agent-os` and `.codex/eval-reports`. Sensitive control surfaces such as `.codex/config.toml`, `.codex/hooks`, `.codex/automations` and `.codex/plugins` remain approval-bound.

On Windows, a managed permission profile can still be blocked by inherited filesystem ACL deny entries on `.codex`. Check the scoped Product-Agent OS paths with:

```powershell
python plugins\product-agent-os\scripts\prepare_windows_codex_permissions.py <workspace>
```

Apply the scoped ACL preparation only with explicit owner approval:

```powershell
python plugins\product-agent-os\scripts\prepare_windows_codex_permissions.py <workspace> --apply
```

The apply mode creates only the approved Product-Agent OS `.codex` subdirectories, disables inherited ACLs on those subdirectories and removes inherited deny ACEs from the same subdirectories. It does not open the `.codex` root, config, hooks, automations or plugin cache by default.

Generated infrastructure also includes the system file hygiene surfaces:

- `.codex/workflows/system-file-hygiene-audit.md`;
- `.codex/artifact-templates/system-file-hygiene-report.md`;
- `.codex/automation-candidates/system-file-hygiene-audit.md`.

Professional Code Authoring infrastructure includes `.codex/workflows/coding-standards.md` and `.codex/artifact-templates/coding-standard-checklist.md`. The public map lives in [Professional Code Authoring Standards](coding-standards.md); the artifacts remain source contracts until a later approved runtime or owner-pilot batch supplies stronger evidence.

## Local commands

Common local checks:

```powershell
python tools\check_docs.py
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
```

Run the read-only system file hygiene audit:

```powershell
python plugins\product-agent-os\scripts\validate_system_file_hygiene.py <workspace> --trigger soft_size_review
```

Use the full unit suite when scripts, templates, fixtures or lifecycle behavior change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Use strict MkDocs when navigation, Mermaid, Markdown extensions or generated site behavior changes:

```powershell
python -m mkdocs build --strict
```

## Self-verification metrics loop

The metrics loop evaluates agents, skills, prompt/policy packs, router/tool policy and harness-version behavior from read-only evidence. It can stage scorecard records, reports and modernization candidates. It must not self-apply updates, create active schedules, leak raw traces or call live providers without explicit approval.

## System file hygiene audit

Product-Agent OS includes a read-only `system_file_hygiene_audit` contract for keeping project system files compact and source-owned. The audit uses hybrid triggers: weekly full review, monthly deep ownership review, on-change review after system-file edits, size-threshold review, and release or automation approval review.

Maintained surfaces include root control-plane files, `README.md`, nested `AGENTS.md`, `.codex/config.toml`, MCP config, `.codex/agents`, `.codex/skills`, `.codex/workflows`, `.codex/artifact-templates`, `.codex/automation-candidates`, `.codex/hooks`, `.codex/evals`, `.codex/pr`, docs source-control files, `.github/workflows`, `CODEOWNERS`, `SECURITY.md`, and checked-in plugin package control files. The audit reports size limits, duplicate headings, mojibake/BOM markers, secret-like literals, historical ledger leakage and active schedule markers inside automation candidates.

The audit does not compact files by itself and does not create a schedule. It emits JSON plus a staged `system-file-hygiene-report.md`; any edit, hook activation, GitHub workflow, Codex App automation, MCP change or external write remains a separate owner-approved slice.

The JSON packet contains `audit_trigger`, `finding_type`, `compaction_decision`, `approval_boundary`, `no_secrets_status` and `active_schedule_markers`. The CLI `--trigger` records the run reason, prints JSON, returns `0` for `ok` or `review_required`, and returns `1` only for `blocked`; the workspace remains read-only.

The status dashboard projection shows `file_statuses`, `mtime_utc`, `age_days`, `content_digest` and `top_finding` as generated review evidence. Dates come from filesystem metadata: they are freshness hints for review, not semantic proof that file content is correct or current enough to claim completion.

## Project code graph and cockpit

The project code graph and cockpit provide orientation evidence. They can stage graph JSON/JSONL and offline HTML/JSON review surfaces under `.codex/product-agent-os/`. They help readers find source files, edges and stale assumptions, but generated views are not source of truth and cannot justify completion claims by themselves.

## Codex installation boundary

Codex plugin installation makes package capabilities available to Codex surfaces. It does not:

- publish the plugin;
- install dependencies;
- start local servers;
- activate hooks or automations;
- call external providers;
- mutate global config;
- stage, commit, push or open PRs;
- approve production data, hosted docs or database access.

## Guardrails

- Keep official OpenAI/Codex behavior source-backed by official docs.
- Keep community claims under `docs/insights/` with trust and verification labels.
- Treat generated reports, dashboards, memory and chat recall as non-authoritative.
- Require explicit owner approval for external writes, live calls, publishing, production data, hosted docs, CI activation, security scans and active automation.
- Preserve staged-first behavior and rollback/disable paths.

## Verification commands for this repo

After documentation-only changes, run:

```powershell
python tools\check_docs.py
```

After plugin scripts, templates, fixtures or tests change, also run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Strict MkDocs is needed when navigation, Mermaid, Markdown extensions or MkDocs configuration change:

```powershell
python -m mkdocs build --strict
```

## Inputs

- The checked-in Product-Agent OS plugin package and repository docs.
- Local Python, MkDocs dependencies and current project instructions.

## Outputs

- Local validation evidence for docs, plugin compatibility and deterministic tooling.
- Operator guidance for installation boundaries and generated artifacts.

## Risks

- Plugin installation does not approve publication, live calls or target workspace writes.
- Generated graph and report output can become stale unless fingerprint and source boundaries are checked.

## Package format and installation: checked 2026-11-05

[Package your plugin](https://developers.openai.com/plugins/build/plugins) describes portable root `plugin.json`, `mcp.json` and OpenAI metadata in `extensions.com.openai`. Legacy `.codex-plugin/plugin.json` remains a compatibility fallback; Plugin Creator can generate that scaffold. Our existing package stays on the legacy layout. This guide does not migrate implementation: renaming `.mcp.json` alone is invalid because the transport schema differs.

[Plugins](https://learn.chatgpt.com/docs/plugins) are available on supported desktop/CLI/web/mobile surfaces with component and authentication limits. The IDE extension does not support native plugins. Working with repository files in the IDE is a separate capability. Start a new chat/session for bundled skills after installation; verify MCP authentication and hook trust separately. See [surface matrix](../codex/surfaces.md) and [skill exposure](../agent-systems/subagents-skills.md).

For per-task section updates see [contract and limits](project-formation.en.md#targeted-documentation-maintenance-after-a-task). `documentation_sync.py` reuses the compaction CAS/journal engine; the original lossless validator remains separate.
