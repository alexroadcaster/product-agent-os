# Supply Chain Review

Source status: `codex-plugin-template`

Use this for dependencies, packages, containers, plugins, CI actions and release artifacts.

## Scope

- Change:
- Owner:
- Security/release reviewer:
- Artifact type: internal app / package / plugin / container / release artifact
- Current Evidence:
- Accepted Gap:
- Residual Risk:

## Review

- Dependencies:
- Existing standard library/framework option:
- Existing current dependency option:
- Project helper or tooling option:
- New dependency requested:
- `negative_dependency_rule`:
- Rejected no-new-dependency alternatives:
- Licenses:
- Vulnerabilities:
- Update path:
- Runtime/build impact:
- Rollback/removal path:
- SBOM status:
- Provenance status:
- CI action pinning:
- Build integrity:
- Release signing:
- Artifact storage:
- Verification command:
- Remediation owner:

SBOM alone is not supply-chain closure. Link to `sbom-manifest.md`, `ci-permissions-review.md`, `vulnerability-response-record.md` and release evidence where applicable.

Do not add a dependency until standard library, framework/platform, current dependency, project helper and small-adapter options are recorded as insufficient.

Do not include raw secrets, credentials, access tokens, private keys, payment data, raw PII, raw private chats or private customer data.
