from . import config

def debug(text):
    if config.data["debugger"]["enabled"]:
        print(f"{config.data["debugger"]["prefix"]}{text}")