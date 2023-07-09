import hashlib


def file_hash(filename, mode='sha256'):
    if mode == 'sha256':
        h = hashlib.sha256()
    elif mode == 'md5':
        h = hashlib.md5()
    else:
        h = hashlib.sha256()  # Fall back default
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()


if __name__ == "__main__":
    print(file_hash(__file__))
