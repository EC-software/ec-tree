
import os

# Single dir (this dir) only
# for count, f in enumerate(os.listdir()):
#     if not f.endswith('.py'):
#         if '_' in f:
#             os.rename(f, f.split('_')[1])

# tavle all sub-dirs
for dirpath, dnames, fnames in os.walk("./"):
    for f in fnames:
        if not f.endswith('.py') \
                and '_' in f \
                and all([c.isdigit for c in f.split('_')[0]]):
            os.rename(f, f.split('_')[1])