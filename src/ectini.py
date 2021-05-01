
""" Initialise the db """

import ectcommon as co

db = co.db()

print(f"INI has a SQLite connection: {db}")

# Make tables if not exists
db.execute('CREATE TABLE IF NOT EXISTS roots ('
           'mode INTEGER NOT NULL, '
           'path varchar NOT NULL PRIMARY KEY);')
db.execute('CREATE TABLE IF NOT EXISTS files ('
           'filename varchar PRIMARY KEY NOT NULL, '
           'filetime varchar NOT NULL, '
           'filesize integer NOT NULL, '
           'shorthash varchar NOT NULL, '
           'longhash varchar NOT NULL, '
           'scantime varchar NOT NULL);')
db.execute('create view collision_short as '
           'select count(*), shorthash '
           'from files '
           'group by shorthash '
           'order by count(*) desc;')
db.close()
