
import os

str_a = "../data2/"
str_b = "../data3/"
lst_targets = ['123456789', '438375583']

for dirpath, dnames, fnames in os.walk(str_a):
    print(dirpath, dnames, fnames)
    for f in fnames:
        print(f"c: {f}")
        if not f.endswith('.py') \
                and '_' in f \
                and len(f.split('_')[0]) == 6 \
                and all([c.isdigit for c in f.split('_')[0]]):
            if any([tok in f for tok in lst_targets]):
                print(f" * {f}")
                os.system(f'cp {os.path.join(str_a, f)} {os.path.join(str_b, f)}')
            print(f"   {f}")