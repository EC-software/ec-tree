
""" Scan """

import datetime
import os
import sys
import time

import ectcommon as co


# CONSTANTS
max_chunks = 1  # The sample-size defining short-hash, where long-hash always is the entire file.


def make_rootlists():
    """ Look at argv and make a 1 element root list of it, if missing make root list from db """
    lst_i, lst_x = list(), list()
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            lst_i.append(sys.argv[1])
    else:  # build from db
        for row in db.execute('SELECT * FROM roots'):
            if row[0].upper() == 'I':
                lst_i.append(row[1])
            elif row[0].upper() == 'X':
                lst_x.append(row[1])
            else:
                print(f"Unexpected mode: {row[0]} in {row}")
            ##print(f"{lst_i}\n{lst_x}")
    return lst_i, lst_x

def timeandsize(str_ffn):
    try:
        str_filetime = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.path.getmtime(str_ffn)))
        str_filesize = os.path.getsize(str_ffn)
        return str_filetime, str_filesize
    except FileNotFoundError:  # some files are very temporary ...
        return "", ""

def scan_file(str_ffn):
    str_scantime = datetime.datetime.now().isoformat()
    str_filetime, str_filesize = timeandsize(str_ffn)
    try:
        str_shorthas = co.hashafile(str_ffn, algorithm='sha1', max_chunks=1)  # We prefer sha1 as it is faster than md5
        str_longhash = ""
        return str_filetime, str_filesize, str_shorthas, str_longhash, str_scantime
    except FileNotFoundError:  # some files are very temporary ...
        return "", "", "", "", str_scantime

def add_file2db(str_ffn):
    str_ffn = str_ffn.replace("'", "")  # ToDo This is not a solid way to handle filenames that include '
    try:
        ##print(f"Add file: {str_ffn}")
        str_fields = "filename, filetime, filesize, shorthash, longhash, scantime"
        str_filetime, str_filesize, str_shorthas, str_longhash, str_scantime = scan_file(str_ffn)
        str_sql = f"INSERT INTO files ({str_fields}) VALUES ('{str_ffn}', '{str_filetime}', '{str_filesize}', '{str_shorthas}', '{str_longhash}', '{str_scantime}');"
        print(f"add_file2db(); sql: {str_sql}")
        db.execute(str_sql)
        db.commit()
    except FileNotFoundError:
        pass  # some files are very temporary ...

def add_longhash_2_shorthash(shorthash):
    str_sql_sel = f"select * from files where shorthash = '{shorthash}'"
    for row in db.execute(str_sql_sel):
        print(f"* {row}")
        if os.path.isfile(row[0]):
            str_longhash = co.hashafile(row[0], algorithm='sha1', max_chunks=1)
            str_sql_update


def scan_root(str_ri, lst_rx):
    """
    Scan one root-dir lst_ri, but skipping sub-dirs listed in lst_rx
    :param str_ri: string, the root dir
    :param lst_rx: list of exceptions, sub dirs that should be skipped
    :return: tbd
    """
    print(f"scan_root(); Scanning: {str_ri, lst_rx}")
    # get db info on this dir
    dic_db = dict()  # dic by ffn of files known to the db
    str_sql = f"SELECT * FROM files where filename like '{str_ri}%'"
    for row in db.execute(str_sql):
        ##print(f"scan_root(); known file: {row}")
        dic_db[row[0]] = row
    # Walk the root-dir
    num_cntfil = 0
    for root, dirs, files in os.walk(str_ri):
        for str_fn in files:
            num_cntfil += 1
            str_ffn = os.path.join(root, str_fn)
            if not any([str_ffn.startswith(x) for x in lst_rx]):  # if the file is not excluded
                if str_ffn in dic_db.keys():  # db knows this file
                    tim, siz = timeandsize(str_ffn)
                    if tim == dic_db[str_ffn][1] and siz == dic_db[str_ffn][2]:
                        print(f" - skipping known file: {str_ffn} == {dic_db[str_ffn]}")
                    else:
                        print(f"WTF: {tim == dic_db[str_ffn][1]} and {str(type(siz))} == {str(type(dic_db[str_ffn][2]))}")
                else:  # db don't know this file - add it.
                    add_file2db(str_ffn)
            if num_cntfil % 100 == 0:
                print(f"Count: {num_cntfil}: {str_ffn}")

def scan_rootlists(lst_ri, lst_rx):
    for root in lst_ri:
        lst_rxs = [tok for tok in lst_rx if tok.find(root) >= 0]
        print(f"\nscan_rootlists(); Clear to scan: ri: {root}, xs: {lst_rxs}")
        scan_root(root, lst_rxs)

if __name__ == '__main__':

    db = co.db()
    print(f"SC has a SQLite connection: {db}")
    print(f"argvar: {sys.argv[1:]}")

    # fill/update the db
    lst_ri, lst_rx = make_rootlists()
    print(f"main(); Go w: {lst_ri, lst_rx}")
    ##scan_rootlists(lst_ri, lst_rx)

    # Look for collisions
    str_sql = f"SELECT * FROM collision_short"
    for row in db.execute(str_sql):
        ##print(f"scan_root(); known file: {row}")
        if row[0] > 3:  # several files with this short-hash  ToDo reset to 1
            print(row)
            add_longhash_2_shorthash(row[1])