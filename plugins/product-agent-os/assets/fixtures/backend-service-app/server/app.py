"""Synthetic backend API entrypoint with health and readiness signals."""


def health() -> dict[str, str]:
    return {"status": "ok", "probe": "health"}


def readiness() -> dict[str, str]:
    return {"status": "ready", "probe": "readiness"}


def create_order(payload: dict[str, str]) -> dict[str, str]:
    return {"order_id": payload.get("order_id", "synthetic-order")}

