import os
import json
import hashlib
from notifier import fileChange
from logger import activityLogger

#CONFIG_PATH = "C:/ProgramData/FileSentinel/config/file_list.json"
CONFIG_PATH = "C:/Users/Jeevan/Desktop/FileSentinel/config/file_list.json"

#This function help to setup the file_list.json in the default path with default file list and return boolean if able to setup or not
def fileSetup():
    default_paths = {
        "C:/Windows/System32/drivers/etc/hosts": ""
    }
    
    try:
        # Ensure config directory exists
        config_dir = os.path.dirname(CONFIG_PATH)
        os.makedirs(config_dir, exist_ok=True)
        
        # Write default structure to file_list.json
        with open(CONFIG_PATH, "w") as f:
            json.dump({"paths": default_paths}, f, indent=2)
        return True
    except Exception as e:
        return False

# Reads the file_list.json config
def readFileList():
    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            return data.get("paths", {})
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"...Error reading file list: {e}")
        return {}

# Writes the given dictionary to file_list.json
def writeFileList(data):
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump({"paths": data}, f, indent=2)
            return True
    except Exception as e:
        print(f"Error writing file list: {e}")
        print(f"Re-writing the monitoring file..")
        fileSetup()
        return False

# Displays all monitored file paths
def showFilePath():
    paths = readFileList()
    print("\nList of File Paths being monitored:\n")
    for path in paths:
        print(f" - {path}")

# Validates whether the given path exists in the system and file can be read or not

def checkFilePath(path: str) -> bool:
    if not os.path.exists(path):
        print("...Invalid path. File not found on system.")
        return False
    # Try opening the file to ensure it's readable
    try:
        with open(path, "rb"):
            return True
    except PermissionError:
        print(f"...Permission denied. Cannot read file: {path} so, cannot be added")
        return False
    except Exception as e:
        print(f"Error accessing file: {path} — {e}")
        return False

# Calculates SHA-256 hash of a file
def updateHash(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            content = f.read()
            return hashlib.sha256(content).hexdigest()
    except:
        return None

# Updates the hash of a specific file path in config
def updateFileHash(path: str) -> bool:
    paths = readFileList()
    if path in paths:
        new_hash = updateHash(path)
        if new_hash:
            paths[path] = new_hash
            writeFileList(paths)
            fileChange(f"Hash updated for: {path}")
            activityLogger(f"Hash Updated for {path}")
            return True
    return False

# Updates hashes for all file paths
def updateAllFileHash():
    paths = readFileList()
    updated = 0
    for path in paths:
        new_hash = updateHash(path)
        if new_hash:
            paths[path] = new_hash
            updated += 1
    writeFileList(paths)
    fileChange("All file hashes updated.")
    activityLogger("All hashes refreshed.")
    print(f"...Updated hashes for {updated} files")

# Adds a new path to monitor
def addFilePath(path: str) -> bool:
    if not checkFilePath(path):
        return False
    paths = readFileList()
    if path in paths:
        print("...This path is already being monitored")
        return False
    paths[path] = updateHash(path) or ""
    writeFileList(paths)
    fileChange(f"File path added to monitor: {path}")
    activityLogger(f"File path: {path} added")
    updateFileHash(path)
    return True

# Removes a monitored path
def removeFilePath(path: str) -> bool:
    paths = readFileList()
    if path in paths:
        del paths[path]
        writeFileList(paths)
        fileChange(f"File path removed from monitor: {path}")
        activityLogger(f"File path removed: {path}")
        return True
    else:
        return False