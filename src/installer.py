import os
import ctypes
from filepath_config import fileSetup, updateAllFileHash
from fileutils import initializeConfig, updateTimeLogger, updateTimeMonitor

# Constants
BASE_DIR = r"C:/ProgramData/FileSentinel"
CONFIG_DIR = os.path.join(BASE_DIR, "config")
LOG_DIR = os.path.join(BASE_DIR, "logs")
MARKER_FILE = os.path.join(BASE_DIR, ".installed")

#This functin creates the main FileSentinel directory structure and initializes config files.
def installSetup():
    try:
        # Create main program directory
        os.makedirs(CONFIG_DIR, exist_ok=True)
        os.makedirs(LOG_DIR, exist_ok=True)
        

        # Call external module functions
        fileSetup()              # Initializes file_path.json
        initializeConfig()       # Initializes sentinel_configuration.json

        # Create installation marker
        with open(MARKER_FILE, "w") as f:
            f.write("installed")

        return True
    except Exception as e:
        print(f"[!] Installation failed: {e}")
        return False

#This function restricts access to the config directory so only administrators can access it. Works on Windows using icacls command.
def managePermission():
    try:
          # Remove inherited permissions
        os.system(f'icacls "{CONFIG_DIR}" /inheritance:r')

        # Grant full access to SYSTEM and Administrators (your tool runs as Admin)
        os.system(f'icacls "{CONFIG_DIR}" /grant:r SYSTEM:F')
        os.system(f'icacls "{CONFIG_DIR}" /grant:r Administrators:F')

        # Deny WRITE access to Users and Everyone (read is OK for basic system ops)
        os.system(f'icacls "{CONFIG_DIR}" /grant:r Users:RW')

        return True
    except Exception as e:
        print(f"[!] managePermission() failed: {e}")
        return False

#This function calls the function to update hashes for all monitored files.
def updateDefaultFileHash():
    try:
        a= updateAllFileHash()
        return True
    except Exception as e:
        print(f"[!] updateDefaultFileHash() failed: {e}")
        return False

#This function is a master installation function that sets up directory, permissions, and file hashes. Returns True if all steps succeed, else False.
def install():
    if installSetup():
        if updateDefaultFileHash():
            if updateTimeLogger(): # not using managePermission as it is locking my program to access directory
                if updateTimeMonitor():
                    return True
    return False