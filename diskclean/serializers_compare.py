
""" Serializer test
Candidates
    pickle:         build-in
    json:           build-in
    msgpack:        https://msgpack.org/, pip install msgpack
    ray:            http://ray.readthedocs.io/en/latest/index.html, pip install ray
    apache arrow:   https://arrow.apache.org/docs/python/, maybee later
"""

import string

import pickle
import json
import msgpack

# Create a larger, nested, dic with multible datatypes inside
payload = dict()
for n in range(13):
    payload[n] = n*n  # ingers
for c in string.printable[:94]:
    payload[c] = "The character {} is stored here".format(c)  # strings
for n in range(6):
    lst_n = [pow(m,n) for m in [m+4 for m in range(4)]]  # lists
    payload["list_"+str(n)] = lst_n
lol_n = list()
for n in range(6):
    lst_n = [[pow(m,n) for m in [m+14 for m in range(4)]]]  # nested lists
    lol_n.append(lst_n)
    payload["list_of_lists"] = lol_n
dic_d = dict()
dic_d['int'] = payload[1]
dic_d['str'] = payload['a']
dic_d['lst'] = payload['list_4']
dic_d['lol'] = payload['list_of_lists']
payload['dic'] = dic_d
# XXX boleans

print "Testing seiralizers..."

### Pickle
str_fn = "payload.pickle"
pickle.dump(payload, open(str_fn, "wb"))
ret_load = pickle.load(open(str_fn, "rb"))
if ret_load == payload:
    print "Pickles is identical"
else:
    print "!!! Error on reload: Pickle"

### JSON
# Note
# Keys in key/value pairs of JSON are always of the type str. When a dictionary is converted into JSON,
# all the keys of the dictionary are coerced to strings. As a result of this, if a dictionary is
# converted into JSON and then back into a dictionary, the dictionary may not equal the original one.
# That is, loads(dumps(x)) != x if x has non-string keys.
str_fn = "payload.json"
json_load = json.dumps(payload, sort_keys=True, indent=4)
with open(str_fn, "w") as fil:
    fil.write(json_load)
with open(str_fn, "r") as fil:
    str_ret = fil.read()
ret_load = json.loads(str_ret)
if ret_load == payload:
    print "JSON is identical"
else:
    print "!!! Error on reload: JSON"
    if json_load == str_ret:
        print "    but json == json, so it's likely just caused by non-string keys in input"

### msgpack
str_fn = "payload.msgpack"
msp_load = msgpack.packb(payload)
with open(str_fn, "w") as fil:
    fil.write(msp_load)
with open(str_fn, "r") as fil:
    str_ret = fil.read()
ret_load = msgpack.unpackb(str_ret)
if ret_load == payload:
    print "MsgPack is identical"
else:
    print "!!! Error on reload: MsgPack"


