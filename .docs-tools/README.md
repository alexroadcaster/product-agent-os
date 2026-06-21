# Project-Local Docs Toolchain

This directory is the Track 11 G1.1 contract for repository-owned documentation
tooling.

Source status: local implementation contract.

## Purpose

- `.docs-tools/node/`: local npm-prefix manifest and cache boundary for
  Markdown/API documentation tools; `DOC-M36` installed `markdownlint-cli2`,
  Prettier and Redocly CLI here.
- `.docs-tools/bin/`: local standalone binary boundary; `DOC-M37` installed
  Vale here with a recorded checksum, while lychee and gitleaks remain future
  approval-gated rows.
- `.docs-tools/vale/`: local Vale styles, vocabulary and smoke fixture for
  advisory terminology, tone and claim-language checks.
- `.docs-tools/reports/`: local generated-report boundary for redacted documentation checks.
- `.venv-docs/`: ignored project-local Python runtime for MkDocs Material,
  installed by the approved `DOC-M35` slice.
- `docs/assets/javascripts/vendor/`: optional checked-in browser/runtime assets after license, source and checksum approval.

## Allowed Checked-In Content

- README files that describe the contract.
- `.docs-tools/node/package.json` and `.docs-tools/node/package-lock.json`.
- Tool configuration files such as `.vale.ini`, `.gitleaks.toml` or documented rules after their slice is approved.
- Vale style rules and vocabulary under `.docs-tools/vale/`.
- Redacted report examples only when the report-retention policy says they are safe to commit.

## Ignored Local Content

- `.venv-docs/`
- `.docs-tools/node/node_modules/`
- `.docs-tools/node/.npm/`
- `.docs-tools/node/.cache/`
- `.docs-tools/bin/*.exe`, `.dll`, `.zip` and `.tar.gz`
- `.docs-tools/reports/*` except this directory's README

## Forbidden Content

- Secrets, tokens, private keys, credentials, unredacted PII or private customer data.
- Raw private chat logs, raw provider responses or raw scanner findings.
- Downloaded binaries, minified assets or vendored runtimes without source, license, checksum and approval notes.
- Generated `site/` freshness claims without current strict MkDocs evidence from a project-local runtime.

## Approval Boundaries

Dependency installation, network download, binary vendoring, broad link scans, broad secret scans, report retention, hook activation, automation activation and publication remain out of scope until a later approved slice records the source, command, expected output, rollback and evidence owner.

`DOC-M37` approved only project-local Vale download/install and advisory smoke.
Vale warnings are not enforcement until a later slice explicitly approves
thresholds, failure policy and report handling.
