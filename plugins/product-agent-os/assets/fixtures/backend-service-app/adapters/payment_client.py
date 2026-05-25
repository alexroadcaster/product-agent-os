"""Synthetic external dependency client with timeout and fallback notes."""


class PaymentClient:
    timeout_seconds = 2
    fallback = "synthetic-decline"

