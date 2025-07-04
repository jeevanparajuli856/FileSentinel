# 🛡️ FileSentinel

**FileSentinel** is a Windows-only CLI-based defensive cybersecurity tool built to help system administrators and security-minded users monitor the integrity of sensitive files in real time. It runs as a persistent background daemon and watches for unauthorized file changes using cryptographic hash comparison. If any tampering is detected, it sends instant alerts via Telegram and logs the event for further review.

---

## 🔧 What It Does

- 📁 Monitors user-specified and default critical system file paths
- 🔐 Detects unauthorized modifications using SHA-256 hashing
- 🔔 Sends real-time Telegram alerts on any detected changes
- 🧑‍💻 Provides an admin-authenticated CLI for secure tool management
- 📜 Maintains detailed logs of authentication attempts, monitoring events, and alert messages
- 🔄 Self-monitors and resists unauthorized shutdown or tampering
- 🗑️ Automatically purges logs older than 2 days

---

## ✅ Current Features

- Real-time file integrity monitoring via daemon process  
- CLI-based configuration and authentication system  
- Telegram alert integration with fallback logging  
- Encrypted configuration and hash storage  
- Secure log handling and cleanup  
- Modular code structure (monitoring, logging, auth, alerting, config)

---

## ⚠️ Important Notes

- This tool is **not open for public contribution or feature extension**.
- Built primarily for **educational, personal, and defensive security purposes**.
- Requires **Python 3.8+** and **administrator privileges**.
- No future AI versions, web dashboard, or other major updates are planned.

---

## 🚀 Getting Started

To use FileSentinel:

1. Clone this repository.
2. Run `FileSentinel.exe` with administrator privileges.
3. Follow the CLI setup for authentication and Telegram alert config.
4. File monitoring begins automatically on startup.

---

## 📌 Stay Updated

This tool is currently under personal development and not intended for general public release or community feature expansion. However, you may ⭐️ star the repo if you'd like to track updates or changes.

