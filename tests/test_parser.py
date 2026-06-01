import pytest
from py_cc_dicts.parser import parse


def test_invalid_dict_type():
    with pytest.raises(ValueError) as exception_info:
        parse("tests/test-input-files/cc-canto/single line def.txt", "SOMETHING")

def test_key_none():
    expected = [{"traditional": "亮",  "simplified": "亮", "pinyin": "liang4", "jyutping": "loeng6", 
                    "definitions": ["bright", "clear", "resonant", "to shine", "to show", "to reveal", "brightly, with understanding"]},
                {"traditional": "充",  "simplified": "充", "pinyin": "chong1", "jyutping": "cung1", 
                    "definitions": ["to fill", "to satisfy", "to fulfill", "to act in place of", "substitute", "sufficient", "full", "to pose as", "to serve as", "to act as"]},
                {"traditional": "係",  "simplified": "係", "pinyin": "xi4", "jyutping": "hai6", 
                    "definitions": ["(Cantonese) to be", "to connect", "to relate to", "to tie up", "to bind", "to be (literary)", "to involve", "relation", "relationship", "consequence", "yes", "indeed", "right"]},
                {"traditional": "開火",  "simplified": "开火", "pinyin": "kai1huo3", "jyutping": "hoi1 fo2", 
                    "definitions": ["(verb) 1. To switch on (a rice cooker, light, etc.); (of cooking)", "Turn on (a gas burner); (slang)", "Argue; 2. Fight"]}]
    assert parse("tests/test-input-files/cc-canto/multi line multi def.txt", "CANTO") == expected

def test_key_none_multi_map_to_same_hz():
    expected = [{"traditional": "重",  "simplified": "重", "pinyin": "zhong4", "jyutping": "cung4", 
                    "definitions": ["to duplicate", "to overlap", "layer", "multiple", "double", "again", "once more", "afresh", "repeatedly", "successivey", "to repeat"]},
                {"traditional": "重", "simplified": "重", "pinyin": "zhong4", "jyutping": "cung5", 
                    "definitions": ["heavy", "weighty", "strong", "deep", "serious", "considerable in amount ", " value", "weight", "heavily", "severely"]},
                {"traditional": "重",  "simplified": "重", "pinyin": "zhong4", "jyutping": "zung6", 
                    "definitions": ["to attach importance to", "important", "significant", "solemn", "discreet", "furthermore", "still", "even", "also", "valuable", "in addition"]},
                {"traditional": "量",  "simplified": "量", "pinyin": "liang4", "jyutping": "loeng4", 
                    "definitions": ["to take a measurement", "to gauge", "to survey", "to deliberate", "to take into consideration"]},
                {"traditional": "量",  "simplified": "量", "pinyin": "liang4", "jyutping": "loeng6", 
                    "definitions": ["capacity", "quantity", "amount", "to estimate", "abbr. for 量词liàngcí [量词], classifier (in Chinese grammar)", "measure word", "to appraise", "to evaluate", "to limit"]}]
    assert parse("tests/test-input-files/cc-canto/multi map to same hz.txt", "CANTO") == expected

def test_definition_as_key():
    expected = {"[\'bright\', \'clear\', \'manifest\', \'to show clearly\']": {"traditional": "昭",  "simplified": "昭", "pinyin": "zhao1", 
                    "definitions": ["bright", "clear", "manifest", "to show clearly"]},
                "[\'to be (followed by substantives only)\', \'correct; right; true\', \'(respectful acknowledgement of a command) very well\', \'(adverb for emphatic assertion)\']": {"traditional": "是", "simplified": "是", "pinyin": "shi4",
                    "definitions": ["to be (followed by substantives only)", "correct; right; true", "(respectful acknowledgement of a command) very well", "(adverb for emphatic assertion)"]},
                "[\'often; frequently\']": {"traditional": "時常",  "simplified": "时常", "pinyin": "shi2chang2", 
                    "definitions": ["often; frequently"]}}
    assert parse("tests/test-input-files/cc-cedict/mixed v1 v2.txt", "CEDICT", "definitions") == expected


