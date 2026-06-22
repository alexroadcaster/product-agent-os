# Guided questions and answer ledger

Source status: `project evidence`

Sources: `plugins/product-agent-os/scripts/product_agent_os/question_protocol.py`, `plugins/product-agent-os/scripts/product_agent_os/question_ledger.py`, `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py`, `tests/product_agent_os/test_question_protocol.py`, `tests/product_agent_os/test_question_ledger.py`, [Scenarios](scenarios.en.md), [Artifact Contracts](artifact-contracts.en.md).

Guided questions help Product-Agent OS ask only what blocks the next safe step, without turning owner answers into hidden requirements or source truth.

## Question Queue

`question_queue` is a read-only packet. It can include:

| Field | Meaning |
| --- | --- |
| `questions` | Typed list of blocking, recommended and optional questions. |
| `next_blocking_question` | The single blocking question that can be shown first. |
| `summary` | Counts for blocking, recommended, optional and remaining questions. |
| `policy.max_blocking_questions_in_first_response` | Limit: `1`. |
| `policy.max_total_questions` | Limit: `8`. |
| `write_policy` | `read_only`. |

If several inputs look blocking, extra blocking rows are downgraded to `recommended` so the first response does not become a questionnaire.

## First Response

`first_response` shows a summary, `next_blocking_question`, `question_counts`, route options and `safe_next_action`. It should not include the full raw question list as conversational pressure. Ambiguous intake may expose two or three route options, but the completion claim remains `not_claimed`.

## Answer Ledger

`answer-ledger-template.json` and answer ledgers are `staged_only` artifacts. They make an owner answer a reviewable change instead of an implicit mutation of source docs.

| Ledger part | Purpose |
| --- | --- |
| `entries` | Owner answers mapped back to question IDs. |
| `artifact_updates` | Proposed docs/control-plane updates after owner review. |
| `summary` | Accepted, blocked, unanswered and total counts. |
| `validation` | Blocks stale, private, secret-like or malicious answers. |
| `write_policy` | `staged_only`. |

The ledger itself is not approval. Apply answers only through staged artifacts, the existing approval flow, source registry updates and relevant verification.

## Routing Rules

| Situation | Route |
| --- | --- |
| One missing owner decision blocks safe next action. | Ask one blocking question. |
| Several useful clarifications exist but work can continue safely. | Put them in recommended/optional packet fields. |
| Answer changes requirements, scope, acceptance or source truth. | Stage docs/control-plane update and run docs checks. |
| Answer requests runtime/browser/provider/git/external action. | Stop and request an exact approval packet. |
| Answer includes secrets/private data/raw logs. | Block, redact and ask for a sanitized restatement. |

## Status Dashboard Boundary

A generated status dashboard can show question ledger summary and artifact update proposals. It remains a generated view only; stale dashboard output, unanswered questions or unreviewed answers cannot support a completion, readiness or release claim.
