

""" Walk the dir, and sub-dirs, and delete all .ect files """

import os


def ect_cleanout(str_dir):
    """ Recursively call all sub-dirs, then delete the .ect file """
    lst_only_dirs = [d for d in os.listdir(str_dir) if os.path.isdir(os.path.join(str_dir, d))]
    for itm in lst_only_dirs:
        ect_cleanout(str_dir + os.sep + itm)
    str_local_ect_file_ffn = str_dir + r'/.ect'
    print("removing: {}".format(str_local_ect_file_ffn))
    try:
        os.remove(str_local_ect_file_ffn)
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    #ect(__file__.rsplit(os.sep, 1)[0])  # run in current directory
    ect_cleanout(r"/home/martin")  # run in specific directory
