def reserve(balance, amount):
    return balance - amount


def apply(state, request_id, amount, notify):
    state["balance"] -= amount
    state["seen"].add(request_id)
    notify(request_id, amount)
    return {"remaining": state["balance"], "request_id": request_id}
