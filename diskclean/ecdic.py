#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Maintain .ecdir file of a dir
    Modes:
        init: Create new .ecdic file. Overwrites existing .ecdic file(s)
        status: compare present state with .ecdir file(s). Newer changes .ecdir
        update: Change the .ecdir to reflect current state of dir
"""

import os, sys
import argparse
import pickle  # was used before json
import json
import datetime
import ec_hash

NUM_MIN_SIZE = 68719476736 # 64Gb, 10485760 # 10Mb, 1073741824 # 1Gb, 1048576 # 1Mb,
VERBOSE_SILENT = 0
VERBOSE_ERROR = 2
VERBOSE_WARNING = 4
VERBOSE_INFO = 6
VERBOSE_CHATTY = 8
VERBOSE_DEBUG = 10


def ecdic_save(dic_dir, str_fn):
    """ Save a ecdic to a file """
    verbose = args['verbose']
    if verbose >= VERBOSE_INFO:
        print("Saving to file: {}".format(str_fn))
    if len(dic_dir.keys()) > 0:
        #pickle.dump(dic_dir, open(str_fn, "wb"))
        json.dump(dic_dir, open(str_fn, "wb"))
    return


def ecdic_load(str_fn):
    """ Load a ecdic from a file """
    verbose = args['verbose']
    if verbose >= VERBOSE_INFO:
        print("Loading from file: {}".format(str_fn))
    #obj_ret = pickle.load(open(str_fn, "rb"))
    obj_ret = json.load(open(str_fn, "rb"))
    return obj_ret


def init(str_dir):
    """ Initializes a new .ecdic"""

    def _init1(str_dir, lst_files, exeptions=('.7z', '.csmsp')):
        """ Initialize this ONE dir only, no subdirs... """
        dic_dir = dict()
        for f in lst_files:
            if os.path.basename(f) == '.ecdir':
                continue
            if any([f.endswith(ext) for ext in exeptions]):
                continue
            else:
                str_fullpath = os.path.join(str_dir, f)
                str_basename = os.path.basename(f)
                statinfo = os.stat(str_fullpath)
                if statinfo.st_size < NUM_MIN_SIZE:  # True: #
                    hash = ec_hash.file_hash(str_fullpath, 'md5')  # 'md5_hash'  #
                    dic_dir[str_basename] = dict()
                    dic_dir[str_basename]['name'] = str_basename
                    dic_dir[str_basename]['size'] = statinfo.st_size
                    dic_dir[str_basename]['time'] = str(datetime.datetime.fromtimestamp(statinfo.st_mtime))
                    dic_dir[str_basename]['hash'] = hash
                    if verbose >= VERBOSE_CHATTY:
                        print(str_fullpath, hash)
        ecdic_save(dic_dir, os.path.join(str_dir, '.ecdir'))
        return

    verbose = args['verbose']
    if verbose >= VERBOSE_INFO:
        print("Creating new ecdir in: {}".format(str_dir))
    # Sort into Dirs and files
    lst_onlyfiles = list()
    lst_onlydirs = list()
    for fn in os.listdir(str_dir):
        ffn = os.path.join(str_dir, fn)
        if not os.path.islink(ffn):  # We don't want to register symbolic links
            if os.path.isfile(ffn):
                lst_onlyfiles.append(ffn)
            elif os.path.isdir(ffn):
                lst_onlydirs.append(ffn)
    #print(" dirs:", lst_onlydirs)
    #print(" fils:", lst_onlyfiles)
    # Handle the local files
    _init1(str_dir, lst_onlyfiles)
    # Handle sub-dirs
    if args['recursive']:
        for sdir in lst_onlydirs:
            init(sdir)
    return

def status(str_root):
    """ Status """
    print("Status for:", str_root)
    # Collect all .ecdir
    if not args['recursive']:
        dic_col = ecdic_load(os.path.join(str_root, '.ecdir'))
    else:
        dic_col = dict()
        for root, dirs, files in os.walk(str_root):
            for fn in files:
                if fn.endswith('.ecdir'):
                    print("- collecting:", os.path.join(root, fn))
                    dic_col[os.path.join(root, fn)] = ()
    # Do stats on collection
    return

def duplic(lst_dir):
    """ Search one, or more, existing .ecdir for potential duplicate files """
    verbose = args['verbose']
    dic_duplis = dict()
    lst_hits = list()
    for dir in lst_dir:
        # find and open .ecdir - abort if missing
        ecdir = ecdic_load(dir+"/.ecdir")
        if ecdir:  # This basically assumes ecdir_load() returns False on fail... Check that XXX
            # travers the .ecdir, collect info
            for fil in ecdir.keys():
                if not ecdir[fil]['hash'] in dic_duplis.keys():
                    dic_duplis[ecdir[fil]['hash']] = [ecdir[fil]]
                else:
                    lst_hits.append(ecdir[fil]['hash'])
                    dic_duplis[ecdir[fil]['hash']].append(ecdir[fil])
        else:
            print("Missing .ecdir file in duplicates analysis:", dir)
    print("Duplis:", len(lst_hits))
    for hit in lst_hits:
        for samp in dic_duplis[hit]:
            print("hit:", hit, samp)
    return lst_hits

def update(dir):
    """ Updates the .ecdic, but only for new and changed files """

    return

if __name__ == "__main__":

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--init", action="store_true")
    group.add_argument("-s", "--status", action="store_true")
    group.add_argument("-u", "--update", action="store_true")
    ap.add_argument("-d", "--directory", required=False, default="./", help="the stat directory")
    ap.add_argument("-r", "--recursive", required=False, default=False, help="go into sub-directories")
    ap.add_argument("-m", "--mode", required=False, default='default', help="only meaningfull with -s")
    ap.add_argument("-v", "--verbose", required=False, type=int, default=4, choices=range(0, 10), help="verbosity [0..9], where 0 is silent and 9 is chatty")
    args = vars(ap.parse_args())
    if args['verbose'] >= VERBOSE_WARNING:
        print(args)

    # Checks input sanity...
    if (args['init'] or args['status'] or args['update']) and not os.path.isdir(args['directory']):
        print("Directory NOT found:", args['directory'])
        sys.exit()

    # Action...
    if args['init']: # Initialize the .ecdir
        init(args['directory'])
    elif args['status']: # Show state of a dir compared to it's .ecdir
        status(args['directory'])
    elif args['update']:# Update the .ecdir to reflect the current state of the dir
        update(args['directory'])
    else:
        if args['verbose'] > VERBOSE_SILENT:
            print("Unknown node... You should never see this!")
