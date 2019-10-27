

""" Search for duplicate files, using the .ect files """

import os
import pprint

import ec_tree_basics as ectb


def join_dics(dic_a, dic_b):
    for key_bh in dic_b.keys():
        if key_bh not in dic_a.keys():
            dic_a[key_bh] = dic_b[key_bh]  # The easy case, with new top key
        else:
            for key_bhf in dic_b[key_bh].keys():
                if key_bhf in dic_a[key_bh].keys():  # Bummer - same file name in two dirs
    return dic_a

def ect_acc(str_dir, dic_ect_acc=dict()):
    """ Recursively call all sub-dirs, load the .ect file and accumulate the contents """
    lst_only_dirs = [d for d in os.listdir(str_dir) if os.path.isdir(os.path.join(str_dir, d))]
    for itm in lst_only_dirs:
        ect_acc(str_dir + os.sep + itm, dic_ect_acc)  # First go into sub directories
        str_ect_ffn = str_dir + os.sep + itm  # Then add the local .ect on the way back
        dic_ect = ectb.read_ect_file(str_ect_ffn)
        for key_h in dic_ect.keys():
            for key_f in dic_ect[key_h].keys():
                dic_ect[key_h][key_f]['dir'] = str_dir
        dic_ect_acc = join_dics(dic_ect_acc, dic_ect)
    return dic_ect_acc

if __name__ == "__main__":
    #ect(__file__.rsplit(os.sep, 1)[0])  # run in current directory
    dic_accu = ect_acc(r"/home/martin/Download")  # run in specific directory
    pprint.pprint(dic_accu)