import time
import psutil # type: ignore
import subprocess
from fileutils import readDaemonStatus,readDaemonStatus
from cli import daemonStart  # ensure this returns subprocess.Popen object or is callable
from logger import activityLogger
from notifier import fileChange
from logger import activityLogger
from notifier import fileChange

PID_PATH = "C:/ProgramData/FileSentinel/config/daemon.pid" 


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
    print("[+] Daemon Watchdog Started.")
    while True:
        if stopFlag(): # This check whether the flag and if found stop then it will stop
            print("Watch dog stopped to run")
            activityLogger("Watch Dog stopped to run")
            break
        pid = readDaemonPID()
        if pid and not isPIDRunning(pid): # this will prevent from the unexpected crash of daemon and it will restart it.
            status = readDaemonStatus()
            if status == "running":
                activityLogger("Found File monitored to forced stopped. Restarting")
                fileChange("Found File monitored to forced stopped. Restarting")
                daemonStart()  # This must start it as subprocess and rewrite daemon.pid
        time.sleep(5) # sleep when dSupport will run
        print(readDaemonPID())

def stopFlag()->bool:
    return readDaemonStatus()=="stop"


if __name__ == "__main__":
    activityLogger("Watch dog started to run")
    print(readDaemonPID())
    monitorDaemon()
    exit(0)