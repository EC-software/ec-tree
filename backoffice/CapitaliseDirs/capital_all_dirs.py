

def cap_all_words(str_in, str_wsep=''):
    """ Capitalize all words in the string str_in
        accepted 'word separators', other than default python wide-space, are all letters in str_wsep """
    str_ou = str_in
    str_ou = ' '.join([w.capitalize() for w in str_ou.strip().split()])
    for wsep in str_wsep:
        str_ou = wsep.join([w.capitalize() for w in str_ou.split(wsep)])
    return str_ou

if __name__ == '__main__':
    print(f'Cap: {cap_all_words("Martin hvidberg")}')
    print(f'Cap: {cap_all_words("Martin hvidberg", "_")}')  # Why is this failing??? ToDo[44] FIX XXX
    print(f'Cap: {cap_all_words("Martin_hvidberg")}')
    print(f'Cap: {cap_all_words("Martin_hvidberg", "_")}')
