# Technical features and installation

Source status: `official + experiment`  
Sources: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [Codex MCP](https://developers.openai.com/codex/mcp), [Codex hooks](https://developers.openai.com/codex/hooks), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk), [Product-Agent OS architecture](architecture.md).

## Quick start

Product-Agent OS is a local Codex plugin package. Use it to stage control-plane artifacts, route product-agent workflows, run deterministic validators and package repeatable methods as skills. Installation does not grant permission to start live systems, call providers, mutate target repositories or publish anything.

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
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run
```

Use staging only with an explicit output directory:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --stage <output-dir>
```

The renderer must preserve user-authored files outside managed sections. Existing unmarked `AGENTS.md`, `.codex/config.toml`, hooks, workflows and automation files are user content and should be staged as companion proposals unless an approved merge path exists.

Packaged hooks and automations are examples or candidates. They must not be activated silently.

Generated infrastructure also includes the system file hygiene surfaces:

- `.codex/workflows/system-file-hygiene-audit.md`;
- `.codex/artifact-templates/system-file-hygiene-report.md`;
- `.codex/automation-candidates/system-file-hygiene-audit.md`.

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
python plugins\product-agent-os\scripts\validate_system_file_hygiene.py <workspace>
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
