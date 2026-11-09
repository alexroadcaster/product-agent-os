"""Independent literals for reviewed synthetic references; not generation context."""

def check(candidate):
    failures = []
    def expect(condition, name):
        if not condition:
            failures.append(name)
    state = {"balance": 100, "seen": set()}
    calls = []
    first = candidate.apply(state, "one", 30, lambda *args: calls.append(args))
    expect(first == {"remaining": 70, "request_id": "one"}, "complete")
    candidate.apply(state, "one", 30, lambda *args: calls.append(args))
    expect(state["balance"] == 70 and len(calls) == 1, "idempotent")
    state = {"balance": 100, "seen": set()}
    def fail(*args):
        raise RuntimeError("synthetic notification unavailable")
    try:
        candidate.apply(state, "two", 30, fail)
    except RuntimeError:
        pass
    expect(state == {"balance": 100, "seen": set()}, "rollback")
    result = candidate.apply(state, "two", 30, lambda *args: None)
    expect(result == {"remaining": 70, "request_id": "two"}, "retry")
    for amount in (-1, 101, True, "30"):
        state = {"balance": 100, "seen": set()}
        calls = []
        rejected = False
        try:
            candidate.apply(state, "invalid", amount, lambda *args: calls.append(args))
        except (ValueError, TypeError):
            rejected = True
        expect(rejected and not calls and state == {"balance": 100, "seen": set()}, "boundary:" + repr(amount))
    expect(candidate.reserve(100, 30) == 70, "legacy")
    return failures
