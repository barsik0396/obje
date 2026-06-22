import sys
import os
import time
import threading
import requests
import json
from . import update

# init
def init():
    # -- load config --
    if not os.path.isdir(os.path.expanduser("~/.obje/")):
        os.makedirs(os.path.expanduser("~/.obje/"), exist_ok=True)
    if os.path.isfile(os.path.expanduser("~/.obje/config.json")):
        try:
            with open(os.path.expanduser("~/.obje/config.json"), "rb") as f:
                config_text = f.read()
            config = json.loads(config_text)
        except json.decoder.JSONDecodeError:
            print("Failed to parse config")
            sys.exit(1)
    else:
        try:
            _ = requests.get("https://raw.githubusercontent.com/barsik0396/obje/refs/heads/main/config.json.example")
            with open(os.path.expanduser("~/.obje/config.json"), "wb") as f:
                f.write(_.content)
        except Exception as e:
            print("Failed to download config:")
            print(f" {e}")
            sys.exit(1)
        init()

    # -- help --
    if len(sys.argv) < 2:
        print("Obje - \x1b[37;1mModern and fast build system\x1b[0m")
        print("")
        print("  \x1b[37;1mUSAGE\x1b[0m")
        print(f"    {sys.argv[0].removeprefix("/home/barsik/obje/dist/").removeprefix("/usr/bin/").removeprefix("/usr/local/bin/").removeprefix("/usr/sbin/").removeprefix("/bin/")} [command] [subcommand] [flags]")
        print("")
        print("  \x1b[37;1mCOMMANDS\x1b[0m")
        print("    update                   Update Obje")
    else:
        # -- updater --
        if sys.argv[1] == "update":
            update.update()