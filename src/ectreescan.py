
""" EC Tree Scan
Starting in the given directory, walks the entire sub-tree, and register all files.
Writes a file with the findings. """


import os
import datetime
#import math
import json
import pprint
import hashlib

#import pyhash


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

def time_algos(str_full_path, dic_times=None):
    print("timing algos on: {}".format(str_full_path))
    lst_algo = [itm for itm in hashlib.algorithms_available if not itm in ['shake_128', 'shake_256']]
    lst_algo = ['md4', 'md5', 'sha1', 'sha512', 'blake2b', 'blake2b512']  # Focus on the fastets...
    if not dic_times or len(dic_times.keys()) < 1:
        dic_times = dict()
        dic_times['cnt'] = 0
        for algo in lst_algo:
            dic_times[algo] = 0
    for algo in lst_algo:
        dtt_a = datetime.datetime.now()
        str_hash = hashafile(str_full_path, algo)
        dur_a = datetime.datetime.now() - dtt_a
        dic_times[algo] += round(dur_a.total_seconds()*1000)
    dic_times['cnt'] += 1
    return dic_times


if __name__ == '__main__':

    str_rootdir = r"/home/martin/Desktop/foto"#/Camera Uploads"

    fil_ectree = open(str_rootdir+os.sep+'.ectree', 'w')  # Making sure we have write access.

    dic_tree = dict()
    max_chunks = 1

    dtt_start = datetime.datetime.now()
    for dir, lst_subdir, lst_file in os.walk(str_rootdir):
        for str_fn in lst_file:
            if str_fn.lower() != '.ectree':
                str_fullfn = dir+os.sep+str_fn
                #dic_tree = time_algos(str_fullfn, dic_tree)
                str_hash = hashafile(str_fullfn, 'sha1', max_chunks)
                #print("h: {} f: {}".format(str_hash, str_fullfn))
                if not str_hash in dic_tree.keys():
                    dic_tree[str_hash] = dict()
                dic_tree[str_hash][str_fullfn] = dict()
                dic_tree[str_hash][str_fullfn]['last_check'] = datetime.datetime.now().isoformat()

    # Look for short collisions
    for key_short in dic_tree.keys():
        if len(dic_tree[key_short].keys()) > 1:
            print("collision_Short: {}".format(key_short))
            for fil in dic_tree[key_short].keys():
                print("  f: {}".format(fil))
                str_hash_full = hashafile(fil, 'sha1', 0)
                dic_tree[key_short][fil]['hash_full'] = str_hash_full
                dic_tree[key_short][fil]['last_check'] = datetime.datetime.now().isoformat()

    # timestamp the .ectree scan
    dic_tree['timestamp'] = datetime.datetime.now().isoformat()

    print("Done in: {} seconds".format((datetime.datetime.now() - dtt_start).total_seconds()))

    json.dump(dic_tree, fil_ectree)

    fil_ectree.close()

    #pprint.pprint(dic_tree)