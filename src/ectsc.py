
""" EC tree Scan
    This is the one you run to find duplicates... """

__version__ = "0.2.0"

# History
# ver. 0.1 Init working version
# ver. 0.2 Handles if existing disk-files change

import datetime
import os
import sys
import time

import ectcommon as co


# CONSTANTS
max_chunks = 1  # The sample-size defining short-hash, where long-hash always is the entire file.


def make_rootlists_OLD(db):
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
    return lst_i, lst_x


def make_rootlists(db):
    """ Look at argv and make a 1 element root list of it, if missing make root list from db """
    lst_i, lst_x, lst_xe = list(), list(), list()
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            lst_i.append(sys.argv[1])
    else:  # build from db
        for row in db.execute('SELECT * FROM roots'):
            if row[0].upper() == 'I':  # include
                lst_i.append(row[1])
            elif row[0].upper() == 'X':  # exclude
                lst_x.append(row[1])
            elif row[0].upper() == 'XE':  # exclude extension
                lst_xe.append(row[1])
            else:
                print(f"Unexpected mode: {row[0]} in {row}")
    return lst_i, lst_x, lst_xe


def timeandsize(str_ffn):
    """ Return the file-time and file-size for file str_ffn, if exist
        else return "", "" """
    try:
        str_filetime = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.path.getmtime(str_ffn)))
        str_filesize = os.path.getsize(str_ffn)
        return str_filetime, str_filesize
    except FileNotFoundError:  # some files are very temporary ...
        return "", ""


def scan_file(str_ffn):
    # if "Glasvinge" in str_ffn:
    #     print(f"G: {str_ffn}")
    str_scantime = datetime.datetime.now().isoformat()
    str_filetime, str_filesize = timeandsize(str_ffn)
    try:
        str_shorthas = co.hashafile(str_ffn, algorithm='sha1', max_chunks=1)  # We prefer sha1 as it is faster than md5
        str_longhash = ""
        return str_filetime, str_filesize, str_shorthas, str_longhash, str_scantime
    except FileNotFoundError:  # some files are very temporary ...
        return "", "", "", "", str_scantime


def add_file2db(str_ffn, db):
    # print(f"Add file: {str_ffn}")
    str_fields = "filename, filetime, filesize, shorthash, longhash, scantime"
    try:
        str_filetime, str_filesize, str_shorthas, str_longhash, str_scantime = scan_file(str_ffn)
        str_ffn = str_ffn.replace("'", "''")  # ToDo This is not a solid way to handle filenames that include '
        str_sql = f"INSERT INTO files ({str_fields}) VALUES ('{str_ffn}', '{str_filetime}', '{str_filesize}', '{str_shorthas}', '{str_longhash}', '{str_scantime}');"
        ##print(f"add_file2db(); sql: {str_sql}")
        db.execute(str_sql)
        db.commit()
    except FileNotFoundError:
        pass  # some files are very temporary ...


def add_longhash_2_shorthash(shorthash, db):
    str_sql_sel = f"SELECT * FROM files WHERE shorthash = '{shorthash}'"
    for row in db.execute(str_sql_sel):
        ##print(f"* {row}")
        if os.path.isfile(row[0]):
            str_longhash = co.hashafile(row[0], algorithm='sha1', max_chunks=1)
            str_sql_upd = f'UPDATE files SET longhash = "{str_longhash}" WHERE filename = "{row[0]}" and shorthash = "{shorthash}";'  # Name should be unique, but better safe than wrong
            ##print(str_sql_upd)
            db.execute(str_sql_upd)
            db.commit()


def scan_root(str_ri, lst_rx, lst_rxe, db):
    """
    Scan one root-dir lst_ri, but skipping sub-dirs listed in lst_rx
    :param str_ri: string, the root dir
    :param lst_rx: list of exceptions, sub dirs that should be skipped
    :return: tbd
    """
    print(f"scan_root(); Scanning: {str_ri, lst_rx, lst_rxe}")
    # get db info on this dir
    dic_db = dict()  # dic by ffn of files known to the db
    str_sql = f"SELECT * FROM files where filename like '{str_ri}%'"
    for row in db.execute(str_sql):
        dic_db[row[0]] = row
    # Remove files that no longer exist
    lst_del_this = list()
    for str_ffn_db in dic_db.keys():
        if not os.path.isfile(str_ffn_db):
            lst_del_this.append(str_ffn_db)
            str_ffn_db__sql = str_ffn_db.replace("'", "''")
            str_sql = f"DELETE FROM files WHERE filename='{str_ffn_db__sql}';"
            db.execute(str_sql)
            db.commit()
    for itm in lst_del_this:  # can't change iterable from inside loop
        del dic_db[itm]
    # Walk the root-dir
    num_cntfil = 0
    for root, dirs, files in os.walk(str_ri):
        for str_fn in files:
            # if str_fn.lower().endswith('.jpg'):
            #     print(str_fn)
            num_cntfil += 1
            if not any([str_fn.endswith(e) for e in lst_rxe]):
                str_ffn = os.path.join(root, str_fn)
                if not any([str_ffn.startswith(x) for x in lst_rx]):  # if the file is not excluded
                    if str_ffn in dic_db.keys():  # db knows this file
                        obj_bdg = dic_db[str_ffn]
                        tim, siz = timeandsize(str_ffn)
                        if tim == dic_db[str_ffn][1] and siz == dic_db[str_ffn][2]:
                            pass  # print(f" - skipping known file: {str_ffn} == {dic_db[str_ffn]}")  #
                        else:
                            ## print(f"WTF: tim? {tim == dic_db[str_ffn][1]} siz? {siz == dic_db[str_ffn][2]} @ ffn: {str_ffn}")
                            # time or date have changed - so re-scanning file, and update DB.
                            str_sql = f"DELETE FROM files WHERE filename='{str_ffn}';"
                            db.execute(str_sql)
                            db.commit()
                            add_file2db(str_ffn, db)
                    else:  # db don't know this file - add it.
                        add_file2db(str_ffn, db)
                if num_cntfil % 1000000 == 0:
                    print(f"Count: {num_cntfil}: {str_ffn}")


def scan_rootlists(lst_ri, lst_rx, lst_rxe, db):
    """
    Scan all roots in rootlist lst_ri, though never the exceptions in lst_rx
    :param lst_ri:
    :param lst_rx:
    :return:
    """
    for root in lst_ri:
        lst_rxs = [tok for tok in lst_rx if tok.find(root) >= 0]
        print(f"\nscan_rootlists(); Clear to scan: ri: {root}, xs: {lst_rxs}")
        scan_root(root, lst_rxs, lst_rxe, db)


def prioritize_candidates(lst_cand):
    """ For a list of candidates, assign priority to each
    The more priority, the less likely to get kicked ...
    :param lst_cand:
    :return:
    """
    print(f"\nprioritize_candidates(); len = {len(lst_cand)}")
    if len(lst_cand) > 1:
        for n in range(len(lst_cand)):
            nc = list(lst_cand[n])
            nc.insert(0,0)
            lst_cand[n] = nc
        for cand in lst_cand:
            # some text adds p
            if cand[1].find("Okay") > -1:
                cand[0] += 10
            if cand[1].lower().find("serie") > -1:
                cand[0] += 10
            if cand[1].find("__NAM") > -1:
                cand[0] += 10
            if cand[1].find("BIX_") > -1:
                cand[0] += 10
            if cand[1].find("REF_") > -1:
                cand[0] += 10
            if cand[1].find("veracrypt1") > -1:
                cand[0] += 100
            if cand[1].find("veracrypt2") > -1:
                cand[0] += -10
            # some text cost p
            if any([cand[1].find(f"-{n}") > -1 for n in range(9)]):
                cand[0] -= 5
            if cand[1].find("DEL") > -1:
                cand[0] -= 10
            if cand[1].find("copy") > -1:
                cand[0] -= 5
            if cand[1].find("output") > -1:
                cand[0] -= 6
            if cand[1].find(".part") > -1:
                cand[0] -= 9
            # deeper path adds p
            cand[0] += cand[1].count(os.sep)
        # If still even, older is better
        lst_top = [cand for cand in sorted(lst_cand, reverse=True)]
        if lst_top[0][0] == lst_top[1][0]:  # No winner
            if lst_top[0][2] < lst_top[1][2]:  # head is oldest
                lst_top[0][0] += 1
            else:
                lst_top[1][0] += 1
        return lst_top
    else:  # Too few to prioritize
        return lst_cand  # return unchanged


def main():

    db = co.db()
    print(f"SC has a SQLite connection: {db}")
    print(f"argvar: {sys.argv[1:]}")  # ToDo: Take argvar out of main()

    # fill/update the db
    lst_ri, lst_rx, lst_rxe = make_rootlists(db)
    # lst_ri.append(r"/home/martin/MEGA/Private/Publications_My")
    print(f"main(); Go w: {lst_ri, lst_rx, lst_rxe}")
    scan_rootlists(lst_ri, lst_rx, lst_rxe, db)

    # Look for short collisions
    print(f"Look for short collisions...")
    str_sql = f"SELECT * FROM collision_short"
    for row in db.execute(str_sql):
        # print(f"main(); short collision: {row}")
        add_longhash_2_shorthash(row[1], db)

    # Look for long collisions
    print(f"Look for Long collisions")
    str_sql_sellong = f"SELECT * FROM collision_long;"
    num_space = 0
    lst_kill = list()
    for row_long in db.execute(str_sql):
        lst_cand = list()
        str_sql_selcand = f'SELECT * from files where longhash = "{row_long[1]}"'
        for row_cand in db.execute(str_sql_selcand):
            lst_cand.append(row_cand)
        # Handle candidates
        ##print("------")
        lst_cand = prioritize_candidates(lst_cand)  # Remember Priority added to head, so all other shift +1
        for cand in sorted(lst_cand, reverse=True):
            print(f" << {cand}")
        num_space += sum([itm[3] for itm in sorted(lst_cand, reverse=True)][1:])
        lst_kill.extend([itm[1] for itm in sorted(lst_cand, reverse=True)][1:])
    print(f"space: {num_space}")
    for kill in lst_kill:
        print(f'rm "{kill}"')


if __name__ == '__main__':
    main()