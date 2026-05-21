import os
import inspect
import pathlib
from parser import DICT_TYPES
from update import load_latest_data, raws_exists, jsons_exists

class CC_Dict:
    def __init__(self, type, update = False):
        self.type = ""
        if "mandarin" in type.lower() or DICT_TYPES[0].lower() in type.lower():
            self.type = "CEDICT"
        elif DICT_TYPES[1] in type.lower():
            self.type = "CANTO"

        data_dir = pathlib.Path(inspect.getabsfile(load_latest_data)).parent.parent # Two parent levels because that's the current structure. Might have to modify this in the future, or make it a property of update.
        self.jsons = []
        if update or not raws_exists(str(data_dir)) or not jsons_exists(str(data_dir)):
            latest_jsons = load_latest_data(str(data_dir))
            for f in latest_jsons:
                if self.type.lower() in f.stem.lower():
                    self.jsons.append(f) 


        
