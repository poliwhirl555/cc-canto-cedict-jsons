import requests
import time
from pathlib import Path
from parser import DICT_TYPES, VALID_KEYS

# This does work and does get the file properly, only issue is the time isn't entered in properly because of formatting issues.
spec_time = time.gmtime()
# print(f"curr time: {spec_time}")
current_time = time.strftime("%Y-%m-%d_%H:%M_%Z", spec_time)
# print(current_time)
filename = f"cedict_1_0_ts_utf-8_mdbg_{current_time}.zip"
savefile = Path(filename)
# savefile = Path(f"../{filename}") # You can in fact save it with relative path syntax using Path
r = requests.get("https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip", timeout = 30)
print(r.headers)
# savefile.write_bytes(r.content)

# Thre's probably no need to read the time if this script is running once a month
# read_time = time.strptime(filename[filename.index("2") : filename.index(".")], "%Y-%m-%d_%H:%M_%Z")
# print(f"read time: {read_time}")

GET_LINKS = {"CEDICT": "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip",
             "CANTO": "https://cantonese.org/cccanto-170202.zip"}
FILE_PREFIXES = {"CEDICT": "cedict_1_0_ts_utf-8_mdbg_",
                 "CANTO": "cccanto-"}
# Fetch the raw zip files from the CC-CEDICT website
def fetch_raw():
    raw_paths = []
    for dt in DICT_TYPES:
        # Should probably check if the files already exist, and to delete them if they already exist. Maybe in a new method?
        # Check if a zip file with the lowercase of the dict type exists, and if so, delete them
        current_time = time.strftime("%Y-%m-%d_%H:%M_%Z", time.gmtime())
        filename = FILE_PREFIXES[dt] + current_time + ".zip"
        savefile = Path(filename)
        r = requests.get(GET_LINKS[dt], timeout = 30)
        savefile.write_bytes(r.content)
        raw_paths.append[savefile]
    return raw_paths

# # for each possible key, including none, generate the json for that key and save it to repository directory
# def generate_jsons():
#     # for dt in DICT_TYPES:
#     return
