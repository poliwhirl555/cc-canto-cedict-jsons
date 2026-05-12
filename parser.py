# I think I have to write the parser myself, so I guess this is the file for it

# CC-Canto
# Split by whitepsace, first is trad, second is simplified, third is pinyin, fourth is jyutping
# Need to figure out how to deal with entries
# Should be every "; " splits into a new entry, so splitting by space is already good, but I can already see a typo in there

# Can source parsing code from here: https://github.com/aaronhktan/jyut-dict/blob/main/src/dictionaries/cedict/generate-readings.py
# Just have to remember to include the MIT License
# Do I even need to since I'm taking a subportion of the code and not the entire thing? Maybe I should just to be safe.

# Use Array, JSON< or SQL/some other sort of database? 
# Need to store the dictionaries in readable form somehow else it'll be annoying to have to run this each time.

# At this point, might as well create JSON and SQLite database version of the data, with an update script, so that
# I don't have to deal with this every time I want to access the data programmatically 

import sqlite3
from typing import List

# Parsing code based on code in Jyut Dictionary
# https://github.com/aaronhktan/jyut-dict/blob/main/src/dictionaries/cedict/generate-readings.py

def parse(filepath, key):
    # Might need a toggle for CC-CEDICT or CC_CANTO, but might not actually since I can just search for the *second* "[" and the first "]"
    # and that would handle both V1 and V2, and mixed version too.
    # But then I still need the toggle since I need to know to search for jyutping, and whether to add that to the dictionary or not
    # Although I could handle that programmatically as well, and just let the person dealing with the output check
    # Maybe I'll need the tag after all since I think CC-Canto and CC-CEDICT handle the surnames different, 
    # with the surnames being split out in CC-CEDICT while not in CC-CANTO,
    # so there would be no need for a surname toggle for CC-CANTO while there might in CC-EDICT

    # TODO: Just copy and pasted from parse_cc_canto, still need to modify for the above

    # Check if the entered key is valid
    if key not in ["traditional", "simplified", "pinyin", "jyutping", None]:
            raise ValueError("Invalid key. Property does not exist in CC-Canto entry.")
    
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
            pinyin = line[line.index("[") + 1 : line.index("]")].lower().replace("v", "u:")
            jyutping = line[line.index("{") + 1 : line.index("}")].lower()

            # Seems like there are python style comments marked by # in the defintions that need handling (see the test input file)
            # This takes care of the comments since it leaves off everything after the last part of the defintion
            # The comments might be useful when trying to merge definitions with the CC-EDICT ones, since the comments say which
            # entries were adapted from CC-EDICT
            definitions = line[line.index("/") + 1 : line.rindex("/")].split("/")

            entry = {"traditional": traditional, "simplified": simplified, "pinyin": pinyin, "jyutping": jyutping, "definitions": definitions}
            
            # Block to handle hanzi with multiple pronounciations and entries, like 重, which has 4 entries, 
            # or if sorting by non-default keys, anything that ends up with the same key
            # Converts into bucket if something hashes into the same key, else add normally
            # If there is no key, just add to the list
            if key == None:
                entries.append(entry)
            elif not entries.get(key):
                entries[entry[key]] = entry
            elif type(entries[key]) is list:
                entries[entry[key]].append(entry)
            else:
                entries[entry[key]] = [entries[entry[key]], entry]

    return entries

# Input: CC-Canto file path, a key to use for the dictionary, one of "traditional", "simplified", "pinyin", "jyutping" or None
# Output: A (k,v) map of v = dicts containing all the information in an entry, k = the inputed key 
#           OR a list of all entries if inputted key is none
def parse_cc_canto(filepath, key = "traditional"):
    return parse(filepath, key)

# Stub for a future parse CC-EDICT function. Moved the surname skipping toggle here since it'll probably be needed for CC-EDICT
def parse_cc_edict(filepath, surnames = True):
    # Might need to change this later
    return parse(filepath, key)



            



            

