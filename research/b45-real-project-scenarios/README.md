# B45-PCA-M29 Real-Project Scenario Inventory

Source status: project-authored read-only inventory. No target source bodies were copied. No target workspace mutation, runtime launch, browser automation, provider call, git write, deployment, publication, or external automation was performed.

## Purpose

`B45-PCA-M29` converts the Batch 45 professional-code-authoring architecture map into concrete scenario candidates from real projects. The inventory is intentionally metadata-only: it records target shape, candidate task families, relevant relative paths, available commands, privacy boundaries, and approval gates.

This is not a refactor packet yet. It is the scenario selection layer for later B45-PCA slices that can copy approved fixtures into `codex_docs`, run the local Product-Agent OS modules, compare outputs, and decide whether a refactor is justified.

## Rereview Verdict

The 2026-06-30 repeat pass confirms that M29 is detailed enough as a scenario selection layer, not as a complete whole-project topology. The current candidate list intentionally prioritizes high-signal professional-code-authoring scenarios. Additional project families are now recorded as deferred so their absence is explicit rather than an accidental coverage gap.

The repeat pass also tightened the inventory method: future copy or fixture work must use recursive exclusions such as `!**/node_modules/**`, not only folder-name globs, and must run a path-metadata denylist pass before any source body is copied.

## Targets Inspected

| Target label | Read-only result | Main shape | Important boundary |
| --- | --- | --- | --- |
| `myPartners` | available and inspected read-only | FastAPI server, Next.js frontend, Cloudflare Worker, docs, tools | Contains active repo state and private-data-sensitive surfaces; future execution must stay fixture/metadata-only unless explicitly approved. |
| `SOL 0.6` | available and inspected read-only | Node/TypeScript backend, Next.js frontend, Python helper scripts, bundled examples/vendor-like material | Root is not a git repository; dependency/build folders and env files must stay excluded from copied evidence. |

Target-selection provenance: the target labels were named by the owner in the current B45-PCA thread for this read-only inventory. That approval does not authorize source-body copying, target command execution, browser/runtime work, provider calls, git writes, deployment, publication, or automation.

## Produced Artifacts

| Artifact | Role |
| --- | --- |
| `source-inventory.md` | Human-readable inventory of target shape, candidate areas, checks, privacy risks, and approval boundaries. |
| `scenario-candidates.json` | Machine-readable candidate list for later selection, scoring, and module routing. |
| `rereview-2026-06-30.md` | Repeat-pass audit of coverage, missed/deferred families, privacy/denylist gaps, and agent review findings. |
| `source-policy.md` | M30 policy for sanitized fixture source classes, forbidden data, path normalization, digest policy, rollback, and approval gates. |
| `scenario-manifest.schema.json` | M30 schema for future per-scenario copy approval and scope records. |
| `fixture-manifest.schema.json` | M30 schema for future copied sanitized fixture file inventories. |
| `redaction-manifest.schema.json` | M30 schema for future redaction rules without storing original sensitive values. |
| `fixtures/sol/SOL-AGENT-ORCH-01/` | M31 sanitized analysis-only fixture pack for the SOL backend agent orchestration scenario. |
| `fixtures/mypartners/MP-CRM-CHAT-OPEN-01/` | M31 sanitized analysis-only fixture pack for the myPartners CRM contact/chat-open workflow scenario. |
| `results/SOL-AGENT-ORCH-01-baseline.json` | M32 fixture-local baseline packet for the SOL agent orchestration scenario. |
| `results/MP-CRM-CHAT-OPEN-01-baseline.json` | M32 fixture-local baseline packet for the myPartners CRM chat-open scenario. |
| `../../docs/superpowers/specs/batch45-real-project-baseline-results.json` | M32 cross-scenario baseline rollup, evidence ceiling and M33 gate decision. |

## Scenario Families

| Scenario id | Target | Family | Candidate use |
| --- | --- | --- | --- |
| `MP-CRM-CHAT-OPEN-01` | `myPartners` | CRM chat/contact workflow | Backend + frontend workflow with existing focused tests and privacy-sensitive message evidence boundaries. |
| `MP-REL-GRAPH-SIGMA-02` | `myPartners` | Relationship graph and Sigma rendering | Graph/domain semantics, layout payloads, frontend adapter contracts, and browser-gated visual proof. |
| `MP-ADVISOR-BOUNDARY-03` | `myPartners` | Advisor local/Worker boundary | API route, local orchestration, inference handoff, Worker handler, and live-provider approval boundary. |
| `MP-RAG-SEMANTIC-04` | `myPartners` | Semantic retrieval and vector readiness | Retrieval interfaces, sqlite/vector readiness, local evals, and private-data-safe fixture policy. |
| `SOL-AGENT-ORCH-01` | `SOL 0.6` | Backend agent orchestration | Agent registry, orchestrator, tool dispatcher, and typed build baseline. |
| `SOL-FRONTEND-CHAT-02` | `SOL 0.6` | Frontend workspace/chat/task UI | Stores, socket client, layout, and primary views with lint/build baseline. |
| `SOL-SKILL-LOADER-03` | `SOL 0.6` | Offline skill loader scripts | Python script workflow candidate for static analysis and minimal command-surface discovery. |

## Deferred Families

| Deferred id | Target | Why deferred |
| --- | --- | --- |
| `MP-SETTINGS-DIAG-OBS-DEFERRED` | `myPartners` | Settings, diagnostics, and observability are real surfaces, but not the first professional-code-authoring pilot path. |
| `MP-APPDATA-SELFCONTEXT-DEFERRED` | `myPartners` | App-data activation, Self Context, memory, and history activation are high-risk data/state workflows requiring stricter approval and metadata-only fixture policy. |
| `MP-BOOTSTRAP-AUTH-SYNC-DEFERRED` | `myPartners` | Bootstrap, auth, scheduler, sync, and Beeper spike surfaces touch credentials, local state, or integration boundaries. |
| `MP-WORKER-INSIGHTS-DEFERRED` | `myPartners` | Worker and insights surfaces need separate runtime/provider/edge-boundary handling. |
| `SOL-DOCS-TASK-TRACE-DEFERRED` | `SOL 0.6` | PRD, architecture notes, task chats, generated project examples, and one-off files are traceability material, not first-pass code fixtures. |

## Approval Boundaries For Later Slices

- Copying source bodies from target projects into `codex_docs` requires exact scenario selection and a redaction/copy policy.
- Running target commands requires exact approval naming the target, command, expected writes, rollback, and evidence.
- Runtime launches, browser automation, Worker/provider/API calls, live DB access, and target git actions are out of scope for M29.
- Env files, local databases, generated build folders, dependency folders, logs, traces, screenshots/videos, raw private messages, raw user data, and private payloads must not be copied into scenario fixtures.

## Recommended Next Selection

Start with one high-signal, low-mutation candidate:

1. `SOL-AGENT-ORCH-01` for architecture/refactor scoring with a simple TypeScript build gate.
2. `MP-CRM-CHAT-OPEN-01` for Product-Agent OS behavior on a richer real workflow, but only with metadata-only fixtures or explicitly approved redacted snippets.
3. `MP-RAG-SEMANTIC-04` when the goal is to test deeper AI/eval/retrieval guidance rather than general code-authoring quality.
