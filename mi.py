import sqlite3 as sq


with sq.connect("pr.db") as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS logs(
        h TEXT,
        t TEXT,
        r TEXT,
        s TEXT
    , UNIQUE(h, t, r, s))""")