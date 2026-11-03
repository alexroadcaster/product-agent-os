# Designing Questions for GPT Models

Source status: `official + experiment`  
Sources: [Prompting](https://developers.openai.com/api/docs/guides/prompting), [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [OpenAI Cookbook](https://github.com/openai/openai-cookbook).

## Formula for a good question

Bad question:

```text
Tell me about agents.
```

Good question:

```text
Goal: Design a multi-agent research workflow for updating Codex documentation.
Audience: Advanced agent builder.
Context: Use only the listed sources and the current docs structure.
Constraints: Do not mix official and community claims.
Output: Return architecture, roles, handoff contract, evals, risks.
Uncertainty: If a source is missing, mark the claim as needs_source.
Verification: State which docs/checks need to be updated.
```

## Prompt packet

Use this packet as the default:

```text
# Role
You are ...

# Goal
...

# Context
<source id="S1">
...
</source>

# Constraints
- ...

# Unknowns and assumptions
- Ask a clarifying question if ...
- Otherwise assume ...

# Tools
- Use ... only when ...

# Output format
...

# Verification
...
```

## Specificity rules

| Instead of | Write |
| --- | --- |
| "Make it better" | "Shorten to 800 words, preserve citations, add failure modes" |
| "Analyze" | "Find contradictions, unsupported claims, missing tests" |
| "Explain in detail" | "Give a mental model, workflow, examples, pitfalls" |
| "Do not hallucinate" | "If a claim is not supported by context, mark `needs_source`" |
| "Answer JSON" | "Return JSON by schema, use an empty array and `missing_context` when data is missing" |

## When to ask a clarifying question

The model should clarify when:

- the task has several incompatible interpretations;
- critical input is missing;
- the action may be dangerous or expensive;
- the result depends on fresh facts and tools are unavailable;
- user intent matters more than repo facts.

If ambiguity does not block the work, it is better to choose an explicit assumption:

```text
Assumption: By "agents" I mean OpenAI Agents SDK, not general AI agents.
```

## Few-shot examples

Few-shot is needed when not only "what", but also "what a good answer looks like" matters. Keep examples short:

```yaml
examples:
  - input: "Check claim: Codex launches subagents by itself."
    output:
      status: "qualified"
      reason: "Local Codex delegation can be requested by the user or applicable AGENTS/skill instructions; project policy may be stricter. Work Ultra has a separate proactive workflow."
      source: "https://learn.chatgpt.com/docs/agent-configuration/subagents"
  - input: "Check claim: Structured Outputs solve all hallucinations."
    output:
      status: "qualified"
      reason: "They constrain shape, but factual mistakes remain possible."
      source: "https://developers.openai.com/api/docs/guides/structured-outputs"
```

## Checklist before sending

- Is there a concrete outcome?
- Is there a list of allowed sources?
- Is there a ban on unsupported facts?
- Is there an output format?
- Is there a rule for uncertainty?
- Is there a verification criterion?

## Prompt review before migration

Before changing a prompt, check the outcome, whether useful work can continue without an answer, the existing authorization boundary, required checks, justification for repetition and promotion owner. Do not request private chain-of-thought; ask for concise rationale, assumptions and evidence. Compare the model with a fixed prompt before changing the prompt separately. See [GPT-6 prompting](overview.md) and the [migration playbook](../playbooks/model-migration.md).
