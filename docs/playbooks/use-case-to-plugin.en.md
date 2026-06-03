# Playbook: use case to plugin

Source status: `official + experiment`  
Sources: [Codex use cases](https://developers.openai.com/codex/use-cases), [Save workflows as skills](https://developers.openai.com/codex/use-cases/reusable-codex-skills), [Create a CLI Codex can use](https://developers.openai.com/codex/use-cases/agent-friendly-clis), [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build).

Use this playbook to turn a repeated Codex workflow into a plugin with narrow skills, clear inputs and outputs, safe write policy, verification and owner maintenance.

## Inputs

- Official use case archetype or proven internal workflow.
- Manual run evidence, failure log, candidate skills and expected verification commands.

## Outputs

- Playbook, skill candidate, plugin blueprint and eval cases.
- Permission model, packaging/update process and owner handoff.

## Verification

Keep the promotion order: manual workflow, playbook, skill, plugin, automation. Run eval cases before packaging and keep automation approval separate.

## Risks

- Packaging too early can turn an unproven prompt into a reusable failure.
- A plugin with unclear permissions can bypass the project approval boundary.
