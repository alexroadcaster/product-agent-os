# Link And Secret Hygiene Fixtures

Source status: local implementation contract.

This directory belongs to Track 11 G1.1 `DOC-M38`.

It stores small, synthetic fixtures for project-local `lychee` and `gitleaks`
smoke checks. The fixtures are not broad repository evidence and do not prove
external-link health, repository-wide secret safety, dependency safety, SBOM
coverage or publication readiness.

## Boundary

- `lychee` smoke must use `--offline` unless a later slice explicitly approves
  external URL crawling.
- `gitleaks` smoke must use `--redact`, scan a narrow fixture or approved docs
  scope, and must not copy raw findings into public docs.
- Reports under `.docs-tools/reports/` remain generated local artifacts unless
  a later report-retention policy explicitly approves checked-in examples.
