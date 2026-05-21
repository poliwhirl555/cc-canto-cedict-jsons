import pytest
import sys
import inspect
from pathlib import Path
sys.path.insert(0, "/home/poliwhirl555/projects/py_cc_cedict_canto_json/src")
from CC_Dict import *
from parser import *


@pytest.fixture
def preload_data():
    data_load_dict = CC_Dict("CANTO")

def test_create_dict_simple_type(preload_data):
    d = CC_Dict("CANTO")
    d2 = CC_Dict("CEDICT")

    assert d.type == DICT_TYPES[1]
    assert d2.type == DICT_TYPES[0]

def test_create_dict_complex_type_canto(preload_data):
    d_canto = []
    d_canto.append(CC_Dict("Cantonese"))
    d_canto.append(CC_Dict("CC-Canto"))
    d_canto.append(CC_Dict("canto"))
    for d in d_canto:
        assert d.type == DICT_TYPES[1]

def test_create_dict_complex_type_cedict(preload_data):
    d_cedict = []
    d_cedict.append(CC_Dict("Mandarin"))
    d_cedict.append(CC_Dict("CC-Cedict"))
    d_cedict.append(CC_Dict("cccedict"))
    for d in d_cedict:
        assert d.type == DICT_TYPES[0]

def test_create_dict_pre_loaded_jsons(preload_data):
    d = CC_Dict("CANTO")
    d2 = CC_Dict("CEDICT")

    assert set(d.jsons.keys()) == set(VALID_KEYS[d.type])
    assert set(d2.jsons.keys()) == set(VALID_KEYS[d2.type])

def test_create_dict_load_data():
    return # TODO: Finish later

def test_create_dict_update():
    return # TODO: Finish later

def test_get_data(preload_data):
    for dt in DICT_TYPES:
        dict = CC_Dict(dt)
        for k in VALID_KEYS[dt]:
            data = dict.get_data(k)
            if k:
                # Single iteration for loop to get any item from the dict
                for dk in data:
                    sample = data[dk]
                    if type(sample) is list:
                        # Check if the dictionary key dk for a particular entry matches the entry's value when accessed with k
                        assert dk == sample[0][k]
                    else:
                        assert dk == sample[k]
                    break
            else: # If keyless (None), just check if it's a list and entries contain the proper keys
                assert type(data) is list
                for dk in data[0].keys():
                    if not dk == "definitions":
                        assert dk in VALID_KEYS[dt]
        

def test_get_raw_path(preload_data):
    file_glob = {DICT_TYPES[0]: f"*{DICT_TYPES[0].lower()}*.u8",
                 DICT_TYPES[1]: f"*{DICT_TYPES[1].lower()}*.txt"}
    for dt in DICT_TYPES:
        dict = CC_Dict(dt)
        raw_path = Path(dict.get_raw_path())
        assert raw_path.is_file() and raw_path.match(file_glob[dt]) == True

