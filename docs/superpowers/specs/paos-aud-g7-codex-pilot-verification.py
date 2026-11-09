"""Replay only the SHA-pinned, human-reviewed synthetic G7 pilot candidates.

No provider calls. This is an evidence reproducer, not an untrusted-code sandbox.
Original checks stay fixed; callback visibility is supplemental, never rescored.
"""
import hashlib
import json
from pathlib import Path

REVIEWED = set(['18e31b2c482b3d245c68d940bb7c9230ca6cfacad4f68c6dd4929b99ac144ffd', '3f93e90aa9ef0f35d0b011f7aa5adc5aa01311811669b0d6eacf36c3c984af73', '4b4c1efdb9c530dbd58a4012aca5c7a1d4d83bd614a1fd0feba8f42b93bd9cfe', '5cbc72127d62861c952312a7978e18397beca51365cb9e4d37d8f13ab3287f55', '7f46a3c5c4c89dfa3f697a58a9793332f193c4fb201a59345a1852837eb52d00', 'b9259dc8707b3a710e0b72b7b90522bdaed5bcd9ca22ed6c670e103360bf8cff', 'd0bda36255a782440fdb3be33da7edf5521006ab56836637467db07646c7cf55', 'e96b0363521ce3acd83f7162c6485354a2d4d51effb5879649166ed4f47b71c2', 'f853c7dd6faa7813949b7305650881b2484ff11d9477579d033d3669a4e9b7a3'])
path = Path(__file__).with_name("paos-aud-g7-codex-pilot-results.json")
receipt = json.loads(path.read_text(encoding="utf-8"))
outcomes = []
supplemental = {}
for item in receipt["assessments"]:
    source = item["source"]
    digest = hashlib.sha256(source.encode()).hexdigest()
    if digest not in REVIEWED or digest != item["source_sha256"]:
        raise ValueError("candidate differs from the explicitly reviewed sources")
    namespace = {}
    exec(compile(source, "<reviewed synthetic candidate>", "exec"), namespace)
    failures = []
    def check(value, name):
        if not value:
            failures.append(name)
    if item["chain"] == "config-format":
        check(namespace["label"](3, prefix="x") == "x3", "legacy")
        check(namespace["label"](3) == "3", "default")
        if item["step"] == "format":
            check(namespace["label"](3, prefix="x", upper=True) == "X3", "upper")
    else:
        step = ["caller", "failure", "format", "regression"].index(item["step"])
        check(namespace["reserve"](100, 30) == 70, "legacy")
        state = {"balance": 100, "seen": set()}
        calls = []
        expected = {"remaining": 70, "request_id": "one"} if step >= 2 else 70
        check(namespace["apply"](state, "one", 30, lambda *a: calls.append(a)) == expected, "result")
        namespace["apply"](state, "one", 30, lambda *a: calls.append(a))
        check(state["balance"] == 70 and len(calls) == 1, "idempotency")
        if step >= 1:
            state = {"balance": 100, "seen": set()}
            def fail(*args):
                raise RuntimeError("synthetic notification unavailable")
            try:
                namespace["apply"](state, "one", 30, fail)
            except RuntimeError:
                pass
            check(state == {"balance": 100, "seen": set()}, "failure rollback")
            check(namespace["apply"](state, "one", 30, lambda *a: None) == expected, "retry")
        if step == 3:
            for amount in (-1, 101, True, "30"):
                state = {"balance": 100, "seen": set()}
                calls = []
                rejected = False
                try:
                    namespace["apply"](state, "invalid", amount, lambda *a: calls.append(a))
                except (ValueError, TypeError):
                    rejected = True
                check(rejected and not calls and state == {"balance": 100, "seen": set()}, "invalid " + repr(amount))
            state = {"balance": 100, "seen": set()}
            observed = []
            namespace["apply"](state, "one", 30, lambda *a: observed.append(
                {"balance": state["balance"], "seen": sorted(state["seen"])}))
            supplemental[item["arm"]] = observed
    if failures != item["failures"]:
        raise AssertionError("assessment drift")
    outcomes.append({"arm": item["arm"], "chain": item["chain"], "step": item["step"], "failures": failures})
print(json.dumps({"replayed": len(outcomes), "passed": sum(not x["failures"] for x in outcomes),
                  "supplemental_callback_snapshot_not_scored": supplemental}, indent=2))
