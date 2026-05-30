import requests
import time
import json
import glob
import os
import sys
from zipfile import *
from pathlib import Path
from py_cc_dicts.parser import DICT_TYPES, VALID_KEYS, parse


GET_LINKS = {DICT_TYPES[0]: "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip",
             DICT_TYPES[1]: "https://cantonese.org/cccanto-170202.zip"}
FILE_PREFIXES = {DICT_TYPES[0]: "cedict_1_0_ts_utf-8_mdbg_",
                 DICT_TYPES[1]: "cccanto-"}
INTERNAL_NAME = {DICT_TYPES[0]: "cedict_ts.u8",
                 DICT_TYPES[1]: "cccanto-webdist.txt"}

def load_latest_data(json_end_dir = "") -> list[Path]:
    """
    Load the latest raw data from the dictionary's websites and generate keyed JSON files for every valid key for each dictionary.

    Old data is deleted from, and JSONs genearted are saved to, json_end_dir, or the current working directory if none provided.
    Returns a list of pathlib.Paths to the newly created JSONs.

    Args:
        json_end_dir: str path to the directory to delete old data from and save the new created JSON files to. Current working directory if none provided.
    """
    # A very lazy way of allowing the data to be dumped to a different directory, by changing the working directory and then changing it back after
    curr_dir = os.getcwd()
    if json_end_dir:
        os.chdir(json_end_dir)
    clean_raws()
    clean_jsons()
    raw_paths = fetch_raw()
    json_paths = []
    for p in raw_paths:
        json_paths.extend(generate_jsons(p))
    os.chdir(curr_dir)
    return json_paths
    

# Fetch the raw zip files from the CC-CEDICT and CC-CANTO website
def fetch_raw():
    """
    Send a GET request to the websites for CC-CEDICT and CC-Canto to download zip files containing the latest raw data, and save it to the current working directory.
    """
    raw_paths = []
    for dt in DICT_TYPES:
        current_time = time.strftime("%Y-%m-%d_%H:%M_%Z", time.gmtime())
        filename = FILE_PREFIXES[dt] + current_time + ".zip"
        savefile = Path(filename)
        r = requests.get(GET_LINKS[dt], timeout = 30)
        r.raise_for_status() # To stop and abort if the status code isn't good
        savefile.write_bytes(r.content)
        raw_paths.append(savefile)
    return raw_paths

# Function to delete all raw files, usually used to remove the old ones
def clean_raws(dir = ""):
    # Does not clean the old .txt and .u8 file, but it doesn't matter as those should be constantly overwritten when unpacking.
    # Might be good to include those just in case though. Maybe in the future
    for f in get_raws(dir):
        os.remove(f)

# For each possible key, including none, generate the json for that key and save it to repository directory
def generate_jsons(input_file_path) -> list[Path]:
    """
    For each CC-CEDICT/CC-Canto raw zip file in directory input_file_path, generate JSONs keyed to each valid key and save it to the current working directory. 
    Returns a list of pathlib.Path objects pointing to the new JSON files.

    Args:
        input_file_path: str path to directory containing the CC-CEDICT/CC-Canto zip files.
    """
    # Figure out which type of dict data we're working with
    dict_type = None
    for dt in DICT_TYPES:
        if input_file_path.match("*" + dt.lower() + "*.zip"):
            dict_type = dt
        
    if not dict_type:
        raise ValueError('Invalid input file path.')
    
    # Get a list of items in the zip
    internals = None
    with ZipFile(input_file_path) as zip:
        internals = zip.infolist()
        zip.extract(internals[0])
    
    filename = internals[0].filename
    output_paths = []
    for key in VALID_KEYS[dict_type]:
        current_time = time.strftime("%Y-%m-%d", time.gmtime())
        dict_data = parse(filename, dict_type, key)
        truncated_filename = filename[:filename.rindex(".")]
        storage_name = truncated_filename + "_key_" + str(key) + "_" + current_time +".json"
        with open(storage_name, "w") as out_file:
            # ensure_ascii as false makes the Hanzi human readable, but hopefully it doesn't cause any problems
            json.dump(dict_data, out_file, ensure_ascii = False, indent = 4)
            output_paths.append(Path(storage_name))
    return output_paths

def clean_jsons(dir = ""):
    for f in get_jsons(dir):
        os.remove(f)

def jsons_exists(dir = ""):
    for dt in DICT_TYPES:
        jsons = get_jsons(dir, dt)
        if not len(jsons) == len(VALID_KEYS[dt]):
            return False
    return True

def raws_exists(dir = ""):
    for dt in DICT_TYPES:
        raws = get_raws(dir, dt)
        if len(raws) == 0:
            return False
    return True

# Get the data jsons from dir for dictionary type dict_type, if they exist
def get_jsons(dir = "", dict_type = ""):
    """
    Search dir for the generated JSON files of the input dict_type, or for both types if none provided, and return the paths as a list of strings.

    Args:
        dir: str path to directory to search. If none provided, searches current working directory.
        dict_type: A string listed in DICT_TYPES in parser.py, to denote which dictionary type to search for. Both searched by default.
    """
    curr_dir = None
    if dir:
        curr_dir = os.getcwd()
        os.chdir(dir)

    jsons = []
    if dict_type:
        jsons = glob.glob(f"*{dict_type.lower()}*.json")
    else:
        for dt in DICT_TYPES:
            jsons.extend(glob.glob(f"*{dt.lower()}*.json"))

    if curr_dir:
        os.chdir(curr_dir)
    return jsons

def get_raws(dir = "", dict_type = ""):
    """
    Search dir for the downloaded raw zip files of the input dict_type, or for both types if none provided, and return the paths as a list of strings.

    Args:
        dir: str path to directory to search. If none provided, searches current working directory.
        dict_type: A string listed in DICT_TYPES in parser.py, to denote which dictionary type to search for. Both searched by default.
    """
    curr_dir = None
    if dir:
        curr_dir = os.getcwd()
        os.chdir(dir)

    raws = []
    if dict_type:
        raws = glob.glob(FILE_PREFIXES[dict_type] + "*" +".zip")
    else:
        for dt in DICT_TYPES:
            raws.extend(glob.glob(FILE_PREFIXES[dt] + "*" +".zip"))
    
    if curr_dir:
        os.chdir(curr_dir)
    return raws
