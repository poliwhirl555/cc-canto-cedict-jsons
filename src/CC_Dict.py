import os
import inspect
import pathlib
import json
from parser import DICT_TYPES, VALID_KEYS
from update import load_latest_data, raws_exists, jsons_exists, INTERNAL_NAME, get_jsons

class CC_Dict:
    data_dir = pathlib.Path(inspect.getabsfile(load_latest_data)).parent.parent # Two parent levels because that's the current structure. Might have to modify this in the future, or make it a property of update.
    def __init__(self, type, key = None, update = False):
        self.type = ""
        if "mandarin" in type.lower() or DICT_TYPES[0].lower() in type.lower():
            self.type = DICT_TYPES[0]
        elif DICT_TYPES[1].lower() in type.lower():
            self.type = DICT_TYPES[1]

        self.jsons = {}
        if update or not raws_exists(str(CC_Dict.data_dir)) or not jsons_exists(str(CC_Dict.data_dir)):
            # Have to temporarily store the variable in a class attribute or else the variable will just fall out of scope and vanish
            self.jsons = load_latest_data(str(CC_Dict.data_dir))
            self.jsons = self.jsons_path_list_to_keyed_dict(self.jsons)
        else: # Fetch the existing jsons from the expected data directory
            self.jsons = map(pathlib.Path, get_jsons(self.data_dir, self.type))
            self.jsons = self.jsons_path_list_to_keyed_dict(self.jsons)

        self.key = key
        self.dict = {}
        # Only automatically load the data if a key is provided. Done this way for backwards compatibility.
        if self.key.lower() not in [None, "description"]: 
            if self.key.lower() not in VALID_KEYS[self.type]:
                raise ValueError("Invalid key for dictionary type!")
            self.dict = self.get_data(self.key)
            
    
    def get_data(self, key = None):
        data = None
        with open(self.jsons[key]) as js:
            data = json.load(js)
        return data
    
    def get_raw_path(self):
        return str(CC_Dict.data_dir) + "/" + INTERNAL_NAME[self.type]
    
    # TODO: Maybe add functions to dump or copy json files to other directories.

    # Utility function
    # Input: A list of Path objects to json
    # Output: A list of Jsons
    def jsons_path_list_to_keyed_dict(self, json_paths):
        keyed_dict = {}
        for f in json_paths:
            if self.type.lower() in f.stem.lower():
                for k in VALID_KEYS[self.type]:
                    if str(k).lower() in f.stem.lower():
                        keyed_dict[k] = f
                        break
        return keyed_dict
    

    # The standard dictionary methods, implemented to allow use of syntatic sugar directly with CC_Dict when accessing the internal dict
    def __getitem__(self, key):
        return self.dict[key]    

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __delitem__(self, key):
        del self.dict[key]

    def __contains__(self, key):
        return key in self.dict
    
    def __len__(self):
       return len(self.dict)
    
    def __iter__(self):
        return iter(self.dict)
    
    def __reversed__(self):
        return reversed(self.dict)
    
    def __eq__(self, other):
        if isinstance(other, CC_Dict):
            return self.dict == other.dict and self.type == other.type and self.key == other.key and self.jsons == other.jsons
        return self.dict == other
    
    def get(self, key, default=None):
        return self.dict.get(key, default)

    def keys(self):
        return self.dict.keys()

    def values(self):
        return self.dict.values()

    def items(self):
        return self.dict.items()

    def pop(self, key, *args):
        return self.dict.pop(key, *args)

    def popitem(self):
        return self.dict.popitem()
    
    def copy(self):
        copy_ccd = CC_Dict(self.type)
        copy_ccd.key = self.key
        copy_ccd.dict = self.dict.copy()
        return copy_ccd