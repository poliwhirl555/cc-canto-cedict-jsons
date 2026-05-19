import pytest
import requests
import os.path
import glob
from parser import *
from update import *

def test_fetch_raw():
    raw_paths = fetch_raw()
    assert len(raw_paths) == 2

def test_clean_raws():
    current_time = time.strftime("%Y-%m-%d_%H:%M_%Z", time.gmtime())
    for dt in DICT_TYPES:
        filename = FILE_PREFIXES[dt] + current_time + ".zip"
        open(filename, "w")
    clean_raws()
    for dt in FILE_PREFIXES:
        f_list = glob.glob(FILE_PREFIXES[dt] + "*.zip")
        assert len(f_list) == 0
    
def test_clean_jsons():
    for k in VALID_KEYS:
        for dt in DICT_TYPES:
            current_time = time.strftime("%Y-%m-%d", time.gmtime())
            truncated_filename = INTERNAL_NAME[dt][:INTERNAL_NAME[dt].rindex(".")]
            storage_name = truncated_filename + "_key_" + str(k) + "_" + current_time +".json"
            open(storage_name, "w")
    clean_jsons()
    for dt in DICT_TYPES:
        assert len(glob.glob(f"*{dt.lower()}*.json")) == 0 
    
def test_load_latest_data():
    load_latest_data()
    for dt in DICT_TYPES:
        # Check that the raws exist
        assert len(glob.glob(FILE_PREFIXES[dt] + "*.zip")) == 1
        # Check that the correct number of jsons are generated and they are readable
        glob_string = f"*{dt.lower()}*.json"
        json_files = glob.glob(glob_string)
        num_json_files = len(json_files)
        num_keys = len(VALID_KEYS[dt])
        assert num_json_files == num_keys
        for jf in json_files:
            with open(jf, "r") as f:
                try:
                    json.load(f)
                except:
                    pytest.fail("Invalid json file created.")