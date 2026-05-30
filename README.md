
Things to Write

- How to install
- Examples on how core parts of the API work.
    - Fetching data by traditional
    - Fetching data by something that returns multiple entries

- Things I might add in the future
    - Helper functions for dealing with data (A function that takes a list of entries that have the same key and strips out the surnames)


The data for CC-CEDICT and CC-Canto, preprocessed into keyed hashmap JSONs for programmatic convenience, along with a Python library to provide access to that data.

Looking online, I've only found parsers in varying languages for the data of CC-EDICT (and none for CC-Canto) , but not the data itself preprocessed, which can be annoying to deal with as you have to figure out how to install it, so I created this project to provide that pre-processed data, as a variety of keyed hashmaps. As well, spawning off this project is also a Python library for generating and updating these JSONs, along with accessing the data, although that second part is probably a dime a dozen.

Each JSON file is affixed with "key_[something]" which denotes which field the hashmap uses as the key. The valid key fields are simplified, traditional, pinyin, jyutping (for CC-Canto), definition (a python list saved as a string), and none, which is a simple list of the dictionary entries.

Provided as well are the raw zips for the data and the text files, dated to allow you to check for recency. Maybe someday I'll get it to update monthly, if I can figure out how to get Github Actions to work for that.

## The Python Library

### Installation

```
insert pip console command here
```

### Modules

The core Python library consists of three files: _parser.py_, which handles parsing the raw text files sourced from the CC-CEDICT and CC-Canto websites and creating the JSONs; _update.py_, which handles fetching the data from those websites and calls functions from parser to generate the JSONS in the right place; and _CC\_Dict.py_, which provides the the class CC_Dict for easier programmatic access of the paths for the JSONs or the data in the JSONs.

The two modules you'll most likely work with are _update.py_ and _CC\_Dict.py_.

### _update.py_

```
# Loads the raws, the plain txt files and the JSONS for both CC-CEDICT and CC-Canto to json_end_dir, if provided, else to current working directory.
load_latest_data(json_end_dir = "")
```


