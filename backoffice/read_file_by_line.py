filepath = '/home/martin/lot of english words.txt'
with open(filepath) as fp:
    for cnt, line in enumerate(fp):
        if line.lower().startswith('t'):
            if line.strip().lower().endswith('t'):
                print("Line {}: {}".format(cnt, line.strip()))