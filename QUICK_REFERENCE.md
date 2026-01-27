# AutoSync Quick Reference Card

## 🚀 Common Commands

### Start AutoSync
```
Double-click: master_launcher.vbs
```

### Stop AutoSync
```
Run: stop_autosync.bat
```

### View Logs
```
Navigate to: logs/sync_YYYY_MM_DD.log
```

### Reconfigure Settings
```
Edit: sync_config.ini
or
Run: setup.bat
```

## 🔧 Quick Fixes

### USB Not Detected?
1. Check drive letter in `sync_config.ini` → `[USB]` → `drive=G:`
2. Verify USB is mounted and accessible

### Git Push Failing?
```batch
cd E:\Pliki\Projects
git config credential.helper store
# Then push once manually to save credentials
```

### MySQL Not Working?
1. Start XAMPP Control Panel
2. Start MySQL service
3. Verify path in config: `[MySQL]` → `bin=C:\xampp\mysql\bin\mysql.exe`

### Files Not Syncing?
- Check paths in `sync_config.ini`
- Verify source folders exist
- Check log for robocopy errors

## 📁 Config Sections Quick Guide

### [USB]
```ini
drive=G:              # Your USB drive letter
check_interval=5      # Seconds between checks
```

### [LocalToUSB] - Mirror Mode (Exact Copy)
```ini
source_src=E:\LocalPath
source_dst={USB}\USBPath
```

### [USBToLocal] - Standard Mode (Keep Newer)
```ini
source_src={USB}\USBPath
source_dst=E:\LocalPath
```

### [Git]
```ini
root=E:\Pliki\Projects
auto_commit=true      # Auto commit changes
auto_push=true        # Auto push to GitHub
smart_messages=true   # Descriptive commit messages
scan_subdirs=true     # Look for git repos in subfolders
```

### [MySQL]
```ini
bin=C:\xampp\mysql\bin\mysql.exe
user=root
pass=                 # Leave empty if no password
sql_base=E:\...\databases
charset=utf8mb4
```

### [WebDeploy]
```ini
source=E:\...\websites
destination=C:\xampp\htdocs\myfiles
```

## 📋 File Operations

### Add New Folder to Sync
1. Open `sync_config.ini`
2. Under `[LocalToUSB]` or `[USBToLocal]`:
   ```ini
   newfolder_src=E:\SourcePath
   newfolder_dst={USB}\DestPath
   ```
3. Save and restart AutoSync

### Database Naming Convention
```
File: databases/klasa2/shop.sql
Creates: klasa2_shop (database)
```

### Web Project Naming
```
Source: websites/klasa2/myproject/
Deploys to: htdocs/myfiles/klasa2_myproject/

Source: websites/standalone/
Deploys to: htdocs/myfiles/standalone/
```

## 🎯 Smart Git Messages Examples

What you see:
```
Auto: 3 modified, 2 added (php, sql files) - 01/27/2026 14:30:22
Auto: 1 modified (cpp files) - 01/27/2026 15:45:10
Auto: 5 added, 1 deleted (py, txt files) - 01/27/2026 16:20:33
```

## 🔍 Log File Interpretation

```log
[14:30:15] USB DETECTED: G:           # USB plugged in
[14:30:16] SYNC: G:\... -> E:\...     # Copying files
[14:30:18] SUCCESS: cpp synced        # Sync completed
[14:30:19] Committing: Auto: 2...     # Git commit
[14:30:22] SUCCESS: Pushed...         # Pushed to GitHub
[14:30:25] Database: shop deployed    # MySQL import done
[14:35:40] USB REMOVED                # USB unplugged
```

## ⏱️ Typical Operation Times

- USB Detection: < 5 seconds
- File Sync (small): 5-30 seconds
- File Sync (large): 1-5 minutes
- Git Commit/Push: 5-15 seconds
- Database Deploy: 1-3 seconds per .sql file
- Web Deploy: 1-2 seconds per project

## 🆘 Emergency Commands

### Force Stop All Operations
```
Press Ctrl+C in console
or
Run stop_autosync.bat
```

### View Current Sync Status
```
Open: logs/sync_YYYY_MM_DD.log
Check last line timestamp
```

### Manual Sync (One-Time)
```
Run: master_sync.bat
Wait for USB detection
Unplug USB after sync completes
Script will wait for next USB insertion
```

### Reset Everything
```
1. Stop AutoSync (stop_autosync.bat)
2. Delete sync_config.ini
3. Run setup.bat
4. Reconfigure from scratch
```

## 💾 Backup Your Config

Important files to backup:
- `sync_config.ini` (your settings)
- `logs/` (your sync history)

Copy these to USB or cloud storage!

## 🔐 Security Notes

- Passwords stored in plain text in `sync_config.ini`
- Keep config file secure
- Don't commit config to public Git repos
- Use `.gitignore` to exclude `sync_config.ini`

## 📞 Quick Troubleshooting Decision Tree

```
Problem: Script not running?
└─> Check: Is master_sync.bat process running?
    ├─> No → Start with master_launcher.vbs
    └─> Yes → Check logs/ for errors

Problem: USB not syncing?
└─> Check: Is USB drive letter correct in config?
    ├─> No → Edit sync_config.ini
    └─> Yes → Check if USB is mounted
              └─> Check logs/ for robocopy errors

Problem: Git not pushing?
└─> Check: Is internet connected?
    ├─> No → Connect to internet
    └─> Yes → Check Git credentials
              └─> Run: git config credential.helper store

Problem: MySQL imports failing?
└─> Check: Is XAMPP MySQL running?
    ├─> No → Start MySQL in XAMPP
    └─> Yes → Check .sql file for errors
              └─> Check logs/ for specific error
```

---

Print this page and keep it handy! 📄
