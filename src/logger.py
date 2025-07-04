import os # to write and delete the file
import socket # to get ip
from datetime import datetime
import time
from fileutils import readTimeLogger, updateTimeLogger, readUserID 

#  Global Constants
logDir = "C:/ProgramData/FileSentinel/logs"
#logDir = "C:/Users/Jeevan/Desktop/FileSentinel/logs" # for testing only
authLogFile = "auth.log"
teleLogFile = "teleAlert.log"
activityLogFile = "activity.log"
monitorLogFile = "monitor.log"
#Helper Constants
localIpAddress = socket.gethostbyname(socket.gethostname())

# Utility Function to Get Current Timestamp. Returns current timestamp as a formatted string.
def getCurrentTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") # it is on 24 hr format


#This is core Function to Write Logs
#Writes the given log line to the specified log file. Creates the log file if it does not exist. Adds error handling to ensure the program doesn't crash.
def logWriter(logLine, fileName):

    try:
        os.makedirs(logDir, exist_ok=True)
        filePath = os.path.join(logDir, fileName)
        with open(filePath, 'a', encoding='utf-8') as file:
            file.write(logLine + '\n')
    except Exception as error:
# Error if logWritter cannot write the log
        print(f"[LOG ERROR] Failed to write log to {fileName}: {error}")

# Authentication Logger
#This function logs authentication-related events such as login attempts,password changes, or authentication setup.
def authLogger(eventType, userId, status):
    currentTime = getCurrentTime()
    logLine = f"[{currentTime}] {eventType} | UserID: {userId} | IP: {localIpAddress} | Status: {status.upper()}"
    logWriter(logLine, authLogFile)

# Telegram Alert Logger
#This function logs failed Telegram message alerts only.
def telegramAlertLogger(messageSummary):
        currentTime = getCurrentTime()
        logLine = f"[{currentTime}] [ERROR] Message failed to send to Telegram: '{messageSummary}'"
        logWriter(logLine, teleLogFile)

# Activity Logger
#This function logs general activities performed by the user.
def activityLogger(message):
    currentTime = getCurrentTime()
    logLine = f"[{currentTime}] {message} | UserID: {readUserID()} | IP: {localIpAddress}"
    logWriter(logLine, activityLogFile)

# File Monitor Logger
#This function logs alerts or info messages from the file integrity monitoring module.
def monitorLogger(message):
    currentTime = getCurrentTime()
    logLine = f"[{currentTime}] [ALERT] {message} | UserID: {readUserID()} | IP: {localIpAddress}"
    logWriter(logLine, monitorLogFile)

# Log Purging Function
#This function checks if it has been more than 2 days since the last log update. If so, deletes all logs and updates the last log time in configuration.
def logPurger():
    try:
        lastLogTime = readTimeLogger()  # Returns time as string: "YYYY-MM-DD HH:MM:SS"
        lastLogEpoch = time.mktime(time.strptime(lastLogTime, "%Y-%m-%d %H:%M:%S"))
        currentEpoch = time.time()

        # Compare with 2-day threshold (2 * 86400 seconds)
        if currentEpoch - lastLogEpoch > 2 * 86400:
            for logFile in [authLogFile, teleLogFile, activityLogFile, monitorLogFile]:
                logPath = os.path.join(logDir, logFile)
                try:
                    if os.path.exists(logPath):
                        os.remove(logPath)
                except Exception as deleteError:
                    activityLogger(f"[LOG PURGE ERROR] Failed to delete {logFile}: {deleteError}")

            updateTimeLogger()

    except Exception as purgeError:
        activityLogger(f"[LOG PURGE ERROR] {purgeError}")

#Demo format for the logs
#[2025-06-28 14:42:11] [ERROR] [Failed] Message sent/failed to send to Telegram: 'summary of msg' -> for telegram alert only fail msg
#[2025-06-28 14:45:02] msg | UserID: userid | IP: 127.0.0.1  -> activity logs
#[2025-06-28 14:42:11] [ALERT] msg(file path deleted, hash updated for file path)|userID: | IP: -> monitoring file log
#[2025-06-28 14:45:02] LOGIN_ATTEMPT/UserID Change/Password Change/Auth Setup | UserID: userid | IP: 127.0.0.1 | Status: SUCCESS/FAILED  -> auth logs

