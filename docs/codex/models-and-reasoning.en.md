# Models and reasoning: selection and applicability

Source status: `official + experiment`

Checked 2026-11-03. Sources: [API model catalog](https://developers.openai.com/api/docs/models), [Codex and ChatGPT Work models](https://learn.chatgpt.com/docs/models), [migration guide](https://developers.openai.com/api/docs/guides/latest-model). This is reference guidance and a candidate Product-Agent OS policy, not a model switch or benchmark result.

## API model matrix

| Model ID / source | API reasoning.effort | Candidate project use | Tools |
| --- | --- | --- | --- |
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

Optional `--observations <file.json>` reads up to 16 KiB of non-secret JSON: `surface` (Codex App, CLI, IDE extension), `client_version` (three numeric components), `configured_model`, `observed_model` (the four model IDs above), `trust` (trusted/untrusted), `native_plugin_observed` and `standalone_skills_observed` (boolean). Other fields are not copied into output; unknown values do not become evidence. Duplicate keys and malformed files are rejected. Inputs are caller-supplied observations, not authenticated receipts; account access and promotion remain not_verified/not_assessed. Exit 0 means local structure only, not absence of host gaps.

`--cache-root <explicit-directory>` compares canonical/cache SHA-256 over manifests, MCP JSON and SKILL.md; results are match/drift/needs_review. Without a cache input: cache_not_provided. Reads are bounded by size/count, links are rejected, contents and absolute paths are not printed. Scope excludes scripts/templates and does not prove host skill selection; full package/host receipts remain separate gates. Caches are neither discovered automatically nor modified. Pins and effort remain unchanged; T23–T29 are not rerun as a new model migration.

## Context and cost

On the review date all four API model pages list a 1,050,000-token context window, 922,000 max input and 128,000 max output. These constraints apply jointly, not as additive independent quotas. GPT-6.1 Sol has an official 500,000-token default context in Codex; do not transfer the API limit to the client automatically.

Cost depends on model, service tier, cache reads/writes and long-context conditions. Do not transfer one model's rates or surcharge to another. Use the dated model page and [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching); Codex/ChatGPT subscription usage is not API pricing. See the [eval accounting method](../agent-systems/evals-observability.md).

## Retirement and historical results

GPT-5.5 retired from Codex with ChatGPT sign-in on 14 October 2026 at 19:00 UTC; API/API-key Codex sessions are not affected by that retirement. GPT-5.4 and GPT-5.4-mini retired from sign-in Codex on 31 August 2026. Check [retirement guidance](https://learn.chatgpt.com/docs/models) for the chosen surface. This page does not claim GPT-5.6 was removed from the API.

Historical pins, approvals, frozen fixtures and eval results retain their original model IDs and dates. Rewriting an old result to name a new model destroys its provenance.

## Current Product-Agent OS state

| Layer | State on 2026-11-03 | Claim ceiling |
| --- | --- | --- |
| 15 active profiles | 13 GPT-6.1 Sol, 2 GPT-6.1 Terra; generic subagent is Sol medium | Pins updated; effort preserved; activation and quality remain unverified |
| 8 packaged profiles and both model-reasoning-policy templates | 6 Sol, 2 Terra; consistent GPT-6 policy | Staged proposals without target activation |
| GPT-6 Astra / Luna | Candidates for a separate comparison | Not assigned to profiles |
| Validator/model allowlist and permissions/MCP | Aligned with parent inheritance | Local checks do not prove effective fresh-session settings |

Executable configuration owns pins; this reference owns applicability and sources; the [playbook](../playbooks/model-migration.md) owns the comparison procedure. [Compatibility](../product-agent-os/codex-compatibility.md) records technical follow-up. Catalog presence, valid TOML and a passing docs build do not establish quality, account availability or activation.
