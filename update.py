import requests
import time
import json
import glob
import os
from zipfile import *
from pathlib import Path
from parser import DICT_TYPES, VALID_KEYS, parse

# read_time = time.strptime(filename[filename.index("2") : filename.index(".")], "%Y-%m-%d_%H:%M_%Z")
# print(f"read time: {read_time}")

GET_LINKS = {"CEDICT": "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip",
             "CANTO": "https://cantonese.org/cccanto-170202.zip"}
FILE_PREFIXES = {"CEDICT": "cedict_1_0_ts_utf-8_mdbg_",
                 "CANTO": "cccanto-"}
INTERNAL_NAME = {"CEDICT": "cedict_ts.u8",
                 "CANTO": "cccanto-webdist.txt"}

def load_latest_data():
    # Add some data cleanup, deleting the old raws
    clean_raws()
    clean_jsons()
    raw_paths = fetch_raw()
    for p in raw_paths:
        generate_jsons(p)
    

# Fetch the raw zip files from the CC-CEDICT and CC_CANTO website
def fetch_raw():
    raw_paths = []
    for dt in DICT_TYPES:
        current_time = time.strftime("%Y-%m-%d_%H:%M_%Z", time.gmtime())
        filename = FILE_PREFIXES[dt] + current_time + ".zip"
        savefile = Path(filename)
        r = requests.get(GET_LINKS[dt], timeout = 30)
        savefile.write_bytes(r.content)
        raw_paths.append[savefile]
    return raw_paths

# Function to delete all raw files, usually used to remove the old ones
def clean_raws():
    for dt in DICT_TYPES:
        files = glob.glob(FILE_PREFIXES[dt] + "*" +".zip")
        for file in files:
            os.remove(file)

# for each possible key, including none, generate the json for that key and save it to repository directory
def generate_jsons(input_file_path):
    # Figure out which type of dict data we're working with
    dict_type = None
    for dt in DICT_TYPES:
        if input_file_path.match("*" + dt.lower() + "*.zip"):
            dict_type = dt
    
    if not dict_type:
        raise ValueError('Invalid invalid input file path.')
    
    # Get a list of items in the zip
    internals = None
    with ZipFile(input_file_path) as zip:
        internals = zip.infolist()
        zip.extract(internals[0])
    
    filename = internals[0].filename
    for key in VALID_KEYS[dt]:
        current_time = time.strftime("%Y-%m-%d", time.gmtime())
        dict_data = parse(filename, dict_type, key)
        storage_name = filename + "_key_" + key + "_" + current_time +".json"
        with open(storage_name, "w") as out_file:
            json.dump(dict_data, out_file, indent = 4)

def clean_jsons():
    search_regex = f"*({DICT_TYPES[0]}|{DICT_TYPES[1]})*.json"
    results = glob.glob(search_regex)
    for file in results:
        os.remove(file)
    