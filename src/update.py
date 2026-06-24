import os
import sys
import time
import requests
import json
import threading
from . import config
from .dbg import debug as dbg

# -- update checker --
def check_for_updates():
    dbg("upd: initing")
    global done, upd_request
    dbg("upd: downloading update.json")
    try:
        upd_request = requests.get("https://raw.githubusercontent.com/barsik0396/obje/refs/heads/main/update.json")
    except requests.exceptions.ConnectionError:
        dbg("err")
        done = True
        print("\r\x1b[0mFailed to download file (py-error requests.exceptions.ConnectionError). Check internet connection.")
        sys.exit(1)
    except Exception as e:
        done = True
        print(f"\r\x1b[0mFailed to download file (py-error {e}).")
        sys.exit(1)
    dbg("upd: done downloading update.json")
    done = True


# -- main update logic --
def update():
    config.load()
    dbg("initing")
    global done
    done = False
    frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    dbg("starting thread")
    threading.Thread(target=check_for_updates, daemon=False).start()
    try:
        dbg("showing spinner")
        # while not completed -> show spinner
        while not done:
            for item in frames:
                if done: 
                    break
                dbg(f"\r{config.data["debugger"]["prefix"]}spinner: next frame")
                print(f"\r\x1b[96m{item}\x1b[0m", end="", flush=True)
                try:
                    time.sleep(0.1)
                # on KeyboardInterrupt (ctrl+c)
                except KeyboardInterrupt:
                    print("\r   \r\x1b[0m", end="")
                    sys.exit(0)
        print("\r \r", end="")
        # if 404 -> show error and exit
        if upd_request.status_code == 404:
            print("\r\x1b[1;31m✗\x1b[0;91m Server returned 404")
            sys.exit(1)
    # -- if error --
    except Exception:
        try:
            print(f"\r\x1b[0m{" " * os.get_terminal_size().columns}\r", end="")
        except Exception:
            # fallback
            print("\r\x1b[0m   \r", end="")
            sys.exit(1)

    dbg("dt: loading data")
    # --- get update data ---
    data = json.loads(upd_request.content)
    dbg("dt-pe: latest stable")
    latest_stable = data["latest"]["stable"]
    dbg("dt-pe: latest pre")
    latest_pre = data["latest"]["pre"]
    dbg("dt-pe: latest nightly")
    latest_nightly = data["latest"]["nightly"]

    dbg("dt-pe: dl stable")
    dl_stable = data["download"]["stable"]
    dbg("dt-pe: dl pre")
    dl_pre = data["download"]["stable"]
    dbg("dt-pe: dl nightly")
    dl_nightly = data["download"]["stable"]

    dbg(f"dt-data: full = {data}")
    dbg(f"dt-data: latest_stable = {latest_stable}")
    dbg(f"dt-data: latest_pre = {latest_pre}")
    dbg(f"dt-data: latest_nightly = {latest_nightly}")
    dbg(f"dt-data: dl_stable = {dl_stable}")
    dbg(f"dt-data: dl_pre = {dl_pre}")
    dbg(f"dt-data: dl_nightly = {dl_nightly}")
    
    

    # -- update installer --
    # TODO: finish this part
    if not config.data["updates-channel"] in "nightly pre stable":
        print("error: ...")
        sys.exit(1)
    ch = config.data["updates-channel"]
    # --- check ---
    if ch == "nightly":

        if latest_nightly == "v0.0.9":
            print("\r\x1b[1;32m✔\x1b[0;92m You have latest version of Obje!\x1b[0m")
            sys.exit(1)
        else:
            print("\r\x1b[1;32mNew nightly build found!\x1b[0m")
    elif ch == "pre":
        if latest_pre == "v0.0.9":
            print("\r\x1b[1;32m✔\x1b[0;92m You have latest version of Obje!\x1b[0m")
            sys.exit(1)
        else:
            print("\r\x1b[1;32mNew pre build found!\x1b[0m")
    elif ch == "stable":
        if latest_stable == "v0.0.9":
            print("\r\x1b[1;32m✔\x1b[0;92m You have latest version of Obje!\x1b[0m")
            sys.exit(1)
        else:
            print("\r\x1b[1;32mNew release found!\x1b[0m")
    else:
        print("error: unk channel")
        sys.exit(1)
    
    # --- dl and install ---
    global done2
    done2 = False
    frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    if ch == "nightly":
        print("Downloading update...")
        try:
            dbg("showing spinner")
            while not done2:
                for item in frames:
                    if done2: 
                        break
                    dbg(f"\r{config.data["debugger"]["prefix"]}spinner: next frame")
                    print(f"\r\x1b[96m{item}\x1b[0m", end="", flush=True)
                    try:
                        time.sleep(0.1)
                    except KeyboardInterrupt:
                        print("\r   \r\x1b[0m", end="")
                        sys.exit(0)
            print("\r \r", end="")
            if upd_request.status_code == 404:
                print("\r\x1b[1;31m✗\x1b[0;91m Server returned 404")
                sys.exit(1)
        except json.decoder.JSONDecodeError:
            print("ok")
        # except Exception:
        #     try:
        #         print(f"\r\x1b[0m{" " * os.get_terminal_size().columns}\r", end="")
        #     except Exception:
        #         print("\r\x1b[0m   \r", end="")
        #         sys.exit(1)