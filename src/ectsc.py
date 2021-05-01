
""" Scan """

import datetime
import os
import sys
import time

import ectcommon as co


# CONSTANTS
max_chunks = 1  # The sample-size defining short-hash, where long-hash always is the entire file.


def make_rootlist():
    """ Look at argv and make a 1 element root list of it, if missing make root list from db """
    lst_ret = []
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            lst_ret.append(sys.argv[1])
    else:  # build from db
        for row in db.execute('SELECT * FROM roots'):
            if os.path.isdir(row[1]):
                lst_ret.append(row[1])
    return lst_ret

def scan_root(str_root):
    print(f"Scanning: {str_root}")
    # get db info on this dir
    dic_db = dict()
    str_sql = f"SELECT * FROM files where filename like '{str_root}%'"
    for row in db.execute(str_sql):
        dic_db[row[0]] = row
        print(row)
    # Walk the dir
    for root, dirs, files in os.walk(str_root):
        for str_fn in files:
            str_ffn = os.path.join(root, str_fn)
            if str_ffn in dic_db.keys():  # db know this file
                pass
            else:  # db don't know this file - add it.
                print(f"Add file: {str_ffn}")
                str_fields = "filename, filetime, filesize, shorthash, longhash, scantime"
                str_filetime = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.path.getmtime(str_ffn)))
                str_filesize = str(os.path.getsize(str_ffn))
                str_shorthas = co.hashafile(str_ffn, algorithm='sha1', max_chunks=1)  # We prefer sh11 as it is faster than md5
                str_longhash = ""
                str_scantime = datetime.datetime.now().isoformat()
                str_sql = f"INSERT INTO files ({str_fields}) VALUES ('{str_ffn}', '{str_filetime}', '{str_filesize}', '{str_shorthas}', '{str_longhash}', '{str_scantime}');"
                print(f"SQL: {str_sql}")
                db.execute(str_sql)
                db.commit()

def scan_rootlist(lst_roots):
    for root in lst_roots:
        scan_root(root)

if __name__ == '__main__':

    db = co.db()
    print(f"AR has a SQLite connection: {db}")
    print(f"argvar: {sys.argv}")

    lst_root = make_rootlist()
    print(f"Go w: {lst_root}")
    scan_rootlist(lst_root)