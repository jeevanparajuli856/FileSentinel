import time
import psutil
import subprocess
from fileutils import readDaemonStatus
from cli import daemonStart  # ensure this returns subprocess.Popen object or is callable

PID_PATH = "C:/ProgramData/FileSentinel/config/daemon.pid"

def is_pid_running(pid):
    return psutil.pid_exists(pid)

def read_daemon_pid():
    try:
        with open(PID_PATH, 'r') as f:
            return int(f.read().strip())
    except:
        return None

# Monitor loop
def monitorDaemon():
    print("[+] Daemon Watchdog Started.")

    while True:
        if stopFlag():
            break
        pid = read_daemon_pid()
        if pid and not is_pid_running(pid):
            status = readDaemonStatus()
            if status == "running":
                print("[!] Daemon crashed/killed. Restarting...")
                daemonStart()  # This must start it as subprocess and rewrite daemon.pid
        time.sleep(20)

def stopFlag()->bool:
    return readDaemonStatus()=="stop"


if __name__ == "__main__":
    monitorDaemon()
    exit(0)