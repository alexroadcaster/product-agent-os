import sqlite3,sys
from pathlib import Path
db=sqlite3.connect(':memory:'); source=Path(sys.argv[1]).read_text()
db.executescript(source); assert db.execute('PRAGMA foreign_keys').fetchone()==(1,); db.executescript('CREATE TABLE parent(id INTEGER PRIMARY KEY); CREATE TABLE child(parent_id INTEGER REFERENCES parent(id));'); rejected=False
try: db.execute('INSERT INTO child VALUES (9)')
except sqlite3.IntegrityError: rejected=True
assert rejected
