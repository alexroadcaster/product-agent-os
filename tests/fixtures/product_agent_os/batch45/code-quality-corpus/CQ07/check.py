import sqlite3,sys
from pathlib import Path
db=sqlite3.connect(':memory:'); source=Path(sys.argv[1]).read_text()
db.executescript("CREATE TABLE items(label TEXT); INSERT INTO items VALUES ('b'),('a'),('b');"); assert db.execute(source).fetchall()==[('a',),('b',)]
