PRAGMA foreign_keys=ON;
CREATE TABLE parent (
  id INTEGER PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  optional_note TEXT,
  doubled INTEGER GENERATED ALWAYS AS (id * 2) STORED
);
CREATE TABLE composite_parent (
  tenant_id INTEGER NOT NULL,
  code TEXT NOT NULL,
  PRIMARY KEY (tenant_id, code)
);
CREATE TABLE child (
  id INTEGER PRIMARY KEY,
  parent_id INTEGER REFERENCES parent(id),
  tenant_id INTEGER,
  code TEXT,
  FOREIGN KEY (tenant_id, code) REFERENCES composite_parent(tenant_id, code)
);
CREATE INDEX child_parent_idx ON child(parent_id);
CREATE TABLE self_node (id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES self_node(id));
CREATE TABLE orphan (id INTEGER PRIMARY KEY, parent_id INTEGER);
CREATE VIEW parent_view AS SELECT id, email FROM parent;
