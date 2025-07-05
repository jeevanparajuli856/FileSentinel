import requests 
import socket
from datetime import datetime
from fileutils import getTelegramId
from logger import telegramAlertLogger

# This function returns current timestamp in YYYY-MM-DD HH:MM:SS format
def getCurrentTime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# This function returns local IP address of system
def getIPAddress() -> str:
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "127.0.0.1"

#This function logs alert message if Telegram sending fails
def failAlert(msg: str):
    telegramAlertLogger(msg + " | Failed to send")

# This is core function to sends alert to Telegram
def sendAlert(alertMsg: str)->bool:
    try:
        telegram_data = getTelegramId() # fetching bot id and chat id
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

# This function sends auth event alert
def authNotifier(messageType: str, userID: str, status: str):
    msg = f"""🔐 [Integrixa Alert]
🕒 Time: {getCurrentTime()}
📢 Message: {messageType}
👤 UserID: {userID}
📍 IP Address: {getIPAddress()}
✅ Status: {status}"""
    if not sendAlert(msg): # sending alert and if not sucess send fail error msg to logger
        failAlert(messageType)


#This function sends file change alert
def fileChange(eventMsg: str):
    msg = f"""🔐 [Integrixa Alert]
📢 Message: {eventMsg}
🕒 Time: {getCurrentTime()}
📍 IP Address: {getIPAddress()}
🚫 Status: Alerted"""
    if not sendAlert(msg):
        failAlert(eventMsg)

#This function sends program kill attempt alert
def programKilled(eventMsg: str):
    msg = f"""🔐 [Integrixa Alert]
📢 Message: {eventMsg}
🕒 Time: {getCurrentTime()}
📍 IP Address: {getIPAddress()}
🚫 Status: Alerted"""
    if not sendAlert(msg):
        failAlert(eventMsg)

# This function sends daemon support alert
def dsupport(eventMsg: str):
    msg = f"""🔐 [Integrixa Alert]
📢 Message: {eventMsg}
🕒 Time: {getCurrentTime()}
📍 IP Address: {getIPAddress()}
🚫 Status: Alerted"""
    if not sendAlert(msg):
        failAlert(eventMsg)

