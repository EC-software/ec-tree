
""" Scan """

import os
import sys

import ectcommon as co

def make_rootlist():
    """ Look at argv and make a 1 element root list of it, if missing make root list from db """
    lst_ret = []
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            lst_ret.append(sys.argv[1])
        else:  # Non valid entry
            return lst_ret
    else:  # build from db
        for row in db.execute('SELECT * FROM roots'):
            if os.path.isdir(row[1]):
                lst_ret.append(row[1])
        return lst_ret

def scan_root(str_root):
    print(f"Scanning: {str_root}")
    # get db info on this dir
    str_sql = 'SELECT * FROM files'
    for row in db.execute(str_sql):
        pass # print(row)
    for root, dirs, files in os.walk(str_root):
        for name in files:
            print(os.path.join(root, name))
        #print(root, "consumes", end=" ")
        #print(sum(os.path.getsize(os.path.join(root, name)) for name in files), end=" ")
        #print("bytes in", len(files), "non-directory files")

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