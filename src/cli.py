import os
import subprocess
import sys
import ctypes
import signal
import time
import psutil
from auth import setAuth, checkAuth, changeUserID, changePassword
from fileutils import setTelegramId,setDaemonStatus,readDaemonStatus
from filepath_config import showFilePath, addFilePath, removeFilePath, updateFileHash, updateAllFileHash
from logger import activityLogger
from notifier import programKilled
from getpass import getpass
from daemonStartHelp import daemonStart


# This function is the main entry point after installation check in main.py
def cliMain(newinstalled: bool,msg:str): # true is new setup where false is already installed.
    bigWelcome()
    print(msg)
    print("[+] Type 'exit' to exit, 'clear' to clear the terminal, or 'help' to view commands at any time.")

    # Run authentication or login
    if not authentication(newinstalled): #checking whether auth have to setup or need to validate credential
        return 

    # Show main options and process user commands
    while True:
        showMainOptions()
        chooseMainOption()


# Shows a large ASCII welcome banner
def bigWelcome():
  print(r"""
___________.__.__           _________              __  .__              .__   
\_   _____/|__|  |   ____  /   _____/ ____   _____/  |_|__| ____   ____ |  |  
 |    __)  |  |  | _/ __ \ \_____  \_/ __ \ /    \   __\  |/    \_/ __ \|  |  
 |     \   |  |  |_\  ___/ /        \  ___/|   |  \  | |  |   |  \  ___/|  |__
 \___  /   |__|____/\___  >_______  /\___  >___|  /__| |__|___|  /\___  >____/
     \/                 \/        \/     \/     \/             \/     \/      
""")

#This function is used to clear the terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Hide text input for passwords and IDs
def hideText(prompt):
    return getpass(prompt)

#Print authentication rules
def authRule():
    print("\n[+]Auth Setup Rules:")
    print("[+]User ID Requirements: Alphanumeric only, up to 12 characters.")
    print("[+]Password Requirements: Minimum 8 characters with at least one uppercase letter, one lowercase letter, one number, and one special character.\n")

# This function handles first-time or returning authentication and return boolean if setup or checking is complete
# new: True for setup, False for login
def authentication(new): # to determine whether to setup new or check.
    if new:
        return setAuthentication()
    else:
        return checkAuthentication()

# This function help to setup new user authentication. And return true after user been able to setup. To setup it use setAuth() function from auth.py
def setAuthentication():
    authRule()
    while True: # loop until user become able to setup new authentication
        user = input("Enter new User ID: ")
        password = hideText("Enter new password: ")
        confirm = hideText("Confirm password: ")
        if password != confirm:
            print("[!] Passwords don't match. Try again.\n")
            continue
        if setAuth(user, password):
            print("[+] Authentication setup successful.")
            setBotID()
            return True
        else:
            print("[!] Requirements not met. Please try again.\n")

# This function prompt to setup Telegram bot credentials. Use helper fn from notifier.py and fileutils.py
def setBotID():
    print("\n[+] Now, let's configure your Telegram notifications.")
    botid = input("Enter your Telegram Bot Token: ")
    chatid = input("Enter your Telegram Chat ID: ")
    setTelegramId(botid, chatid)
    print("[+] Telegram bot configuration saved.\n")
    activityLogger("Bot ID updated.")

# This function will check user login credentials for already installed program. This function return true if authentication is passed. Use fn from auth.py and logger.py and notifier.py
def checkAuthentication():
    attempts = 3
    for _ in range(attempts):
        userid = input("Enter your User ID: ")
        password = hideText("Enter your Password: ")
        if checkAuth(userid, password):
            return True
        print("[!] Invalid username or password.\n")
    print("[!] Too many failed attempts. Exiting...")
    activityLogger("Authentication failed: 3 invalid attempts.")
    programKilled("Authentication failed: 3 invalid attempts.")
    exit()


# Displays main options
def showMainOptions():
       print("""
==============Main Menu ==============
1. Configure monitored files
2. Change Telegram bot configuration
3. Change user ID
4. Change password
5. Start monitoring
6. Stop monitoring
             
Type 'exit' to exit from program.
""")

# This function serve the user to choose main menu option
def chooseMainOption():
    while True:
        choice = input("option> ").lower()
        if choice.strip().lower() == "exit":
            activityLogger("User exited the program.")
            sys.exit(0)
        elif choice.strip().lower() == "help":
            showMainOptions()
        elif choice =="clear":
            clear()
        elif choice == "1":
            configureMonitor()
        elif choice == "2":
            changeBotID()
        elif choice == "3":
            setUserID()
        elif choice == "4":
            setPassword()
        elif choice == "5":
            startProgram()
        elif choice == "6":
            killProgram()
        else:
            print("Invalid option. Type 'help' to see available commands.")

# Shows monitor file configuration menu
def showFileMonOption():
       print("""
==== File Monitor Configuration Menu ====
1. View monitored file list
2. Add a file path to monitor
3. Remove a monitored file path
4. Update file hash signatures
5. Update all file hash signatures
             
Type 'exit' to return to the main menu.
""")

# This function serve the option to chosse for monitor configuration sub-menu
def configureMonitor():
    showFileMonOption()
    while True:
        opt = input("option> ").lower()
        if opt.strip().lower() == "exit":
            showMainOptions()
            return #go back to  main option selection 
        elif opt.strip().lower() == "help":
            showFileMonOption()
        elif opt =="clear":
            clear()
        elif opt == "1":
            listFile()
        elif opt == "2":
            addPath()
        elif opt == "3":
            removePath()
        elif opt == "4":
            updateHash()
        elif opt == "5":
            updateAll()
        else:
            print("Invalid option. Type 'help' to see configuration commands.")

# This function help to change telegram bot ID
def changeBotID():
    botid = input("Enter your Telegram Bot Token: ")
    chatid = input("Enter your Telegram Chat ID: ")
    setTelegramId(botid, chatid) #calling fileutils fn
    print("[+] Bot ID updated.\n")
    activityLogger("Bot ID updated.")

# This function help to change user ID
def setUserID():
    authRule()
    for _ in range(3): #giving 3 chance to meet requirement
        new_id = input("Enter new User ID: ")
        if changeUserID(new_id):
            print("[+] User ID updated.\n")
            return
        else:
            print("[!] Invalid user ID format. Must be alphanumeric. Try again.")
    print("[!] Too many failed attempts. Returning to main menu.")

# This function help to change password. This also have rate limiting
def setPassword():
    authRule()
    for _ in range(3):
        pwd = hideText("Enter new password: ")
        confirm = hideText("Confirm password: ")
        if pwd != confirm:
            print("[!] Passwords don't match. Try again.\n")
            continue
        if changePassword(pwd):
            print("[+] Password changed successfully.\n")
            return
        else:
            print("[!] Invalid password format. Try again.")
    print("[!] Too many failed attempts. Returning to main menu.")

# This function help to stop monitor
def killProgram():
    choice = input("Are you sure you want to stop FileSentinel? (Y/N): ").strip().lower()
    if choice == 'y' and readDaemonStatus() !="stop":
        print("[+] File monitoring stopped. Stopping...")
        activityLogger("File monitoring stopped by user.")
        setDaemonStatus("stop")
        disableAutoStartup()


#This Function help to start monitoring files.
def startProgram():
    try:
        if readDaemonStatus() !="running":
            setDaemonStatus("running")
            daemonStart()
            time.sleep(2)
            dSupportStart()
            enableAutoStartup()
        else:
            print("[!] File monitoring is already running.")

    except Exception as e:
        print(f"[!] Failed to start file monitoring: {e}")



#Second major option helper function
# This functio help to show file list
def listFile():
    showFilePath()

# This functio help to add file to monitor
def addPath():
    path = input("Enter the complete file path: ")
    if addFilePath(path):
        print(f"[+] '{path}' is now being monitored.")

# This function help to remove the file path from monitoring config
def removePath():
    path = input("Enter the complete file path: ")
    if removeFilePath(path):
        print("[+] File path deleted.")
    else:
        print("[!] Path not found in monitored list.")

# This function help to update file hash
def updateHash():
    path = input("Enter file path to update hash: ")
    if updateFileHash(path):
        print("[+] Hash updated.")
    else:
        print("[!] Invalid path. File path does not match any in the monitored list.")

# This function will update all filepath hashes
def updateAll():
    print(updateAllFileHash())


#This function main purpose is to call dsupport.py which is executable and it check whether the daemon is running or not
def dSupportStart():
 # Determine base directory (whether running as .py or bundled .exe)
    # base_dir = os.path.dirname(os.path.abspath(sys.executable))
    # print(base_dir)

    # # Path to the services folder
    # services_dir = os.path.join(base_dir, "services")

    # # Full path to daemon.exe
    # watchdog_exe = os.path.join(services_dir, "watchdog.exe")


    watchdog_exe =r"C:\Program Files\FileSentinel\services\watchdog.exe"

    if not os.path.exists(watchdog_exe):
        print("[!] watchdog.exe not found.")
        return
    
    try:
        # Use ShellExecuteW with "runas" verb to elevate
        ctypes.windll.shell32.ShellExecuteW(
            None,              # hwnd
            "runas",           # operation => run as admin
            watchdog_exe,      # file
            None,              # parameters
            None,              # directory
            0                  # show window
        )
        print("[+] Watchdog.exe started with admin rights.")
    except Exception as e:
        print(f"[!] Failed to start watchdog.exe: {e}")



# #This function help to make the file monitor watch dog to be auto startup when everytime the pc boot. Creating system to start causes issue as system dont have access to program files early
# def enableAutoStartup():
#     # base_path = os.path.dirname(os.path.abspath(sys.executable)) # this will give base directory
#     # exe_path = os.path.join(base_path, "services", "watchdog.exe") # it will append service/watchdog.exe
    
#     exe_path = r"C:\ProgramData\FileSentinel\services\watchdog.exe"
    
#     if not os.path.exists(exe_path):
#         print(f"[!] watchdog.exe not found at: {exe_path}")
#         return

#     result = subprocess.run([
#         "schtasks",
#         "/Create",
#         "/SC", "ONSTART",
#         "/TN", "FileSentinelWatchdog",
#         "/TR", r"C:\ProgramData\FileSentinel\services\watchdog.exe",
#         "/RU", "SYSTEM",      # Run As SYSTEM account
#         "/DELAY", "0002:00"
#         "/F"                  # Force overwrite
#     ], capture_output=True, text=True)

#     if result.returncode == 0:
#         print("[+] Scheduled Task created successfully.")
#         activityLogger("Watchdog will now auto-start on system boot.")
#     else:
#         print("[!] Failed to create task:")
#         print(result.stderr)
#         activityLogger(f"Failed to create watchdog task: {result.stderr}")


#This function help to make the file monitor watch dog to be auto startup when everytime the pc boot. Creating system to start causes issue as system dont have access to program files early
def enableAutoStartup():
    xml_path = r"C:\Program Files\FileSentinel\services\watchdog_task.xml"

    if not os.path.exists(xml_path):
        print(f"[!] Task XML file not found at: {xml_path}")
        return
    
    
    # Create new task from XML
    result = subprocess.run([
        "schtasks", "/Create",
        "/TN", "FileSentinelWatchdog",
        "/XML", xml_path,
        "/RU", "SYSTEM",
        "/F"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print("[+] Scheduled task registered successfully.")
    else:
        print("[!] Failed to register scheduled task:")
        print(result.stderr)




#This function help to disable the auto startup for the watchdog.
def disableAutoStartup():
    cmd = 'schtasks /Delete /TN "FileSentinelWatchdog" /F'
    os.system(cmd)
    print("[+] Scheduled Task stopped successfully.")
    activityLogger("Watchdog auto-start on boot has been disabled.")