# Automations and GitHub

Source status: `official + experiment`  
Sources: [Codex automations](https://developers.openai.com/codex/app/automations), [Codex workflows](https://developers.openai.com/codex/workflows), [Codex best practices](https://developers.openai.com/codex/learn/best-practices).

Automation should come after a stable manual workflow or skill. GitHub workflows belong to CI/PR contexts when the repository owner has approved the trigger, permissions and rollback path.

## Inputs

- Stable workflow, owner, cadence, expected evidence and failure handling.
- GitHub or automation permissions, data policy and approval record.

## Outputs

- Automation candidate, GitHub workflow proposal or approved recurring check.
- Audit-ready evidence for what ran, where it wrote and how to disable it.

Good automation candidates include scheduled documentation freshness audit, system file hygiene audit for `AGENTS.md`, control-plane files, subagents, skills, workflows, hooks, evals and automation candidates, recurring security review, CI failure triage and release-note drafting.

## Verification

Before activating automation, verify manual success evidence, input stability, output expectations and rollback/disable path.

System file hygiene automation should start as `.codex/automation-candidates/system-file-hygiene-audit.md`: weekly/monthly cadence, on-change trigger and size trigger are proposals, not an active schedule. Before approval, use only the read-only command:

```powershell
python plugins\product-agent-os\scripts\validate_system_file_hygiene.py <workspace>
```

## Risks

- A scheduled workflow without stable inputs can repeat bad decisions.
- GitHub permissions and external writes need least privilege and explicit approval.
