
#!/usr/bin/env python3

import shutil

file = "/"  # __file__
total, used, free = shutil.disk_usage(file)
print(f'infil: {file}\ntotal: {total}\n used: {used} = {round(used*100/total)}%\n free: {free} = {round(free*100/total)}%')