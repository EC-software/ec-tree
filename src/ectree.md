# EC TREE

ver. 3.x - DB based

## Plan

1. There is one, and only one, place to store the info about the tree(s), and that place is a database.

    a. there is one, and only one, db per user
   
2. One table holds the roots. Each entry describes one root, i.e. the beginning of one tree. 
   
3. Another table holds the files. Each entry describes one file.
   
    a. filename. full OS filename
   
    b. filetime. the OS time stamp of the file, when it was last scanned
   
    c. filesize. the OS file size when it was last scanned
   
    d. shorthash. the hash value of the first n bytes
   
    e. longhash. the hash value of the entire file 
   
    f. scantime. the time this reqord was last updated


## Commands

### ectini()

**Initialise** an empty db, if it does not exist.

### ectar(dir)

**Add root** to the db

### ectrr(dir)

**Remove root** from the db

### ectsc(dir, dir, ...)

**Scan** tree(s) to update the db. If dir is given, only scan dir, otherwise scan all trees known to the db. Non-mounted trees are ignored silently. Updates all info about each file, except longhash. 

If a file have disappeared from the filesystem, it is removed from the db.

If a new file is found, it is added to the db. Files -name, -time and -size is noted in the db, as well as it's shorthash.

If a file is re-found, and it's -time and -size is unchanged, no action is taken. If -time or -size has changed, then it's smallhash is updated, and the longhash is deleted.

### ectfd(dir, dir, ...)

**Find Duplicate** files in tree(s), by searching the db. If dir is non-empty, limit the search to that/these dir(s). Otherwise search all trees known to the db. Non-mounted are ignores, but a warning is raised.

**Note** if files have changes since last ectsc(), then the db may be out of sync, and ectfd() will provide incorrect answers. Always consider running ectsc() before ectfd().

Files are compared by hash, nothing else. For files with identical shorthash, the longhash is calculated and noted in the db if not available.

Files with same longhash is announced identical, in groups of same longhash.

If a dir is given, that is not in the db, a error is raised. Considering option -f, --force which will call ectsc(dir) with each missing dir - and then run ectfd().

Output is list(s) of long-collisions.

### ectree.conf

Configuration file co-located with the scripts. Tells where the db is.

### ectree.sqlite

Database file.