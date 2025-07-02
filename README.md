# 🛡️ FileSentinel

**FileSentinel** is a CLI-based defensive cybersecurity tool designed to **monitor the integrity of sensitive files** on a system in real time. Built for sysadmins and security enthusiasts, FileSentinel acts as a background daemon, watching for unauthorized file changes and sending **instant Telegram alerts** when tampering is detected.

---

## What It Does

- 📁 **Monitors specified file paths** for changes (including default critical system files)
- 🔐 Uses cryptographic hashing to detect unauthorized modifications
- 🔔 Sends alerts via **Telegram** on file tampering
- 📜 Maintains activity and authentication logs with auto-cleanup
- 🧑‍💻 Includes an admin-authenticated CLI interface for secure management
- 🧱 Self-monitors for integrity and resists unauthorized termination

---

## Features (Planned/Active)

- [x] File hash generation and comparison  
- [x] Real-time daemon service  
- [x] Telegram notification integration  
- [x] Secure password/user ID authentication  
- [x] File access logging system  
- [ ] Web dashboard integration *(Coming Soon)*  
- [ ] Encrypted backup of hash values  
- [ ] Advanced evasion detection & rule tuning  

---

## Development Status

> **This project is currently in active development.**  
> A stable version will be released soon. Stay tuned!

---

## Note

- This tool is intended for **educational and professional system defense use**.
- It requires **Python 3.8+** and **admin/root privileges** for some features.

---

## Stay Updated

Want to contribute, test, or follow the release?  
⭐️ Star the repo and stay tuned for version `v1.0`!