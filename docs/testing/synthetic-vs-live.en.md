# Synthetic, runtime and human acceptance

Source status: repository_source / static_contract_review; DG06, 2026-11-15.

Owner: verification owner + owner of the changed surface. Scope/version: repository `259977f3b257ba7fc0e932396f8963262bd327ad`; update when the evidence route changes. Sources: [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/TEST.md), [EVALS.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/EVALS.md), [behavioral evals](../product-agent-os/behavioral-evals.md), [frontend accessibility](../frontend/accessibility.md). Test links do not imply a new run.

| Evidence | Supported conclusion | Limit and next step |
| --- | --- | --- |
| Source/static inspection | What checked code and configuration declare at a stated revision | Alone it does not prove execution, host loading, current user settings or model output. |
| Unit/fixture/transcript | Assertions for specific inputs, synthetic workspace and harness | Does not prove real-project quality, model access, production readiness or correctness of the entire route. |
| Synthetic browser/native or local service | Observed interaction in the described fixture environment | State launcher, browser, profile, scenarios and limits; do not claim a real account or human acceptance. |
| Actual runtime/provider | Observed route and result in the stated environment and authorized scope | Requires selector, intended/prior path and fallback evidence for a relevant route change; it does not extend to other environments or future runs. |
| Human acceptance | What the owner/user actually checked and accepted | Does not replace technical negative checks, security review or release qualification. |

For each result retain date, revision and changed inputs, command/scenario, environment, test-data class, outcome, failures and limits. Bind evidence to unchanged inputs; when code, config, fixtures, dependencies, data or environment affect a result, select a rerun under TEST. `not_run`, `blocked`, `failed` and `not_available` are different states. Missing cases and unknown metrics do not become zero or success.

## Historical and unstable results

[DG01](../planning/documentation-architecture-2026-11-15.md#dg01-results) retained the date and original migration failures: archive assertions for missing EN siblings and a historical PostToolUse assertion; site checks for EN/search parity and strict build had initial failures. DG01 later corrected sources and test expectations with justification and recorded a retest. Do not call an early failure current or a historical retest a new DG06 run. Changing hook trust was not the way to close it.

[DG02](../planning/documentation-architecture-2026-11-15.md#dg02-results) recorded crashes in initial Chrome/Edge render attempts in the sandbox and a later bounded successful render in another run. This does not establish deterministic behavior across browsers. Retain both receipts and conditions; for a recurring or suspected flaky result state frequency/conditions, owner and the next reproducible step. Do not rename an unknown cause as flaky or delete a failure to obtain a green result. If a path is unavailable or authority is missing, record blocked and its effect on acceptance.

Manual screen-reader scenarios and full WCAG evaluation are not established in the [frontend guide](../frontend/accessibility.md); V3 visual evidence is `needs_user_acceptance`. Passing synthetic browser tests do not close those gaps. Release and production claims need separate qualification and owner decisions.
