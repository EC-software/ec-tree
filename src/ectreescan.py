
""" EC Tree Scan
Starting in the given directory, walks the entire sub-tree, and register all files.
Writes a file with the findings. """


import os
import datetime
import hashlib

rootDir = r"/home/martin/Desktop/foto"


def hashafile(str_full_path, algorithm='md5'):
    if algorithm in hashlib.algorithms_available:
        hash_alg = hashlib.new(algorithm)
    else:
        print("Available hash algorithms are: {}".format(hashlib.algorithms_available))
        hash_alg = hashlib.md5()  # It's our default
    with open(str_full_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_alg.update(chunk)
    return hash_alg.hexdigest()

def time_algos(str_full_path, dic_times=None):
    print("timing: {}".format(str_full_path))
    lst_algo = [itm for itm in hashlib.algorithms_available if not itm in ['shake_128', 'shake_256']]
    if not dic_times:
        dic_times = dict()
        for algo in lst_algo:
            dic_times[algo] = 0
    for algo in lst_algo:
        print("go: {}".format(algo))
        dtt_a = datetime.datetime.now()
        str_hash = hashafile(str_full_path, algo)
        dur_a = datetime.datetime.now() - dtt_a
        dic_times[algo] += dur_a.total_seconds()
        print(" << {} in {}".format(str_hash, dur_a.total_seconds()))
    return dic_times

dic_tree = dict()

for dir, lst_subdir, lst_file in os.walk(rootDir):
    #print("Dir: {}".format(dir))
    for str_fn in lst_file:
        #print("{} / {}".format(dir, str_fn))
        # print(hashafile(dir+os.sep+str_fn, 'odd'))
        if str_fn == 'MOV_0060.mp4':
            dic_t = time_algos(dir+os.sep+str_fn)
            for key_a in sorted(dic_t.keys()):
                print("k: {} t: {}".format(key_a, dic_t[key_a]))