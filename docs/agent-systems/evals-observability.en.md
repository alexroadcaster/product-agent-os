# Evals and Observability

Source status: `official + experiment`
Sources: [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python), [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses), [Codex workflows](https://developers.openai.com/codex/workflows).

## Why This Belongs In The Codex Knowledge Base

An advanced Codex workflow should be checked with more than project tests. Agent systems need separate quality gates:

- source fidelity;
- task completion;
- tool correctness;
- safety policy adherence;
- handoff completeness;
- regression stability.

## Guardrails

Guardrails in Agents SDK are used to check inputs and outputs. In a documentation project, a guardrail can be described as a verifiable rule:

| Guardrail | Check |
| --- | --- |
| Official-source fidelity | Every factual claim has an official source or `community/experiment` status |
| No secret retention | Docs, insights, and memory do not contain secrets |
| Handoff completeness | Handoff payload contains goal, constraints, sources, claims, risks |
| Tool boundary | Tool call stays within the sandbox/approval policy |
| Structured output | Agent returns JSON/YAML by contract when required |

## Tracing

Tracing is needed for debugging and monitoring agent applications: which agents were called, which tools were used, where latency appeared, and where a failure occurred.

For Codex documentation, the tracing equivalent is an evidence trail:

```yaml
task: "Update memory docs"
sources:
  - "https://developers.openai.com/codex/memories"
  - "https://openai.github.io/openai-agents-js/guides/sessions/"
decisions:
  - "AGENTS.md is mandatory policy; memories are recall layer."
checks:
  - "python tools/check_docs.py"
  - "python -m mkdocs build --strict"
result: "accepted | needs_review | rejected"
```

## Evals For The Knowledge Base

Minimal eval suite:

| Eval | Prompt | Pass condition |
| --- | --- | --- |
| Source audit | "Check the section for claims without sources" | No unsupported official claims |
| Navigation | "Find the path from Codex App to multi-agent playbook" | The path goes through overview -> surfaces -> agent systems -> playbook |
| Insight separation | "Find community tricks in core docs" | Community claims appear only with explicit status |
| Handoff quality | "Evaluate the handoff contract" | goal, constraints, sources, claims, risks are present |
| Build health | `python tools/check_docs.py` + MkDocs build | Both pass |

## Long-Horizon Improvement Loop

For complex product tasks, use this loop:

1. Run baseline eval.
2. Identify one bottleneck.
3. Make one focused change.
4. Re-run deterministic checks and LLM-as-judge.
5. Inspect artifact directly when output is visual or subjective.
6. Log score and decision in `RUNLOG.md`.
7. Continue until explicit thresholds are met.

Do not change several independent things in one iteration: otherwise you cannot understand what improved the score.

## LLM-as-judge + Deterministic Checks

| Layer | What it proves | What it does not prove |
| --- | --- | --- |
| Deterministic checks | Code compiles, links exist, schema passes | UX quality, usefulness, semantic correctness |
| LLM-as-judge | Rubric-based quality, clarity, relevance | Security correctness by itself |
| Artifact inspection | Real generated output matches intent | No hidden regression elsewhere |
| Human review | Product fit and risk judgment | Repeatability without evals |

## Failure Taxonomy

| Failure | Symptom | Fix |
| --- | --- | --- |
| Source drift | Official page changed and docs became stale | Update the source card and affected sections |
| Context rot | Agent uses old assumptions | Reopen sources and reduce memory reliance |
| Handoff loss | Worker loses constraints | Introduce structured handoff schema |
| Tool overreach | Agent asks for overly broad permissions | Tighten approval policy |
| Eval blind spot | Build passes, but quality is weak | Add scenario eval |

## Model migration: measurable contract

Follow the [model migration playbook](../playbooks/model-migration.md): fixed baseline, one variable, independent assessment, predefined thresholds and budget. New models remain `documented_candidate_not_evaluated` without real results. This method does not authorize model/provider calls.

| Measurement | Run packet record |
| --- | --- |
| Reproducibility | Revision, corpus/input hashes, client/auth/runtime, model/effort, prompts, skills, tools and permissions |
| Quality | Task success, correctness, regressions, unsupported claims; identical rubric for paired runs |
| Behavior | Tool failures, unnecessary approvals, premature final, repeated checks without new evidence |
| Time | End-to-end latency and distribution when the sample is adequate |
| Cost | Input/output/reasoning tokens, cache reads/writes, retries/subagents, tier, pricing date and cost per completed task |
| Activation | Effective path, no masking fallback and fresh-session evidence |

Numerical thresholds/budgets are fixed before execution; missing measurements are not zero. Safety and schema failures block promotion regardless of average score. Compare the supported baseline effort first; optimize effort and prompt separately. Unit/docs checks prove their contracts, not model quality or runtime activation. Method source: [official migration guidance](https://developers.openai.com/api/docs/guides/latest-model).
