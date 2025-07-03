import requests 
import socket
from datetime import datetime
from fileutils import getTelegramId
from logger import telegramAlertLogger

# Returns current timestamp
def getCurrentTime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Returns local IP address
def getIPAddress() -> str:
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "127.0.0.1"

# Logs alert message if Telegram sending fails
def failAlert(msg: str):
    telegramAlertLogger(msg + " | Failed to send")

# Sends alert to Telegram
def sendAlert(alertMsg: str)->bool:
    try:
        telegram_data = getTelegramId()
        bot_id = telegram_data.get("bot_id")
        chat_id = telegram_data.get("chat_id")
        url = f"https://api.telegram.org/bot{bot_id}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": alertMsg
        }
        response = requests.post(url, data=payload, timeout=5)
        if response.status_code == 200:
            return response.json().get("ok", False) # as just comparing status code wasnt working so using response.json to make sure the true if alert send.
        else:
            return False
    except Exception:
        return False

# Sends auth event alert
def authNotifier(messageType: str, userID: str, status: str):
    msg = f"""🔐 [FileSentinel Alert]
🕒 Time: {getCurrentTime()}
📢 Message: {messageType}
👤 UserID: {userID}
📍 IP Address: {getIPAddress()}
✅ Status: {status}"""
    if not sendAlert(msg):
        failAlert(messageType)


# Sends file change alert
def fileChange(eventMsg: str):
    msg = f"""🔐 [FileSentinel Alert]
📢 Message: {eventMsg}
🕒 Time: {getCurrentTime()}
📍 IP Address: {getIPAddress()}
🚫 Status: Alerted"""
    if not sendAlert(msg):
        failAlert(eventMsg)

# Sends program kill attempt alert
def programKilled(eventMsg: str):
    msg = f"""🔐 [FileSentinel Alert]
📢 Message: {eventMsg}
🕒 Time: {getCurrentTime()}
📍 IP Address: {getIPAddress()}
🚫 Status: Alerted"""
    if not sendAlert(msg):
        failAlert(eventMsg)

# Sends daemon support alert
def dsupport(eventMsg: str):
    msg = f"""🔐 [FileSentinel Alert]
📢 Message: {eventMsg}
🕒 Time: {getCurrentTime()}
📍 IP Address: {getIPAddress()}
🚫 Status: Alerted"""
    if not sendAlert(msg):
        failAlert(eventMsg)


# 🔐 [FileSentinel Alert]
# 📢 Message: LOGIN_ATTEMPT
# 👤 UserID: admin
# 🕒 Time: 2025-06-28 14:47:22
# 📍 IP Address: 127.0.0.1
# ✅ Status: FAILED

# 🔐 [FileSentinel Alert]
# 📢 Message: PROGRAM_KILL_ATTEMPT
# 🕒 Time: <YYYY-MM-DD HH:MM:SS>
# 📍 IP Address: 127.0.0.1
# 🚫 Status:Alerted