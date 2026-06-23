import json
import os
import sys
import datetime as dt

def _lconf(path):
    global data
    try:
        with open("Objeconf.json", "r") as f:
           data = json.loads(f.read())
    except  json.decoder.JSONDecodeError:
        print("=== \x1b[1;31mObjeconf crashed\x1b[0m ===")
        print(f"Date: {dt.datetime.now()}")
        print("Error: json.decoder.JSONDecodeError (Failed to load config)")
        print("Crashcode: 3wokd")
        print("See \x1b[94;1m\u001b]8;;https://barsik0396.github.io/obje/crashcode/3wokd\u001b\\documentation\u001b]8;;\u001b\\\x1b[0m for more details.")
        sys.exit(1)
    except Exception as e:
        print("=== \x1b[1;31mObjeconf crashed\x1b[0m ===")
        print(f"Date: {dt.datetime.now()}")
        print(f"Error: {e}")
        print(f"Crashcode: 5d40n")
        print("See \x1b[94;1m\u001b]8;;https://barsik0396.github.io/obje/crashcode/5d40n\u001b\\documentation\u001b]8;;\u001b\\\x1b[0m for more details.")
        sys.exit(1)

def load():
    global config
    if os.path.isfile("Objeconf.json"):
        _lconf("Objeconf.json")
    elif os.path.isfile(os.path.expanduser("~/.obje/Objeconf.json")):
        _lconf(os.path.expanduser("~/.obje/Objeconf.json"))
    else:
        print("=== \x1b[1;31mERROR\x1b[0m ===")
        print("No obje configuration found.")
        print("Create config via")
        print("  \x1b[30mobje configure -p\x1b[0m")
        print("Or")
        print("  \x1b[30mobje configure -g\x1b[0m")
        sys.exit(1)