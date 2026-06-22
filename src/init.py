import sys, os, time, threading, requests, json

def check_for_updates():
    global done, upd_request
    upd_request = requests.get("https://raw.githubusercontent.com/barsik0396/obje/refs/heads/main/update.json")
    done = True

def init():
    if len(sys.argv) < 2:
        print("Obje - \x1b[37;1mModern and fast build system\x1b[0m")
        print("")
        print(f"  \x1b[37;1mUSAGE\x1b[0m")
        print(f"    {sys.argv[0].removeprefix("/home/barsik/obje/dist/").removeprefix("/usr/bin/").removeprefix("/usr/local/bin/").removeprefix("/usr/sbin/").removeprefix("/bin/")} [command] [subcommand] [flags]")
        print("")
        print("  \x1b[37;1mCOMMANDS\x1b[0m")
        print("    update                   Update Obje")
    else:
        if sys.argv[1] == "update":
            global done
            done = False
            frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
            threading.Thread(target=check_for_updates, daemon=False).start()
            try:
                while done == False:
                    for item in frames:
                        if done == True: break
                        print(f"\r\x1b[96m{item}\x1b[36m", end="", flush=True)
                        time.sleep(0.1)
                if upd_request.status_code == 404:
                    print("\r\x1b[1;31m✗\x1b[0;91m Server returned 404")
                    sys.exit(1)
                print(f"\r\x1b[1;32m✔\x1b[0;92m You have latest version of Obje!\x1b[0m")
            except:
                try:
                    print(f"\r\x1b[0m{" " * os.get_terminal_size().columns}\r", end="")
                except:
                    print("\r\x1b[0m                                       \r", end="")
                sys.exit(1)