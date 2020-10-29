import re


def quote(string):
    return '"' + string + '"'

def clean(string):
    string = string.strip()
    string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
    chars_to_remove = [".","|","[","]","{","}"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string) # remove the list of chars defined above
    string = string.replace('&', 'and')
    string = string.replace("'", "''")
    # string = string.lower() # normalise case - capital at start of each word
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single space
    string = re.sub(r'[,-./]|\sBD',r'', string)
    return string

def merge_nested_dict(a,b):
    c = {}
    if not isinstance(a, dict):
        return b

    if not isinstance(b, dict):
        return a

    for k in a:
        if k in b: c[k] = merge_nested_dict(a[k], b[k])
        else: c[k] = a[k]

    for k in b:
        if k not in a: c[k] = b[k]
    return c

def merge_list_of_nested_dict(l):
    d = {}
    for dd in l:
        d = merge_nested_dict(dd, d)
    return d
