#!/usr/bin/python

import os
import string
src_dir = r"/csmsp/.TMP"  # "/media/veracrypt2/NCLN_3" # ):
ZONEY = r"/csmsp/.TMP"  # "/media/veracrypt2/NCLN_3"
# src_dir = "/media/veracrypt1" # "/home/output/.TMP" # /.TMP/NEWS_1"):
# ZONEY = "/media/veracrypt1" # "/home/output/.TMP"

for root, dirs, files in os.walk(src_dir):
    for file in files:
        str_ffn = os.path.join(root, file)
        #print(str_ffn)
        num_fs = os.stat(str_ffn).st_size
        if num_fs < 100:
            print(f"size: {num_fs} file: {file}")
            os.remove(str_ffn) # removes a file.
for dirpath, _, _ in os.walk(src_dir, topdown=False):
    if dirpath == src_dir:
        break
    try:
        os.rmdir(dirpath)
        print(f"mkdir {dirpath}")
    except OSError as ex:
        pass  # print(f"Fail:: {ex}")
