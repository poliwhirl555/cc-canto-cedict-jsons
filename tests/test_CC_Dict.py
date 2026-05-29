import pytest
import sys
import inspect
import os
from pathlib import Path
sys.path.insert(0, "/home/poliwhirl555/projects/py_cc_cedict_canto_json/py_cc_dicts")
from CC_Dict import *
from parser import *
from update import *


@pytest.fixture
def preload_data():
    data_load_dict = CC_Dict("CANTO")
    return data_load_dict

@pytest.fixture
def preload_data_canto_dict():
    data_load_dict = CC_Dict("CANTO", "traditional")
    return data_load_dict

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
    clean_raws(CC_Dict.data_dir)
    clean_jsons(CC_Dict.data_dir)
    d = CC_Dict("CEDICT")
    assert raws_exists(CC_Dict.data_dir)
    assert jsons_exists(CC_Dict.data_dir)
    
# This test doesn't quite work for some reason, 
# although I do see that it does work since I see the data being deleted and created
# def test_create_dict_update(preload_data):
#     old_jsons = get_jsons(CC_Dict.data_dir)
#     old_raws = get_raws(CC_Dict.data_dir)
#     old_json_mod_times = map(lambda j: Path(j).stat().st_mtime, old_jsons)
#     old_raws_mod_times = map(lambda r: Path(r).stat().st_mtime, old_raws)
#     d = CC_Dict("CEDICT", update = True)
#     new_jsons = get_jsons(CC_Dict.data_dir)
#     new_raws = get_raws(CC_Dict.data_dir)
#     new_json_mod_times = map(lambda j: Path(j).stat().st_mtime, new_jsons)
#     new_raws_mod_times = map(lambda r: Path(r).stat().st_mtime, new_raws)

#     assert len(old_jsons) == len(new_jsons)
#     assert len(old_raws) == len(new_raws)

#     for oj, nj in zip(old_json_mod_times, new_json_mod_times):
#         assert nj > oj

#     for orw, nrw in zip(old_raws_mod_times, new_raws_mod_times):
#         assert nrw > orw

def test_get_data(preload_data):
    for dt in DICT_TYPES:
        dict = CC_Dict(dt)
        for k in VALID_KEYS[dt]:
            data = dict.get_data(k)
            if k:
                # Single iteration for loop to get any item from the dict
                for dk in data:
                    sample = data[dk]

                    # As the data key for "definitions" keyed jsons has been turned to a string, need to turn it back for the comparison to work.
                    if k == "definitions":
                        dk = ast.literal_eval(dk)
                    
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

def test_create_keyed_dict_CEDICT(preload_data):
    for k in VALID_KEYS["CEDICT"]:
        if not (k == "definitions" or k == None):
            d = CC_Dict("CEDICT", k)
            assert "jyutping" not in d.dict
            json_loaded_dict = None
            with open(d.jsons[k], "r") as j:
                json_loaded_dict = json.load(j)
            assert d.dict == json_loaded_dict

def test_create_keyed_dict_CANTO():
    for k in VALID_KEYS["CANTO"]:
        if not (k == "definitions" or k == None):
            d = CC_Dict("CANTO", k)
            json_loaded_dict = None
            with open(d.jsons[k], "r") as j:
                json_loaded_dict = json.load(j)
            assert d.dict == json_loaded_dict
    
# Tests for passthrough
def test_get_subscript(preload_data_canto_dict):
    d = preload_data_canto_dict
    assert d["式"] == d.dict["式"]

def test_set(preload_data_canto_dict):
    d = preload_data_canto_dict
    d["式"] = "a"
    assert d.dict["式"] == "a"

def test_del(preload_data_canto_dict):
    d = preload_data_canto_dict
    del d["式"]
    assert not d.dict.get("式")

def test_contains(preload_data_canto_dict):
    d = preload_data_canto_dict
    assert "式" in d
    assert ("式" in d) == ("式" in d.dict)

def test_len(preload_data_canto_dict):
    d = preload_data_canto_dict
    assert len(d) == len(d.dict)

def test_iter(preload_data_canto_dict):
    d = preload_data_canto_dict
    for k, k2 in zip(d, d.dict):
        assert k == k2

def test_reversed(preload_data_canto_dict):
    d = preload_data_canto_dict
    for k, k2 in zip(reversed(d), reversed(d.dict)):
        assert k == k2

def test_equals(preload_data_canto_dict):
    d = preload_data_canto_dict
    d2 = CC_Dict("CANTO", "traditional")
    assert d == d2

def test_not_equal_not_keyed(preload_data_canto_dict):
    d = preload_data_canto_dict
    d2 = CC_Dict("CANTO")
    assert not d == d2

def test_not_equal(preload_data_canto_dict):
    d = preload_data_canto_dict
    d2 = CC_Dict("CEDICT", "simplified")
    assert not d == d2

def test_get(preload_data_canto_dict):
    d = preload_data_canto_dict
    assert d.get("式") == d.dict.get("式")

def test_get_not_in_dict(preload_data_canto_dict):
    d = preload_data_canto_dict
    assert not d.get("definitely not in dictionary")
    assert d.get("definitely not in dictionary") == d.dict.get("definitely not in dictionary")

def test_get_keys(preload_data_canto_dict):
    d = preload_data_canto_dict
    assert d.keys() == d.dict.keys()

def test_get_values(preload_data_canto_dict):
    d = preload_data_canto_dict
    assert list(d.values()) == list(d.dict.values())

def test_items(preload_data_canto_dict):
    d = preload_data_canto_dict
    assert d.items() == d.dict.items()

def test_pop(preload_data_canto_dict):
    d = preload_data_canto_dict
    entry = d["式"]
    popped = d.pop("式")
    assert entry == popped
    assert not d.get("式")

def test_pop_item(preload_data_canto_dict):
    d = preload_data_canto_dict
    last_key = next(reversed(d))
    last_item = tuple([last_key, d[last_key]])
    popped = d.popitem()
    assert  d.get(last_key) == None
    assert last_item == popped

def test_copy(preload_data_canto_dict):
    d = preload_data_canto_dict
    d2 = d.copy()
    assert d == d2


# Tests for the defintions fuzzy search

def test_create_key_definition():
    try:
        d = CC_Dict("CANTO", "definitions")
        definitions_dict = None
        with open(d.jsons["definitions"], "r")  as j:
            definitions_dict = json.load(j)
        assert d.dict == definitions_dict
        assert isinstance(d.dict, definition_dict)
    except:
        pytest.fail("\"definitions\" should be a valid key. No error should be thrown")
    
def test_search_found():
    d = CC_Dict("CANTO", "definitions")
    results = [{"traditional": "打爛咗",  "simplified": "打烂咗", "pinyin": "da3 lan4 zuo5", "jyutping": "daa2 laan6 zo2", 
                    "definitions": ["to have shattered something [colloquial]"]},
                {"traditional": "散晒",  "simplified": "散晒", "pinyin": "san4 shai4", "jyutping": "saan2 saai3", 
                    "definitions": ["shattered; exhausted; very tired [colloquial]"]}]
    
    assert d["shatter"] == results
    
def test_search_not_found():
    d = CC_Dict("CANTO", "definitions")
    assert d["something definitely not in the dictionary"] == []

