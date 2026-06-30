"""Local reference runner for Batch 45 Enterprise/Olympiad V3 tasks.

The runner intentionally keeps C++ and Rust tasks as reference-fixture checks
because the current workspace has no approved local C++/Rust toolchain.
"""

from __future__ import annotations

import argparse
import heapq
import json
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any, Callable


def _case(name: str, actual: Any, expected: Any) -> dict[str, Any]:
    if actual != expected:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")
    return {"case": name, "status": "passed"}


def _result(task_id: str, proof_level: str, cases: list[dict[str, Any]], notes: list[str] | None = None) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "proof_level": proof_level,
        "status": "passed",
        "passed": len(cases),
        "total": len(cases),
        "cases": cases,
        "notes": notes or [],
    }


class SagaEngine:
    """Tiny saga state machine for idempotent retry and compensation fixtures."""

    def __init__(self) -> None:
        self.records: dict[str, dict[str, Any]] = {}
        self.side_effects: defaultdict[str, int] = defaultdict(int)
        self.events: list[str] = []

    def run(self, saga_id: str, order: dict[str, Any], *, fail_step: str | None = None, compensation_fail: str | None = None) -> dict[str, Any]:
        """Run or replay a saga while preserving conflict and compensation invariants."""

        body = json.dumps(order, sort_keys=True)
        if saga_id in self.records:
            record = self.records[saga_id]
            if record["body"] != body:
                return {"state": "conflict", "error": "saga_body_conflict"}
            return {"state": record["state"], "replayed": True, "events": list(self.events)}

        record = {"body": body, "state": "started", "completed_steps": [], "compensations": []}
        self.records[saga_id] = record
        try:
            self._step(record, saga_id, "reserve_inventory", fail_step)
            self._step(record, saga_id, "authorize_payment", fail_step)
            self._step(record, saga_id, "create_shipment", fail_step)
            event_id = f"order_confirmed:{saga_id}"
            self.events.append(event_id)
            record["state"] = "confirmed"
            return {"state": "confirmed", "replayed": False, "events": [event_id]}
        except RuntimeError as exc:
            for step in reversed(record["completed_steps"]):
                compensation = {
                    "create_shipment": "cancel_shipment",
                    "authorize_payment": "void_payment",
                    "reserve_inventory": "release_inventory",
                }[step]
                if compensation_fail == compensation:
                    record["state"] = "compensation_failed"
                    record["resume_from"] = compensation
                    return {"state": "compensation_failed", "error": str(exc), "resume_from": compensation}
                self.side_effects[f"{saga_id}:{compensation}"] += 1
                record["compensations"].append(compensation)
            record["state"] = "failed"
            return {"state": "failed", "error": str(exc), "compensations": list(record["compensations"])}

    def _step(self, record: dict[str, Any], saga_id: str, step: str, fail_step: str | None) -> None:
        if fail_step == step:
            raise RuntimeError(f"{step}_failed")
        self.side_effects[f"{saga_id}:{step}"] += 1
        record["completed_steps"].append(step)


def run_ent_py_01() -> dict[str, Any]:
    engine = SagaEngine()
    cases: list[dict[str, Any]] = []
    order = {"order_id": "o1", "amount": 1250, "sku": "sku-1"}
    cases.append(_case("successful saga confirms once", engine.run("s1", order)["state"], "confirmed"))
    replay = engine.run("s1", order)
    cases.append(_case("exact retry is replayed", replay["replayed"], True))
    cases.append(_case("retry does not duplicate confirmation", engine.events, ["order_confirmed:s1"]))
    payment_failure = engine.run("s2", order, fail_step="authorize_payment")
    cases.append(_case("payment failure fails saga", payment_failure["state"], "failed"))
    cases.append(_case("payment failure releases inventory", payment_failure["compensations"], ["release_inventory"]))
    shipment_failure = engine.run("s3", order, fail_step="create_shipment")
    cases.append(_case("shipment failure compensates reverse order", shipment_failure["compensations"], ["void_payment", "release_inventory"]))
    compensation_failure = engine.run("s4", order, fail_step="create_shipment", compensation_fail="void_payment")
    cases.append(_case("compensation failure is resumable", compensation_failure["state"], "compensation_failed"))
    conflict = engine.run("s1", {"order_id": "o1", "amount": 1300, "sku": "sku-1"})
    cases.append(_case("same saga id different body conflicts", conflict["error"], "saga_body_conflict"))
    return _result("V3-ENT-PY-01", "passed_target_runtime_python_3_13_5", cases)


@dataclass
class OutboxRow:
    event_id: str
    aggregate_id: str
    sequence: int
    status: str = "pending"
    attempts: int = 0


class Publisher:
    """Failure-injection publisher used to exercise outbox ack and retry invariants."""

    def __init__(self, *, fail_before_ack: set[str] | None = None, crash_after_publish: set[str] | None = None) -> None:
        self.fail_before_ack = fail_before_ack or set()
        self.crash_after_publish = crash_after_publish or set()
        self.published: list[str] = []

    def publish(self, row: OutboxRow) -> str:
        if row.event_id in self.fail_before_ack:
            raise RuntimeError("broker_unavailable")
        self.published.append(row.event_id)
        if row.event_id in self.crash_after_publish:
            self.crash_after_publish.remove(row.event_id)
            raise RuntimeError("relay_crashed_after_publish")
        return "ack"


class OutboxRelay:
    """Reference transactional-outbox relay with per-aggregate ordering and retry budget."""

    def __init__(self, rows: list[OutboxRow], publisher: Publisher, *, max_attempts: int = 3) -> None:
        self.rows = rows
        self.publisher = publisher
        self.max_attempts = max_attempts

    def run_once(self) -> None:
        """Publish only rows whose earlier same-aggregate events are no longer pending."""

        pending = [row for row in self.rows if row.status == "pending"]
        pending.sort(key=lambda row: (row.aggregate_id, row.sequence))
        for row in pending:
            earlier_pending = any(
                other.aggregate_id == row.aggregate_id
                and other.sequence < row.sequence
                and other.status == "pending"
                for other in self.rows
            )
            if earlier_pending:
                continue
            row.attempts += 1
            try:
                self.publisher.publish(row)
                row.status = "sent"
            except RuntimeError:
                if row.attempts >= self.max_attempts:
                    row.status = "dead_letter"


def run_ent_py_02() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    rows = [OutboxRow("a1", "acct-a", 1), OutboxRow("a2", "acct-a", 2), OutboxRow("b1", "acct-b", 1)]
    publisher = Publisher()
    relay = OutboxRelay(rows, publisher)
    relay.run_once()
    cases.append(_case("per-aggregate order preserved", publisher.published[:2], ["a1", "a2"]))
    cases.append(_case("independent aggregate sent", rows[2].status, "sent"))

    rows = [OutboxRow("c1", "acct-c", 1)]
    publisher = Publisher(fail_before_ack={"c1"})
    relay = OutboxRelay(rows, publisher)
    relay.run_once()
    cases.append(_case("crash before ack keeps pending", rows[0].status, "pending"))

    rows = [OutboxRow("d1", "acct-d", 1)]
    publisher = Publisher(crash_after_publish={"d1"})
    relay = OutboxRelay(rows, publisher)
    relay.run_once()
    cases.append(_case("crash after publish keeps retryable row", rows[0].status, "pending"))
    relay.run_once()
    cases.append(_case("retry uses stable event id", publisher.published, ["d1", "d1"]))
    cases.append(_case("retry can mark sent", rows[0].status, "sent"))

    rows = [OutboxRow("p1", "acct-p", 1)]
    publisher = Publisher(fail_before_ack={"p1"})
    relay = OutboxRelay(rows, publisher)
    for _ in range(3):
        relay.run_once()
    cases.append(_case("poison message dead letters after retry budget", rows[0].status, "dead_letter"))
    return _result("V3-ENT-PY-02", "passed_target_runtime_python_3_13_5", cases)


def plan_query(filters: dict[str, Any]) -> dict[str, Any]:
    """Build safe query predicates with tenant isolation and partial-index eligibility."""

    allowed = {"tenant_id", "deleted", "status", "created_after", "created_before", "admin_scope", "audit_reason"}
    unknown = set(filters) - allowed
    if unknown:
        raise ValueError("unknown_filter")
    predicates: list[str] = []
    audit: list[str] = []
    if filters.get("admin_scope"):
        if not filters.get("audit_reason"):
            raise ValueError("admin_audit_reason_required")
        audit.append("high_risk_cross_tenant_query")
    elif not filters.get("tenant_id"):
        raise ValueError("tenant_predicate_required")
    if filters.get("tenant_id"):
        predicates.append("tenant_id = :tenant_id")
    if filters.get("deleted") is False:
        predicates.append("deleted_at IS NULL")
    elif filters.get("deleted") is True:
        predicates.append("deleted_at IS NOT NULL")
    if "status" in filters:
        predicates.append("status = :status")
    hint = "documents_active_tenant_partial_idx" if "tenant_id = :tenant_id" in predicates and "deleted_at IS NULL" in predicates else None
    return {"predicates": predicates, "index_hint": hint, "audit": audit}


def run_ent_rs_01() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    plan = plan_query({"tenant_id": "t1", "deleted": False, "status": "active"})
    cases.append(_case("tenant and soft-delete predicates present", plan["predicates"][:2], ["tenant_id = :tenant_id", "deleted_at IS NULL"]))
    cases.append(_case("partial index hint only when predicate implies it", plan["index_hint"], "documents_active_tenant_partial_idx"))
    cases.append(_case("deleted query does not use active partial index", plan_query({"tenant_id": "t1", "deleted": True})["index_hint"], None))
    try:
        plan_query({"deleted": False})
        raise AssertionError("missing tenant should fail")
    except ValueError as exc:
        cases.append(_case("tenant omitted is rejected", str(exc), "tenant_predicate_required"))
    try:
        plan_query({"tenant_id": "t1", "raw_sql": "1=1"})
        raise AssertionError("unknown filter should fail")
    except ValueError as exc:
        cases.append(_case("unknown filter rejected", str(exc), "unknown_filter"))
    try:
        plan_query({"admin_scope": True})
        raise AssertionError("admin reason should fail")
    except ValueError as exc:
        cases.append(_case("admin query requires audit reason", str(exc), "admin_audit_reason_required"))
    admin = plan_query({"admin_scope": True, "audit_reason": "support-escalation"})
    cases.append(_case("admin query records high-risk audit", admin["audit"], ["high_risk_cross_tenant_query"]))
    return _result(
        "V3-ENT-RS-01",
        "fixture_self_checked_reference_only",
        cases,
        ["target Rust runtime blocked: rustc/cargo unavailable in PATH"],
    )


class Dinic:
    """Residual graph implementation for max-flow fixture coverage."""

    def __init__(self, n: int) -> None:
        self.graph: list[list[list[int]]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, capacity: int) -> None:
        forward = [v, capacity, len(self.graph[v])]
        backward = [u, 0, len(self.graph[u])]
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def max_flow(self, source: int, sink: int) -> int:
        """Compute max flow with Dinic levels and residual-capacity augmentation."""

        flow = 0
        n = len(self.graph)
        while True:
            level = [-1] * n
            level[source] = 0
            queue = deque([source])
            while queue:
                u = queue.popleft()
                for v, capacity, _ in self.graph[u]:
                    if capacity > 0 and level[v] < 0:
                        level[v] = level[u] + 1
                        queue.append(v)
            if level[sink] < 0:
                return flow
            it = [0] * n

            def dfs(u: int, pushed: int) -> int:
                if u == sink:
                    return pushed
                while it[u] < len(self.graph[u]):
                    edge = self.graph[u][it[u]]
                    v, capacity, rev = edge
                    if capacity > 0 and level[v] == level[u] + 1:
                        sent = dfs(v, min(pushed, capacity))
                        if sent:
                            # Residual reverse capacity preserves the augmenting-path invariant.
                            edge[1] -= sent
                            self.graph[v][rev][1] += sent
                            return sent
                    it[u] += 1
                return 0

            while pushed := dfs(source, 10**30):
                flow += pushed


def download_speed(n: int, edges: list[tuple[int, int, int]]) -> int:
    dinic = Dinic(n)
    for u, v, capacity in edges:
        dinic.add_edge(u - 1, v - 1, capacity)
    return dinic.max_flow(0, n - 1)


def run_oly_cpp_01() -> dict[str, Any]:
    cases = [
        _case("single edge", download_speed(2, [(1, 2, 7)]), 7),
        _case("parallel edges", download_speed(2, [(1, 2, 3), (1, 2, 4)]), 7),
        _case("unreachable sink", download_speed(3, [(1, 2, 5)]), 0),
        _case("bottleneck cut", download_speed(4, [(1, 2, 10), (1, 3, 10), (2, 4, 3), (3, 4, 4)]), 7),
        _case("large capacity", download_speed(2, [(1, 2, 3_000_000_000)]), 3_000_000_000),
    ]
    return _result("V3-OLY-CPP-01", "fixture_self_checked_reference_only", cases, ["target C++ runtime blocked: no local compiler"])


def functional_graph_distance(nexts: list[int], source: int, target: int) -> int:
    seen: set[int] = set()
    node = source
    steps = 0
    while node not in seen:
        if node == target:
            return steps
        seen.add(node)
        node = nexts[node - 1]
        steps += 1
    return -1


def run_oly_cpp_02() -> dict[str, Any]:
    nexts = [2, 3, 4, 2, 3, 6]
    cases = [
        _case("tree to cycle", functional_graph_distance(nexts, 1, 4), 3),
        _case("same cycle forward", functional_graph_distance(nexts, 2, 4), 2),
        _case("cycle to tree unreachable", functional_graph_distance(nexts, 3, 1), -1),
        _case("different components unreachable", functional_graph_distance(nexts, 6, 4), -1),
        _case("self node distance zero", functional_graph_distance(nexts, 5, 5), 0),
        _case("self-loop component", functional_graph_distance(nexts, 6, 6), 0),
    ]
    return _result("V3-OLY-CPP-02", "fixture_self_checked_reference_only", cases, ["target C++ runtime blocked: no local compiler"])


def flight_routes(n: int, edges: list[tuple[int, int, int]], k: int) -> list[int]:
    """Return the k cheapest route costs, counting duplicate path variants separately."""

    graph: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, cost in edges:
        graph[u].append((v, cost))
    heap = [(0, 1)]
    counts = [0] * (n + 1)
    answers: list[int] = []
    while heap and len(answers) < k:
        cost, node = heapq.heappop(heap)
        counts[node] += 1
        if node == n:
            answers.append(cost)
        if counts[node] <= k:
            for nxt, weight in graph[node]:
                heapq.heappush(heap, (cost + weight, nxt))
    return answers


def run_oly_rs_01() -> dict[str, Any]:
    cases = [
        _case("two alternatives", flight_routes(4, [(1, 4, 5), (1, 3, 2), (3, 4, 2)], 2), [4, 5]),
        _case("equal cost routes count separately", flight_routes(2, [(1, 2, 1), (1, 2, 1)], 2), [1, 1]),
        _case("cycle creates route variants", flight_routes(3, [(1, 2, 1), (2, 1, 1), (2, 3, 1), (1, 3, 5)], 3), [2, 4, 5]),
        _case("large weights", flight_routes(2, [(1, 2, 3_000_000_000)], 1), [3_000_000_000]),
    ]
    return _result("V3-OLY-RS-01", "fixture_self_checked_reference_only", cases, ["target Rust runtime blocked: rustc/cargo unavailable in PATH"])


def apply_poly_update(values: list[int], left: int, right: int) -> None:
    for index in range(left - 1, right):
        values[index] += index - (left - 1) + 1


def run_oly_rs_02() -> dict[str, Any]:
    values = [0, 0, 0, 0, 0]
    apply_poly_update(values, 1, 5)
    cases = [
        _case("full update last value", values[4], 5),
        _case("full update sum", sum(values), 15),
    ]
    apply_poly_update(values, 2, 4)
    cases.append(_case("nested update values", values, [1, 3, 5, 7, 5]))
    cases.append(_case("subrange sum", sum(values[1:4]), 15))
    apply_poly_update(values, 3, 3)
    cases.append(_case("single point update", values[2], 6))
    return _result("V3-OLY-RS-02", "fixture_self_checked_reference_only", cases, ["target Rust runtime blocked: rustc/cargo unavailable in PATH"])


class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n + 1))

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> None:
        a, b = self.find(left), self.find(right)
        if a != b:
            self.parent[b] = a


def new_roads_queries(n: int, roads: list[tuple[int, int]], queries: list[tuple[int, int]]) -> list[int]:
    """Slow oracle for earliest connectivity day; suitable for fixtures, not production scale."""

    answers = [0 if a == b else -1 for a, b in queries]
    dsu = DSU(n)
    for day, (u, v) in enumerate(roads, start=1):
        dsu.union(u, v)
        for idx, (a, b) in enumerate(queries):
            if answers[idx] == -1 and dsu.find(a) == dsu.find(b):
                answers[idx] = day
    return answers


def run_oly_cpp_03() -> dict[str, Any]:
    roads = [(1, 2), (3, 4), (2, 3), (2, 3), (5, 6)]
    queries = [(1, 4), (1, 5), (2, 2), (5, 6), (3, 4)]
    cases = [
        _case("mixed connectivity days", new_roads_queries(6, roads, queries), [3, -1, 0, 5, 2]),
        _case("never connected", new_roads_queries(4, [(1, 2)], [(1, 4)]), [-1]),
        _case("duplicate road does not corrupt answer", new_roads_queries(3, [(1, 2), (1, 2), (2, 3)], [(1, 3)]), [3]),
    ]
    return _result("V3-OLY-CPP-03", "fixture_self_checked_reference_only", cases, ["target C++ runtime blocked: no local compiler"])


TASKS: dict[str, Callable[[], dict[str, Any]]] = {
    "V3-ENT-PY-01": run_ent_py_01,
    "V3-ENT-PY-02": run_ent_py_02,
    "V3-ENT-RS-01": run_ent_rs_01,
    "V3-OLY-CPP-01": run_oly_cpp_01,
    "V3-OLY-CPP-02": run_oly_cpp_02,
    "V3-OLY-RS-01": run_oly_rs_01,
    "V3-OLY-RS-02": run_oly_rs_02,
    "V3-OLY-CPP-03": run_oly_cpp_03,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=sorted(TASKS) + ["all"], required=True)
    args = parser.parse_args()
    if args.task == "all":
        payload = [TASKS[task]() for task in sorted(TASKS)]
    else:
        payload = TASKS[args.task]()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
