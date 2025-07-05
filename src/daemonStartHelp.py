#This function main purpose is to call daemon.py which is executable and it control the monitoring itself
import os
import sys
import ctypes
import psutil
import subprocess
from logger import activityLogger
from notifier import fileChange

def daemonStart():
 # Determine base directory (whether running as .py or bundled .exe)
    # base_dir = os.path.dirname(os.path.abspath(sys.executable))

    # # Path to the services folder
    # services_dir = os.path.join(base_dir, "services")

    # # Full path to daemon.exe
    # daemon_exe = os.path.join(services_dir, "monitor.exe")

    daemon_exe = r"C:\Program Files\FileSentinel\services\monitor.exe"

    if not os.path.exists(daemon_exe):
        print("[!] monitor.exe not found.")
        activityLogger("monitor.exe not found.")
        fileChange("monitor.exe not found.")
        return

    if isProcessRunning():
        print("[!] monitor.exe is already running. Skipping launch.")
        return
    

    try:
        # Use ShellExecuteW with "runas" verb to elevate
        ctypes.windll.shell32.ShellExecuteW(
            None,              # hwnd
            "runas",           # operation => run as admin
            daemon_exe,        # file
            None,              # parameters
            None,              # directory
            0                  # show window
        )
        print("[+] monitor.exe started with admin rights.")
        activityLogger(f"monitor.exe started with admin rights.")
        fileChange("monitor.exe started with admin rights.")
        
    except Exception as e:
        print(f"[!] Failed to start monitor.exe: {e}")
        activityLogger(f"failed to start monitor.exe: {e}")
        fileChange("failed to start monitor.exe")


#This function is for watchdog to restart the daemon if found stopped
def daemonStartWatchdog():
#  # Determine base directory (whether running as .py or bundled .exe)
#     base_dir = os.path.dirname(os.path.abspath(sys.executable))

#     # Full path to daemon.exe
#     daemon_exe = os.path.join(base_dir, "monitor.exe")

    daemon_exe = r"C:\Program Files\FileSentinel\services\monitor.exe"

    if not os.path.exists(daemon_exe):
        
        activityLogger("monitor.exe not found.")
        fileChange("monitor.exe not found.")
        return
    
    if isProcessRunning(): #if found running it just skip the launch of monitor.exe
        return

    try:
        # Use ShellExecuteW with "runas" verb to elevate
        ctypes.windll.shell32.ShellExecuteW(
            None,              # hwnd
            "runas",           # operation => run as admin
            daemon_exe,        # file
            None,              # parameters
            None,              # directory
            0                 # show window
        )
        activityLogger("[+] daemon.exe re-started with admin rights.")
        fileChange("[+] daemon.exe re-started with admin rights.")
        
    except Exception as e:
        activityLogger(f"failed to start monitor.exe: {e}")
        fileChange("failed to start monitor.exe")

#This function check whether monitor.exe is already running or not.
def isProcessRunning():
    pid_path = r"C:/Program Files/FileSentinel/config/daemon.pid"
    if not os.path.exists(pid_path):
        return False

    try:
        with open(pid_path, 'r') as f:
            pid = int(f.read().strip())
        proc = psutil.Process(pid)
        return "monitor.exe" in proc.name().lower()
    except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError):
        return False