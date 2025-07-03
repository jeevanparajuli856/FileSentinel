import os
import json
import hashlib
from datetime import datetime

# Path to config file
#CONFIG_PATH = "C:/ProgramData/FileSentinel/config/sentinel_config.json"
CONFIG_PATH = "C:/Users/Jeevan/Desktop/FileSentinel/config/sentinel_config.json"

# Default skeleton for initial config file creation
SKELETON = {
    "userid": "admin",
    "password": "Password@123",
    "bot_id": "",
    "chat_id": "",
    "log_start_time": ""
}

# Default salt for password hashing (for consistent, reversible comparison)
DEFAULT_SALT = "xxxxxxxxxxx" #put the consistent salting  

# Ensure config file exists with skeleton
#Ensures the sentinel_config.json file exists. If not, creates it using the default skeleton.
def initializeConfig():
    try:
        if not os.path.exists(CONFIG_PATH): # does nothing if exist only write if not exist we can use this in installer.py also 
            with open(CONFIG_PATH, "w") as file:
                json.dump(SKELETON, file, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to initialize config file: {e}")

# Read the full config file and return as dictionary
#Reads the configuration from sentinel_config.json. Returns the config as a dictionary. Falls back to SKELETON if file is unreadable or corrupted.
def readConfig():
    initializeConfig()
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("[ERROR] Config file is corrupted. Resetting to default.")
        writeConfig(SKELETON)
        return SKELETON
    except Exception as e:
        print(f"[ERROR] Failed to read config file: {e}")
        return SKELETON

# Overwrite the config file with provided dictionary
def writeConfig(data: dict):
    with open(CONFIG_PATH, "w") as file:
        json.dump(data, file, indent=2)

# Password Handling
#Hashes the provided password using SHA-256 and a default salt. Returns the hashed string.
def hashPassword(password: str) -> str:
    salted = DEFAULT_SALT + password
    return hashlib.sha256(salted.encode()).hexdigest()

#Updates the 'password' field in sentinel_config.json. Takes an already hashed password string. Returns True if successful, False on failure.
def updatePassword(password: str) -> bool:
    try:
        hashed_password= hashPassword(password)
        config = readConfig()
        config["password"] = hashed_password
        writeConfig(config)
        return True
    except:
        return False

#Reads and returns the hashed password from config.
def readPassword() -> str:
    config = readConfig()
    return config.get("password", "")

#User ID Handling
#Updates the 'userid' field in the config file. Returns True if successful, False on failure.
def updateUserID(userId: str) -> bool:
    try:
        config = readConfig()
        config["userid"] = userId
        writeConfig(config)
        return True
    except:
        return False

#Reads and returns the 'userid' from config.
def readUserID() -> str:
    config = readConfig()
    return config.get("userid", "")

# Telegram Configuration

#Sets or updates the Telegram bot ID and chat ID in the config file. Returns True if successful, False on failure.
def setTelegramId(botId: str, chatId: str) -> bool:
    try:
        config = readConfig()
        config["bot_id"] = botId
        config["chat_id"] = chatId
        writeConfig(config)
        return True
    except:
        return False
    
#Fetches the Telegram bot ID and chat ID from the config file. Returns a dictionary
def getTelegramId() -> dict:
    config = readConfig()
    return {
        "bot_id": config.get("bot_id", ""),
        "chat_id": config.get("chat_id", "")
    }

# Log Time Handling
#Reads and returns the log_start_time from the config file
def readTimeLogger() -> str:
    config = readConfig()
    return config.get("log_start_time", "")


#Updates the log_start_time field with the given timestamp. The timestamp must be in 'YYYY-MM-DD HH:MM:SS' format.
def updateTimeLogger(currentTime: str) -> None:
    config = readConfig()
    config["log_start_time"] = currentTime
    writeConfig(config)
