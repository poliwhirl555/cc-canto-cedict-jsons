import os
import inspect
import pathlib
import json
from parser import DICT_TYPES, VALID_KEYS
from update import load_latest_data, raws_exists, jsons_exists, INTERNAL_NAME, get_jsons

class CC_Dict:
    data_dir = pathlib.Path(inspect.getabsfile(load_latest_data)).parent.parent # Two parent levels because that's the current structure. Might have to modify this in the future, or make it a property of update.
    def __init__(self, type, update = False):
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
    

        
