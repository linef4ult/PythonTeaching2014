__author__ = 'mark'

import shelve
import pickle
import json

with shelve.open('spam') as db:
    db['eggs'] = 'eggs'

"""
Any object in python can be pickled so that it can be saved on disk. What pickle does is that it “serialises” the
object first before writing it to file. Pickling is a way to convert a python object (list, dict, etc.) into a
character stream. The idea is that this character stream contains all the information necessary to reconstruct the
object in another python script.


"""

a = "a random bunch of words".split()
with open("pickle1", "wb") as f:
    pickle.dump(a, f)

with open("pickle1", "rb") as f:
    b = pickle.load(f)

print("a == b is {}".format(a == b))


# An arbitrary collection of objects supported by pickle.
data = {
    'a': [1, 2.0, 3, 4+6j],
    'b': ("character string", b"byte string"),
    'c': set([None, True, False])
}

with open('pickle2', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

# The following example reads the resulting pickled data.

with open('pickle2', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data = pickle.load(f)

print("{}".format(data))


my_thing = {'1':[1,2,3,{'1.1': 'aa', '1.2': 'bb'}]}

json_thing = json.dumps(my_thing)

print("my_thing is a {} ... {}".format(type(my_thing),my_thing))

for k,v in my_thing.items():
    print("{}: {}".format(k, type(v)))

print("json_thing is a {} ... {}".format(type(json_thing), json_thing))


