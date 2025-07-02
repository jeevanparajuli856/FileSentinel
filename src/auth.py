import re
import hashlib
from fileutils import hashPassword, updatePassword, updateUserID, readPassword, readUserID #handle the major configuration for authentication
from logger import authLogger #handles the logging
from notifier import authNotifier #handles the notification to telegram

# Hashes and stores the password using fileutils.hashPassword
def setPassword(password: str) -> bool:
    return updatePassword(password)

# Stores the user ID using fileutils.userID. Returns True if successful, False otherwise. UserID should be only alphanumeric(can be only alpha or both)
def setUserID(userid: str) -> bool:
    if not userid or userid.strip() == "" or not userid.isalnum():
        return False
    userid= userid.strip() #stripping for admin1   like username.
    return updateUserID(userid)

# Validates password to ensure it is at least 8 characters long and contains letters, numbers, and a symbol.
def checkPasswordLen(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True

# Checks if the user ID is less than or equal to 12 characters.
def userIDLenCheck(userid: str) -> bool:
    return len(userid) <= 12

# First-time authentication setup.
def setAuth(userid: str, password: str) -> bool:
    if not userIDLenCheck(userid):
        authLogger("Auth Setup", userid, "FAILED")
        authNotifier("Auth Setup", userid, "FAILED")
        return False
    if not setUserID(userid):
        authLogger("Auth Setup", userid, "FAILED")
        authNotifier("Auth Setup", userid, "FAILED")
        return False

    if not checkPasswordLen(password):
        authLogger("Auth Setup", userid, "FAILED")
        authNotifier("Auth Setup", userid, "FAILED")
        return False

    if not setPassword(password):
        authLogger("Auth Setup", userid, "FAILED")
        authNotifier("Auth Setup", userid, "FAILED")
        return False

    authLogger("Auth Setup", userid, "SUCCESS")
    authNotifier("Auth Setup", userid, "SUCCESS")
    return True

# Auth check during login
def checkAuth(userid: str, password: str) -> bool:
    stored_userid = readUserID()
    stored_password_hash = readPassword()

    input_userid = userid
    input_password_hash = hashPassword(password)

    if userIDLenCheck(userid) and input_userid == stored_userid and input_password_hash == stored_password_hash:
        authLogger("LOGIN_ATTEMPT", userid, "SUCCESS")
        authNotifier("LOGIN_ATTEMPT", userid, "SUCCESS")
        return True
    else:
        authLogger("LOGIN_ATTEMPT", userid, "FAILED")
        authNotifier("LOGIN_ATTEMPT", userid, "FAILED")
        return False

# Change password logic
def changePassword(new_password: str) -> bool:
    userid = readUserID()
    if not checkPasswordLen(new_password):
        authLogger("Password Change", userid, "FAILED")
        authNotifier("Password Change", userid, "FAILED")
        return False

    if not setPassword(new_password):
        authLogger("Password Change", userid, "FAILED")
        authNotifier("Password Change", userid, "FAILED")
        return False

    authLogger("Password Change", userid, "SUCCESS")
    authNotifier("Password Change", userid, "SUCCESS")
    return True

# Change user ID logic
def changeUserID(new_userid: str) -> bool:
    if not userIDLenCheck(new_userid):
        authLogger("Auth Setup", new_userid, "FAILED")
        authNotifier("Auth Setup", new_userid, "FAILED")
        return False
    if not setUserID(new_userid):
        authLogger("Auth Setup", new_userid, "FAILED")
        authNotifier("Auth Setup", new_userid, "FAILED")
        return False

    authLogger("UserID Change", new_userid, "SUCCESS")
    authNotifier("UserID Change", new_userid, "SUCCESS")
    return True

# log format: [2025-06-28 14:45:02] LOGIN_ATTEMPT/UserID Change/Password Change/Auth Setup | UserID: userid | IP: 127.0.0.1 | Status: SUCCESS/FAILED

#Alert Format
# 🔐 [FileSentinel Alert]
#   message: LOGIN_ATTEMPT/UserID Change/Password Change/Auth Setup 
# 👤 UserID: userid
# 🕒 Time: 2025-06-28 14:47:22
# 📍 IP Address: 127.0.0.1
# ✅ Status: SUCCESS/FAILED
