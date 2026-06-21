# Vale Language Guard

Source status: local implementation contract.

This directory owns the Track 11 G1.1 `DOC-M37` terminology, tone and
claim-language checks for Product-Agent OS documentation.

The rules are local and advisory. They catch wording that can accidentally turn
orientation evidence into readiness, publication, dependency-safety or source
truth claims.

## Layout

- `ProductAgentOS/`: local Vale style rules.
- `config/vocabularies/ProductAgentOS/`: accepted canonical project terms.
- `fixtures/`: small smoke fixtures for project-local Vale checks.

## Claim Boundary

Vale is a prose guard. It does not prove that a source is correct, that a
runtime works, that legal or compliance review happened, or that a release is
safe.

Failures remain advisory until a later slice explicitly approves enforcement.
