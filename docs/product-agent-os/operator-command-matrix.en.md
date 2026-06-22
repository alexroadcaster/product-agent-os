# Operator command matrix

Source status: `project evidence`

Sources: `plugins/product-agent-os/scripts/run_first_project_analysis.py`, `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py`, `plugins/product-agent-os/scripts/scan_project_code_graph.py`, `tools/docs_install.ps1`, `tools/docs_node_install.ps1`, `tools/docs_vale_install.ps1`, `tools/docs_link_secret_install.ps1`, `tools/docs_mermaid_install.ps1`, `tools/docs_dependency_audit.ps1`, `.docs-tools/node/package.json`, [CLI Reference](cli-reference.en.md).

This matrix answers the operator question: which command is safe preview, which command writes only generated artifacts, and which command needs separate approval.

## First-run analysis

`run_first_project_analysis.py` chooses exactly one mode per invocation.

| Mode | Example | Writes | Boundary |
| --- | --- | --- | --- |
| Help | `python plugins\product-agent-os\scripts\run_first_project_analysis.py --help` | No | Safe help inspection. |
| `--full-dry-run` | `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --full-dry-run` | No | Safe first-run orchestration without target writes. |
| `--dry-run` | `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --dry-run` | No | Prints packet; generated files are not created. |
| `--stage <dir>` | `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --stage C:\tmp\product-agent-os-first-run` | External stage root | Stage path must be outside the target workspace; stage-inside-target is blocked. |
| `--write-analysis` | `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --write-analysis` | `.codex/product-agent-os/analysis/` | Generated packet and offline HTML only; not source mutation. |
| `--write` | `python plugins\product-agent-os\scripts\run_first_project_analysis.py <workspace> --write` | `.codex/product-agent-os/analysis/first-run-analysis-packet.json` | Legacy generated-packet write; no live/runtime/provider/browser/git action. |

`--stage` and `--write-analysis` are not approvals for target source edits. They are generated artifact routes.

## Project code graph

| Mode | Example | Writes | Boundary |
| --- | --- | --- | --- |
| `--dry-run` | `python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --dry-run` | No | Prints graph JSON as orientation evidence. |
| `--stage <dir>` | `python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --stage C:\tmp\product-agent-os-graph-stage` | Explicit stage root | Stages generated graph/cockpit artifacts. |
| `--query <kind>` | `python plugins\product-agent-os\scripts\scan_project_code_graph.py <workspace> --query status --graph <project-code-graph.json>` | No | Reads an existing graph; query packet remains bounded and source-free. |
| Extension gates | `--build-index`, `--build-backend`, `--build-semantic-index`, `--build-llm-proposals`, `--verify-extensions` | Stage root | Generated extension artifacts; provider/live/canonical mutation remains approval_required. |
| Live and real-testing gates | `--validate-live-runtime`, `--validate-embedding-provider`, `--build-real-testing-readiness`, `--build-runtime-qa` | Stage root | Governance/readiness packets only; no live server, browser automation or provider call by default. |

## Documentation Tooling

| Command family | Safe row | Approval-required row |
| --- | --- | --- |
| Python MkDocs runtime | `powershell -NoProfile -ExecutionPolicy Bypass -File tools\docs_install.ps1` prints a plan. | `-Install` plus `-AllowNetwork` or `-OfflineWheelhouse <path>`. |
| Node docs tooling | `powershell -NoProfile -ExecutionPolicy Bypass -File tools\docs_node_install.ps1` prints a plan. | `-Install` plus `-AllowNetwork` or `-OfflineCache <path>`. |
| Markdownlint | `npm.cmd --prefix .docs-tools\node run markdownlint:smoke` | Broad docs lint/enforcement needs owner-approved scope and report policy. |
| Prettier | `npm.cmd --prefix .docs-tools\node run prettier:check:readme` | Broad autoformat is not approved by smoke evidence. |
| Redocly | `npm.cmd --prefix .docs-tools\node run redocly:version` | OpenAPI lint/bundle enforcement is `not_applicable` until an OpenAPI source contract exists. |
| Vale | `.docs-tools\bin\vale.exe --version` and scoped fixtures | Broad claim-language enforcement remains advisory until thresholds/report retention are approved. |
| Lychee/gitleaks | Scoped local fixtures only | External URL crawling, broad repository scans, raw findings and retained reports require explicit approval. |
| Mermaid | Local vendored asset/static MkDocs smoke | Browser diagram proof/root `site` freshness remain separate. |
| Dependency audit | `tools\docs_dependency_audit.ps1` only when the current slice asks for audit evidence | Remediation, raw report retention, Python vulnerability audit/SBOM and complete repo SBOM require separate approval. |

## Forbidden Shortcut

Docs commands do not approve live servers, browser automation, provider/API calls, target mutation, broad scans, external crawling, report retention, root `site` rebuild, git actions, release, deploy, publish or automation activation. Those surfaces need their own approval packet and rollback evidence.
