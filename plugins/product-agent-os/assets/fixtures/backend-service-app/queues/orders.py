"""Synthetic queue contract for order events."""

QUEUE_NAME = "synthetic-orders"
RETRY_POLICY = "timeout retry backoff max attempts dead-letter replay idempotency"

