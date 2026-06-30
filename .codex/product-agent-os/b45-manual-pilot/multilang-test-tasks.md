# Multilanguage Task Test Sets

Source status: internet-sourced local test artifact.

Task id: `B45-MULTILANG-TASK-TEST-SETS-A01`.

Created at: 2026-06-30T00:50:00+03:00.

## Scope And Boundary

Goal: collect 5-10 public programming tasks across C++, Rust, Python and JavaScript, record compact test sets, and run local tests where the language runtime/toolchain is available.

Sources: Exercism `problem-specifications`, which documents `canonical-data.json` as standardized test inputs/outputs for exercises and is MIT licensed.

Execution boundary:

- Python runtime: available, `Python 3.13.5`.
- JavaScript runtime: available, `Node.js v22.18.0`.
- C++ compiler: blocked, `g++`, `clang++` and `cl` are not available in PATH.
- Rust compiler: blocked, `rustc`, `cargo` and `rustup` are not available in PATH.
- No compiler/toolchain installation, external online compiler execution, provider/model/API call, browser automation, live server, git action or external write was performed.

## Source Links

- Exercism problem specifications README: https://raw.githubusercontent.com/exercism/problem-specifications/main/README.md
- Exercism problem specifications license: https://raw.githubusercontent.com/exercism/problem-specifications/main/LICENSE
- Leap canonical data: https://raw.githubusercontent.com/exercism/problem-specifications/main/exercises/leap/canonical-data.json
- Grains canonical data: https://raw.githubusercontent.com/exercism/problem-specifications/main/exercises/grains/canonical-data.json
- Luhn canonical data: https://raw.githubusercontent.com/exercism/problem-specifications/main/exercises/luhn/canonical-data.json
- Hamming canonical data: https://raw.githubusercontent.com/exercism/problem-specifications/main/exercises/hamming/canonical-data.json
- Raindrops canonical data: https://raw.githubusercontent.com/exercism/problem-specifications/main/exercises/raindrops/canonical-data.json
- Isogram canonical data: https://raw.githubusercontent.com/exercism/problem-specifications/main/exercises/isogram/canonical-data.json
- Pangram canonical data: https://raw.githubusercontent.com/exercism/problem-specifications/main/exercises/pangram/canonical-data.json
- Bob canonical data: https://raw.githubusercontent.com/exercism/problem-specifications/main/exercises/bob/canonical-data.json

## Task Matrix

| ID | Language | Task | Property | Local execution status |
| --- | --- | --- | --- | --- |
| ML-CPP-01 | C++ | Leap | `leapYear(year) -> bool` | `blocked_missing_local_cpp_compiler` |
| ML-CPP-02 | C++ | Grains | `square(n) -> integer`, `total() -> integer` | `blocked_missing_local_cpp_compiler` |
| ML-RS-01 | Rust | Luhn | `valid(value) -> bool` | `blocked_missing_local_rust_compiler` |
| ML-RS-02 | Rust | Hamming | `distance(strand1, strand2) -> integer/error` | `blocked_missing_local_rust_compiler` |
| ML-PY-01 | Python | Raindrops | `convert(number) -> string` | `passed_local_runtime_python_3_13_5` |
| ML-PY-02 | Python | Isogram | `is_isogram(phrase) -> bool` | `passed_local_runtime_python_3_13_5` |
| ML-JS-01 | JavaScript | Pangram | `isPangram(sentence) -> boolean` | `passed_local_runtime_node_22_18_0` |
| ML-JS-02 | JavaScript | Bob | `response(heyBob) -> string` | `passed_local_runtime_node_22_18_0` |

## Result Marking Rubric

Use this section to mark each test set with an explicit proof level.

| Status | Meaning | Batch 45 interpretation |
| --- | --- | --- |
| `passed_target_runtime` | The selected cases ran in the intended language runtime/toolchain in the current run. | Usable as local runtime evidence for that language slice. |
| `fixture_self_checked_reference_only` | Expected values were checked by a small reference runner in an available runtime, but not in the intended target language. | Useful to validate fixture consistency, not a target-language proof. |
| `blocked_missing_local_toolchain` | The test set is collected, but no approved local compiler/toolchain is available. | Record as a gap; do not claim language runtime coverage. |
| `baseline_smoke` | Small kata-style cases that exercise simple logic and edge cases. | Good for smoke, weak for enterprise reviewer usefulness. |
| `enterprise_v2` | Production-like cases covering state, retries, legacy constraints, observability, invalid input or failure modes. | Better signal for checklist false positives, reviewer usefulness and advisory-vs-blocker decisions. |

Current assessment:

- Baseline multilanguage set: `baseline_smoke`; useful for source/test plumbing and flake check.
- Enterprise V2 set: `enterprise_v2`; better suited for Batch 45 because it adds stateful behavior, legacy/refactoring constraints, error handling and operational semantics.
- Runtime gap: C++ and Rust remain `blocked_missing_local_toolchain`; their V2 fixtures have only `fixture_self_checked_reference_only` evidence until a local compiler/toolchain or approved external runner exists.

## Selected Test Sets

### ML-CPP-01: Leap

Compact goal: detect Gregorian leap-year edge cases.

| Case | Input | Expected |
| --- | --- | --- |
| common year | `2015` | `false` |
| divisible by 4 not 100 | `1996` | `true` |
| divisible by 100 not 400 | `2100` | `false` |
| divisible by 400 | `2000` | `true` |
| divisible by 200 not 400 | `1800` | `false` |

Result: `blocked_missing_local_cpp_compiler`.

### ML-CPP-02: Grains

Compact goal: test powers of two, 64-bit boundary and invalid square range.

| Case | Input | Expected |
| --- | --- | --- |
| square 1 | `square=1` | `1` |
| square 16 | `square=16` | `32768` |
| square 32 | `square=32` | `2147483648` |
| square 64 | `square=64` | `9223372036854775808` |
| total | `total()` | `18446744073709551615` |
| invalid low | `square=0` | error |
| invalid high | `square=65` | error |

Result: `blocked_missing_local_cpp_compiler`.

### ML-RS-01: Luhn

Compact goal: validate digit processing, whitespace tolerance and non-digit rejection.

| Case | Input | Expected |
| --- | --- | --- |
| single digit | `"1"` | `false` |
| simple valid | `"059"` | `true` |
| Canadian SIN valid | `"055 444 285"` | `true` |
| Canadian SIN invalid | `"055 444 286"` | `false` |
| invalid card | `"8273 1232 7352 0569"` | `false` |
| punctuation invalid | `"055-444-285"` | `false` |
| many zeros | `"0000 0"` | `true` |
| long valid | `"9999999999 9999999999 9999999999 9999999999"` | `true` |

Result: `blocked_missing_local_rust_compiler`.

### ML-RS-02: Hamming

Compact goal: compare equal-length DNA strings and reject unequal lengths.

| Case | Input | Expected |
| --- | --- | --- |
| empty strands | `("", "")` | `0` |
| identical single | `("A", "A")` | `0` |
| different single | `("G", "T")` | `1` |
| long identical | `("GGACTGAAATCTG", "GGACTGAAATCTG")` | `0` |
| long different | `("GGACGGATTCTG", "AGGACGGATTCT")` | `9` |
| unequal first longer | `("AATG", "AAA")` | error |
| unequal second longer | `("ATA", "AGTG")` | error |

Result: `blocked_missing_local_rust_compiler`.

### ML-PY-01: Raindrops

Compact goal: factor-based string generation for 3, 5 and 7.

| Case | Input | Expected |
| --- | --- | --- |
| no factor | `1` | `"1"` |
| factor 3 | `3` | `"Pling"` |
| factor 5 | `5` | `"Plang"` |
| factor 7 | `7` | `"Plong"` |
| factors 3 and 5 | `15` | `"PlingPlang"` |
| factors 3 and 7 | `21` | `"PlingPlong"` |
| factors 5 and 7 | `35` | `"PlangPlong"` |
| factors 3, 5 and 7 | `105` | `"PlingPlangPlong"` |
| large factor 5 | `3125` | `"Plang"` |

Result: `passed_local_runtime_python_3_13_5`, 9/9 selected cases passed.

### ML-PY-02: Isogram

Compact goal: ignore spaces/hyphens and detect duplicate letters case-insensitively.

| Case | Input | Expected |
| --- | --- | --- |
| empty string | `""` | `true` |
| lower-case isogram | `"isogram"` | `true` |
| duplicate | `"eleven"` | `false` |
| mixed-case duplicate | `"Alphabet"` | `false` |
| hyphen isogram | `"thumbscrew-japingly"` | `true` |
| duplicated hyphen only | `"six-year-old"` | `true` |
| duplicated letter with hyphens | `"up-to-date"` | `false` |

Result: `passed_local_runtime_python_3_13_5`, 7/7 selected cases passed.

### ML-JS-01: Pangram

Compact goal: detect full alphabet coverage while ignoring case, punctuation, numbers and separators.

| Case | Input | Expected |
| --- | --- | --- |
| empty | `""` | `false` |
| alphabet | `"abcdefghijklmnopqrstuvwxyz"` | `true` |
| quick fox | `"the quick brown fox jumps over the lazy dog"` | `true` |
| missing x | `"a quick movement of the enemy will jeopardize five gunboats"` | `false` |
| underscores | `"the_quick_brown_fox_jumps_over_the_lazy_dog"` | `true` |
| numbers | `"the 1 quick brown fox jumps over the 2 lazy dogs"` | `true` |
| substituted digits | `"7h3 qu1ck brown fox jumps ov3r 7h3 lazy dog"` | `false` |
| mixed punctuation | `"\"Five quacking Zephyrs jolt my wax bed.\""` | `true` |
| a-m plus A-M | `"abcdefghijklm ABCDEFGHIJKLM"` | `false` |

Result: `passed_local_runtime_node_22_18_0`, 9/9 selected cases passed.

### ML-JS-02: Bob

Compact goal: conversational branch coverage for question, shouting, forceful question, silence and statements.

| Case | Input | Expected |
| --- | --- | --- |
| question | `"Does this cryogenic chamber make me look fat?"` | `"Sure."` |
| shouting | `"WATCH OUT!"` | `"Whoa, chill out!"` |
| forceful question | `"WHAT'S GOING ON?"` | `"Calm down, I know what I'm doing!"` |
| silence | `""` | `"Fine. Be that way!"` |
| statement | `"Tom-ay-to, tom-aaaah-to."` | `"Whatever."` |
| shouting numbers | `"1, 2, 3 GO!"` | `"Whoa, chill out!"` |
| statement with question mark | `"Ending with ? means a question."` | `"Whatever."` |

Result: `passed_local_runtime_node_22_18_0`, 7/7 selected cases passed.

## Enterprise V2 Source Links

These sources were used as task inspiration and requirements anchors. The local fixtures below are compact, synthetic test sets derived from the public task/pattern descriptions; they do not copy full source bodies.

- AWS Builders Library, safe retries and idempotent APIs: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
- Gilded Rose Refactoring Kata requirements: https://github.com/emilybache/GildedRose-Refactoring-Kata/blob/main/GildedRoseRequirements.md
- CodeKata 09, checkout pricing: https://codekata.com/kata/kata09-back-to-the-checkout/
- Coding Dojo Bank OCR kata: https://codingdojo.org/kata/BankOCR/
- Martin Fowler, Circuit Breaker pattern: https://martinfowler.com/bliki/CircuitBreaker.html
- Microservices.io, Idempotent Consumer pattern: https://microservices.io/patterns/communication-style/idempotent-consumer.html
- OpenTelemetry feature flag semantic conventions: https://opentelemetry.io/docs/specs/semconv/feature-flags/
- OpenFeature evaluation context: https://openfeature.dev/docs/reference/concepts/evaluation-context/
- LRU cache with TTL design prompt reference: https://lldhub.in/problem/cache-system

## Enterprise V2 Task Matrix

| ID | Language | Task | Production signal | Result mark |
| --- | --- | --- | --- | --- |
| ENT-PY-01 | Python | Idempotency ledger for payment API retries | API safety, replay semantics, conflict handling, TTL | `passed_target_runtime_python_3_13_5`, 7/7 |
| ENT-PY-02 | Python | Gilded Rose legacy/refactoring regression | legacy constraints, mutation rules, regression preservation | `passed_target_runtime_python_3_13_5`, 10/10 |
| ENT-JS-01 | JavaScript | Feature flag evaluator with audit event | targeting precedence, percentage rollout, observability | `passed_target_runtime_node_22_18_0`, 7/7 |
| ENT-JS-02 | JavaScript | Checkout pricing engine | enterprise pricing rules, invalid input, weighted quantities | `passed_target_runtime_node_22_18_0`, 11/11 |
| ENT-CPP-01 | C++ | LRU cache with TTL | cache correctness, eviction order, expiry semantics | `fixture_self_checked_reference_only`, 9/9; `blocked_missing_local_cpp_compiler` |
| ENT-CPP-02 | C++ | Bank OCR legacy batch parser | fixed-width legacy input, checksum, illegal glyphs | `fixture_self_checked_reference_only`, 4/4; `blocked_missing_local_cpp_compiler` |
| ENT-RS-01 | Rust | Circuit breaker state machine | resilience state transitions, cooldown, half-open recovery | `fixture_self_checked_reference_only`, 7/7; `blocked_missing_local_rust_compiler` |
| ENT-RS-02 | Rust | Idempotent event consumer | duplicate delivery, sequence gaps, stale events | `fixture_self_checked_reference_only`, 6/6; `blocked_missing_local_rust_compiler` |

Dedicated legacy/refactoring entries:

- `ENT-PY-02`: direct legacy-refactoring regression surface.
- `ENT-CPP-02`: legacy fixed-width batch import/parsing surface.

### ENT-PY-01: Idempotency Ledger

Production goal: protect mutating payment API retries from duplicate side effects.

| Case | Input | Expected |
| --- | --- | --- |
| first request | `POST /payments`, key `k1`, amount `100`, time `0` | `201`, `payment_id=pay-001`, `replayed=false` |
| exact replay | same request, key `k1`, time `10` | cached `201`, `payment_id=pay-001`, `replayed=true` |
| same key, different body | key `k1`, amount `101`, time `20` | `409 idempotency_conflict` |
| same key, different path | `POST /refunds`, key `k1`, time `30` | `409 key_scope_conflict` |
| missing key | `POST /payments`, no key, time `40` | `400 missing_idempotency_key` |
| TTL expired | original request, key `k1`, time `90000` | new `201`, `payment_id=pay-002` |
| read-only request | `GET /payments/pay-001`, no key | `200`, no idempotency cache mutation |

Result: `passed_target_runtime_python_3_13_5`, 7/7 selected cases passed.

### ENT-PY-02: Gilded Rose Legacy Regression

Production goal: preserve legacy item update behavior while making refactoring safe.

| Case | Input | Expected after one update |
| --- | --- | --- |
| normal item | `+5 Dexterity Vest`, sell_in `10`, quality `20` | sell_in `9`, quality `19` |
| aged brie | `Aged Brie`, sell_in `2`, quality `0` | sell_in `1`, quality `1` |
| normal item second sample | `Elixir of the Mongoose`, sell_in `5`, quality `7` | sell_in `4`, quality `6` |
| legendary item | `Sulfuras, Hand of Ragnaros`, sell_in `0`, quality `80` | unchanged |
| backstage above 10 days | sell_in `15`, quality `20` | sell_in `14`, quality `21` |
| backstage at 10 days | sell_in `10`, quality `49` | sell_in `9`, quality `50` |
| backstage at 5 days | sell_in `5`, quality `49` | sell_in `4`, quality `50` |
| backstage after concert | sell_in `0`, quality `10` | sell_in `-1`, quality `0` |
| conjured before sell date | `Conjured Mana Cake`, sell_in `3`, quality `6` | sell_in `2`, quality `4` |
| conjured after sell date | `Conjured Mana Cake`, sell_in `0`, quality `6` | sell_in `-1`, quality `2` |

Result: `passed_target_runtime_python_3_13_5`, 10/10 selected cases passed.

### ENT-JS-01: Feature Flag Evaluator

Production goal: evaluate flags predictably and emit enough evaluation metadata for debugging rollout impact.

| Case | Input | Expected |
| --- | --- | --- |
| disabled flag | enabled `false`, allowlisted user | value `false`, reason `disabled`, event flag key present |
| missing context | no user context | value `false`, reason `default`, event flag key present |
| tenant allowlist | tenant `enterprise-a`, country `US` | value `true`, reason `targeting_match` |
| country deny rule | tenant `standard`, country `DE` | value `false`, reason `targeting_match` |
| percentage included | user `u0`, 50 percent rollout | value `true`, reason `split` |
| percentage excluded | user `zzzzzzzz`, 50 percent rollout | value `false`, reason `fallthrough` |
| precedence check | tenant allowlist and denied country | tenant rule wins, value `true` |

Result: `passed_target_runtime_node_22_18_0`, 7/7 selected cases passed.

### ENT-JS-02: Checkout Pricing Engine

Production goal: support retail pricing rules, weighted quantities and invalid input handling.

| Case | Input | Expected |
| --- | --- | --- |
| empty basket | `[]` | `0` |
| unit price | `A x1` | `50` |
| bulk special | `A x3` | `130` |
| bulk plus unit | `A x4` | `180` |
| mixed order | `B x2`, `A x3`, `D x1` | `190` |
| buy two get one free | `F x3` | `20` |
| buy two get one free remainder | `F x5` | `40` |
| weighted item | `APPLES_KG x1.25`, `199` cents/kg | `249` |
| unknown SKU | `Z x1` | error |
| zero quantity | `A x0` | error |
| fractional unit SKU | `A x1.5` | error |

Result: `passed_target_runtime_node_22_18_0`, 11/11 selected cases passed.

### ENT-CPP-01: LRU Cache With TTL

Production goal: verify eviction and expiry semantics before adding concurrency or storage concerns.

| Case | Operation | Expected |
| --- | --- | --- |
| insert A | `put(A,1,t=0)` | ok |
| insert B | `put(B,2,t=1)` | ok |
| touch A | `get(A,t=2)` | hit `1` |
| capacity eviction | `put(C,3,t=3)` | evict `B` |
| evicted read | `get(B,t=4)` | miss `not_found` |
| retained read | `get(A,t=5)` | hit `1` |
| TTL expiry | `get(C,t=14)` | miss `expired` |
| insert D | `put(D,4,t=15)` | ok |
| old A expiry | `get(A,t=16)` | miss `expired` |

Result: `fixture_self_checked_reference_only`, 9/9 selected cases passed by Python reference runner; target C++ execution is `blocked_missing_local_cpp_compiler`.

### ENT-CPP-02: Bank OCR Legacy Batch Parser

Production goal: parse fixed-width legacy OCR input and preserve explicit error classification.

| Case | Input | Expected |
| --- | --- | --- |
| all zeros | OCR rows for `000000000` | `000000000` |
| valid account | OCR rows for `123456789` | `123456789` |
| invalid checksum | OCR rows for `111111111` | `111111111 ERR` |
| illegal glyph | one unreadable glyph in `123456789` | `1?3456789 ILL` |

Result: `fixture_self_checked_reference_only`, 4/4 selected cases passed by Python reference runner; target C++ execution is `blocked_missing_local_cpp_compiler`.

### ENT-RS-01: Circuit Breaker State Machine

Production goal: prevent cascading failures around remote calls by modeling closed/open/half-open transitions.

| Case | Event | Expected |
| --- | --- | --- |
| initial call | `allow(t=0)` | allowed, `closed` |
| first failure | `record_failure(t=1)` | `closed`, failures `1` |
| second failure | `record_failure(t=2)` | `closed`, failures `2` |
| threshold failure | `record_failure(t=3)` | `open`, `open_until=33` |
| call while open | `allow(t=10)` | denied, retry after `23` |
| cooldown elapsed | `allow(t=33)` | allowed, `half_open` |
| recovery success | `record_success(t=34)` | `closed`, failures `0` |

Result: `fixture_self_checked_reference_only`, 7/7 selected cases passed by Python reference runner; target Rust execution is `blocked_missing_local_rust_compiler`.

### ENT-RS-02: Idempotent Event Consumer

Production goal: handle at-least-once message delivery without double-applying account mutations.

| Case | Event | Expected |
| --- | --- | --- |
| first event | `m1`, account `acct-1`, seq `1`, amount `100` | applied, balance `100` |
| duplicate delivery | same `m1` again | duplicate ignored, balance `100` |
| sequence gap | `m3`, seq `3`, amount `5` before seq `2` | gap detected, expected seq `2` |
| missing event arrives | `m2`, seq `2`, amount `-20` | applied, balance `80` |
| next event replayed after gap fixed | `m3`, seq `3`, amount `5` | applied, balance `85` |
| stale sequence | `m4`, seq `3`, amount `7` | stale sequence rejected, expected seq `4` |

Result: `fixture_self_checked_reference_only`, 6/6 selected cases passed by Python reference runner; target Rust execution is `blocked_missing_local_rust_compiler`.

## Execution Log

- 2026-06-30T00:50:00+03:00: Source selection recorded. Python and Node available. C++ and Rust execution blocked by missing local compilers.
- 2026-06-30T00:57:00+03:00: Python local inline runner passed `ML-PY-01` 9/9 and `ML-PY-02` 7/7 on `Python 3.13.5`.
- 2026-06-30T00:57:00+03:00: Node.js local inline runner passed `ML-JS-01` 9/9 and `ML-JS-02` 7/7 on `Node.js v22.18.0`.
- 2026-06-30T00:59:00+03:00: C++ and Rust execution remained blocked because no local `g++`, `clang++`, `cl`, `rustc`, `cargo` or `rustup` executable was available in PATH.
- 2026-06-30T01:10:00+03:00: `B45-ENTERPRISE-TEST-SETS-A02` started to add result marking and a production-like V2 suite.
- 2026-06-30T01:12:00+03:00: Python local inline runner passed `ENT-PY-01` 7/7 and `ENT-PY-02` 10/10 on `Python 3.13.5`.
- 2026-06-30T01:12:00+03:00: Node.js local inline runner passed `ENT-JS-01` 7/7 and `ENT-JS-02` 11/11 on `Node.js v22.18.0`.
- 2026-06-30T01:13:00+03:00: Python reference runner self-checked target-language-blocked fixtures: `ENT-CPP-01` 9/9, `ENT-CPP-02` 4/4, `ENT-RS-01` 7/7 and `ENT-RS-02` 6/6.
- 2026-06-30T01:13:00+03:00: Toolchain check confirmed `g++`, `clang++`, `cl`, `rustc`, `cargo` and `rustup` are still missing from PATH, so C++/Rust target runtime proof remains blocked.
- 2026-06-30T01:39:00+03:00: `B45-MULTILANG-V3-ENTERPRISE-OLYMPIAD-A03` started to add a serious collection-only Variant 3 with 10 enterprise/olympiad tasks.
- 2026-06-30T01:43:00+03:00: V3 matrix recorded 10 collected tasks: 5 enterprise and 5 olympiad. Execution remains `collected_not_executed`.

## Enterprise/Olympiad V3 Challenge Source Links

These sources were used as anchors for a harder collection-only test variant. The task briefs below summarize requirements and acceptance focus; they do not copy full problem statements or source bodies.

- AWS Builders Library, safe retries and idempotent APIs: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
- Microservices.io, Saga pattern: https://microservices.io/patterns/data/saga.html
- Microservices.io, Transactional outbox pattern: https://microservices.io/patterns/data/transactional-outbox.html
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP IDOR Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- OpenTelemetry semantic conventions: https://opentelemetry.io/docs/concepts/semantic-conventions/
- OpenFeature evaluation context: https://openfeature.dev/docs/reference/concepts/evaluation-context/
- PostgreSQL partial indexes: https://www.postgresql.org/docs/current/sql-createindex.html
- CSES Download Speed: https://cses.fi/problemset/task/1694
- CSES Planets Queries II: https://cses.fi/problemset/task/1160/
- CSES Flight Routes: https://cses.fi/problemset/task/1196/
- CSES Polynomial Queries: https://cses.fi/problemset/task/1736
- CSES New Roads Queries: https://cses.fi/problemset/task/2101/

## Enterprise/Olympiad V3 Task Matrix

Variant id: `B45-MULTILANG-V3-ENTERPRISE-OLYMPIAD-A03`.

Purpose: stress Professional Code Authoring with serious production and algorithmic tasks before any advisory hook or blocker decision.

Execution status after `B45-MULTILANG-V3-TEST-RUN-A04`: Python and Node.js target-runtime tasks passed locally; C++ and Rust target-runtime proof remains blocked by missing local toolchains, so those tasks have reference-fixture proof only. No external judges, online compilers, C++/Rust toolchain installs, provider calls, browser automation, hooks, blockers or active automation were run.

| ID | Track | Language | Task | Hardness signal | Current status |
| --- | --- | --- | --- | --- | --- |
| V3-ENT-PY-01 | Enterprise | Python | Saga orchestration with compensation ledger | distributed transaction workflow, rollback ordering, idempotent steps | `passed_target_runtime_python_3_13_5`, 8/8 |
| V3-ENT-PY-02 | Enterprise | Python | Transactional outbox relay with retry and ordering | exactly-once illusion, relay crashes, duplicate publish protection | `passed_target_runtime_python_3_13_5`, 7/7 |
| V3-ENT-JS-01 | Enterprise | JavaScript/TypeScript | Resource authorization and IDOR-safe policy engine | object-level authorization, tenancy, deny-by-default | `passed_target_runtime_node_22_18_0`, 7/7 |
| V3-ENT-JS-02 | Enterprise | JavaScript/TypeScript | Audit-log redaction and semantic event mapper | privacy-safe observability, schema normalization, field redaction | `passed_target_runtime_node_22_18_0`, 6/6 |
| V3-ENT-RS-01 | Enterprise | Rust | Tenant-scoped query planner with partial-index hints | multitenant filtering, soft-delete safety, query-shape validation | `fixture_self_checked_reference_only`, 7/7; target runtime blocked without Rust toolchain |
| V3-OLY-CPP-01 | Olympiad | C++ | CSES Download Speed | max flow, residual graph correctness, high-capacity arithmetic | `fixture_self_checked_reference_only`, 5/5; target runtime blocked without C++ compiler |
| V3-OLY-CPP-02 | Olympiad | C++ | CSES Planets Queries II | functional graph decomposition, binary lifting, cycle/tree cases | `fixture_self_checked_reference_only`, 6/6; target runtime blocked without C++ compiler |
| V3-OLY-RS-01 | Olympiad | Rust | CSES Flight Routes | k-shortest paths, repeated nodes, duplicate route costs | `fixture_self_checked_reference_only`, 4/4 after fixture fix; target runtime blocked without Rust toolchain |
| V3-OLY-RS-02 | Olympiad | Rust | CSES Polynomial Queries | lazy segment tree with arithmetic progression updates | `fixture_self_checked_reference_only`, 5/5; target runtime blocked without Rust toolchain |
| V3-OLY-CPP-03 | Olympiad | C++ | CSES New Roads Queries | offline connectivity time, DSU merge tree/LCA style reasoning | `fixture_self_checked_reference_only`, 3/3; target runtime blocked without C++ compiler |

### V3-ENT-PY-01: Saga Orchestration With Compensation Ledger

Source anchors: Microservices.io Saga pattern; AWS idempotent API guidance.

Build a saga coordinator for an order workflow: reserve inventory, authorize payment, create shipment and emit order-confirmed event. Each step is a local transaction with an idempotency key. If a step fails after earlier successes, compensating transactions must run in reverse dependency order.

Acceptance focus:

- A fully successful saga returns `confirmed`, persists step states and emits one confirmation.
- A payment decline after inventory reservation triggers inventory release and no shipment.
- A shipment failure after payment authorization triggers payment void, inventory release and a failed saga state.
- Retrying the same saga id must not duplicate local step side effects or events.
- A compensation failure must leave the saga in `compensation_failed` with a resumable ledger.
- Reviewer focus: state machine clarity, idempotent boundary, explicit failure taxonomy, no hidden side effects.

Suggested hidden/stress cases:

- Duplicate delivery of `payment_authorized`.
- Out-of-order step callback after the saga is already failed.
- Compensation resume after process restart.
- Conflict where the same saga id is reused with a different order body.

### V3-ENT-PY-02: Transactional Outbox Relay With Retry And Ordering

Source anchor: Microservices.io Transactional outbox pattern.

Build a local outbox relay that reads committed outbox rows, publishes events in aggregate order and marks rows as sent only after publisher acknowledgement. The relay must tolerate crashes between publish and mark-sent by preserving deduplication metadata.

Acceptance focus:

- Rows for the same aggregate are published in commit order.
- Relay crash before acknowledgement leaves the row pending.
- Relay crash after publish but before mark-sent may retry, but emits the same event id for consumer dedupe.
- Poison messages move to `dead_letter` after a bounded retry count.
- Independent aggregates may publish concurrently without per-aggregate reordering.
- Reviewer focus: transactional boundary, retry budget, observability counters, dead-letter behavior.

Suggested hidden/stress cases:

- Two relay workers racing on the same pending row.
- Backoff schedule after transient broker failure.
- Replaying an already sent row after database restore.
- Large batch with one poison row in the middle.

### V3-ENT-JS-01: Resource Authorization And IDOR-Safe Policy Engine

Source anchors: OWASP Authorization Cheat Sheet; OWASP IDOR Prevention Cheat Sheet.

Build a policy evaluator for resource access requests. Inputs include actor, tenant, role, resource owner, resource tenant, action and resource sensitivity. The evaluator must decide allow/deny and return a short explanation code suitable for audit logs.

Acceptance focus:

- Deny by default when no policy matches.
- Tenant mismatch is denied even if a guessed resource id exists.
- Owner can read own low-sensitivity resource, but cannot admin it.
- Support agent can read tenant resources only with active support session.
- Admin cannot cross tenant boundaries without explicit break-glass grant.
- Break-glass grant requires reason, expiry and audit event.
- Reviewer focus: no auth-by-obscurity, policy order is explicit, audit reason has no PII.

Suggested hidden/stress cases:

- Resource id exists but belongs to another tenant.
- Expired break-glass grant.
- Role name casing or unknown role.
- Bulk export action with mixed-resource tenants.

### V3-ENT-JS-02: Audit-Log Redaction And Semantic Event Mapper

Source anchors: OWASP Logging Cheat Sheet; OpenTelemetry semantic conventions.

Build an audit event normalizer that accepts application events, redacts sensitive fields and maps the remaining data to a stable semantic schema. It must preserve useful debugging metadata while refusing raw credentials, tokens, emails and raw request bodies.

Acceptance focus:

- `password`, `token`, `authorization`, `cookie` and raw body fields are replaced with redaction markers.
- Email-like values are tokenized or redacted according to policy.
- Event severity and category are normalized to allowed values.
- Trace/span correlation ids are preserved when syntactically valid.
- Invalid events are rejected with bounded error output, not logged verbatim.
- Reviewer focus: privacy boundary, schema compatibility, no secret leakage in errors.

Suggested hidden/stress cases:

- Deeply nested sensitive keys.
- Arrays with mixed public/private values.
- Unicode homoglyphs in sensitive key names.
- Oversized event body.

### V3-ENT-RS-01: Tenant-Scoped Query Planner With Partial-Index Hints

Source anchor: PostgreSQL `CREATE INDEX` partial-index behavior.

Build a query planner helper for a multitenant document repository. It receives filters such as tenant, status, soft-delete flag, created range and sort order. It must produce a safe query plan descriptor and optional partial-index hint only when tenant and soft-delete predicates are present.

Acceptance focus:

- Every read plan includes a tenant predicate.
- Active-document queries include `deleted_at IS NULL`.
- Partial-index hint is allowed only when the query predicate implies the index predicate.
- Cross-tenant admin search requires explicit admin scope and records a high-risk audit marker.
- Unknown filters are rejected rather than ignored.
- Reviewer focus: query safety, index hint correctness, soft-delete leakage prevention.

Suggested hidden/stress cases:

- Query with tenant omitted but resource ids supplied.
- Query with `deleted_at` filter inverted.
- Admin query with missing audit reason.
- Filter that looks like SQL injection in a string value.

### V3-OLY-CPP-01: CSES Download Speed

Source: CSES task 1694.

Implement maximum flow from source computer `1` to sink computer `n` in a directed capacity network.

Acceptance focus:

- Handles parallel edges by combining or preserving residual capacities correctly.
- Uses 64-bit capacity arithmetic.
- Produces zero flow when sink is unreachable.
- Handles bottleneck cut smaller than any single outgoing source edge.
- Reviewer focus: residual graph correctness, overflow safety, time complexity.

Suggested hidden/stress cases:

- Multiple parallel edges between the same ordered pair.
- Reverse residual edge needed to find the optimal flow.
- Very high capacities close to 32-bit overflow.
- Disconnected sink.

### V3-OLY-CPP-02: CSES Planets Queries II

Source: CSES task 1160.

Answer reachability-distance queries in a functional graph where every node has exactly one outgoing edge.

Acceptance focus:

- Distinguishes tree-to-cycle, same-cycle and unreachable cases.
- Returns minimum teleportation count, not merely reachability.
- Handles self-loops as one-node cycles.
- Preprocesses for large `n` and `q` without per-query traversal.
- Reviewer focus: component decomposition, binary lifting, cycle position math.

Suggested hidden/stress cases:

- Query from cycle node to attached tree node.
- Query within the same tree branch.
- Two nodes in different components.
- Self-loop component with long incoming chain.

### V3-OLY-RS-01: CSES Flight Routes

Source: CSES task 1196.

Find the `k` shortest route prices from city `1` to city `n`; routes may revisit cities and equal-cost routes count separately.

Acceptance focus:

- Maintains up to `k` distances per node.
- Allows repeated nodes/routes when they form valid path variants.
- Does not collapse equal-cost routes incorrectly.
- Handles large edge weights with 64-bit totals.
- Reviewer focus: priority queue invariant, duplicate path accounting, memory bounds.

Suggested hidden/stress cases:

- Multiple equal-cost direct routes.
- Short cycle creates several valid route variants.
- Node receives more than `k` candidate distances.
- Destination is reached before all `k` answers are known.

### V3-OLY-RS-02: CSES Polynomial Queries

Source: CSES task 1736.

Maintain an array with range updates that add `1,2,3,...` across a selected interval, and range-sum queries.

Acceptance focus:

- Lazy propagation stores enough data to compose arithmetic-progression updates.
- Overlapping updates with different starts produce correct sums.
- Query over a strict subrange of an updated range adjusts the arithmetic offset.
- Uses 64-bit sums.
- Reviewer focus: lazy tag composition, segment offset math, off-by-one safety.

Suggested hidden/stress cases:

- Update `[1,n]`, query `[n,n]`.
- Update `[l,r]`, then nested update `[l+1,r-1]`.
- Many adjacent single-point updates.
- Alternating updates and full-range sums.

### V3-OLY-CPP-03: CSES New Roads Queries

Source: CSES task 2101.

Given roads added by day, answer when two cities first become connected.

Acceptance focus:

- Reports `-1` for pairs that never become connected.
- Reports day `0` for identical city query if accepted by the chosen contract.
- Handles repeated roads without corrupting merge history.
- Supports many offline queries without binary searching each query over all days.
- Reviewer focus: DSU merge tree or parallel binary-search design, repeated edge handling, LCA/time semantics.

Suggested hidden/stress cases:

- Duplicate road between already connected components.
- Query whose answer is the final day.
- Two components that never connect.
- Star-like merge tree and chain-like merge tree.

## Enterprise/Olympiad V3 Result Marking

| Mark | Meaning |
| --- | --- |
| `collected_not_executed` | Task brief, source, acceptance focus and hidden/stress ideas are recorded, but no target implementation/tests were run. |
| `ready_for_reference_fixture` | Next step is to write compact fixtures plus a reference checker for small/medium cases. |
| `ready_for_target_runtime` | Next step is to implement in the named language and run local target runtime/toolchain tests. |
| `blocked_missing_toolchain` | Target-language proof is blocked until the local compiler/toolchain is approved/available. |

V3 assessment:

- Enterprise tasks: `ready_for_reference_fixture`; Python and Node.js runtimes are available for future local execution.
- Olympiad C++ tasks: `blocked_missing_toolchain` for target runtime, but can still get reference-fixture validation in Python first.
- Olympiad Rust tasks: `blocked_missing_toolchain` for target runtime, but can still get reference-fixture validation in Python first.
- Reviewer usefulness expectation: high, because the set mixes lifecycle/state-machine reasoning, privacy/security, query-safety, graph algorithms, flow, k-shortest paths and lazy data structures.

## Enterprise/Olympiad V3 Test Run A04 Results

Run id: `B45-MULTILANG-V3-TEST-RUN-A04`.

Runtime boundary:

- Python: `Python 3.13.5`.
- Node.js: `v22.18.0`.
- C++ target runtime: `blocked_missing_local_cpp_compiler`; `g++` and `clang++` were not found.
- Rust target runtime: `blocked_missing_local_rust_toolchain`; `rustc` and `cargo` were not found.

Intermediate result ledger:

| ID | Proof level | Cases | Status | Notes |
| --- | --- | --- | --- | --- |
| `V3-ENT-PY-01` | `passed_target_runtime_python_3_13_5` | 8/8 | `passed` | Saga success, retry replay, no duplicate confirmation, payment/shipment compensation, resumable compensation failure and body conflict covered. |
| `V3-ENT-PY-02` | `passed_target_runtime_python_3_13_5` | 7/7 | `passed` | Per-aggregate ordering, independent aggregate send, crash-before-ack, crash-after-publish retry, stable event id and dead-letter retry budget covered. |
| `V3-ENT-JS-01` | `passed_target_runtime_node_22_18_0` | 7/7 | `passed` | Owner read, tenant mismatch/IDOR deny, ownership-admin deny, support session, same-tenant admin, expired break-glass deny and audited break-glass allow covered. |
| `V3-ENT-JS-02` | `passed_target_runtime_node_22_18_0` | 6/6 | `passed` | Sensitive-field redaction, nested email redaction, trace id preservation, invalid taxonomy rejection, oversized event rejection and array redaction covered. |
| `V3-ENT-RS-01` | `fixture_self_checked_reference_only` | 7/7 | `passed_with_target_runtime_blocked` | Tenant and soft-delete predicates, partial-index hint eligibility, deleted query no-hint, missing tenant, unknown filter and admin audit requirements covered. Rust target proof blocked because `rustc/cargo` are unavailable. |
| `V3-OLY-CPP-01` | `fixture_self_checked_reference_only` | 5/5 | `passed_with_target_runtime_blocked` | Max-flow reference fixtures cover single edge, parallel edges, unreachable sink, bottleneck cut and 64-bit-scale capacity. C++ target proof blocked because no local compiler is available. |
| `V3-OLY-CPP-02` | `fixture_self_checked_reference_only` | 6/6 | `passed_with_target_runtime_blocked` | Functional-graph fixtures cover tree-to-cycle, same-cycle, unreachable cycle-to-tree, different components, zero self-distance and self-loop cases. C++ target proof blocked because no local compiler is available. |
| `V3-OLY-RS-01` | `fixture_self_checked_reference_only` | 4/4 | `passed_with_target_runtime_blocked_after_fixture_fix` | k-shortest path fixtures cover alternative routes, equal-cost duplicate routes, cycle-generated variants and 64-bit-scale weights. First run exposed a fixture destination mismatch, corrected before this pass. Rust target proof blocked because `rustc/cargo` are unavailable. |
| `V3-OLY-RS-02` | `fixture_self_checked_reference_only` | 5/5 | `passed_with_target_runtime_blocked` | Polynomial range-update fixtures cover full-range update, last-point value, nested update composition, subrange sum and single-point update. Rust target proof blocked because `rustc/cargo` are unavailable. |
| `V3-OLY-CPP-03` | `fixture_self_checked_reference_only` | 3/3 | `passed_with_target_runtime_blocked` | New-roads fixtures cover mixed connectivity days, never-connected pair and duplicate road handling. C++ target proof blocked because no local compiler is available. |

Intermediate defect log:

- `V3-OLY-RS-01`: first reference-run attempt failed because the `two alternatives` fixture used destination `n=3` while the expected answer targeted node `2`. This was a fixture-definition error, not accepted as task proof; runner fixture was corrected before recording the final task result.

Rollup:

- Total tasks tested: 10/10.
- Target-runtime proof: 4/10 tasks, 28/28 cases passed on Python/Node.js.
- Reference-fixture proof: 6/10 tasks, 30/30 cases passed with C++/Rust target proof blocked by missing local toolchains.
- Total final accepted cases: 58/58 passed.
- Intermediate defect found: 1 fixture-definition error in `V3-OLY-RS-01`, fixed before final result.
- Runner artifacts: `.codex/product-agent-os/b45-manual-pilot/v3_reference_runner.py` and `.codex/product-agent-os/b45-manual-pilot/v3_js_runner.mjs`.
