def reserve(balance, amount):
    if amount < 0 or amount > balance:
        raise ValueError("invalid amount")
    return balance - amount
