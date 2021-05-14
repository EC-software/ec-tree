
""" Initialise the db """

import ectcommon as co

db = co.db()

print(f"INI has a SQLite connection: {db}")

# Make tables if not exists
db.execute('''CREATE TABLE roots (
  mode INTEGER NOT NULL,
  path varchar NOT NULL PRIMARY KEY
);''')
db.execute('''CREATE TABLE files (
  filename varchar PRIMARY KEY NOT NULL,
  filetime varchar NOT NULL,
  filesize integer NOT NULL,
  shorthash varchar NOT NULL,
  longhash varchar NOT NULL,
  scantime varchar NOT NULL
);''')
db.execute('''CREATE VIEW collision_short as 
  select count(*), shorthash 
  from files 
  where shorthash <> ""
  group by shorthash 
  having count(*) > 1
  order by count(*) desc
;''')
db.execute('''CREATE VIEW collision_long as 
  select count(*), longhash 
  from files 
  where longhash <> ""
  group by longhash 
  having count(*) > 1
  order by count(*) desc
;''')
db.close()
