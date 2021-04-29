
""" Add root to the db """

import sys
import ectcommon as co

db = co.db()
print(f"AR has a SQLite connection: {db}")

print(f"The script has the name: {sys.argv[0]}")
print(f"The script has the para: {sys.argv[1]}")

# Check if already in db
bol_known = False
for row in db.execute('SELECT * FROM roots'):
    ##print(f"row: {row}")
    if row[1].lower() == 'o':
        if row[2] == sys.argv[1]:
            ##print(f"Bingo: {sys.argv[1]}")
            bol_known = True
        else:
            pass ##print(f"Not my Dir: {row[2]} \n         != {sys.argv[1]}")
    else:
        pass ##print(f"Not Open: {row[1]}")  ToDo: Introduce X (exclude) directories
# Insert if not existing
if not bol_known:
    # Add to the db
    str_sql = f"INSERT INTO roots VALUES ('O','{sys.argv[1]}')"
    print(f"SQL: {str_sql}")
    db.execute(str_sql)
    db.commit()