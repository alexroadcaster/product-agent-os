# Product-Agent OS Codex compatibility

Source status: `official + experiment`  

## Task 22 canonical safety boundary

Task 22 canonical safety boundary: no live model call, no separate OpenAI API key, no standalone Agents SDK activation, no global config mutation, no silent MCP/server/hook/automation activation, no unapproved external writes, no hosted docs or DB introspection require approval bypass, and no readiness claims from detection.

Codex App, CLI, IDE extension, skills, MCP declarations and staged hooks are supported package surfaces. They are not permission to mutate target workspaces, GitHub, CI, package registries, production databases, hosted documentation, security systems or schedules without explicit approval and current verification evidence.
Источники: [Codex App](https://developers.openai.com/codex/app), [Codex CLI](https://developers.openai.com/codex/cli), [Codex IDE extension](https://developers.openai.com/codex/ide), [Codex build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Codex MCP](https://developers.openai.com/codex/mcp), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security).

Product-Agent OS поддерживает Codex App, CLI и IDE extension как целевые surfaces. Compatibility здесь означает: package можно проверять как Codex plugin, без требования non-Codex adapters, без separate model runner и без silent external activation.

## Inputs

- plugin root: `plugins/product-agent-os/`;
- `.codex-plugin/plugin.json`;
- bundled `skills/`;
- bundled MCP config `.mcp.json`;
- staged hooks under `assets/templates/hooks/`;
- `README.md` and user-facing docs;
- validation script `plugins/product-agent-os/scripts/validate_codex_compatibility.py`.

## Outputs

- compatibility report with supported surfaces: Codex App, CLI, IDE extension;
- evidence that `.codex-plugin/plugin.json`, skills, MCP and staged hooks are present;
- explicit result that the plugin requires no standalone Agents SDK app and no separate OpenAI API key;
- empty list of required non-Codex adapters;
- residual risk if docs or package boundaries change without rerunning validation.

## Track 10 compatibility boundaries

Compatibility means the package fits Codex surfaces. It does not approve live execution, external systems or git actions.

| Boundary | Compatible staged work | Requires separate explicit approval |
| --- | --- | --- |
| Live server | Validate disabled local runtime contract, auth policy, lifecycle controls and graph-only fallback. | Launch server, keep process running, expose network route or collect live runtime evidence. |
| Browser automation | Stage browser smoke expectations, generated-view labels, source-boundary labels and mobile overflow checks. | Run Playwright/browser automation against a live local runtime. |
| Provider/API calls | Stage embedding, reranker and LLM provider gate/eval packets with redaction/cache/budget policy. | Call external model/API/provider, spend tokens or store provider cache from live data. |
| Canonical mutation | Stage review ledger, proposal diff, mutation dry-run plan, journal and rollback proof. | Apply accepted mutation to canonical graph or source-controlled state. |
| Git actions | Prepare release/PR packet and closure evidence. | `git add`, commit, push, PR creation, tag, release or package upload. |

## Compatibility Contract

| Surface | Supported scope | Boundary |
| --- | --- | --- |
| Codex App | Interactive local product-agent threads, steering, artifacts, skills and automations when explicitly created. | Product-Agent OS does not create active automations from templates. |
| CLI | Local read/edit/run workflows, fixture evals, staged renderer and validation commands. | Commands obey sandbox, approvals and local workspace policy. |
| IDE extension | Editor-context implementation and review with project docs and `AGENTS.md`. | Plugin docs do not assume IDE-only APIs. |
| `.codex-plugin/plugin.json` | Required manifest and packaged plugin metadata. | Manifest must not point to non-Codex runtime adapters. |
| skills | Reusable lifecycle methods loaded by Codex through progressive disclosure. | Skills remain task-specific and do not silently mutate external systems. |
| MCP | Context7 declared as bundled MCP config for Codex. | Credentials stay outside checked-in package; MCP is not a background service launched by Product-Agent OS scripts. |
| staged hooks | Hook templates are packaged as examples and target-project assets. | staged hooks are inactive until explicit approval and target-project activation. |

## Non-Goals

- no standalone Agents SDK runtime;
- no separate OpenAI API key;
- no Claude, Cursor, OpenCode, Gemini or other non-Codex adapter requirement;
- no package manager publish, marketplace submission, active automation, hook activation, remote CI mutation or external write without explicit approval;
- no hidden live service started by the plugin.

## Verification

Run the compatibility validator after manifest, README, skills, MCP, hooks or package-boundary docs change:

```powershell
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

Expected report shape:

```json
{
  "status": "compatible",
  "supported_surfaces": ["Codex App", "CLI", "IDE extension"],
  "requires_non_codex_adapters": false
}
```

Also run full plugin verification when package files change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python tools\check_docs.py
```

## Risks

- Official Codex plugin interfaces can change; package claims must stay tied to source registry checks.
- A compatible package can still be misused if a target project activates hooks, MCP credentials, automations or external writes without review.
- The compatibility check proves packaging scope, not product quality or scenario readiness.
- Hosted docs, marketplace publishing and external integrations are outside this compatibility claim unless separately approved and verified.

Next artifact: use [Behavioral evals](behavioral-evals.md) to test route behavior and [Scenarios](scenarios.md) to select the correct workflow.
