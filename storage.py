import argparse
import os
import tempfile
import json


parser = argparse.ArgumentParser()
parser.add_argument('--key', type=str)
parser.add_argument('--value', type=str, default=None)
var = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
if not os.path.exists(storage_path):
    with open(storage_path, 'w') as f:
        pass

if os.stat(storage_path).st_size == 0:
    with open(storage_path, 'w') as f:
        json.dump({}, f)

with open(storage_path, 'r') as f:
    my_dict = json.load(f)
    if var.value is None:
        my_dict.get(var.key, None)
        print(my_dict.get(var.key, None))
    else:
        if var.key in my_dict:
            my_dict[var.key] += f', {var.value}'
        else:
            my_dict[var.key] = var.value

with open(storage_path, 'w') as f:
    json.dump(my_dict, f)


    


