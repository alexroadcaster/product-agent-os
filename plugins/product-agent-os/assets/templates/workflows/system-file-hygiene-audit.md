# System File Hygiene Audit

Project: {project_name}
Profile: {profile_name}

## Purpose

Keep Product-Agent OS system files compact, source-owned and safe for agents to read. This workflow is read-only by default and emits review artifacts only.

## Trigger Policy

- Weekly full audit: scan every maintained system file class and emit a report.
- Monthly deep ownership review: compare file purpose, source-of-truth routing, stale evidence and duplicate guidance.
- On-change audit: run after changes to root control-plane files, `README.md`, `.codex/agents`, `.codex/skills`, `.codex/workflows`, `.codex/hooks`, `.codex/evals` or `.codex/automation-candidates`.
- Size-triggered audit: run when a system file crosses its soft limit; stage compaction before crossing its hard limit.
- Release-triggered audit: run before plugin packaging, PR creation, external automation approval or schedule activation.

Cadence is a recommendation, not an active schedule. Do not create Codex App automations, GitHub Actions, recurring jobs, hooks or external workflows from this workflow without explicit owner approval.

## Maintained System File Classes

| Class | Files |
| --- | --- |
| Root control plane | `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` |
| Project entrypoint | `README.md` |
| Nested instruction layers | `**/AGENTS.md` |
| Codex config and MCP | `.codex/config.toml`, `.codex/settings.json`, `.mcp.json`, `.codex/*.mcp.json` |
| Subagents | `.codex/agents/*.toml` |
| Skills | `.codex/skills/**/SKILL.md`, `skills/**/SKILL.md` |
| Workflows | `.codex/workflows/*.md` |
| Artifact templates | `.codex/artifact-templates/*.md` |
| Automation candidates | `.codex/automation-candidates/*.md` |
| Hooks | `.codex/hooks/*` |
| Evals | `.codex/evals/*.json`, `evals/*.json` |
| PR and release packets | `.codex/pr/*.md`, `.github/PULL_REQUEST_TEMPLATE*.md` |
| Docs source control | `docs/sources/registry*.md`, `docs/sources/*backlog*.md`, `docs/sources/*approval*.md`, `docs/insights/*.md`, `docs/playbooks/*.md`, `docs/product-agent/**/*.md`, `docs/product-agent-os/**/*.md`, `docs/runtime/**/*.md`, `docs/artifact-templates/**/*.md`, `mkdocs.yml`, `tools/check_docs.py` |
| External automation policy | `.github/workflows/*`, `CODEOWNERS`, `SECURITY.md`, `.github/dependabot.yml` |
| Plugin package control | `plugins/*/.codex-plugin/plugin.json`, `plugins/*/README.md`, `plugins/*/.mcp.json`, `plugins/*/skills/**/SKILL.md`, `plugins/*/assets/templates/**/*.md`, `plugins/*/assets/templates/**/*.json` |

## Checks

- File exists where Product-Agent OS expects it.
- UTF-8 can be read without BOM or mojibake markers.
- Secret-like assignments are absent.
- File size is below the class soft and hard limits.
- Markdown headings are not duplicated accidentally.
- Historical `Task`, `Track`, `Batch`, `T*`, `B*` and `done_through` markers are not leaking into files that should stay current or product-facing.
- Automation candidates remain candidate-only and contain no active schedule.
- Source-of-truth ownership is clear when a file contains long evidence or historical status.

## Output

- `.codex/artifact-templates/system-file-hygiene-report.md`
- JSON from `validate_system_file_hygiene.py`
- Optional staged compaction proposal per file
- Optional automation candidate packet after manual stability evidence exists

## Stop Conditions

- The audit would need to write target files without approval.
- A candidate contains active schedule instructions.
- A system file contains secret-like literals.
- Evidence ownership is unclear enough that compaction could hide failures.
