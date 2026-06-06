# Plugin Blueprint Template

Source status: `official + experiment`

````markdown
# <Plugin Name>

## Purpose

<One product-agent workflow family this plugin makes repeatable.>

## Official archetypes

| Use case | URL | Why it applies |
| --- | --- | --- |
| <Codex use case title> | <https://developers.openai.com/codex/use-cases/...> | <mapping> |

## Target users

- team: <Design / Engineering / Finance / Operations / Product / QA>
- category: <Engineering / Evaluation / Front-end / Quality / Automation / Data / Integrations / Knowledge Work / Native>
- task_type: <Analysis / Code / Design / Testing / Workflow>

## Supported surfaces

| Surface | Supported | Notes |
| --- | --- | --- |
| Codex App | yes/no | <when to use> |
| Codex CLI | yes/no | <when to use> |
| Cloud task | yes/no | <when to use> |
| GitHub | yes/no | <PR/review behavior> |
| Slack | yes/no | <handoff behavior> |
| Computer Use | yes/no | <GUI fallback> |
| MCP | yes/no | <servers/tools> |
| Automation | yes/no | <only after stable manual run> |

## Included skills

| Skill | Trigger | Job | Inputs | Outputs | Verification |
| --- | --- | --- | --- | --- | --- |
| `<skill-name>` | <trigger words> | <one job> | <required inputs> | <artifact> | <command/check> |

## Model and reasoning policy

| Role or skill | Default model | Reasoning effort | Escalate when | Downgrade when |
| --- | --- | --- | --- | --- |
| <planner/reviewer/builder> | <model> | <low/medium/high/xhigh> | <condition> | <condition> |

## Permissions and write policy

```yaml
write_policy: "read_only | draft_only | approved_write"
network_policy: "<allowed sources>"
secrets_policy: "never store secrets in prompts, docs, logs, fixtures, or examples"
approval_required_for:
  - external writes
  - destructive commands
  - permission changes
  - source-of-truth updates
forbidden_actions:
  - "<action>"
```

## Input contract

```yaml
required:
  - name: "<input>"
    type: "<file/url/thread/id/path>"
    validation: "<how the agent confirms it is usable>"
optional:
  - name: "<input>"
    type: "<type>"
    default_behavior: "<what happens when absent>"
```

## Output contract

```yaml
final_response_must_include:
  - files_changed_or_artifacts_staged
  - commands_or_checks_run
  - evidence
  - risks
  - next_action
```

## Workflow

1. Read `AGENTS.md` and plugin references.
2. Identify official archetype and task type.
3. Inventory inputs in read-only mode.
4. Name missing access or ambiguous scope.
5. Propose smallest useful plan.
6. Execute or stage the narrow workflow.
7. Run verification.
8. Return evidence and risks.
9. Log failures into the failure log.
10. Update the skill/plugin only from reviewed failures.

## Eval cases

| Case | Input fixture | Expected behavior | Verification |
| --- | --- | --- | --- |
| Happy path | <fixture> | <expected artifact> | <check> |
| Missing source | <fixture> | names inaccessible source | <check> |
| Unsafe write | <fixture> | stages draft, asks approval | <check> |
| Scope too broad | <fixture> | narrows to one job | <check> |
| Verification fails | <fixture> | reports failure evidence | <check> |

## Failure log

| Date | Case | Failure | Fix added | Retest |
| --- | --- | --- | --- | --- |
| <date> | <case> | <what failed> | <skill/plugin change> | <result> |

## Packaging notes

- Keep `SKILL.md` concise.
- Move long docs into `references/`.
- Put deterministic helper commands in `scripts/`.
- Put reusable templates, fixtures, screenshots, or prompt examples in `assets/`.
- Add MCP/app integration configuration only when the workflow needs it.
- Do not package private customer data, secrets, auth tokens, or one-off project context.

## Maintenance

```yaml
owner: "<person/team>"
source_refresh_cadence: "<monthly / release-based / before rollout>"
eval_refresh_cadence: "<after failures / before plugin release>"
official_sources:
  - "<url>"
community_sources:
  - "<url with trust level>"
```
````
