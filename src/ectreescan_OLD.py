
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

# Constants
NUM_MIN_SIZE = 1024

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


def main(str_rootdir, lst_protected_types):

    fil_ectree = open(str_rootdir+os.sep+'.ectree', 'w')  # Making sure we have write access.
    fil_longco = open(str_rootdir+os.sep+'collisions_remover.sh', "w")

    dic_tree = dict()
    max_chunks = 1

    print("Scanning: {}".format(str_rootdir))
    dtt_start = datetime.datetime.now()
    for dir, lst_subdir, lst_file in os.walk(str_rootdir):
        for str_fn in lst_file:
            if '.' in str_fn and str_fn.rsplit('.', 1)[1] not in lst_protected_types:
                if str_fn.lower() != '.ectree':
                    str_fullfn = dir+os.sep+str_fn
                    #dic_tree = time_algos(str_fullfn, dic_tree)
                    str_hash = hashafile(str_fullfn, 'sha1', max_chunks)
                    #print("h: {} f: {}".format(str_hash, str_fullfn))
                    if not str_hash in dic_tree.keys():
                        dic_tree[str_hash] = dict()
                    dic_tree[str_hash][str_fullfn] = dict()
                    dic_tree[str_hash][str_fullfn]['last_check'] = datetime.datetime.now().isoformat()

    # Look for short, collisions
    print("Looking through short collisions: {}".format(str_rootdir))
    for key_short in dic_tree.keys():
        if len(dic_tree[key_short].keys()) > 1:
            #print("collision_Short: {}".format(key_short))
            for fil in dic_tree[key_short].keys():
                dic_tree[key_short][fil]['hash_full'] = hashafile(fil, 'sha1', 0)  # Full Hash
                dic_tree[key_short][fil]['last_check'] = datetime.datetime.now().isoformat()
                dic_tree[key_short][fil]['size'] = os.stat(fil).st_size

    # timestamp the .ectree scan
    dic_tree['timestamp'] = datetime.datetime.now().isoformat()

    num_run_dur = (datetime.datetime.now() - dtt_start).total_seconds()

    json.dump(dic_tree, fil_ectree)

    fil_ectree.close()

    #print('Full dic as pretty')
    #pprint.pprint(dic_tree)

    # Look for real (long) Collisions
    print("Looking through long collisions: {}".format(str_rootdir))
    dic_long = dict()
    for key_short in dic_tree.keys():
        if isinstance(dic_tree[key_short], dict):  # Ignore dic_tree['timestamp'] etc.
            if len(dic_tree[key_short].keys()) > 1:  # There is a short collision
                for fil in dic_tree[key_short].keys():
                    if not dic_tree[key_short][fil]['hash_full'] in dic_long.keys():
                        ##print("Opening Long list: {}".format(dic_tree[key_short][fil]['hash_full']))
                        dic_long[dic_tree[key_short][fil]['hash_full']] = list()
                    if dic_tree[key_short][fil]['size'] > NUM_MIN_SIZE:
                        ##print(" Add to Long list: {}".format(fil))
                        # Add (priority, filename, size)
                        dic_long[dic_tree[key_short][fil]['hash_full']].append([0, fil, dic_tree[key_short][fil]['size']])

    # Try to prioritise which long-collision copy to keep
    # Filename contains specific strings
    lst_mad_words = ['copy', 'cpy', 'backup', 'extra', '(1)', '.lnk']
    lst_god_words = ['FREE', 'COMM']
    for long_colis in dic_long.keys():
        for colis in dic_long[long_colis]:
            for str_god in lst_god_words:
                if str_god in colis[1]:
                    colis[0] -= 1
            for str_mad in lst_mad_words:
                if str_mad in colis[1]:
                    colis[0] += 1
    # one is in a subdir, relative to the other
    for long_colis in dic_long.keys():
        for colis in dic_long[long_colis]:
            str_this_dir = colis[1].rsplit(os.sep, 1)[0]
            for other_colis in dic_long[long_colis]:
                str_othr_dir = other_colis[1].rsplit(os.sep, 1)[0]
                if str_this_dir != str_othr_dir:  # Donøt compare to same dir
                    if str_othr_dir.find(str_this_dir) >= 0:
                        colis[0] += 1
                    if str_this_dir.find(str_othr_dir) >= 0:
                        other_colis[0] += 1
    # Cibling directories prioritising
    # TBD

    # write remove strings
    lst_rm = list()
    for long_colis in dic_long.keys():
        for colis in sorted(dic_long[long_colis])[1:]:  # Spare the first, with lowest priority for deletion
            str_rm = 'rm "{}"'.format(colis[1])
            print(str_rm)
            lst_rm.append(str_rm)

    # Write Longcollision file
    print("Writing output files: ")
    for long_colis in dic_long.keys():
        fil_longco.write("# Collision : {}\n".format(long_colis))
        for colis in dic_long[long_colis]:
            fil_longco.write("# - {}\n".format(colis))
    for str_rm in lst_rm:
        fil_longco.write(str_rm+'\n')
    fil_longco.close()

    print("Done in: {} seconds".format(num_run_dur))


if __name__ == '__main__':

    str_rootdir = r"/home/martin/Desktop/foto" #/Camera Uploads"
    str_rootdir = r"/home/martin/Music"
    str_rootdir = r"/home/martin/Guru_and_Books"

    lst_protected_types = ['gif','svg','js','jpg','png','html','css','py','js','doc','wav']

    main(str_rootdir, lst_protected_types)
