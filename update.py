import requests
from pathlib import Path
import time

# This does work and does get the file properly, only issue is the time isn't entered in properly because of formatting issues.
current_time = time.strftime("%Y-%m-%d_%H:%M_%Z", time.gmtime())
# print(current_time)
filename = f"cedict_1_0_ts_utf-8_mdbg_{current_time}.zip"
savefile = Path(filename)
r = requests.get("https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip")
# print(r.headers)
savefile.write_bytes(r.content)

