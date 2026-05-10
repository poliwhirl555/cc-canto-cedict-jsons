import io
import pytest
from parser import *

# Single line parse, simple entry
def test_single_def_parse():
    assert parse_cc_canto("test-input-files/cc-canto/single line def.txt") == {"鰠": 
                                                            {"traditional": "鰠", 
                                                             "simplified": "鳋", 
                                                             "pinyin": "sao1", 
                                                             "jyutping": "sou1", 
                                                             "definitions": ["carp"]}
                                                            }

# Single line, multiple defintions/
def test_multi_def_parse():
    expected = {"式": {"traditional": "式",  "simplified": "式", "pinyin": "shi4", "jyutping": "sik1", 
                    "definitions": ["type", "form", "pattern", "style", "formula", "standards", "ceremony", "ritual", "mode", "tense"]}}
    assert parse_cc_canto("test-input-files/cc-canto/single line multi def.txt") == expected