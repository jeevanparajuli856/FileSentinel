import os
import sys
import time
import psutil # type: ignore
import subprocess
from daemonStartHelp import daemonStartWatchdog
from fileutils import readDaemonStatus,readDaemonStatus
from logger import activityLogger
from notifier import fileChange
from logger import activityLogger
from notifier import fileChange

PID_PATH = r"C:/Program Files/FileSentinel/config/daemon.pid" 
DAEMON_NAME = "monitor.exe" #change this if file change

def isCorrectDaemon(pid):
    try:
        proc = psutil.Process(pid)
        return DAEMON_NAME in proc.name().lower()
    except:
        return False
    
#This function check whether daemon still running or not
def isPIDRunning(pid):
    return psutil.pid_exists(pid)

#This function help to fetch the pid from the daemon.pid file
def readDaemonPID():
    try:
        with open(PID_PATH, 'r') as f:
            return int(f.read().strip())
    except:
        return None

# This function will monitor loop
def monitorDaemon():
    activityLogger("Watch dog started to run")
    fileChange("Watch dog started to run")
    while True:
        if stopFlag(): # This check whether the flag and if found stop then it will stop
            activityLogger("Watch Dog stopped to run")
            break
        pid = readDaemonPID()
        if pid and (not isPIDRunning(pid) or not isCorrectDaemon(pid)): # this will prevent from the unexpected crash of daemon and it will restart it.
            status = readDaemonStatus()
            if status == "running":
                try:
                    activityLogger("Found File monitor to forced stopped. Restarting")
                    fileChange("Found File monitor to forced stopped. Restarting")
                    daemonStartWatchdog()# This must start it as subprocess and rewrite daemon.pid

                except Exception as e:
                    activityLogger(f"[!] Failed to restart daemon from watchdog: {e}")
                    fileChange(f"Watchdog failed to restart daemon: {e}")

        time.sleep(10) # sleep when dSupport will run

def stopFlag()->bool:
    return readDaemonStatus()=="stop"


if __name__ == "__main__":
    monitorDaemon()
    sys.exit(0)
