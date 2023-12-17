
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
        return {}

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
                    ffn_r = os.path.join(str_dir_, file)
                    ffn_t = os.path.join(str_dirt, file)
                    dic_ret[ffn_r] = {'otyp': 'fil'}
                    if os.path.isfile(ffn_t):
                        dic_ret[ffn_r]['xsts'] = 'both'
                        dic_ret[ffn_r]['cofp'] = cofp(ffn_r, ffn_t)
                    else:
                        dic_ret[ffn_r]['xsts'] = 'refe'
            else:
                dic_ret[str_dir_]['xsts'] = 'refe'
    print("<<< End R scan >>>")
    pprint.pprint(dic_ret)
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
    print("<<< End T scan >>>")
    return dic_ret


def tcd(tco) -> str:
    """ Read a tco dictionary from function tco(), and turn it into a human friendly description
    Return: str: text description of the contents in the tco """

    return str(tco)

if __name__ == "__main__":
    TR = "/home/martin/Repos/ec-tree/treecomp/data/R"
    TT = "/home/martin/Repos/ec-tree/treecomp/data/T"
    pprint.pprint(tco(TR, TT))
    # print(tcd(tco(TR, TT)))

    # for root, dirs, files in os.walk(tr, topdown=True, onerror=None, followlinks=False):  # Walk Reference dir
    #     for file in files:
    #         ffn = os.path.join(root, file)
    #         if os.path.isfile(ffn):
    #             print(f"fil: {ffn}")