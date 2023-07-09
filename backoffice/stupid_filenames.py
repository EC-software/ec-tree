import os

str_bad = ")(!'&%¤#+*‿’▶►◄`,😻🛁•▷🥇"

num_cntfil = 0
for root, dirs, files in os.walk("/media/veracrypt1"):  # "/home/output"):
    for str_fn in files:
        if any([tok in str_fn for tok in str_bad]):
            print(str_fn)
            newname = str_fn
            for l in str_bad:
                newname = newname.replace(l, '_')
            while '__' in newname:
                newname = newname.replace('__', '_')
            str_old_ffn = os.path.join(root, str_fn)
            str_new_ffn = os.path.join(root, newname)
            os.rename(str_old_ffn, str_new_ffn)
        num_cntfil += 1
print(num_cntfil)

       # str_ffn = os.path.join(root, str_fn)