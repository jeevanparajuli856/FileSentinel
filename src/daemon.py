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
                activityLogger("File monitor stop command received. Stopping")
                fileChange("File monitor stop command received. Stopping")  
                break
        except Exception as e:
            activityLogger(f"File monitor encountered an error: {str(e)}. Restart by stopping and starting it")
            fileChange(f"Daemon encountered an error: {str(e)}.")

def stopFlag()->bool:
    return readDaemonStatus()=="stop"

if __name__ == "__main__":
    try:
        print("Launching Daemon")
        activityLogger("File Monitoring Started")
        with open("C:/ProgramData/FileSentinel/config/daemon.pid", "w") as f:
            f.write(str(os.getpid()))
        protectDaemon()
        activityLogger("Daemon exiting cleanly")
    except Exception as e:
        error_msg = f"[FATAL] Daemon crashed unexpectedly: {str(e)}"
        print(error_msg)
        activityLogger(error_msg)
    finally:
        sys.exit(0)