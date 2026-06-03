from py_cc_dicts.parser import parse_cc_cedict

def test_single_entry_single_def_v2():
    expected = {"時常": {"traditional": "時常",  "simplified": "时常", "pinyin": "shi2chang2", "jyutping": "si4 soeng4",
                    "definitions": ["often; frequently"]}}
    assert parse_cc_cedict("tests/test-input-files/cc-cedict/single line single def v2.txt") == expected

def test_single_entry_multi_def_v2():
    expected = {"是": {"traditional": "是", "simplified": "是", "pinyin": "shi4", "jyutping": "si6",
                    "definitions": ["to be (followed by substantives only)", "correct; right; true", "(respectful acknowledgement of a command) very well", "(adverb for emphatic assertion)"]}}
    assert parse_cc_cedict("tests/test-input-files/cc-cedict/single line multi def v2.txt") == expected

def test_mixed_v1_v2():
    expected = {"昭": {"traditional": "昭",  "simplified": "昭", "pinyin": "zhao1", "jyutping": "ciu1",
                    "definitions": ["bright", "clear", "manifest", "to show clearly"]},
                "是": {"traditional": "是", "simplified": "是", "pinyin": "shi4", "jyutping": "si6",
                    "definitions": ["to be (followed by substantives only)", "correct; right; true", "(respectful acknowledgement of a command) very well", "(adverb for emphatic assertion)"]},
                "時常": {"traditional": "時常",  "simplified": "时常", "pinyin": "shi2chang2", "jyutping": "si4 soeng4",
                    "definitions": ["often; frequently"]}}
    assert parse_cc_cedict("tests/test-input-files/cc-cedict/mixed v1 v2.txt") == expected