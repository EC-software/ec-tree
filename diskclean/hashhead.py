
import os
import datetime
import hashlib

""" Hash the Head of each file """

root = r"/home/martin"
h = hashlib.sha256()
lst_sec = list()
n = 16  # How many Kb to sample for file head. 128 is about 0.0005 sec, larger non-linear

for root, dirs, files in os.walk(root):
    for name in files:
        fnfp = os.path.join(root, name)
        dtt_beg = datetime.datetime.now()
        try:
            with open(fnfp, 'rb') as fili:
                b = fili.read(n*1024)
                h.update(b)
            num_has = h.hexdigest()
            dur_rah = datetime.datetime.now() - dtt_beg
            if dur_rah.total_seconds() > 0.1:
                print(num_has, dur_rah.total_seconds(), fnfp)
            lst_sec.append(dur_rah.total_seconds())
        except:
            pass
print(sum(lst_sec) / float(len(lst_sec)))