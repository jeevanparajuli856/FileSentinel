#This function main purpose is to call daemon.py which is executable and it control the monitoring itself
import os
import sys
import ctypes
def daemonStart():
 # Determine base directory (whether running as .py or bundled .exe)
    base_dir = os.path.dirname(os.path.abspath(sys.executable))
    print(base_dir)

    # Point to daemon.exe in the same folder as main executable
    daemon_exe = os.path.join(base_dir, "daemon.exe")

    if not os.path.exists(daemon_exe):
        print("[!] daemon.exe not found.")
        return

    try:
        # Use ShellExecuteW with "runas" verb to elevate
        ctypes.windll.shell32.ShellExecuteW(
            None,              # hwnd
            "runas",           # operation => run as admin
            daemon_exe,        # file
            None,              # parameters
            None,              # directory
            1                  # show window
        )
        print("[+] daemon.exe started with admin rights.")
        
    except Exception as e:
        print(f"[!] Failed to start daemon.exe: {e}")