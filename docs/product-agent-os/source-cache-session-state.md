# Source, cache and active-session state

Source status: `official + project evidence`

Источники: [Agent Skills](https://developers.openai.com/codex/skills), [Plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Skill exposure and invocation boundary](../diagrams/skill-exposure-and-invocation.md), `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`.

Product-Agent OS разделяет три похожих, но разных состояния: source tree, installed cache и active Codex session. Ошибка диагностики часто начинается там, где наличие файла принимается за runtime exposure.

## State Model

| State | Example evidence | Allowed conclusion |
| --- | --- | --- |
| Source tree | `plugins/product-agent-os/skills/*/SKILL.md`, scripts, templates, docs. | Capability exists in repository source. |
| Packaged plugin | `.codex-plugin/plugin.json`, plugin metadata, bundled skills/apps/MCP/hook config. | Capability can be packaged or installed through plugin route. |
| Installed cache | Local installed plugin copy and skill files. | Capability may be available to Codex after install/restart, subject to enablement. |
| Active session | Current session skill list, plugin/app/tool exposure, loaded instructions. | Capability is visible in this session. |
| Route evidence | Prompt fixture, transcript eval, current response or runtime route packet. | Capability was selected for this prompt class. |

## Read-only comparison packet

Before any cache refresh or global config change, create a read-only packet:

| Field | Meaning |
| --- | --- |
| `source_skill_count` | Count and names from repository source. |
| `cache_skill_count` | Count and names from installed cache, or `not_inspected`. |
| `active_session_exposure` | Skills/plugins/tools visible in the current or fresh session. |
| `policy_flags` | `allow_implicit_invocation`, explicit-only gates and forbidden automatic surfaces. |
| `restart_boundary` | Whether a new thread, app restart or CLI restart is required for proof. |
| `unsupported_claims` | Claims that remain unproved. |
| `next_safe_action` | Smallest non-mutating action or exact approval needed. |

Do not store local absolute user paths, raw private prompts, raw logs, secrets, tokens or unredacted sensitive findings in public docs or examples.

## No Auto-Repair

The comparison packet does not authorize:

- plugin cache write or refresh;
- global Codex config write;
- project `.codex/config.toml` mutation;
- hook trust change;
- MCP/app connector install;
- active automation creation;
- fresh-session proof claim without actually starting a fresh session.

If repair is needed, route it as a separate approval with owner, target surface, rollback, verification and no-unapproved-actions proof.

## Fresh-session proof

A fresh-session proof should record what changed between old and new context:

1. Source evidence used.
2. Cache/install evidence used.
3. Session start or restart boundary.
4. Visible skills/plugins/tools.
5. Prompt used for route smoke.
6. Resulting route and unsupported claims.
7. Residual risk if current session remains stale.

Until this exists, use `present_unverified`, `planned-only` or `approval_required` instead of fixed/ready language.
