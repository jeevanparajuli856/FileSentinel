import os
import sys
from installer import install
from cli import cliMain

# Define all required paths
BASE_DIR = "C:/ProgramData/FileSentinel"
CONFIG_DIR = os.path.join(BASE_DIR, "config")
LOG_DIR = os.path.join(BASE_DIR, "logs")
CONFIG_FILE = os.path.join(CONFIG_DIR, "sentinel_config.json")
FILE_LIST = os.path.join(CONFIG_DIR, "file_list.json")
INSTALL_FLAG = os.path.join(BASE_DIR, ".installed")

#Checks whether FileSentinel has already been installed correctly. If any critical file or folder is missing, returns False.
def checkInstallation():
    if not os.path.exists(INSTALL_FLAG):
        print("installed")
        return False
    if not os.path.exists(BASE_DIR):
        print("[!] Missing or incomplete installation detected. Reinstalling components...")
        return False

    if not os.path.exists(CONFIG_DIR) or not os.path.exists(LOG_DIR):
        print("[!] Missing or incomplete installation detected. Reinstalling components...")
        return False

    if not os.path.isfile(CONFIG_FILE) or not os.path.isfile(FILE_LIST):
        print("[!] Missing or incomplete installation detected. Reinstalling components...")
        return False

    return True

#Entry point for the FileSentinel program. Checks installation status and calls install() or cliMain() accordingly.
def main():
    if checkInstallation():
        # All good, run the CLI normally
        cliMain(False,"")
    else:
        install()
        cliMain(True,"[+] Hi Admin, welcome to FileSentinel. Please set up your account.")

if __name__ == "__main__":
    main()
    sys.exit(0)