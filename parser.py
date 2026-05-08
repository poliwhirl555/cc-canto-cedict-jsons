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
def parse_cc_canto(file):
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
            definitions = line[line.index("/") + 1 : line.rindex("/")].split("/")
            entry = {"traditional": traditional, "simplified": simplified, "pinyin": pinyin, "jyutping": jyutping, "definitions": definitions}
            # Might need to add code to remove surnames, not sure how this handles characters with multiple pronounciations and definitions
            # Example would be 重. Has 4 different entries, and the key has to be unique
            # Trick might be to check first if the key exists, 
            # if it does, check if it's a list, 
            # if it is not, then create a list with the current entry, and append the new entry to it
            # Should still probably skip surnames though
            entries[traditional] = entry

    return entries

            



            

