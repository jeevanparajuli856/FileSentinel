import os
import json
import hashlib
from notifier import fileChange
from logger import activityLogger

CONFIG_PATH = r"C:/Program Files/Integrixa/config/file_list.json"
#CONFIG_PATH = "C:/Users/Jeevan/Desktop/Integrixa/config/file_list.json"

#This function help to setup the file_list.json in the default path with default file list and return boolean if able to setup or not
def fileSetup():
    default_paths = {
        "C:/Windows/System32/drivers/etc/hosts": ""
    }
    
    try:
        # Ensure config directory exists and if file dont present then creat the file and write it down.
        config_dir = os.path.dirname(CONFIG_PATH)
        os.makedirs(config_dir, exist_ok=True)
        
        # Write default structure to file_list.json
        with open(CONFIG_PATH, "w") as f:
            json.dump({"paths": default_paths}, f, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to initialize config file: {e}")
        return False

# This function is to read the file_list.json config in format of path:hash and return dictionary
def readFileList():
    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            return data.get("paths", {})
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"[!] Error reading file list: {e}")
        return {}

#This function Writes the given filepath to file_list.json and if coudn't write it will resetup the file completely. Return Boolean if able to write the path or not
def writeFileList(data):
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump({"paths": data}, f, indent=2)
            return True
    except Exception as e:
        print(f"[!] Error writing file list: {e}")
        print(f"[+] Rewriting the monitoring file...")
        fileSetup() #later better to check from main.py to see the file present or not
        return False

# This function displays all monitored file paths
def showFilePath():
    paths = readFileList()
    print("\n[+] List of file paths being monitored:\n")
    for path in paths:
        print(f" - {path}")

# This function validates whether the given path exists in the system and file can be read or not and return boolean
def checkFilePath(path: str) -> bool:
    if not os.path.exists(path):
        print("[!] Invalid path. File not found on system.")
        return False
    # Try opening the file to ensure it's readable
    try:
        with open(path, "rb"):
            return True
    except PermissionError:
        print(f"[!] Permission denied: Cannot read file '{path}', so it cannot be added.")
        return False
    except Exception as e:
        print(f"[!] Error accessing file '{path}': {e}")
        return False

# This function open the file path and return the file hash. Calculates SHA-256 hash of a file
def getHash(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            content = f.read()
            return hashlib.sha256(content).hexdigest()
    except:
        return None

# This function update the hash of a specific file path in config. Return true or false
def updateFileHash(path: str) -> bool:
    paths = readFileList() 
    if path in paths: # making sure the path user given by user is in monitoring file
        new_hash = getHash(path)
        if new_hash:
            paths[path] = new_hash
            writeFileList(paths) #update the file hash
            fileChange(f"Hash updated for: {path}")
            activityLogger(f"Hash Updated for {path}")
            return True
    return False

#This function helps to updates hashes for all file paths
def updateAllFileHash():
    paths = readFileList()
    updated = 0
    for path in paths: # loop all path to update their new hash as baseline hash
        new_hash = getHash(path)
        if new_hash:
            paths[path] = new_hash
            updated += 1
    writeFileList(paths)
    fileChange(f"{updated} file hashes updated successfully.")
    activityLogger("All hashes refreshed successfully.")
    return f"[+] Updated hashes for {updated} files."

# This function adds a new path to monitor in the configuration file. Return the boolean
def addFilePath(path: str) -> bool:
    if not checkFilePath(path): # checking valid file path and can be read or not to get hash
        return False
    paths = readFileList() 
    if path in paths:
        print("[!] This path is already being monitored.")
        return False
    paths[path] = getHash(path) or "" #if hash not found it will update as ""
    writeFileList(paths)
    fileChange(f" File path added to monitor: '{path}' ")
    activityLogger(f"File path: {path} added")
    return True

#This function removes file path from a monitored config file and remove from monitoring
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