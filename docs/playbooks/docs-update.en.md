# Playbook: documentation update

Source status: `official + experiment`

Sources: [official documentation](https://learn.chatgpt.com/docs), [AGENTS discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Inputs

A changed official source or project behavior, affected pages, active project rules and authorized scope. Change supported claims only; inaccessible sources remain explicit gaps. A research report does not automatically authorize implementation or publication.

## Procedure

1. Read the owning source and both language versions. Separate current guides from dated archives.
2. Verify the official claim for product/client/version/authentication. Update registry URL, claim scope and `checked_at` only for material actually reviewed.
3. Update RU/EN together: commands, identifiers, permissions, prerequisites, results and limitations must agree in meaning.
4. Preserve history. Clarify dates and current pointers; never translate code tokens.
5. Run documentation contract checks and `git diff --check`.
6. If scope includes navigation, Mermaid, MkDocs configuration or generated output, run the authorized strict build in the owning `site_dir`.
7. Compare expected routes with generated HTML, then check links/anchors, search and language switching. Diagrams need parse/render checks; build exit 0 does not prove rendering.
8. Record current evidence, changed pages, gaps and the publication boundary.

## Documentation closure order

Source docs → registry RU/EN → docs tests → `check_docs.py` → applicable strict MkDocs → links/diagrams → optional full closure for implementation changes.

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools/check_docs.py
git diff --check
# When site/nav/diagram scope is authorized:
.venv-docs/Scripts/python.exe -m mkdocs build --strict
```

Do not install dependencies automatically. The full plugin/runtime suite is required only for affected behavior. Browser/server, provider calls, Git and publication remain separate actions; reuse existing precise authority rather than asking twice.

## Prompt

```text
Update affected pages against current official sources.
Synchronize RU/EN and the registry; preserve history and canonical identifiers.
Run mandatory documentation checks.
Rebuild site only within authorized scope.
For a build, check expected routes, links/anchors and diagrams.
Return changes, evidence and remaining limits; do not publish.
```

## Outputs and failure modes

Output: updated guides/registry and dated checks. Failures: changing a date without source review; checking existing links while missing new routes; treating a generated view as source truth; claiming runtime activation from text edits.

## Verification

Use the applicable commands above and inspect generated output before reporting closure.

## Risks

Unsupported source claims, stale builds and missing routes remain explicit gaps until checked.
