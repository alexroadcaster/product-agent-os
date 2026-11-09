"""Synthetic reference; notification failure must not commit local state."""

def reserve(balance, amount):
    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or not 0 <= amount <= balance:
        raise ValueError("invalid amount")
    return balance - amount


def apply(state, request_id, amount, notify):
    if request_id in state["seen"]:
        return {"remaining": state["balance"], "request_id": request_id}
    remaining = reserve(state["balance"], amount)
    notify(request_id, amount)
    state["balance"] = remaining
    state["seen"].add(request_id)
    return {"remaining": remaining, "request_id": request_id}


class _Dispatcher:
    def __init__(self, action):
        self.action = action

    def invoke(self, *args):
        return self.action(*args)


def apply_batch(state, requests, notify):
    handler = _Dispatcher(apply)
    return [handler.invoke(state, request_id, amount, notify) for request_id, amount in requests]
