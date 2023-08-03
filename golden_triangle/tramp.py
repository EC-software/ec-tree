#!/usr/bin/python3

""" Trampolin
    Automatically move all files in dir A to dir B """

import datetime
import getopt
import os
import pprint
import sys
import time


def valid_ab(str_da, str_db):
    """ Validate that A and B is directories with the right parameters """
    # Are they identifiable directories?
    for path in [str_da, str_db]:
        if os.path.isdir(path):
            # # print(f"  is a Dir: {path}")  # remove later...
            pass  # As expected - it's a dir
        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path_ff = os.path.join(dir_path, path)
            if os.path.isdir(path_ff):
                # # print(f"  is a Dir: {path_ff}")  # remove later...
                pass  # As expected - it's a dir
            else:
                print(f"!!! Err.: NOT a Dir: {path}")
                return False
    # Do we have R+W access ?
    for path in [str_da, str_db]:
        if os.access(path, os.W_OK):
            # # print(f"  Has Write access: {path}")  # remove later...
            pass  # As expected we have Write access
            # We will not check Write and Delete access to alle files - that is handled individually.
        else:
            print(f"!!! Err.: No Write access: {path}")
            return False
    return True


def parse_cmd(argv):
    """ Handle the cmd-line parameters """
    # Set default values
    dir_a, dir_b = None, None
    num_ttl, num_pause = 60, 1
    boo_valid = True  # assume valid input, until proven false...
    str_usage = f'{__file__} -i <inputdir> -o <outputdir> -p <pause> -t <time to live>'
    # Look for cmd line parameters
    try:
        # # print(f"argv: {argv}")
        opts, args = getopt.getopt(argv, "i:o:t:p:h")  # , ["i_dir=", "o_dir=", "--ttl=", "--pause=", "--help"]
        # # print(f"opts: {opts}")
        # # print(f"args: {args}")
    except getopt.GetoptError:
        print(str_usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(str_usage)
            sys.exit()
        else:
            if opt in ("-i", "--i_dir"):  # input dir
                dir_a = arg
            if opt in ("-o", "--o_dir"):  # output dir
                dir_b = arg
            if opt in ("-t", "--ttl"):  # stop program after this many seconds
                num_ttl = arg
            if opt in ("-p", "--pause"):  # pause this many seconds after each loop
                num_pause = arg

    if valid_ab(dir_a, dir_b):  # test -i and -o
        print(f"Input file: {dir_a}\nOutput file: {dir_b}")
    else:
        boo_valid = False
    try:  # test -t
        num_ttl = int(num_ttl)
    except ValueError:
        boo_valid = False
        print(f"parameter -t must be integer: {num_ttl}")
    try:  # test -p
        num_pause = int(num_pause)
    except ValueError:
        boo_valid = False
        print(f"parameter -p must be integer: {num_pause}")
    return {'v': boo_valid, 'a': dir_a, 'b': dir_b, 'p': num_pause, 't': num_ttl}


def move_data(a, b, n=3):
    """ Execute n attempt(s) to move each file in A to B """

    def move_file_if_movable(ffn_a, ffn_b):
        """ Move file if possible.
            return True if moved, otherwise False. """
        return True

    print(f" @ {datetime.datetime.now()}   ***   Move_data: {a} -> {b} ")
    for i in range(n):  # loop n times over the dir_a, in case some files are momentarily locked
        for itm_a in os.listdir(a):
            itm_a_ff = os.path.join(a, itm_a)
            itm_b_ff = itm_a_ff.replace(a, b)
            print(f" @ {datetime.datetime.now()}\n\t< {itm_a_ff}\n\t> {itm_b_ff}")
            move_file_if_movable(itm_a_ff, itm_b_ff)



def pause(n):
    """ Simply wait for n seconds """
    time.sleep(n)


def is_timeout(start, n):
    """ Evaluate if n seconds have passed since start, and it's time to stop """
    if (datetime.datetime.now() - start).total_seconds() > n:
        return True
    else:
        return False


def main(argv):
    dtt_start = datetime.datetime.now()
    dic_argv = parse_cmd(argv)
    if dic_argv['v']:
        # Main loop
        pprint.pprint(dic_argv)
        while not is_timeout(dtt_start, dic_argv['t']):
            move_data(dic_argv['a'], dic_argv['b'])
            pause(dic_argv['p'])
    else:
        print(f"\nTerminating, Command line parameters are missing or bad: {argv}")
    dtt_stop = datetime.datetime.now()
    print(f"Done. Start: {dtt_start}, Stopped: {dtt_stop}, Ran for {(dtt_stop - dtt_start).total_seconds()} of planned {dic_argv['t']} seconds")


if __name__ == "__main__":
    main(sys.argv[1:])
