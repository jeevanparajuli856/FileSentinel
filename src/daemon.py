import time
from datetime import datetime, timedelta
from file_monitor import monitorFile
from fileutils import readTimeMonitor, updateTimeMonitor, readDaemonStatus
from dsupport import stopDsupport
from logger import activityLogger
from notifier import fileChange


# Run monitorFile if 15 minutes have passed since last run
def runFileMonitor():
    try:
        last_time_str = readTimeMonitor()
        last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        print("checking time completed")
        if current_time - last_time >= timedelta(minutes=2):
            activityLogger("File Monitor Started")
            success = monitorFile()
            if success:
                updateTimeMonitor()
                activityLogger("File monitor ran successfully and time updated.")

            else:
                activityLogger("File monitor failed or returned False.")
    except Exception as e:
        activityLogger(f"Error in runFileMonitor: {str(e)}")

# Protect daemon from unexpected stop, run in loop
def protectDaemon():
    activityLogger("Daemon started.")
    while True:
        try:
            if not stopFlag():
                print("checkingFileMonitor")
                runFileMonitor()
                time.sleep(10)  # Sleep 60s between checks
            else:
                stopDaemon()
                break
        except Exception as e:
            activityLogger(f"Daemon encountered an error: {str(e)}. Restarting")
            fileChange(f"Daemon encountered an error: {str(e)}. Restarting")

# Stop daemon properly
def stopDaemon():
    print("stoping everything")
    activityLogger("Daemon stop command received. Stopping")
    fileChange("Daemon stop command received. Stopping..")
    stopDsupport()
    activityLogger("Daemon stopped successfully.")

def stopFlag()->bool:
    return readDaemonStatus()=="stop"

# Entry point
if __name__ == "__main__":
    print("Launching Daemon")
    protectDaemon()
    exit(0)