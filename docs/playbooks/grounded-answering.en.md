# Playbook: grounded answering

Source status: `official + experiment`  
Sources: [Prompting](https://developers.openai.com/api/docs/guides/prompting), [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Model optimization](https://developers.openai.com/api/docs/guides/model-optimization), [OpenAI Cookbook](https://github.com/openai/openai-cookbook).

## Goal

Give a GPT-model answer with minimal hallucination risk: retrieve, constrain, answer, cite, verify, escalate uncertainty.

## Procedure

1. Determine the question type: factual, design, coding, current data, opinion.
2. Collect context from allowed sources.
3. Package context with source IDs.
4. Formulate the prompt contract.
5. Require citations or structured output.
6. Pass the answer through a verifier.
7. If context is insufficient, return missing context instead of guessing.

## Prompt

```text
# Role
You are a grounded answer generator.

# Goal
Answer the user question using only the provided sources.

# Context
<source id="S1" type="official" url="...">
...
</source>

# Rules
- Every factual claim must cite a source ID.
- If a claim is not supported, put it in unsupported_claims.
- If sources conflict, describe the conflict.
- If context is insufficient, do not guess.

# Output
Return:
- answer
- citations
- assumptions
- unsupported_claims
- missing_context
- confidence: high | medium | low
```

## Verifier prompt

```text
Check the answer against the provided sources.

For each factual claim:
- supported
- unsupported
- contradicted
- needs_fresh_check

Return verdict: pass | fail | needs_more_context.
```

## Acceptance criteria

- No factual claims without citation.
- No invented source IDs.
- Missing context is named explicitly.
- If confidence is below high, the answer explains why.
- For current facts, fresh verification was performed or the inability to verify is stated.

