# Playbook: documentation update

Source status: `official + experiment`  
Sources: [Codex changelog](https://developers.openai.com/codex/changelog), [Codex workflows](https://developers.openai.com/codex/workflows).

Use this playbook when Codex, Agents SDK, Product-Agent OS or project behavior changes and the documentation must stay source-backed.

## Inputs

- Changed source docs, official references, source registry entries and affected pages.
- Project rules for Russian/English terminology, source status and approvals.

## Outputs

- Updated documentation pages, source registry entry and focused docs tests when needed.
- Current verification evidence for docs structure and MkDocs build.

## Verification

Recommended order:

```powershell
python tools\check_docs.py
python -m mkdocs build --strict
git diff --check
```

## Risks

- Adding claims without registry support can make docs drift from source truth.
- Rebuilding generated `site/` without source updates does not prove the docs are correct.
