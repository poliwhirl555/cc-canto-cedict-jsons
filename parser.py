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

# Input: CC-Canto file
# Output: A (k,v) map of v = dicts containing all the information in an entry, k = the traditional character
def parse_cc_canto(file, surnames = True):
    entries = {}
    with open(file, "r", encoding="utf8") as f:

        for line in f:
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

            # Added a toggle for surnames, with the default being true as to capture a full scope of the dictionary
            # Skip surname if surname toggle is false and the entry has surname in it's definition
            # Hmm, actually this might not work since the surname is added as a definition within the definitions, and not as something separate
            # Might be good though, since I can just keep it in and not have to worry about this
            if not surnames and "surname" in definitions:
                continue

            entry = {"traditional": traditional, "simplified": simplified, "pinyin": pinyin, "jyutping": jyutping, "definitions": definitions}
            
            


            # Block to handle hanzi with multiple pronounciations and entries, like 重, which has 4 entries.
            # Converts into bucket if something hashes into the same key, else add normally
            if not entries.get(traditional):
                entries[traditional] = entry
            elif type(entries[traditional]) is list:
                entries[traditional].append(entry)
            else:
                entries[traditional] = [entries[traditional], entry]
            

    return entries





            



            

