# Playbook: Context7 deep research

Source status: `official + experiment`
Sources: [Context7 results for OpenAI docs](../sources/context7-research.md), [Source registry](../sources/registry.md).

## Goal

Use Context7 as a fast retrieval layer for expanding the knowledge base while preserving official-source discipline.

## Procedure

1. State the research question as a list of capabilities, not as a broad query.
2. Resolve the library ID for each library.
3. Query docs for no more than the three most important directions in one pass.
4. Split results into:
   - official facts;
   - examples/recipes;
   - architecture implications;
   - claims that need direct source verification.
5. Add or update source cards.
6. Apply changes to docs.
7. Run checks.

## Good Query

```text
Extract authoritative design details for the OpenAI Agents SDK:
Agent, Runner, tools, handoffs, guardrails, sessions, tracing,
context, multi-agent orchestration, and recommended architecture patterns.
Focus on concepts useful for documenting multi-agent systems with memory.
```

## Bad Query

```text
Tell me everything about agents.
```

It is too broad: the result will be hard to verify and move into the source registry.

## Output contract

```yaml
context7_libraries:
  - library_id: ""
    source_reputation: "High | Medium | Low"
findings:
  - claim: ""
    source_url: ""
    target_doc: ""
    action: "add | update | reject | verify_directly"
risks:
  - ""
verification:
  - "python tools/check_docs.py"
  - "python -m mkdocs build --strict"
```

