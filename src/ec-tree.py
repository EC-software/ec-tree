

""" Bla, bla, bla ...
Recursive, distributed solution. Maintains a .ec-tree file en every dir """

import os
import datetime
import json
import hashlib

# CONSTANTS
ect_fn = ".ect"
max_chunks = 1


def read_ect_file(str_ect_ffn):
    if os.path.isfile(str_ect_ffn):
        with open(str_ect_ffn, 'r') as fil_in:
            dic_ect = json.load(fil_in)
    else:
        dic_ect = dict()
    return dic_ect


def write_ect_file(str_ect_ffn, dic_ect):
    with open(str_ect_ffn, 'w') as fil_ou:
        json.dump(dic_ect, fil_ou)


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


def ect_upd_dir(str_dir):
    """ Updates the local .ect file with info on the local file in this dir
    The .ect file is only filled with short-hash and file-size - Long-hash is only calculated when needed.
    For files all ready in the .ect, data is only updated if the file is changed since the .ect record. """

    def refresh_file_record(fil_n, dic_ect):
        str_hash = hashafile(str_dir + os.sep + fil_n, 'sha1', max_chunks)
        if not str_hash in dic_ect.keys():  # In the unlikely event that other files have same short-hash
            dic_ect[str_hash] = dict()
        dic_ect[str_hash][fil_n] = dict()
        dic_ect[str_hash][fil_n]['last_check'] = datetime.datetime.now().isoformat().replace('T',' ')
        dic_ect[str_hash][fil_n]['size'] = os.stat(str_dir + os.sep + fil_n).st_size
        return dic_ect

    # Consider
    if r"/.cache/" in str_dir:
        return  # Don't .ect in the cache area ...
    # /.PyCharmCE2019.2/
    # .eclipse
    # .mozilla
    # .thunderbird
    # .config
    # .local

    str_ect_ffn = str_dir + os.sep + ect_fn
    print("ect_upd: {}".format(str_ect_ffn))
    dic_ect = read_ect_file(str_ect_ffn)

    # Remove .ect records for deletaed files
    lst_removals = list()
    for has in dic_ect.keys():
        for fil in dic_ect[has].keys():
            if not os.path.isfile(os.path.join(str_dir, fil)):
                lst_removals.append((has,fil))
    for remo in lst_removals:
        del dic_ect[remo[0]]
    lst_removals = list()
    for has in dic_ect.keys():
        if len(dic_ect[has].keys()) == 0:
            lst_removals.append(has)
    for remo in lst_removals:
        del dic_ect[remo]

    # Refresh .ect for all existing files
    lst_only_files = [f for f in os.listdir(str_dir) if os.path.isfile(os.path.join(str_dir, f))]
    for fil_n in lst_only_files:
        if fil_n != ect_fn:
            ##print(" > fil: {}".format(str_dir + os.sep + fil_n))
            lst_hash_old = [key_short for key_short in dic_ect.keys() if fil_n in dic_ect[key_short].keys()]
            if len(lst_hash_old) > 0: # if itm is in existing .ect
                if len(lst_hash_old) == 1:
                    ##print(" existing: {}".format(fil_n))
                    bol_changed = False  # Assume the file is unchanged, until proven otherwise.
                    str_hash_old = lst_hash_old[0]
                    # Check date
                    flt_timestamp = os.path.getmtime(str_dir + os.sep + fil_n)
                    ddt_file = datetime.datetime.fromtimestamp(flt_timestamp)
                    str_last = dic_ect[str_hash_old][fil_n]['last_check']
                    ddt_last = datetime.datetime.strptime(str_last, '%Y-%m-%d %H:%M:%S.%f')
                    if ddt_file > ddt_last:  # File was changed since last check
                        print("File was changed DATE")
                        bol_changed = True
                    # Check date and size
                    num_size_file = os.stat(str_dir + os.sep + fil_n).st_size
                    num_size_last = dic_ect[str_hash_old][fil_n]['size']
                    if num_size_file != num_size_last:
                        print("File was changed SIZE")
                        bol_changed = True
                    if bol_changed:  # File has changed, remap it ...
                        if len(dic_ect[str_hash_old].keys()) > 1:
                            del dic_ect[str_hash_old][fil_n]
                        else:
                            del dic_ect[str_hash_old]
                        dic_ect = refresh_file_record(fil_n, dic_ect)
                else:
                    print("Multible entries for file {} That is strange!!!".format(fil_n))
            else:  # file not known to .ect
                dic_ect = refresh_file_record(fil_n, dic_ect)
    write_ect_file(str_ect_ffn, dic_ect)

def ect(str_dir):
    """ Recursively call all sub-dirs, then make a .ect file with the local files only (can be empty) """
    # First: Sub-dirs
    lst_only_dirs = [d for d in os.listdir(str_dir) if os.path.isdir(os.path.join(str_dir, d))]
    for itm in lst_only_dirs:
        ect(str_dir + os.sep + itm)
    # Second: Local files
    ect_upd_dir(str_dir)


if __name__ == "__main__":
    #ect(__file__.rsplit(os.sep, 1)[0])  # run in current directory
    ect(r"/home/martin")  # run in specific directory