# import sqlite3

# These being in capitals causes so much grief I should really just change them to lowercase
DICT_TYPES = ["CEDICT", "CANTO", "READINGS"]
VALID_KEYS = {DICT_TYPES[0]: ["traditional", "simplified", "pinyin", "jyutping", "definitions", None],
                DICT_TYPES[1]: ["traditional", "simplified", "pinyin", "jyutping", "definitions", None],
                DICT_TYPES[2]: ["traditional", "simplified", "pinyin", None]}

# Parsing code based on code in Jyut Dictionary
# https://github.com/aaronhktan/jyut-dict/blob/main/src/dictionaries/cedict/generate-readings.py

def parse(filepath, dict_type, key = None):
    """
    Parse a dictionary text file into a keyed JSON.

    Parse the given raw dictionary text file of dictionary type *dict_type* at *filepath* into a JSON file 
    containing a dict of entries keyed with *key*, or a list of entries if *key* is none.

    Args:
        filepath (str): Path to txt or u8 file containing dictionary data to parse.
        dict_type (str): Type of dictionary data being parsed. Must be valid, as defined in parser.py
        key (str): Key of output dictionary. Must be valid for the dictionary type, as defined in parser.py
    """

    # Check if dict_type is valid
    if dict_type not in DICT_TYPES:
        raise ValueError("Invalid dictionary type")
    
    # Check if the entered key is valid
    if key not in VALID_KEYS[dict_type]:
            raise ValueError(f"Invalid key. Property does not exist in CC-{dict_type}.")

    if key == None:
        entries = []
    else:
        entries = {}

    with open(filepath, "r", encoding="utf8") as f:
        for line in f:
            # Might be good to move everything below into it's own get_entry function, but that might impact readability and be unnecessary
            # Depends on when and if I do the SQLite version
            if len(line) == 0 or line[0] == "#":
                continue

            split = line.split()  # Splits by whitespace
            traditional = split[0]
            simplified = split[1]
            pinyin = line[line.index("[") + 1 : line.index("]")].lower().replace("v", "u:").replace("[", ""). replace("]", "") # Strip extra [] for V2 CC_CEDICT entries
            if dict_type == DICT_TYPES[1]:
                jyutping = line[line.index("{") + 1 : line.index("}")].lower()
            

            # Seems like there are python style comments marked by # in the defintions that need handling (see the test input file)
            # This takes care of the comments since it leaves off everything after the last part of the defintion
            # The comments might be useful when trying to merge definitions with the CC-EDICT ones, since the comments say which
            # entries were adapted from CC-EDICT
            definitions = []
            if not dict_type == DICT_TYPES[2]:
                definitions = line[line.index("/") + 1 : line.rindex("/")].split("/")

            entry = {"traditional": traditional, "simplified": simplified, "pinyin": pinyin}

            if dict_type == DICT_TYPES[1]:
                entry["jyutping"] = jyutping

            if not dict_type == DICT_TYPES[2]:
                entry["definitions"] = definitions

            storage = None
            if key == "definitions":
                # Temporarily convert the definitions list to a string so 
                # it can be used as a dictionary key without having to change too much code.
                # As lists are not serializable.
                storage = entry[key]
                entry[key] = str(entry[key])
                
            # Block to handle hanzi with multiple pronounciations and entries, like 重, which has 4 entries, 
            # or if sorting by non-default keys, anything that ends up with the same key
            # Converts into bucket if something hashes into the same key, else add normally
            # If there is no key, just add to the list
            if key == None:
                entries.append(entry)
            elif not entries.get(entry[key]):
                entries[entry[key]] = entry
            elif type(entries[entry[key]]) is list:
                entries[entry[key]].append(entry)
            else:
                entries[entry[key]] = [entries[entry[key]], entry]

            # Restore the definition list back to being a list if it was changed
            if storage:
                entry[key] = storage

    return entries

def parse_cc_canto(filepath, key = "traditional") -> (list[dict] | dict):
    """
    Parse provided CC-Canto dictionary text file into a JSON dict keyed with input key.

    Returns either a list of dicts cointaining dictionary entries if key is None, or a dict containing entries of (key, entry dict).

    Args:
        filepath (str): Path to text or u8 file containing raw dictionary data
        key (str): Valid key as defined in parser.py, to key the output JSON with
    """
    return parse(filepath, DICT_TYPES[1], key)

def parse_cc_cedict(filepath, key = "traditional", surnames = True) -> (list[dict] | dict):
    """
    Parse provided CC-CEDICT dictionary text file into a JSON dict keyed with input key.

    Returns either a list of dicts cointaining dictionary entries if key is None, or a dict containing entries of (key, entry dict).

    Args:
        filepath (str): Path to text or u8 file containing raw dictionary data
        key (str): Valid key as defined in parser.py, to key the output JSON with
        surnames (bool): _Unused_ For future implementation of the ability to exclude surname entries.
    """
    # Might need to change this later if I add surname exclusion
    return parse(filepath, DICT_TYPES[0], key)

def parse_readings(filepath, key = "traditional") -> dict:
    """
    Parse provided CC-CEDICT Jyutping reading file into a JSON dict keyed with input key.

    Returns either a list of dicts cointaining reading entries if key is None, or a dict containing entries of (key, entry dict).

    Args:
        filepath (str): Path to text or u8 file containing raw dictionary data
        key (str): Valid key as defined in parser.py, to key the output JSON with
    """
    return parse(filepath, DICT_TYPES[2], key)

# Maybe add a surname remover at some point
# And or some SQLite integration later as well, for easier searching