
""" Initialise the db """

import ectcommon as co

db = co.db()

print(f"INI has a SQLite connection: {db}")

# Make tables if not exists
db.execute('CREATE TABLE IF NOT EXISTS roots ('
           'id INTEGER PRIMARY KEY, '
           'mode INTEGER NOT NULL, '
           'path varchar NOT NULL)')
db.execute('CREATE TABLE IF NOT EXISTS files ('
           'id INTEGER PRIMARY KEY, '
           'filename varchar NOT NULL, '
           'filetime varchar NOT NULL, '
           'filesize integer NOT NULL, '
           'shorthash varchar NOT NULL, '
           'longhash varchar NOT NULL, '
           'scantime varchar NOT NULL)')
db.close()
