# Prompt & Context Engineering

Source status: `official + experiment`  
Sources: [Prompting](https://developers.openai.com/api/docs/guides/prompting), [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [Model optimization](https://developers.openai.com/api/docs/guides/model-optimization), [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [OpenAI Cookbook](https://github.com/openai/openai-cookbook).

## Separation of concepts

Prompt engineering is responsible for instructions: what the model should do, in what style, with what constraints and in what result format.

Context engineering is responsible for the working memory of a specific call: which facts, documents, citations, history, tool outputs and session state the model sees before answering.

To reduce hallucinations, the important part is not the "perfect phrase", but full control of the circuit:

```mermaid
flowchart LR
    Q["Question"] --> P["Prompt contract"]
    C["Retrieved context"] --> P
    M["Memory / session"] --> P
    P --> R["Model response"]
    R --> V["Verifier / guardrail"]
    V -->|Pass| O["Final answer"]
    V -->|Fail| E["Clarify / retrieve more / refuse"]
```

## Prompt as a contract

A good prompt should answer eight questions explicitly:

| Question | Prompt contract field |
| --- | --- |
| Who answers? | `Role` |
| What counts as success? | `Goal` |
| What can it rely on? | `Context` |
| What is forbidden? | `Constraints` |
| What should happen with unknowns? | `Uncertainty policy` |
| Which tools can be used? | `Tools` |
| How should the result be returned? | `Output format` |
| How should the answer be checked? | `Verification` |

## Instruction hierarchy

For API and agentic systems, it is useful to separate levels:

- System/developer instructions: stable policy, tone, safety, tool rules.
- User task: concrete task, data, goal.
- Retrieved context: facts, documents, tool outputs.
- Examples: compact few-shot examples of the desired result.
- Output schema: machine-checkable contract.

Do not put transient task details into the permanent system prompt. Do not put long-term policy into a user message if it must always be followed.

## Optimization cycle

OpenAI model optimization guidance describes a cycle: eval baseline, prompt/context, realistic test inputs, measurement, adjustment, repeat. For this knowledge base, this means:

1. First define the eval: "the answer must cite source IDs", "it must not invent a source", "it must ask a clarification when data is missing".
2. Then write the prompt.
3. Check it on question sets similar to real ones.
4. Version the prompt and record changes.

## Anti-hallucination baseline

Minimal baseline for factual tasks:

```text
Answer only from the provided context.
If the context is insufficient, say what is missing.
Do not invent facts, citations, file paths, versions, prices, dates, or line numbers.
Separate verified facts from assumptions.
Return citations for every factual claim when sources are provided.
```

