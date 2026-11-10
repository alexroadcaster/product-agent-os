"""Independent literal checks for the frozen G7 sequence; no model calls."""

def check(namespace, chain, step):
    failures = []
    def expect(value, name):
        if not value:
            failures.append(name)
    try:
        if chain == "config-format":
            label = namespace["label"]
            expect(label(3, prefix="x") == "x3", "legacy_label")
            expect(label(3) == "3", "default_label")
            if step == "format":
                expect(label(3, prefix="x", upper=True) == "X3", "upper_label")
            return failures
        stage = ["caller", "failure", "format", "regression"].index(step)
        apply, reserve = namespace["apply"], namespace["reserve"]
        expect(reserve(100, 30) == 70, "legacy_reserve")
        expected = {"remaining": 70, "request_id": "one"} if stage >= 2 else 70
        state = {"balance": 100, "seen": set()}
        calls, observed = [], []
        def notify(*args):
            calls.append(args)
            observed.append((state["balance"], set(state["seen"])))
        expect(apply(state, "one", 30, notify) == expected, "result")
        apply(state, "one", 30, notify)
        expect(state == {"balance":70,"seen":{"one"}} and calls == [("one",30)], "idempotency")
        if stage >= 1:
            expect(observed == [(100, set())], "callback_boundary")
            state = {"balance": 100, "seen": set()}
            def fail(*args):
                raise RuntimeError("synthetic notification failure")
            propagated = False
            try:
                apply(state, "one", 30, fail)
            except RuntimeError:
                propagated = True
            expect(propagated and state == {"balance":100,"seen":set()}, "failure_no_commit")
            expect(apply(state, "one", 30, lambda *args: None) == expected, "retry")
        if stage == 3:
            for amount in (-1, 101, True, "30"):
                state = {"balance":100,"seen":set()}
                calls=[]
                rejected=False
                try:
                    apply(state, "invalid", amount, lambda *args:calls.append(args))
                except (ValueError,TypeError):
                    rejected=True
                expect(rejected and not calls and state == {"balance":100,"seen":set()}, "invalid_"+repr(amount))
            state = {"balance":100,"seen":set()}
            calls=[]
            result=namespace["apply_batch"](state, [("a",30),("a",30),("b",20)], lambda *args:calls.append(args))
            expect(result == [{"remaining":70,"request_id":"a"},{"remaining":70,"request_id":"a"},{"remaining":50,"request_id":"b"}]
                   and state == {"balance":50,"seen":{"a","b"}} and calls==[("a",30),("b",20)], "batch_reuse")
            state={"balance":100,"seen":set()}
            calls=[]
            def batch_notify(request_id, amount):
                calls.append(request_id)
                if request_id == "b":
                    raise RuntimeError("synthetic")
            propagated=False
            try:
                namespace["apply_batch"](state, [("a",30),("b",20),("c",10)], batch_notify)
            except RuntimeError:
                propagated=True
            expect(propagated and state=={"balance":70,"seen":{"a"}} and calls==["a","b"], "batch_partial_failure")
    except Exception as error:
        failures.append("exception:"+type(error).__name__)
    return failures
