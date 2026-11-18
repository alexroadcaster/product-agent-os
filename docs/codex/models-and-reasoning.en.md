# Models and reasoning: selection and applicability

Source status: `official + experiment`

Checked 2026-11-18. Sources: [Codex and ChatGPT Work models](https://learn.chatgpt.com/docs/models), [Prompting GPT‑6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra), the [API model catalog](https://developers.openai.com/api/docs/models), and [Using GPT‑6.2](https://developers.openai.com/api/docs/guides/latest-model). This reference describes model applicability and settings in Product-Agent OS source. Account access, activation, and comparative quality require separate evidence.

## API model matrix

| Model ID / source | API reasoning.effort | Candidate project use | Tools |
| --- | --- | --- | --- |
| [gpt-6.2-sol](https://developers.openai.com/api/docs/models/gpt-6.2-sol) | `low`, `medium`, `high`, `xhigh`, `max`. The API rejects `none` | Project default for implementation, planning, verification, documentation, and context gathering | Tool calling and Structured Outputs through Responses |
| [gpt-6.2-astra](https://developers.openai.com/api/docs/models/gpt-6.2-astra) | `low`, `medium`, `high`, `xhigh`, `max`. The API rejects `none` | Architecture, independent review, and complex security risk | Tool calling and Structured Outputs through Responses |
| [gpt-6-astra](https://developers.openai.com/api/docs/models/gpt-6-astra) | `low`, `medium`, `high`, `xhigh`, `max`; no `none` | Hardest architecture, research and ambiguous decisions | Tool calling through Responses |
| [gpt-6.1-sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | `low`, `medium` (API default), `high`, `xhigh`, `max` | Complex coding and sustained engineering tasks | Tool calling through Responses |
| [gpt-6.1-terra](https://developers.openai.com/api/docs/models/gpt-6.1-terra) | `none`, `low`, `medium` (API default), `high`, `xhigh`, `max` | Documents, visual work, computer use; not an automatic replacement for previous builder roles | Tool calling through Responses |
| [gpt-6-luna](https://developers.openai.com/api/docs/models/gpt-6-luna) | `none`, `low`, `medium` (API default), `high`, `xhigh`, `max` | Narrow repeatable tasks after bounded evaluation | Responses; Chat Completions function calling only with `none` |

Candidate roles interpret official positioning for this project; their quality has not been measured here. Endpoint listings do not establish every endpoint/effort/tool combination. Apply the [API compatibility matrix](../agent-systems/sdk-patterns.md).

## Surface, authentication and client version

| Surface | Conditions | Check before selection |
| --- | --- | --- |
| OpenAI API / API-key session | Model availability and the chosen API contract | Account access, model ID, endpoint, service tier, budget |
| Codex App / CLI / IDE with ChatGPT sign-in | Plan, workspace policy, client version and rollout | Available picker/catalog and effective configuration |
| GPT-6.1 Terra in CLI | Official minimum: CLI 0.159.0 | The actual client version; CLI version does not prove App version |
| ChatGPT Work | Product modes and plan availability | UI values and support in the selected model |

Account-specific availability was not checked in this refresh. No unsupported minimum version is claimed for the other rows. `Light` maps to `low` in the relevant product context. `Max` increases single-agent reasoning; `Ultra` uses subagents in supported products. Luna does not support Ultra. Do not send UI `Ultra` as an ordinary API `reasoning.effort`; the model page defines API values.

## Local diagnostics — PAOS-AUD-G2, 2026-11-09

`validate_codex_compatibility.py` separates local package structure from host diagnostics. Without extra inputs, client/model receipt/trust remain missing, not_verified or unknown; installed CLI is not used as an App version. The documented [CLI 0.159.0 minimum for GPT-6.1 Terra](https://learn.chatgpt.com/docs/models) applies only to that model/surface pair. Other minimums are not invented.

Optional `--observations <file.json>` reads up to 16 KiB of non-secret JSON: `surface` (Codex App, CLI, IDE extension), `client_version` (three numeric components), `configured_model`, `observed_model` (the model IDs above), `trust` (trusted/untrusted), `native_plugin_observed` and `standalone_skills_observed` (boolean). Other fields are not copied into output; unknown values do not become evidence. Duplicate keys and malformed files are rejected. Inputs are caller-supplied observations, not authenticated receipts; account access and promotion remain not_verified/not_assessed. Exit 0 means local structure only, not absence of host gaps.

`--cache-root <explicit-directory>` compares canonical/cache SHA-256 over manifests, MCP JSON and SKILL.md; results are match/drift/needs_review. Without a cache input: cache_not_provided. Reads are bounded by size/count, links are rejected, contents and absolute paths are not printed. Scope excludes scripts/templates and does not prove host skill selection; full package/host receipts remain separate gates. Caches are neither discovered automatically nor modified. These diagnostics do not change pins or effort. T23–T29 remain historical checks.

## Context and cost

The GPT‑6.2 Sol and Astra API model pages list a 1,050,000-token context window, 922,000 max input, and 128,000 max output. Check these limits together. The effective Codex context depends on the client, model, and effective configuration. API limits apply to the relevant API endpoint.

Cost depends on model, service tier, cache reads/writes and long-context conditions. Do not transfer one model's rates or surcharge to another. Use the dated model page and [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching); Codex/ChatGPT subscription usage is not API pricing. See the [eval accounting method](../agent-systems/evals-observability.md).

## Working with GPT‑6.2

- **Codex.** Give the expected result, constraints, and observable checks. For established code, point to the target path and an existing example. For UI work, supply a reference when available and inspect the result at its intended size. Give subagents independent work with explicit ownership. [Prompting GPT‑6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra)
- **Reasoning effort.** Project profiles retain each role's prior effort. Compare 6.1 and 6.2 on the same tasks and at the same effort. Use a separate run for a lower supported effort. Record quality, tool failures, latency, and cost per completed task. [Model migration playbook](../playbooks/model-migration.md)
- **A custom Responses API client.** For GPT‑6.2, top-level `instructions` are appended after `input`. Put stable reusable guidance in the first `developer` message in `input` so it can be eligible for prefix caching. Use `instructions` for guidance that applies to the current request. This applies to API request construction. `AGENTS.md` and Codex app-server's `developerInstructions` remain separate surfaces. [Using GPT‑6.2](https://developers.openai.com/api/docs/guides/latest-model)

## Retirement and historical results

GPT-5.5 retired from Codex with ChatGPT sign-in on 14 October 2026 at 19:00 UTC; API/API-key Codex sessions are not affected by that retirement. GPT-5.4 and GPT-5.4-mini retired from sign-in Codex on 31 August 2026. Check [retirement guidance](https://learn.chatgpt.com/docs/models) for the chosen surface. This page does not claim GPT-5.6 was removed from the API.

Historical pins, approvals, frozen fixtures and eval results retain their original model IDs and dates. Rewriting an old result to name a new model destroys its provenance.

## Current Product-Agent OS state

| Layer | Source configuration on 2026-11-18 | Claim ceiling |
| --- | --- | --- |
| 15 project profiles | 12 use `gpt-6.2-sol`, 3 use `gpt-6.2-astra` (`architect`, `reviewer`, `security-privacy-supply-chain-reviewer`). The generic subagent default is Sol at `medium` | Role efforts were preserved. Account access and effective configuration require separate observation |
| 8 packaged profiles | 6 use Sol, 2 use Astra (`architect`, `reviewer`) | Staged proposals for target projects |
| Compatibility and rollback | Validators accept GPT‑6.2 and the prior GPT‑6.1 Sol/Terra profile pins. They accept GPT‑6.1 Sol as the generic default on rollback | Local validator acceptance does not establish model access |
| Behavioral evaluation | GPT‑6.1 Sol/Terra remain the baseline. `config_pinned_behavioral_promotion_pending` | Comparative quality, cost, latency, and fresh-session loading are unmeasured |

Executable configuration owns the pins. The [playbook](../playbooks/model-migration.md) defines comparisons, thresholds, and rollback. [Compatibility](../product-agent-os/codex-compatibility.md) describes client diagnostics. When handing off results, report the observed model, effort, and environment if available.
