import pytest
import requests
import os.path
import glob
from parser import *
from update import *

def test_fetch_raw():
    raw_paths = fetch_raw()
    assert len(raw_paths) == 2

def test_clean_raws():
    return
    