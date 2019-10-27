
""" Functions used by several other ec-tree modules """

import os
import json


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