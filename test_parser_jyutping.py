import io
import pytest
from parser import parse_cc_canto

# Single line parse, simple entry
def test_single_def():
    assert parse_cc_canto("test-input-files/cc-canto/single line def.txt") == {"鰠": 
                                                            {"traditional": "鰠", 
                                                             "simplified": "鳋", 
                                                             "pinyin": "sao1", 
                                                             "jyutping": "sou1", 
                                                             "definitions": ["carp"]}
                                                            }

# Single line, multiple defintions/
def test_multi_def():
    expected = {"式": {"traditional": "式",  "simplified": "式", "pinyin": "shi4", "jyutping": "sik1", 
                    "definitions": ["type", "form", "pattern", "style", "formula", "standards", "ceremony", "ritual", "mode", "tense"]}}
    assert parse_cc_canto("test-input-files/cc-canto/single line multi def.txt") == expected

def test_multi_entry_single_def():
    # TODO Finish
    expected = {"式": {"traditional": "式",  "simplified": "式", "pinyin": "shi4", "jyutping": "sik1", 
                    "definitions": ["type", "form", "pattern", "style", "formula", "standards", "ceremony", "ritual", "mode", "tense"]}}
    return

def test_multi_entry_multi_def():
    expected = {"亮": {"traditional": "亮",  "simplified": "亮", "pinyin": "liang4", "jyutping": "loeng6", 
                    "definitions": ["bright", "clear", "resonant", "to shine", "to show", "to reveal", "brightly, with understanding"]},
                "充": {"traditional": "充",  "simplified": "充", "pinyin": "chong1", "jyutping": "cung1", 
                    "definitions": ["to fill", "to satisfy", "to fulfill", "to act in place of", "substitute", "sufficient", "full", "to pose as", "to serve as", "to act as"]},
                "係": {"traditional": "係",  "simplified": "係", "pinyin": "xi4", "jyutping": "hai6", 
                    "definitions": ["(Cantonese) to be", "to connect", "to relate to", "to tie up", "to bind", "to be (literary)", "to involve", "relation", "relationship", "consequence", "yes", "indeed", "right"]},
                "開火": {"traditional": "開火",  "simplified": "开火", "pinyin": "kai1huo3", "jyutping": "hoi1 fo2", 
                    "definitions": ["(verb) 1. To switch on (a rice cooker, light, etc.); (of cooking)", "Turn on (a gas burner); (slang)", "Argue; 2. Fight"]}}
    assert parse_cc_canto("test-input-files/cc-canto/multi line multi def.txt") == expected