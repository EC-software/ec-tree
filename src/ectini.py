
import os.path
import sqlite3
import sys

import configparser

FN = os.path.join(".", "ectree.conf")  # Default config file is assumed to be in same folder as this script

cfg = configparser.ConfigParser()
cfg.read(FN)

if 'sqlite' in cfg.keys():
    if 'format' in cfg['sqlite'].keys() and cfg['sqlite']['format'] == 'sqlite':
        if 'name' in cfg['sqlite'].keys():
            str_dbfn = cfg['sqlite']['name']
            if '~' in str_dbfn:
                str_dbfn = str_dbfn.replace('~', os.path.expanduser("~"))
            db = sqlite3.connect(str_dbfn)  # Also creates the DB if not exists
        else:
            print(".conf SQLite entry, holds no name")
            sys.exit(3)
    else:
        print(".conf SQLite entry, holds no valid format")
        sys.exit(2)
else:
    print(".conf file holds no SQLite entry")
    sys.exit(1)
print(f"We have a SQLite, called: {str_dbfn}: {db}")

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

