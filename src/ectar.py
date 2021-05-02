
""" Add root to the db """

import sys
import ectcommon as co


db = co.db()
##print(f"AR has a SQLite connection: {db}")


def add_root(db, str_root, str_mode):
    """ Add a str_root and str_mode to the db, if not all ready known to the db
    :param db: tha data base
    :param str_root: the root - a string describing a directory path
    :param str_mode: the mode - a string containing 'I' or 'X' (include or exclude)
    :return: n/a
    """
    bol_known = False  # Assume unknown to the db, until proven otherwise
    for row in db.execute(f"SELECT * FROM roots where path = '{str_root}' and mode = '{str_mode}'"):
        bol_known = True
    if not bol_known:  # Insert if not existing
        str_sql = f"INSERT INTO roots VALUES ('{str_mode}', '{str_root}')"
        print(f"SQL: {str_sql}")
        db.execute(str_sql)
        db.commit()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        str_mode = sys.argv[1]
        str_root = sys.argv[2]
        add_root(db, str_root, str_mode)
        # ToDo Check for nested roots with same mode
        # ToDo Check for samme root with opposite mode
    else:
        print(f"Expected command line parameter as input: <mode> <path>, found: {sys.argv[1:]}")
