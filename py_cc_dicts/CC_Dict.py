import os
import inspect
import pathlib
import json
import ast
from py_cc_dicts.parser import DICT_TYPES, VALID_KEYS
from py_cc_dicts.update import load_latest_data, raws_exists, jsons_exists, INTERNAL_NAME, get_jsons

class CC_Dict(dict):
    """
    Provides access to paths, files and the data for keyed CC-CEDICT and CC-Canto JSONs.

    Has methods to access the raw data and JSON file paths, alongside being a container for dict that allows access to the keyed dictionary data for the chosen key.
    Extends dict for polymorphism purposes and to enable non passed through dict methods. However, the current structure has to be maintained in order to allow for the definition fuzzy search.

    Attributes:
        load_latest_dir (Path): Description
        data_dir (Path): Description
    """
    load_latest_dir = pathlib.Path(inspect.getabsfile(load_latest_data)).parent # Need the parent to strip off the update.py part of the path
    data_dir = load_latest_dir.parent # One parent level because that's the current structure. Might have to modify this in the future, or make it a property of update.
    def __init__(self, type, key = None, data_dir = None, update = False):
        """
        Construct a CC_Dict of the provided dictionary *type*.

        Optional arguments allow for this object to access the keyed data for the provided *key* via dictionary access syntax.

        Args:
            type (str): The type of dictionary this CC_Dict represents, that defines which JSONs and data the class functions give you access to. 
                One of the valid dict types as defined in DICT_TYPES in parser.py, or you can enter "Mandarin" or "Cantonese".
            key (str): One of the valid keys for the dictionary type *type*, as defined in parser.py. 
                If provided, a dict keyed to this key type containing the dictionary data will be preloaded into this object, allowing for easy access via standard dict syntax.
            data_dir (str): The directory as a string to check for the raw dictionary data and JSONs, and where to download them if they don't exist. 
                Defaults to current working directory if none provided, unless called one directory up from where this script is located, in which case defaults to that directory. (This is for Github presentation purposes, and should never matter in day to day use)
            update (bool): Whether to forcibly update the data for the dictionaries if already downloaded.
        """
        self.type = ""
        if "mandarin" in type.lower() or DICT_TYPES[0].lower() in type.lower():
            self.type = DICT_TYPES[0]
        elif DICT_TYPES[1].lower() in type.lower():
            self.type = DICT_TYPES[1]

        if data_dir:
            self.data_dir = data_dir
        elif pathlib.Path.cwd == CC_Dict.data_dir: 
            # A trick to avoid having to refactor tests and make this work on Github.
            # If the script is called specifically from the place you'd expect data to be for the Github page (one directory above the package),
            # then save data to that directory by default. (This will never happen if installed as a package due to the directory being buried in the Python 3.8 folder)
            self.data_dir = CC_Dict.data_dir
        else: # save data to the same folder as update.py, i.e. the package folder
            self.data_dir = CC_Dict.load_latest_dir.parent

        self.jsons = {}
        if update or not raws_exists(str(self.data_dir)) or not jsons_exists(str(self.data_dir)):
            # Have to temporarily store the variable in a class attribute or else the variable will just fall out of scope and vanish
            self.jsons = load_latest_data(str(self.data_dir))
            self.jsons = self.jsons_path_list_to_keyed_dict(self.jsons)
        else: # Fetch the existing jsons from the expected data directory
            self.jsons = map(pathlib.Path, get_jsons(self.data_dir, self.type))
            self.jsons = self.jsons_path_list_to_keyed_dict(self.jsons)

        self.key = key
        self.dict = {}
        # Only automatically load the data if a key is provided. Done this way for backwards compatibility.
        if self.key and not self.key.lower() == "definitions" : 
            if self.key.lower() not in VALID_KEYS[self.type]:
                raise ValueError(f"{self.key} is an invalid key for dictionary type!")
            self.dict = self.get_data(self.key)
        elif self.key == "definitions":
            # Need to get a way to get the definition dict somehow
            self.dict = definition_dict(self.get_data(self.key))
        super().__init__(self.dict)
            
    
    def get_data(self, key = None) -> (dict |list[dict]):
        """
        Load the keyed data for the given *key* from the appropriate JSON file.

        Args:
            key (str): Valid key as defined in parser.py, for which the output dict of entries will be keyed by.

        Returns:
            (dict | list[dict]): dict if key entered is *not* None, otherwise, list (as the entries won't have a key)
        """
        data = None
        with open(self.jsons[key]) as js:
            data = json.load(js)
        return data
    
    def get_raw_path(self):
        """
        Produce the path to the raw txt/u8 dictionary data files.
        """
        return str(CC_Dict.data_dir) + "/" + INTERNAL_NAME[self.type]
    
    # TODO: Maybe add functions to dump or copy json files to other directories.

    def jsons_path_list_to_keyed_dict(self, json_paths):
        """
        Converts a list of Paths to dictionary data JSON files to a list of dicts with the JSON data.

        Utility function.

        Args:
            json_paths (list[Path]): A list of pathlib.Path objects to dictionary data JSON files.
        """
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
        elif isinstance(other, dict):
            return self.dict == other
        else:
            return False
    
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

class definition_dict(dict):
    """
    A special class extending dict to allow for a probably inefficient search of definition keys when using the subscript access operator.

    Overrides __getitem__ and get(), transforming the argument in subscript access into a basic search for all definitions that contain the input string. All other dictionary functions should work as normal.
    
    Example: For d = definitions_dict, d["something"] would search all the keys of the dict (which should be strings) and return a list of entries whose keys contained the string "something"

    *Not designed for use outside of the class CC_Dict*
    """
    def __getitem__(self, key):
        # This should technically work but it's actually insane and impossible to read
        # Basically, accumulate all entries for all definitions, entry pairs in the dict that is self where key is in any of the definitions in definitions 
        return [entry for definitions,entry in zip(self, self.values()) if key in definitions]
    
    def get(self, key, default):
        return self[key]