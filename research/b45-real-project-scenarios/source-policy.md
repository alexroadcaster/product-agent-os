# B45-PCA-M30 Sanitized Fixture Source Policy

Source status: project-authored fixture policy. This is a pre-copy contract for later `B45-PCA-M31` work. No target source bodies were copied for M30. No target workspace mutation, target build/test command, runtime launch, browser automation, provider/API call, git write, deployment, publication, or external automation was performed.

## Purpose

`B45-PCA-M30` defines the policy for creating sanitized real-project fixture packs inside `codex_docs`. It exists because `B45-PCA-M29` proved that useful real-project scenarios exist, but did not prove that any source body is safe to copy.

M30 is the stop gate between metadata-only inventory and fixture construction. M31 may proceed only after exact owner approval names:

- selected `scenario_id`;
- target label;
- relative source paths;
- intended fixture directory;
- allowed source classes;
- explicit forbidden classes;
- verification commands;
- rollback/delete path.

## Current Selection Recommendation

| Rank | Scenario | Reason | M31 status |
| --- | --- | --- | --- |
| 1 | `SOL-AGENT-ORCH-01` | Smallest high-signal code scenario; TypeScript backend architecture; low fixture breadth. | Recommended first, still approval-required before copying. |
| 2 | `MP-CRM-CHAT-OPEN-01` | Rich backend/frontend workflow and privacy-safe evidence test. | Useful second scenario, requires stricter privacy review. |
| 3 | `MP-RAG-SEMANTIC-04` | Deep AI/RAG/eval architecture. | High value, but high data/privacy risk. |

Deferred families from M29 remain out of fixture scope unless a later approval explicitly reclassifies them.

## Allowed Source Classes

Allowed does not mean automatically copied. Every copied file must be listed in a scenario manifest and fixture manifest.

| Class | Allowed when | Required notes |
| --- | --- | --- |
| Application source code | The file is directly needed for the selected scenario. | Record role, scenario reason, language, and dependency relationship. |
| Focused tests/contracts | The file verifies the selected scenario without private data. | Record expected command, unsupported runtime/browser claims, and privacy status. |
| Minimal manifests | Needed to understand dependencies or available commands. | Prefer `package.json`, `pyproject.toml`, `tsconfig.json`; lockfiles are conditional and need size/relevance justification. |
| Synthetic fixtures | Clearly synthetic and not derived from private/customer data. | Record synthetic source and generation note. |
| Architecture/docs excerpts | Needed for requirements or traceability and safe to copy. | Prefer summary metadata; copy source body only if approved and denylist-clean. |

## Forbidden Source Classes

These classes must not be copied into `codex_docs` fixtures.

| Class | Examples |
| --- | --- |
| Secrets and credentials | `.env`, `*.env`, API keys, tokens, private keys, certs, OAuth secrets, provider credentials. |
| Private data and payloads | Raw chats, raw messages, private prompts, raw model/provider responses, customer/user data, private graph payloads. |
| Databases and runtime state | `*.db`, `*.sqlite`, sqlite WAL/SHM files, `.sol_data`, `.wrangler/state`, app data, production data. |
| Logs and traces | `*.log`, logs folders, HAR files, Playwright traces, videos, screenshots, runtime dumps. |
| Generated/dependency trees | `node_modules`, `.next`, `dist`, `build`, `site`, `coverage`, `.turbo`, `.vite`, caches. |
| Git and workspace metadata | `.git`, worktrees, nested repo metadata, editor local state. |
| Unbounded corpora | Bundled vendor/example repositories or generated project corpora unless selected as the scenario and separately approved. |

## Conditional Source Classes

| Class | Default | Required before copy |
| --- | --- | --- |
| Lockfiles | Exclude by default. | Allow only if dependency analysis needs exact version graph and file size is reasonable. |
| Docs/task transcripts | Exclude by default. | Allow only if selected as traceability scenario and checked for raw chat/private content. |
| Binary assets | Exclude by default. | Allow only if synthetic, small, relevant, and not a screenshot of private data. |
| Tool scripts | Case-by-case. | Confirm no external writes, provider calls, registry calls, or mutation side effects. |
| Redacted files | Avoid when entire-file exclusion is safer. | Redaction manifest must record rule, replacement, reviewer, and residual risk. |

## Path Normalization

- Store only repository-relative paths in manifests.
- Use `/` as the canonical manifest separator.
- Do not store absolute user-specific roots in fixtures.
- Record target identity through `target_id` and `target_label`, not through local absolute paths.
- Preserve the original relative path under a fixture root unless doing so would expose a private identifier.
- Reject paths containing `..`, drive letters, UNC roots, shell expansions, or symlink-style ambiguity.

## Digest Policy

For every copied file, the fixture manifest must record:

- `sha256` of the copied sanitized content;
- byte size of the copied sanitized content;
- original relative path;
- fixture relative path;
- source class;
- copy reason;
- redaction status.

For excluded files, record path metadata and reason only. Do not hash private source bodies when hashing requires reading forbidden content.

## Redaction Policy

Redaction is allowed only when all of these are true:

1. The file is necessary for the selected scenario.
2. The sensitive material is narrow and mechanically replaceable.
3. The redacted version remains useful.
4. The redaction manifest records rule, original value class, replacement token, reviewer, and residual risk.

If those conditions are not met, exclude the file.

Never store original secret values, raw private text, raw prompts, raw provider responses, or raw customer/user data in redaction manifests.

## Target Read-Only Proof

Before any M31 fixture copy:

1. Run path-only inventory using recursive exclusions.
2. Run hidden/ignored path metadata scan to identify risk surfaces.
3. Record target dirty state where available.
4. Record that no target writes were performed.
5. Stop if a selected path is not needed for the scenario, is too broad, or belongs to a forbidden class.

Target read-only proof is not runtime proof.

## Fixture Directory Policy

Allowed future fixture roots:

```text
research/b45-real-project-scenarios/fixtures/mypartners/<scenario_id>/
research/b45-real-project-scenarios/fixtures/sol/<scenario_id>/
```

Required files per future fixture pack:

```text
scenario-manifest.json
fixture-manifest.json
redaction-manifest.json
README.md
```

The fixture body directory should be:

```text
src/
tests/
config/
docs/
```

Only include directories that are needed.

## Rollback And Deletion

Rollback for M31 fixture creation is limited to `codex_docs` fixture paths. Target projects remain read-only and need no rollback because they must not be modified.

Deletion steps for a rejected fixture:

1. Delete the fixture directory under `research/b45-real-project-scenarios/fixtures/...`.
2. Remove its registry/source-plan status entry if it was added.
3. Re-run JSON validation and docs checks.
4. Record the rejected reason in the scenario manifest or source-policy notes only if no private data is exposed.

## Evidence Retention

Keep:

- scenario manifests;
- fixture manifests;
- redaction manifests;
- path-only denylist reports;
- command names and exit statuses;
- sanitized hashes and byte sizes.

Do not keep:

- raw denylist match lines containing values;
- raw source excerpts from private files;
- screenshots/videos/traces of private data;
- raw provider/model responses;
- local DB contents.

## Stop Conditions

Stop before copying if:

- source-copy approval is missing;
- selected paths include forbidden classes;
- path scope expands beyond the approved scenario;
- a file requires reading private data to decide whether it is safe;
- fixture usefulness depends on runtime/browser/provider proof not approved for the slice;
- redaction would be broad, ambiguous, or unverifiable;
- target command execution would be needed to understand the scenario.

## M31 Approval Packet Template

```yaml
approval_packet:
  task_id: B45-PCA-M31
  scenario_id: ""
  target_id: ""
  fixture_root: ""
  selected_relative_paths: []
  excluded_relative_paths: []
  allowed_source_classes: []
  forbidden_source_classes_acknowledged: true
  redaction_expected: false
  target_commands_to_run: []
  codex_docs_commands_to_run:
    - "json schema validation for manifests"
    - "python -m unittest tests.product_agent_os.test_product_agent_os_docs -v"
    - "python tools\\check_docs.py"
    - "git diff --check"
  rollback_path: "delete only the created fixture directory and registry/status edits in codex_docs"
  unsupported_claims:
    - "runtime behavior"
    - "browser behavior"
    - "provider/live API behavior"
    - "target command success"
```

