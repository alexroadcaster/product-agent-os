"""Synthetic independent pressure/batch outcomes; never generator context."""
def check(candidate):
    state = {"balance": 100, "seen": set()}
    observed = []
    def notify(request_id, amount):
        observed.append((state["balance"], set(state["seen"])))
    first = candidate.apply(state, "one", 30, notify)
    if first != {"remaining": 70, "request_id": "one"} or observed != [(100, set())]:
        return ["callback_must_observe_uncommitted_state"]
    candidate.apply(state, "one", 30, notify)
    if len(observed) != 1 or state["balance"] != 70:
        return ["duplicate_must_not_charge_or_notify"]
    state = {"balance": 100, "seen": set()}
    def fail(*args):
        raise RuntimeError("synthetic")
    try:
        candidate.apply(state, "two", 30, fail)
    except RuntimeError:
        pass
    else:
        return ["failure_must_propagate"]
    if state != {"balance": 100, "seen": set()}:
        return ["failed_notification_must_not_commit"]
    return []


def check_batch(candidate):
    state = {"balance": 100, "seen": set()}
    calls = []
    result = candidate.apply_batch(state, [("a", 30), ("a", 30), ("b", 20)], lambda *args: calls.append(args))
    return [] if result == [{"remaining":70,"request_id":"a"}, {"remaining":70,"request_id":"a"}, {"remaining":50,"request_id":"b"}] and state["balance"] == 50 and len(calls) == 2 else ["batch_reuse_contract"]
