import os
from auth import setAuth, checkAuth, changeUserID, changePassword
from fileutils import setTelegramId
from filepath_config import showFilePath, addFilePath, removeFilePath, updateFileHash, updateFileHashAll
from logger import activityLogger
from notifier import programKilled
from installer import stop
from getpass import getpass

# Main entry point after installation check in main.py
def cliMain(newinstalled: bool): # true is new setup where false is already installed.
    bigWelcome()
    print("Type 'exit' to exit or 'clear' to clear terminal or 'help' to view commands at any time.")

    # Run authentication or login
    if not authentication(newinstalled): #checking whether auth have to setup or need to validate credential
        return 

    # Show main options and process user commands
    while True:
        showMainOptions()
        chooseMainOption()


# Shows a large ASCII welcome banner
def bigWelcome():
  print("""
___________.__.__           _________              __  .__              .__   
\_   _____/|__|  |   ____  /   _____/ ____   _____/  |_|__| ____   ____ |  |  
 |    __)  |  |  | _/ __ \ \_____  \_/ __ \ /    \   __\  |/    \_/ __ \|  |  
 |     \   |  |  |_\  ___/ /        \  ___/|   |  \  | |  |   |  \  ___/|  |__
 \___  /   |__|____/\___  >_______  /\___  >___|  /__| |__|___|  /\___  >____/
     \/                 \/        \/     \/     \/             \/     \/      
""")

#to clear the terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
# Hide text input for passwords and IDs
def hideText(prompt):
    return getpass(prompt)

# Print authentication rules
def authRule():
    print("\nAuth Setup Rules:")
    print("User ID Requirements: Alphanumeric only, up to 12 characters.")
    print("Password Requirements: Minimum 8 characters with at least one uppercase letter, one lowercase letter, one number, and one special character.\n")

# Handles first-time or returning authentication
# new: True for setup, False for login

def authentication(new): # to determine whether to setup new or check.
    if new:
        return setAuthentication()
    else:
        return checkAuthentication()

# New user authentication setup
def setAuthentication():
    authRule()
    while True: # loop until user become able to setup new authentication
        user = input("Enter new User ID: ")
        password = hideText("Enter new password: ")
        confirm = hideText("Confirm password: ")
        if password != confirm:
            print("Passwords don’t match! Try again.\n")
            continue
        if setAuth(user, password):
            print("Authentication setup successful.")
            setBotID()
            return True
        else:
            print("Requirements not met. Please try again.\n")

# Prompt to setup Telegram bot credentials
def setBotID():
    print("\nNow, let's configure your Telegram notifications")
    botid = input("Enter your Telegram Bot Token: ")
    chatid = input("Enter your Telegram Chat ID: ")
    setTelegramId(botid, chatid)
    print("Telegram bot configuration saved..../\n")
    activityLogger("Bot ID updated.")

# For already installed program: check user login credentials
def checkAuthentication():
    attempts = 3
    for _ in range(attempts):
        userid = input("Enter your User ID: ")
        password = hideText("Enter your Password: ")
        if checkAuth(userid, password):
            return True
        print("Invalid username or password.\n")
    print("Too many failed attempts. Exiting...")
    activityLogger("Authentication failed: 3 invalid attempts.")
    programKilled("Authentication failure: 3 invalid attempts.")
    exit()

# Displays main options

def showMainOptions():
       print("""
==============Main Menu ==============
1. Configure monitored files
2. Change Telegram Bot configuration
3. Change user ID
4. Change password
5. Stop Monitoring
Type 'exit' to exit from program.
""")

# Choose main menu option

def chooseMainOption():
    while True:
        choice = input("option> ").lower()
        if choice.strip().lower() == "exit":
            activityLogger("User exited program.")
            exit()
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
            killProgram()
        else:
            print("Invalid option. Type 'help' to see available commands.")

# Shows monitor file configuration menu

def showFileMonOption():
       print("""
------ File Monitor Configuration Menu ------
1.View monitored file list
2.Add a file path to monitor
3.Remove a monitored file path
4.Update file hash signatures
5.Update all file hash signatures
Type 'exit' to return to the main menu.
""")

# Monitor configuration sub-menu

def configureMonitor():
    while True:
        showFileMonOption()
        opt = input("option> ").lower()
        if opt.strip().lower() == "exit":
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

# Telegram bot ID changer
def changeBotID():
    botid = input("Enter your Telegram Bot Token: ")
    chatid = input("Enter your Telegram Chat ID: ")
    setTelegramId(botid, chatid) #calling fileutils fn
    print("Bot ID updated.\n")
    activityLogger("Bot ID updated.")

# Change user ID
def setUserID():
    authRule()
    for _ in range(3): #giving 3 chance to meet requirement
        new_id = input("Enter new User ID: ")
        if changeUserID(new_id):
            print("User ID updated.\n")
            return
        else:
            print("Invalid User ID. Try again.")
    print("Too many failed attempts. Returning to main menu.")

# Change password
def setPassword():
    authRule()
    for _ in range(3):
        pwd = hideText("Enter new password: ")
        confirm = hideText("Confirm password: ")
        if pwd != confirm:
            print("Passwords don’t match. Try again.\n")
            continue
        if changePassword(pwd):
            print("Password changed successfully.\n")
            return
        else:
            print("Invalid password format. Try again.")
    print("Too many failed attempts. Returning to main menu.")

# Uninstall the program
def killProgram():
    choice = input("Are you sure you want to stop FileSentinel? (Y/N): ").lower()
    if choice == 'y':
        print("File Monitoring Stopped. Exiting...")
        activityLogger("Monitoring Stopped by user.")
        stop()
        exit()

#Second major option helper function
# Show file list
def listFile():
    showFilePath()

# Add file to monitor
def addPath():
    path = input("Enter the complete file path: ")
    if addFilePath(path):
        print("Filepath added.")
    else:
        print("Failed to add filepath.")

# Remove file path
def removePath():
    path = input("Enter the complete file path: ")
    if removeFilePath(path):
        print("Filepath deleted.")
    else:
        print("Failed to delete filepath.")

# Update file hash
def updateHash():
    path = input("Enter file path to update hash: ")
    if updateFileHash(path):
        print("Hash updated.")
    else:
        print("Failed to update hash.")

# Update all hashes
def updateAll():
    if updateFileHashAll():
        print("All file hashes updated.")
    else:
        print("Failed to update some hashes.")
