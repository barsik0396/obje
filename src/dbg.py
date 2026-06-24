from . import config
import os, sys

def debug(text):
    if os.environ.get("OBJE_DEBUGGER_ENABLED", "false") == "false":
        enabled = False
    elif os.environ.get("OBJE_DEBUGGER_ENABLED", "false") == "true":
        enabled = True
    else:
        print("error: ")
        sys.exit(1)
    if config.data["debugger"]["enabled"] or enabled:
        print(f"{config.data["debugger"]["prefix"]}{text}")