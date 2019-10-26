
""" EC Tree Scan
Reads a file as made by ectreescan, and finds duplicate files """

import os
import datetime
import json

str_rootdir = r"/home/martin/Desktop/foto"  # /Camera Uploads"
str_rootdir = r"/home/martin/.TMP"  # /Camera Uploads"

with open(str_rootdir + os.sep + '.ectree', 'r') as fil_tree:
    dic_tree = json.load(fil_tree)

del fil_tree  # Clean house

dic_conf = dict()  # Dictionary of conflicts
for key_short in dic_tree.keys():
    if key_short != 'timestamp':
        if len(dic_tree[key_short].keys()) > 1:
            #print("collision_Short: {}".format(key_short))
            dic_cols = dic_tree[key_short]  # shorthand to save typing
            for fil_sus in dic_cols.keys():
                #print("             hl: {} f: {}".format(dic_cols[fil_sus]['hash_full'], fil_sus))
                if not dic_cols[fil_sus]['hash_full'] in dic_conf.keys():
                    dic_conf[dic_cols[fil_sus]['hash_full']] = list()
                dic_conf[dic_cols[fil_sus]['hash_full']].append(fil_sus)
            # Remove entries that were not real conflicts, i.e. not same long_hash
            lst_del = list()
            for hash_long in dic_conf.keys():
                if len(list(set(dic_conf[hash_long]))) <= 1:
                    lst_del.append(hash_long)  # Don't change dic in loop
            for hash_long in lst_del:
                del dic_conf[hash_long]
print("Reals conclicts: {}, {}".format(len(dic_conf), dic_conf))

del dic_tree, dic_cols, fil_sus, hash_long, key_short, lst_del  # Clean house...

# Save Real-conflicts to json file, for reference
str_fn_rc = 'real_conflicts_'+datetime.datetime.now().isoformat().split('.')[0].replace('-', '_').replace(':', '_') + '.ectree'
str_ffn_rc = str_rootdir + os.sep + str_fn_rc
fil_rc = open(str_ffn_rc, 'w')
json.dump(dic_conf, fil_rc)
fil_rc.close()

# Prioritise and make remove-file
# Priorities:
#  - tags in filename, e.g. 'copy'
#  - Ranking sibling dirs, e.g. /NAM over /NEW
#  - Keep deeper dirs

def prio_tags(lst_ffn, lst_tag=[]):
    """"""
    LST_DEFAULT_TAGS = ['copy', 'backup']
    if len(lst_ffn) <= 1:  # No more to prioritise
        return lst_ffn
    for tag in LST_DEFAULT_TAGS:  # Make sure these tags are checked, though last.
        if tag not in lst_tag:
            lst_tag.append(tag)
    for tag in lst_tag:
        for fn, ffn in [(ffn.rsplit(os.sep, 1)[0], ffn) for ffn in lst_ffn]:
            if tag in fn.lower():
                lst_ffn.remove(ffn)
                lst_ffn = prio_tags(lst_ffn, lst_tag)
                return lst_ffn
    return lst_ffn
