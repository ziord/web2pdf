import json
import os

def get_info():
    fp_lst = (os.path.abspath(__file__).split(os.path.sep)[:-1])
    fp_lst.append("_info.json")
    pkg_file_path = os.path.sep.join(fp_lst)
    with open(pkg_file_path) as file:
        json_data = json.load(file)
    return json_data
