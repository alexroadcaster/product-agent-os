import sqlite3,sys
from pathlib import Path
db=sqlite3.connect(':memory:'); source=Path(sys.argv[1]).read_text()
db.executescript("CREATE TABLE items(id INTEGER,tenant TEXT); INSERT INTO items VALUES (1,'blue'),(2,'red'),(3,'blue');"); assert db.execute(source).fetchall()==[(1,),(3,)]
