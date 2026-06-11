from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


TaskStatus = Literal["queued", "running", "complete", "failed"]


@dataclass(frozen=True)
class TaskRecord:
    task_id: str
    status: TaskStatus
    owner: str


def health_payload() -> dict[str, str]:
    return {"status": "ok", "readiness": "synthetic"}


def task_payload(task: TaskRecord) -> dict[str, str]:
    return {"task_id": task.task_id, "status": task.status, "owner": task.owner}


def error_payload(code: str, message: str) -> dict[str, str]:
    return {"error": code, "message": message}

