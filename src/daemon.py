import time
import os
import sys
from datetime import datetime, timedelta
from file_monitor import monitorFile
from fileutils import readTimeMonitor, updateTimeMonitor, readDaemonStatus
from logger import activityLogger
from notifier import fileChange


# This function run monitorFile if 15 minutes have passed since last run
def runFileMonitor():
    try:
        last_time_str = readTimeMonitor()
        last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        print("checking time completed")
        if current_time - last_time >= timedelta(minutes=2): #Checking the time between current and last run
            activityLogger("File Monitor Started")
            success = monitorFile()
            if success:
                updateTimeMonitor()
                activityLogger("File monitor ran successfully and time updated.")
            else:
                activityLogger("File monitor failed to run.")
    except Exception as e:
        activityLogger(f"Error in runFileMonitor: {str(e)}")

# This function will protect daemon from unexpected stop, run in loop
def protectDaemon():
    activityLogger("Daemon started.")
    while True:
        try:
            if not stopFlag(): #seeing whether the stop flag is in config or not
                print("checkingFileMonitor")
                runFileMonitor()
                time.sleep(10)  # Sleep 60s between checks
            else:
                print("File monitor stop command received. Stopping")
                activityLogger("file monitor stop command received. Stopping")
                fileChange("file monitor stop command received. Stopping")  
                break
        except Exception as e:
            activityLogger(f"File monitor encountered an error: {str(e)}. Restart by stopping and starting it")
            fileChange(f"Daemon encountered an error: {str(e)}.")

def stopFlag()->bool:
    return readDaemonStatus()=="stop" 

# Entry point for launching the daemon
if __name__ == "__main__":
    print("Launching Daemon")
    activityLogger("File Monitoring Started")
    with open("C:/ProgramData/FileSentinel/config/daemon.pid", "w") as f: # this will help to grab the pid of the daemon process by creating file
        f.write(str(os.getpid()))
    protectDaemon()
    exit(0)