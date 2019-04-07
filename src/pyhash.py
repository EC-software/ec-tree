
#pyhash.py
#Charles J. Lai
#October 11, 2013
# modified for python 3 and fixed indentation '20190407/mh

"""
FNV (Fowler-Noll-Vo) hashes
See README file for top level documentation. """


def fnv1_32(str_in, seed=0):
    """ Returns: The FNV-1 hash of a given str_in. """
    #Constants
    FNV_prime = 16777619
    offset_basis = 2166136261
    #FNV-1a Hash Function
    hash = offset_basis + seed
    for char in str_in:
        hash = hash * FNV_prime
        hash = hash ^ ord(char)
    return hash


def fnv1a_32(str_in, seed=0):
    """ Returns: The FNV-1a (alternate) hash of a given str_in """
    #Constants
    FNV_prime = 16777619
    offset_basis = 2166136261
    #FNV-1a Hash Function
    hash = offset_basis + seed
    for char in str_in:
        hash = hash ^ ord(char)
        hash = hash * FNV_prime
    return hash


def fnv1_64(str_in, seed=0):
    """ Returns: The FNV-1 hash of a given str_in. """
    #Constants
    FNV_prime = 1099511628211
    offset_basis = 14695981039346656037
    #FNV-1a Hash Function
    hash = offset_basis + seed
    for char in str_in:
        hash = hash * FNV_prime
        hash = hash ^ ord(char)
    return hash


def fnv1a_64(str_in, seed=0):
    """ Returns: The FNV-1a (alternate) hash of a given str_in """
    #Constants
    FNV_prime = 1099511628211
    offset_basis = 14695981039346656037
    #FNV-1a Hash Function
    hash = offset_basis + seed
    for char in str_in:
        hash = hash ^ ord(char)
        hash = hash * FNV_prime
    return hash

# ====== The Modulus variants =============

def fnv1_32m(str_in, seed=0):
    """ Returns: The FNV-1 hash of a given str_in. """
    #Constants
    FNV_prime = 16777619
    offset_basis = 2166136261
    #FNV-1a Hash Function
    hash = offset_basis + seed
    for char in str_in:
        hash = hash * FNV_prime
        hash = hash ^ ord(char)
        hash = hash % ((2**32)-1)
    return hash


def fnv1a_32m(str_in, seed=0):
    """ Returns: The FNV-1a (alternate) hash of a given str_in """
    #Constants
    FNV_prime = 16777619
    offset_basis = 2166136261
    #FNV-1a Hash Function
    hash = offset_basis + seed
    for char in str_in:
        hash = hash ^ ord(char)
        hash = hash * FNV_prime
        hash = hash % ((2**32)-1)
    return hash


def fnv1_64m(str_in, seed=0):
    """ Returns: The FNV-1 hash of a given str_in. """
    #Constants
    FNV_prime = 1099511628211
    offset_basis = 14695981039346656037
    #FNV-1a Hash Function
    hash = offset_basis + seed
    for char in str_in:
        hash = hash * FNV_prime
        hash = hash ^ ord(char)
        hash = hash % ((2**64)-1)
    return hash


def fnv1a_64m(str_in, seed=0):
    """ Returns: The FNV-1a (alternate) hash of a given str_in """
    #Constants
    FNV_prime = 1099511628211
    offset_basis = 14695981039346656037
    #FNV-1a Hash Function
    hash = offset_basis + seed
    for char in str_in:
        hash = hash ^ ord(char)
        hash = hash * FNV_prime
        hash = hash % ((2**64)-1)
    return hash


def main():
    """ Testing application: Do something """
    str_test = "lolxxxyyyzzz"
    num_seed = 2**13
    print(fnv1_32(str_test, num_seed))
    print(fnv1a_32(str_test, num_seed))
    print(fnv1_64(str_test, num_seed))
    print(fnv1a_64(str_test, num_seed))

    print(fnv1_32m(str_test, num_seed))
    print(fnv1a_32m(str_test, num_seed))
    print(fnv1_64m(str_test, num_seed))
    print(fnv1a_64m(str_test, num_seed))

if __name__ == '__main__':
    main()