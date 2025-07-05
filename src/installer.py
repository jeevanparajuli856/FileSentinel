import os
import ctypes
import shutil
import sys
from filepath_config import fileSetup, updateAllFileHash
from fileutils import initializeConfig, updateTimeLogger, updateTimeMonitor

# Constants
BASE_DIR = r"C:/Program Files/FileSentinel"
CONFIG_DIR = os.path.join(BASE_DIR, "config")
LOG_DIR = os.path.join(BASE_DIR, "logs")
MARKER_FILE = os.path.join(BASE_DIR, ".installed")

#This functin creates the main FileSentinel directory structure and initializes config files.
def installSetup():
    try:
        # Create main program directory
        os.makedirs(CONFIG_DIR, exist_ok=True)
        os.makedirs(LOG_DIR, exist_ok=True)
        

        # Call external module functions
        fileSetup()              # Initializes file_path.json
        initializeConfig()       # Initializes sentinel_configuration.json
        copyExecutablesToSystemPath()
        writeWatchdogTaskXML()

        # Create installation marker
        with open(MARKER_FILE, "w") as f:
            f.write("installed")

        return True
    except Exception as e:
        print(f"[!] Installation failed: {e}")
        return False

#To make the configuration file of the program to only admin access we can use this function but have to run main.py with admin right to work
# #This function restricts access to the config directory so only administrators can access it. Works on Windows using icacls command.
# def managePermission():
#     try:
#           # Remove inherited permissions
#         os.system(f'icacls "{CONFIG_DIR}" /inheritance:r')

#         # Grant full access to SYSTEM and Administrators (your tool runs as Admin)
#         os.system(f'icacls "{CONFIG_DIR}" /grant:r SYSTEM:F')
#         os.system(f'icacls "{CONFIG_DIR}" /grant:r Administrators:F')

#         # Deny WRITE access to Users and Everyone (read is OK for basic system ops)
#         os.system(f'icacls "{CONFIG_DIR}" /grant:r Users:RW')

#         return True
#     except Exception as e:
#         print(f"[!] managePermission() failed: {e}")
#         return False

#This function calls the function to update hashes for all monitored files.
def updateDefaultFileHash():
    try:
        a= updateAllFileHash()
        return True
    except Exception as e:
        print(f"[!] Failed to update hashes of default file paths: {e}")
        return False
    
    import shutil
import os

def copyExecutablesToSystemPath():
    # Determine where current exe is running from
    base_dir = os.path.dirname(os.path.abspath(sys.executable))
    service_src = os.path.join(base_dir, "services")

    # Destination for permanent service executables
    system_services_dir = r"C:\Program Files\FileSentinel\services"
    os.makedirs(system_services_dir, exist_ok=True)

    try:
        shutil.copy(os.path.join(service_src, "watchdog.exe"), system_services_dir)
        shutil.copy(os.path.join(service_src, "monitor.exe"), system_services_dir)
    except Exception as e:
        print(f"[!] Failed to copy executables: {e}")




def writeWatchdogTaskXML():
    exe_path = r"C:\Program Files\FileSentinel\services\watchdog.exe"
    xml_path = r"C:\Program Files\FileSentinel\services\watchdog_task.xml"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(xml_path), exist_ok=True)

    xml_content = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Start FileSentinel Watchdog when user logs in</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <Delay>PT30S</Delay>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>C:\Program Files\FileSentinel\services\watchdog.exe</Command>
    </Exec>
  </Actions>
</Task>
"""

    try:
        with open(xml_path, "w", encoding="utf-16") as f:
            f.write(xml_content)
    except Exception as e:
        print(f"[!] Failed to write XML file: {e}")


#This function is a master installation function that sets up directory, permissions, and file hashes. Returns True if all steps succeed, else False.
def install():
    if installSetup():
        if updateDefaultFileHash():
            if updateTimeLogger(): # not using managePermission as it is locking my program to access directory
                if updateTimeMonitor():
                    return True
    return False