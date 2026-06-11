from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    schema = (ROOT / "schema" / "orders.sql").read_text(encoding="utf-8")
    migration = (ROOT / "migrations" / "001_init_orders.sql").read_text(encoding="utf-8")
    rules = json.loads((ROOT / "data" / "quality-rules.json").read_text(encoding="utf-8"))
    trace = json.loads((ROOT / "traces" / "no-live-db-action.json").read_text(encoding="utf-8"))
    rows = [
        json.loads(line)
        for line in (ROOT / "data" / "synthetic-orders.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    errors: list[str] = []
    for token in ["CREATE TABLE orders", "CREATE TABLE invoices", "REFERENCES orders(id)", "CHECK"]:
        if token not in schema:
            errors.append(f"schema_missing:{token}")
    if "Migration execution status: not_run_approval_required" not in migration:
        errors.append("migration_boundary_missing")
    if len(rows) != rules["expected_rows"]:
        errors.append("unexpected_row_count")
    for row in rows:
        if sorted(rules["required_fields"]) != sorted(row.keys()):
            errors.append(f"bad_fields:{row.get('id', 'unknown')}")
        if row["status"] not in rules["allowed_statuses"]:
            errors.append(f"bad_status:{row['status']}")
        if not row["customer_ref"].startswith("synthetic_"):
            errors.append("non_synthetic_customer_ref")
    if rules["production_data_allowed"] is not False:
        errors.append("production_data_allowed_not_false")
    for key, value in trace.items():
        if value is not False:
            errors.append(f"live_action_not_false:{key}")

    result = {
        "status": "ok" if not errors else "failed",
        "schema_tables": ["orders", "invoices"],
        "synthetic_rows": len(rows),
        "migration_executed": trace["migration_executed"],
        "live_database_connected": trace["live_database_connected"],
        "production_data_accessed": trace["production_data_accessed"],
        "errors": errors,
    }
    print(json.dumps(result, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

