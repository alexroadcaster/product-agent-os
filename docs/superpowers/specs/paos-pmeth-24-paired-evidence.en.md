# PMETH-24. Paired evaluation of methodological advice

Source status: local protocol and direct Codex CLI telemetry.

## Protocol registered before inference

The initial protocol was registered on November 19, 2026, at 12:07:38 UTC
on revision `2939c996786b74041d23b020e1160e3ae11dca49`, SHA-256
`8986ecae1a4d3eae4c5109ced08fc8b4e66f9966ac3e70d07f4d083204ad9c8c`.
It binds the Codex binary, response schema, measurement code, advice and
fixture files by SHA-256. See the [Russian report](paos-pmeth-24-paired-evidence.md)
for the original scenario table and run order.

The four synthetic cases form two backend bug pairs (`counter-bug` and
`bound-bug`) and two docs-only pairs (`counter-docs` and `cache-docs`). Each
pair uses the same fixture, request, tool boundaries, model `gpt-6.1-sol`
and `medium` reasoning effort. Each run uses a fresh ephemeral CLI session.
Only the advised arm receives the actual Product-Agent OS recommendation.

The metrics are correct first choice, exact verified outcome, time to the
decisive check, end-to-end wall time, extra actions, and input, cached input,
output and reasoning token usage. Cost in currency requires an actual charge.
A profile needs two eligible pairs with preserved bytes and no policy breaches.
Benefit requires quality preserved or improved in both pairs, with each pair
showing better quality, at least one fewer extra action, or at least 20% less
time to the decisive check. If neither pair qualifies, the verdict is
`no_benefit` for these fixtures. Other cases are `insufficient_evidence`.

## Protocol amendment

All eight sessions in the first series finished with zero MCP calls. A
credential-free loopback reproduction observed MCP `initialize` and
`tools/list` followed by an empty model request `tools` array. The series was
excluded from the comparison. Its receipt SHA-256 is
`c6c15affb655a91f1c2ba0d8ea871c24de926f37b96f2d41c9107f996214ec18`.

The amendment was registered before the second series at 12:15:55 UTC,
SHA-256 `3716c6adb2ba3801278ac8a7c1d24c4bd8d9100545bb81b87ad77ea22f907a68`.
It preserves the cases, fixture bytes, model, reasoning effort, run order,
advice and decision thresholds. Both arms receive the same synthetic files
inline. Codex selects one check and reports a predicted result. An independent
local verifier executes the selected named unittest or compares the selected
source with the guide. Before inference, it confirmed four expected outcomes,
rejected unknown targets and confirmed that both distractor tests pass.

Time to the decisive check includes CLI completion and local verification.
The amended protocol can count an unnecessary selected check. It cannot measure
autonomous tool use, search effort or agent iterations.

## Results

All eight scored runs completed on Codex CLI `0.170.0` with `gpt-6.1-sol`
and `medium` reasoning effort. Each arm chose the right first check in 4/4
cases, produced an independently verified outcome in 4/4 cases, and picked
zero extra checks. Each arm reproduced two RED outcomes and identified two
documentation mismatches. There were no cancellations, timeouts, owner
interventions, or changes to fixture bytes in the scored series.

| Case | Observed / expected | Baseline, s | Advised, s | Time change | Including advice generation |
| --- | --- | ---: | ---: | ---: | ---: |
| `counter-bug` | RED, 5 / 4 | 6.315 | 6.626 | +4.9% | +9.8% |
| `bound-bug` | RED, 2 / 3 | 7.356 | 5.367 | −27.0% | −23.0% |
| `counter-docs` | `guide.md` / `counter.py`, 5 / 4 | 6.007 | 6.192 | +3.1% | +8.1% |
| `cache-docs` | `manual.md` / `cache.py`, 45 / 60 | 6.164 | 6.022 | −2.3% | +2.6% |

- **Backend bug — `insufficient_evidence`.** The boundary test reached the
  check 27.0% sooner, or 23.0% sooner after adding advice generation. The
  counter took 4.9% longer, or 9.8% longer with advice generation. One of the
  two pairs met the threshold.
- **Docs-only — `no_benefit` on the measured cases.** The pairs had identical
  quality and action counts. Neither pair met the timing threshold.

| Scored series | Input tokens | Cached input subset | Output tokens | Reasoning subset |
| --- | ---: | ---: | ---: | ---: |
| Baseline | 46,018 | 0 | 217 | 46 |
| Advised | 46,125 | 7,296 | 223 | 52 |

The advised arm used 107 more input tokens and 6 more output tokens. The
observed cache hit came from one advised run. This sample cannot attribute
the cache effect to the advice. Generating advice locally took 0.299–0.305 s
per scenario without a model call. The eight scored run durations sum to
50.048 s. Actual currency cost is unavailable for the ChatGPT sessions.
The excluded series separately used 288,845 input tokens (181,632 cached)
and 1,382 output tokens (194 reasoning).

## Evidence and limitations

There was one run per arm and two cases per profile. The trial cannot isolate
the effect of advice on duration from provider latency, caching and run
order. Autonomous tool selection in a workspace, repair effort, reopens,
post-fix defects, real owner acceptance and the other B3/B4 profiles are
outside the measured sample. The treatment is actual Product-Agent OS CLI
advice added to the prompt. The experiment did not measure automatic
application of the advice in Web or fresh-session skill activation.

The owner authorized the bounded synthetic experiment. Delivery remains on
[`hold`](paos-pmeth-b2-evidence.en.md#rollout-decision) and the broader
usefulness verdict remains `insufficient_evidence`.

The [machine-readable receipt](paos-pmeth-24-paired-receipts.json) preserves
both protocols and both series, including per-run metrics and observations.
The scored receipt SHA-256 is
`312a329bb842f2f54203ab97b788adbf4f22e91315760256489f3f2c9e6927e2`.
Executed commands are listed in the [Russian report](paos-pmeth-24-paired-evidence.md).
