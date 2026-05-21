import pytest
import sys
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

def test_create_dict_load_data():
    return # TODO: Finish later

def test_create_dict_update():
    return # TODO: Finish later
