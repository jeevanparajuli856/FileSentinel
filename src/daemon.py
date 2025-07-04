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
        print("checking time completed")#Remove after testing
        if current_time - last_time >= timedelta(minutes=2): #Checking the time between current and last run
            activityLogger("File monitoring started.")
            success = monitorFile()
            if success:
                updateTimeMonitor()
                activityLogger("File monitoring ran successfully. Time updated.")
            else:
                activityLogger("File monitoring failed to run.")
    except Exception as e:
        activityLogger(f"Error in runFileMonitor: {str(e)}")

# This function will protect daemon from unexpected stop, run in loop
def protectDaemon():
    activityLogger("File Monitoring started.")
    while True:
        try:
            if not stopFlag(): #seeing whether the stop flag is in config or not
                print("checkingFileMonitor") #Remove after testing
                runFileMonitor()
                time.sleep(7)  # Sleep 60s between checks
            else:
                print("File monitoring stop command received. Stopping")
                activityLogger("File monitoring stop command received. Stopping")
                fileChange("File monitoring stop command received. Stopping")  
                break
        except Exception as e:
            activityLogger(f"File monitoring encountered an error: {str(e)}. Restart by stopping and starting it")
            fileChange(f"File monitoring encountered an error: {str(e)}.")

def stopFlag()->bool:
    return readDaemonStatus()=="stop"

if __name__ == "__main__":
    try:
        print("Launching File monitoring")
        activityLogger("File monitoring started")
        with open("C:/ProgramData/FileSentinel/config/daemon.pid", "w") as f:
            f.write(str(os.getpid()))
        protectDaemon()
        activityLogger("File Monitoring exiting cleanly")
    except Exception as e:
        error_msg = f"[FATAL] File Monitoring crashed unexpectedly: {str(e)}"
        activityLogger(error_msg)
    finally:
        sys.exit(0)