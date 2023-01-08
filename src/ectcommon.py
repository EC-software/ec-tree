
""" functions common to several modules """

import hashlib
import os
import sqlite3
import sys


def db():
    """
    Create connection to the db
    :return: connection
    """
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
                print(f"db() opened {str_dbfn} found in {FN}")
                return sqlite3.connect(str_dbfn)  # Also creates the DB if not exists
            else:
                print(".conf SQLite entry, holds no name")
                sys.exit(3)
        else:
            print(".conf SQLite entry, holds no valid format")
            sys.exit(2)
    else:
        print(".conf file holds no SQLite entry")
        sys.exit(1)


def hashafile(str_full_path, algorithm='md5', max_chunks=0):
    if algorithm == 'sha1':
        hash_alg = hashlib.sha1()  # Frequently used, speed access
    elif algorithm in hashlib.algorithms_available:
        hash_alg = hashlib.new(algorithm)
    else:
        hash_alg = hashlib.md5()  # It's our default
    with open(str_full_path, "rb") as f:
        num_chunk = 0
        for chunk in iter(lambda: f.read(65536), b""):  # 64k buffer
            hash_alg.update(chunk)
            num_chunk += 1
            if max_chunks > 0 and num_chunk >= max_chunks:
                return hash_alg.hexdigest()
    return hash_alg.hexdigest()

