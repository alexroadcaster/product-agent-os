# Codex Workflows

Source status: `official`  
Sources: [Codex workflows](https://developers.openai.com/codex/workflows), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Prompting](https://developers.openai.com/codex/prompting).

## Structure of a good task

Codex works better when it receives explicit context and a definition of done. Minimal task packet:

```text
Goal:
Context:
Constraints:
Allowed changes:
Out of scope:
Verification:
Expected output:
```

## Use cases as a workflow catalog

The official [Codex use cases](https://developers.openai.com/codex/use-cases) section should be read as a practical map of repeatable tasks: each card defines outcome, audience, starter prompt, skills/plugins, constraints, verification and related workflows.

For project work, use [Deep analysis of Codex use cases](use-cases-deep-analysis.md):

- choose the closest official archetype;
- transfer its inputs, constraints and verification into the task packet;
- run the workflow manually;
- only after a successful runlog, turn it into a skill;
- if the workflow is needed by several projects or requires a bundle of skills, MCP and app integrations, package a plugin.

## Workflow: understand a codebase

Use for onboarding, analysis of a service, protocol or request flow.

```text
Study the selected module and return:
- a short map of file responsibilities;
- request/data flow step by step;
- where data is validated;
- 2-3 risks when making changes;
- a list of files to read next.
Do not change files.
```

Verification:

- request a numbered flow;
- check the mentioned files;
- verify that Codex did not invent nonexistent entrypoints.

## Workflow: fix a bug

For a bugfix, a reproducible symptom is needed first.

```text
Bug:
Repro steps:
Expected:
Actual:
Suspected files:
Constraints:
Verification command:
```

If reproduction is not provided, the first Codex task is to find or propose a minimal reproducible scenario, not to change code immediately.

## Workflow: update documentation

```text
Compare official sources with current docs.
Do not change claims without a source registry link.
Return:
- outdated claims;
- new facts;
- proposed edits;
- verification checklist.
```

This workflow has been turned into a separate [playbook](../playbooks/docs-update.md).

