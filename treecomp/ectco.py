
""" EC tree - Tree Compare
    Compare two trees ... """

__version__ = "0.2.0"

# History
# ver. 0.1 Init working version

import os
import pprint

TR = ""  # Tree Reference
TT = ""  # Tree Target

def tco(tr=TR, tt=TT) -> dict:
    """ Compares two directories, recursively, and point out all similarities and differences
    Resulting data type is designed to be transformed to text description by function tcd()
    return dictionary of results """
    # print(f"dr: {tr}\ndt: {tt}")

    def cofp(ffna, ffnb) -> dict:
        """ Compare file pair
        return dict with result """
        assert os.path.isfile(ffna)
        assert os.path.isfile(ffnb)
        stat_a = os.stat(ffna)
        stat_b = os.stat(ffnb)
        # print(f"\tR: {stat_a})")
        # print(f"\tT: {stat_b})")
        dic_cofp = dict()
        # st_mode - File mode: file type and file mode bits (permissions).
        # st_ino - Platform dependent, but if non-zero, uniquely identifies the file for a given value of st_dev. Typically: the inode number on Unix; the file index on Windows
        # st_dev - Identifier of the device on which this file resides.
        # st_nlink - Number of hard links.
        # st_uid - User identifier of the file owner.
        # st_gid - Group identifier of the file owner.
        # st_size - Size of the file in bytes, if it is a regular file or a symbolic link. The size of a symbolic link is the length of the pathname it contains, without a terminating null byte.
        if stat_a.st_size > stat_b.st_size:
            dic_cofp['refe_size'] = '>'
        elif stat_a.st_size < stat_b.st_size:
            dic_cofp['refe_size'] = '<'
        else:
            dic_cofp['refe_size'] = '='
        # st_atime - Time of most recent access expressed in seconds.
        # st_mtime - Time of most recent content modification expressed in seconds.
        if stat_a.st_mtime > stat_b.st_mtime:
            dic_cofp['refe_mtime'] = '>'
        elif stat_a.st_mtime < stat_b.st_mtime:
            dic_cofp['refe_mtime'] = '<'
        else:
            dic_cofp['refe_mtime'] = '='
        # st_ctime - Time of most recent metadata change expressed in seconds. Changed in version 3.12: st_ctime is deprecated on Windows. Use st_birthtime for the file creation time. In the future, st_ctime will contain the time of the most recent metadata change, as for other platforms.

        return dic_cofp

    assert all(os.path.isdir(tok) for tok in [tr, tt])
    dic_ret = dict()
    for path, dirnames, filenames in os.walk(tr):  # Walk reference to establish basis
        str_dirr = str(path)
        str_dirt = str_dirr.replace(tr, tt)
        str_dir_ = str_dirr.replace(tr, '')
        if str_dir_ not in dic_ret.keys():
            dic_ret[str_dir_] = {'otyp': 'dir'}
            if os.path.isdir(str_dirt):  # Dir also in target
                dic_ret[str_dir_]['xsts'] = 'both'
                for file in filenames:  # check the files
                    ffn_r = os.path.join(str_dirr, file)
                    ffn_t = os.path.join(str_dirt, file)
                    ffn__ = ffn_r.replace(tr, '')
                    dic_ret[ffn__] = {'otyp': 'fil'}
                    if os.path.isfile(ffn_t):
                        dic_ret[ffn__]['xsts'] = 'both'
                        dic_ret[ffn__]['cofp'] = cofp(ffn_r, ffn_t)
                    else:
                        dic_ret[ffn__]['xsts'] = 'refe'
            else:
                dic_ret[str_dir_]['xsts'] = 'refe'
    # print("<<< End R scan >>>")
    # pprint.pprint(dic_ret)
    for path, dirnames, filenames in os.walk(tt):  # Walk target to find target-only objects
        str_dirt = str(path)
        str_dirr = str_dirt.replace(tt, tr)
        str_dir_ = str_dirr.replace(tr, '')
        if str_dir_ not in dic_ret.keys():
            dic_ret[str_dir_] = {'otyp': 'dir', 'xsts': 'trgt'}
        for file in filenames:  # check the files
            # ffn_t = os.path.join(str_dirt, file)
            ffn_r = os.path.join(str_dirr, file)
            ffn__ = ffn_r.replace(tr, '')
            if ffn__ not in dic_ret.keys():
                dic_ret[ffn__] = {'otyp': 'fil', 'xsts': 'trgt'}
    # print("<<< End T scan >>>")
    return dic_ret


def tcd(tco) -> str:
    """ Read a tco dictionary from function tco(), and turn it into a human friendly description
    Return: str: text description of the contents in the tco """
    str_tcd = "# Header"
    for k in sorted(tco.keys()):
        if tco[k]['otyp'] == 'dir':
            otyp = 'd'
            if tco[k]['xsts'] == 'refe':
                xsts = r'//'
            elif tco[k]['xsts'] == 'trgt':
                xsts = r'\\'
            elif tco[k]['xsts'] == 'both':
                xsts = r'=='
        elif tco[k]['otyp'] == 'fil':
            otyp = 'f'
            if tco[k]['xsts'] == 'refe':
                xsts = r'//'
            elif tco[k]['xsts'] == 'trgt':
                xsts = r'\\'
            elif tco[k]['xsts'] == 'both':
                if 'cofp' in tco[k].keys():
                    xsts = f"{tco[k]['cofp']['refe_mtime']}{tco[k]['cofp']['refe_size']}"
                else:
                    xsts = r'**'
        str_tcd += f"\n{otyp}\t{xsts}\t{k}"
    return str_tcd

if __name__ == "__main__":
    TR = "/home/martin/Repos/ec-tree/treecomp/data/R"
    TT = "/home/martin/Repos/ec-tree/treecomp/data/T"
    TR = "/home/martin/Repos/bix"
    TT = "/home/martin/Repos/bix_2"
    print("--- tco() ---")
    tco_ = tco(TR, TT)
    # pprint.pprint(tco_)
    print("--- tcd() ---")
    tcd_ = tcd(tco_)
    print(tcd_)