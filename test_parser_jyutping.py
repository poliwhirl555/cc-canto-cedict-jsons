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

# Single line, multiple defintions
def test_multi_def():
    expected = {"式": {"traditional": "式",  "simplified": "式", "pinyin": "shi4", "jyutping": "sik1", 
                    "definitions": ["type", "form", "pattern", "style", "formula", "standards", "ceremony", "ritual", "mode", "tense"]}}
    assert parse_cc_canto("test-input-files/cc-canto/single line multi def.txt") == expected

# Multi line, multi def
def test_multi_entry_single_def():
    expected = {"一夫": {"traditional": "一夫",  "simplified": "一夫", "pinyin": "yi1 fu1", "jyutping": "jat1 fu1", 
                    "definitions": ["One husband"]},
                "鰠": {"traditional": "鰠", "simplified": "鳋", "pinyin": "sao1", "jyutping": "sou1", 
                                    "definitions": ["carp"]},
                "件件": {"traditional": "件件",  "simplified": "件件", "pinyin": "jian4 jian4", "jyutping": "gin6 gin6", 
                                    "definitions": ["pieces (spoken)"]},
                "上天無路": {"traditional": "上天無路",  "simplified": "上天无路", "pinyin": "shang4 tian1 wu2 lu4", "jyutping": "soeng6 tin1 mou4 lou6", 
                                    "definitions": ["Come to a dead end;have no way out"]},
                "從": {"traditional": "從",  "simplified": "从", "pinyin": "cong2", "jyutping": "cung4", 
                                    "definitions": ["(preposition, conjunction, adverb) Since"]}}
    assert parse_cc_canto("test-input-files/cc-canto/multi line multi def.txt") == expected

# Multi line, multi def
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

# Multiple mapping to same Hanzi
def test_multi_map_to_same_hz():
    expected = {"重": {"traditional": "重",  "simplified": "重", "pinyin": "zhong4", "jyutping": "cung4", 
                    "definitions": ["to duplicate", "to overlap", "layer", "multiple", "double", "again", "once more", "afresh", "repeatedly", "successivey", "to repeat"]},
                "重": {"traditional": "重", "simplified": "重", "pinyin": "zhong4", "jyutping": "cung5", 
                                    "definitions": ["heavy", "weighty", "strong", "deep", "serious", "considerable in amount ", " value", "weight", "heavily", "severely"]},
                "重": {"traditional": "重",  "simplified": "重", "pinyin": "zhong4", "jyutping": "zung6", 
                                    "definitions": ["to attach importance to", "important", "significant", "solemn", "discreet", "furthermore", "still", "even", "also", "valuable", "in addition"]},
                "量": {"traditional": "量",  "simplified": "量", "pinyin": "liang4", "jyutping": "loeng4", 
                                    "definitions": ["to take a measurement", "to gauge", "to survey", "to deliberate", "to take into consideration"]},
                "量": {"traditional": "量",  "simplified": "量", "pinyin": "liang4", "jyutping": "loeng6", 
                                    "definitions": ["capacity", "quantity", "amount", "to estimate", "abbr. for 量词liàngcí [量词], classifier (in Chinese grammar)", "measure word", "to appraise", "to evaluate", "to limit"]}}
    assert parse_cc_canto("test-input-files/cc-canto/multi map to same hz.txt")

def test_multi_map_to_same_pinyin():
    # TODO
    return

def test_multi_map_to_same_jyutping():
    # TODO
    return
    