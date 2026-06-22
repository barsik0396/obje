import sys
import os
import time
import threading
import requests
import json

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
                            print("\r           \r\x1b[0m", end="")
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
                    print("\r\x1b[0m                                       \r", end="")
                sys.exit(1)


            # --- update data ---
            data = json.loads(upd_request.content)
            latest_stable = data["latest"]["stable"]
            latest_pre = data["latest"]["pre"]
            latest_nightly = data["latest"]["nightly"]

            dl_stable = data["download"]["stable"]
            dl_pre = data["download"]["stable"]
            dl_nightly = data["download"]["stable"]
            
            # if latest_(channel) == (installed version) -> ok
            # TODO: finish this part
            if latest_stable == "v0.1.0":
                print("\r\x1b[1;32m✔\x1b[0;92m You have latest version of Obje!\x1b[0m")