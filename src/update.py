import os
import sys
import time
import requests
import json
import threading

# update checker
def check_for_updates():
    global done, upd_request
    try:
        upd_request = requests.get("https://raw.githubusercontent.com/barsik0396/obje/refs/heads/main/update.json")
    except requests.exceptions.ConnectionError:
        done = True
        print("\r\x1b[0mFailed to download file (py-error requests.exceptions.ConnectionError). Check internet connection.")
        sys.exit(1)
    except Exception as e:
        done = True
        print(f"\r\x1b[0mFailed to download file (py-error {e}).")
        sys.exit(1)
    done = True

def update():
    global done
    done = False
    frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    threading.Thread(target=check_for_updates, daemon=False).start()
    try:
        # while not completed -> show spinner
        while not done:
            for item in frames:
                if done: 
                    break
            print(f"\r\x1b[96m{item}\x1b[36m", end="", flush=True)
            try:
                time.sleep(0.1)
            # on KeyboardInterrupt (ctrl+c)
            except KeyboardInterrupt:
                print("\r   \r\x1b[0m", end="")
                sys.exit(0)

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


    # --- get update data ---
    data = json.loads(upd_request.content)
    latest_stable = data["latest"]["stable"]
    latest_pre = data["latest"]["pre"]
    latest_nightly = data["latest"]["nightly"]

    dl_stable = data["download"]["stable"]
    dl_pre = data["download"]["stable"]
    dl_nightly = data["download"]["stable"]

    print(f"[dbg] {latest_stable}=latest_stable {latest_pre}=latest_pre {latest_nightly}=latest_nightly {dl_stable}=dl_stable {dl_pre}=dl_pre {dl_nightly}=dl_nightly")

    # if latest_(channel) == (installed version) -> ok
    # TODO: finish this part
    if latest_stable == "v0.1.0":
        print("\r\x1b[1;32m✔\x1b[0;92m You have latest version of Obje!\x1b[0m")