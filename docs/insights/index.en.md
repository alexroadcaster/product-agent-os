# Insights Layer

Source status: `community | experiment`

Insights are the unofficial layer: user tricks, observations, GitHub issues, Reddit patterns, blog posts, and local experiments. They are useful for improving work, but they are not a source of truth.

## Rules

- An insight is not moved into the main guide without verification.
- Every insight has `verification_status`.
- If an insight conflicts with official documentation, it stays in insights with a conflict note.
- If an insight is confirmed locally, add a reproduction or transcript summary.
- If an insight becomes stale after a changelog update, mark it as `stale`.

## Verification Statuses

| Status | Meaning |
| --- | --- |
| `unverified` | Found in community/source, not verified |
| `reproduced` | Verified locally once |
| `adopted` | Became part of the project workflow |
| `rejected` | Verification did not confirm it |
| `stale` | Was useful, but may have become outdated |

## Adding An Insight

1. Copy the [card template](insight-card-template.md).
2. Specify the source and date.
3. Describe the risk.
4. Define the verification.
5. Move the conclusion into a playbook only after verification.
