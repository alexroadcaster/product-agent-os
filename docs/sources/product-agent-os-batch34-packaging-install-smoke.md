# Product-Agent OS Batch 34 packaging/install smoke packet

Source status: `internal`

## Scope

This packet records `B34-DOC-M15` packaging/install smoke evidence for Product-Agent OS. It is staged evidence only. It does not publish the plugin, install a new plugin version, mutate the plugin cache, create a release, upload artifacts, activate hooks, create automation, start Batch 35 execution or perform git stage/commit/push/PR.

## Inputs Inspected

- Checked-in plugin root: `plugins/product-agent-os`.
- Checked-in Codex manifest: `plugins/product-agent-os/.codex-plugin/plugin.json`.
- Checked-in skills directory: `plugins/product-agent-os/skills`.
- Installed plugin cache path: `$CODEX_HOME\plugins\cache\local-product-agent-plugins\product-agent-os\0.1.0`.
- Installed plugin cache manifest: `$CODEX_HOME\plugins\cache\local-product-agent-plugins\product-agent-os\0.1.0\.codex-plugin\plugin.json`.
- Compatibility script: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py`.

## Command Evidence

`python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.

Observed compatibility checks:

- `bundled_skills`: ok, 11 bundled skills found in the installed package view.
- `codex_manifest`: ok, Codex manifest is present.
- `context7_mcp`: ok, Context7 MCP config is secret-free.
- `non_codex_adapters_absent`: ok, no non-Codex adapter paths are packaged.
- `readme_codex_scope`: ok, README states Codex-only surfaces.
- `staged_hooks`: ok, hooks are templates only.

Manifest and cache probe result:

```yaml
checked_manifest_present: true
checked_root_manifest_present: false
cache_manifest_present: true
checked_docs_maintainer_present: true
cache_docs_maintainer_present: false
checked_pr_release_operator_present: true
cache_pr_release_operator_present: true
checked_skill_count: 12
cache_skill_count: 11
```

Checked-in skills:

```text
agent-team-designer, automation-promoter, docs-maintainer, implementation-planner, learning-loop-maintainer, project-lifecycle-orchestrator, pr-release-operator, references, requirements-author, risk-reviewer, test-eval-designer, workspace-discovery-auditor
```

Installed cache skills:

```text
agent-team-designer, automation-promoter, implementation-planner, learning-loop-maintainer, project-lifecycle-orchestrator, pr-release-operator, references, requirements-author, risk-reviewer, test-eval-designer, workspace-discovery-auditor
```

## Findings

- Checked-in source has `skills/docs-maintainer/SKILL.md`.
- Installed plugin cache lacks `skills/docs-maintainer/SKILL.md`.
- This is the Batch 34 docs-maintainer plugin-cache gap.
- The checked-in `docs-maintainer` guidance remains the source for Batch 34 docs maintenance until the installed plugin cache is refreshed by an explicit owner-approved packaging/install action.
- Checked-in and cached package surfaces both include `pr-release-operator`.
- Compatibility validator reports the installed Product-Agent OS package as Codex-compatible for Codex App, CLI and IDE extension surfaces.

## Approval Boundary

Packaging/install smoke is evidence only. It does not approve:

- plugin publication;
- marketplace submission;
- package registry upload;
- hook activation;
- active schedules or automations;
- external writes;
- live server launch;
- browser automation;
- provider/live external model/API calls;
- canonical graph mutation;
- git stage/commit/push/PR;
- Batch 35 execution.

## Residual Risks

- Installed cache can remain behind checked-in source until an explicit owner-approved refresh happens.
- Compatibility smoke proves package shape and Codex scope, not semantic quality of every skill.
- No marketplace install, package registry publish, external install or live runtime execution was performed.
- The broad repository contains intentional secret/redaction policy terms and synthetic fixture markers, so this packet does not claim a full secret scan. The compatibility validator only records the Context7 MCP config as secret-free.

## Next Action

Use `docs/sources/product-agent-os-batch35-approval-packet-draft.md` as the staged handoff packet. Batch 35 remains blocked until the owner selects one action and gives separate explicit approval for that action.
