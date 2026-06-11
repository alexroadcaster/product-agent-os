-- Source status: Synthetic Batch 39 M17 fixture.
-- Migration execution status: not_run_approval_required.
-- This file is static fixture evidence only.
CREATE TABLE orders (
  id TEXT PRIMARY KEY,
  customer_ref TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('created', 'paid', 'cancelled')),
  created_at TEXT NOT NULL
);

CREATE TABLE invoices (
  id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL REFERENCES orders(id),
  amount_cents INTEGER NOT NULL CHECK (amount_cents >= 0)
);

