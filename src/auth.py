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
        authLogger("New Auth Setup", userid, "FAILED")
        authNotifier("New Auth Setup", userid, "FAILED")
        return False
    if not setUserID(userid):
        authLogger("New Auth Setup", userid, "FAILED")
        authNotifier("New Auth Setup", userid, "FAILED")
        return False

    if not checkPasswordLen(password):
        authLogger("New Auth Setup", userid, "FAILED")
        authNotifier("New Auth Setup", userid, "FAILED")
        return False

    if not setPassword(password):
        authLogger("New Auth Setup", userid, "FAILED")
        authNotifier("New Auth Setup", userid, "FAILED")
        return False

    authLogger("New Auth Setup", userid, "SUCCESS")
    authNotifier("New Auth Setup", userid, "SUCCESS")
    return True

# Auth check during login
def checkAuth(userid: str, password: str) -> bool:
    stored_userid = readUserID()
    stored_password_hash = readPassword()

    input_userid = userid
    input_password_hash = hashPassword(password)

    if userIDLenCheck(userid) and input_userid == stored_userid and input_password_hash == stored_password_hash:
        authLogger("Login Attempt", userid, "SUCCESS")
        authNotifier("Login Attempt", userid, "SUCCESS")
        return True
    else:
        authLogger("Login Attempt", userid, "FAILED")
        authNotifier("Login Attempt", userid, "FAILED")
        return False

# Change password logic
def changePassword(new_password: str) -> bool:
    userid = readUserID()
    if not checkPasswordLen(new_password):
        authLogger("Password change attempt", userid, "FAILED")
        authNotifier("Password change attempt", userid, "FAILED")
        return False

    if not setPassword(new_password):
        authLogger("Password change attempt", userid, "FAILED")
        authNotifier("Password change attempt", userid, "FAILED")
        return False

    authLogger("Password change attempt", userid, "SUCCESS")
    authNotifier("Password change attempt", userid, "SUCCESS")
    return True

# Change user ID logic
def changeUserID(new_userid: str) -> bool:
    if not userIDLenCheck(new_userid):
        authLogger("UserID change attempt", new_userid, "FAILED")
        authNotifier("UserID change attempt", new_userid, "FAILED")
        return False
    if not setUserID(new_userid):
        authLogger("UserID change attempt", new_userid, "FAILED")
        authNotifier("UserID change attempt", new_userid, "FAILED")
        return False

    authLogger("UserID change attempt", new_userid, "SUCCESS")
    authNotifier("UserID change attempt", new_userid, "SUCCESS")
    return True
