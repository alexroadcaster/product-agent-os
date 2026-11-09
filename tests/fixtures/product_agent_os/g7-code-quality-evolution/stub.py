def reserve(balance, amount):
    return balance


def apply(state, request_id, amount, notify):
    return {"remaining": state["balance"], "request_id": request_id}
