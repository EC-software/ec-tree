
""" Reload the test data to initial situation,
    i.e. move all files from LAO and THA to MMR """

# after git filter-repo --force --strip-blobs-bigger-than 10M

import os
import shutil
import stat

KNOWN_METHODS = ["os.", "shutil.", "cmd"]


def movefile_byos(src, dst):
    print(f"Move: {src} --> {dst}, by os.")
    try:
        with open(src, 'br') as fil_in:
            with open(dst, 'bw') as fil_ou:
                fil_ou.write(fil_in.read())
    except:
        print(f"Can't copy file with os.: {src} --> {dst}")
        return 101
    os.remove(src)


def movefile_byshutil(src, dst):
    print(f"Move: {src} --> {dst}, by .shutil")
    try:
        shutil.copyfile(src, dst)
    except OSError:
        return 201
    except:
        print(f"Can't move file with shutil: {src} --> {dst}")
        return 202
    os.remove(src)


def movefile_bycmd(src, dst):
    print(f"Move: {src} --> {dst}, by cmd")
    str_osname = os.name
    if str_osname == 'posix':  # Linux ----------------------------------------
        str_tmpfilename = r"__temp__file__.sh"
        with open(str_tmpfilename, 'w') as fil_cmd:
            fil_cmd.write(f"cp {src} {dst}\nrm {src}\n")
        os.chmod(str_tmpfilename, stat.S_IXUSR)
        os.system(str_tmpfilename)
        os.remove(str_tmpfilename)
    elif str_osname == 'nt':  # windows ---------------------------------------
        pass
    elif str_osname == 'java':  # Java ----------------------------------------
        print(f"Warning: movefile_bycmd() detects UNSUPPORTED OS: {str_osname}")
        return 302
    else:  # ------------------------------------------------------------------
        print(f"Warning: movefile_bycmd() detects unknown OS: {str_osname}")
        return 301


def moveall(str_fdn_from, str_fdn_to, method="none", ttt=3):
    """ move all files in dir_f to dir_t, No traveling sub-directories!
        using method (os., xxx. or cmd)
        ttt (time to try) default 3 """
    if method in KNOWN_METHODS:
        if method == "os.":
            for str_fn in os.listdir(str_fdn_from):
                movefile_byos(os.path.join(str_fdn_from, str_fn), os.path.join(str_fdn_to, str_fn))
        elif method == "shutil.":
            for str_fn in os.listdir(str_fdn_from):
                movefile_byshutil(os.path.join(str_fdn_from, str_fn), os.path.join(str_fdn_to, str_fn))
        elif method == "cmd":
            for str_fn in os.listdir(str_fdn_from):
                movefile_bycmd(os.path.join(str_fdn_from, str_fn), os.path.join(str_fdn_to, str_fn))
        else:
            raise ValueError(f"Error: something is out of wagg with method: {method} #2045")
    else:
        raise ValueError(f"Error: Unknown method: {method}")


def main():
    moveall("data/LAO", "data/MMR", "os.")
    moveall("data/THA", "data/MMR", "shutil.")
    moveall("data/XTR", "data/MMR", "cmd")


if __name__ == "__main__":
    main()