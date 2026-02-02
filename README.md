# AutoSync v2.1 - FIXED & ENHANCED 🚀

**Complete automation for USB backups, Git synchronization, database deployment, and web file management.**

## 🔧 What's Fixed in v2.1

### Critical Fixes:
1. ✅ **master_sync.bat now calls ALL modules** (Git, DB, Web Deploy were missing!)
2. ✅ **XAMPP paths corrected to E: drive** (was C:, now E:)
3. ✅ **Enhanced launcher with start/stop/restart** (merged best of Scripts/launcher)
4. ✅ **Better process management** (can properly stop/restart AutoSync)

### Changed Paths:
- MySQL: `C:\xampp\mysql\bin\mysql.exe` → `E:\xampp\mysql\bin\mysql.exe`
- htdocs: `C:\xampp\htdocs\myfiles` → `E:\xampp\htdocs\myfiles`

---

## 📁 Project Structure

```
AutoSync/
├── master_launcher.vbs       ← NEW: Start/stop/restart AutoSync
├── master_sync.bat            ← FIXED: Now runs ALL 4 modules
├── sync_config.ini            ← FIXED: E: drive paths
├── stop_autosync.bat          ← NEW: Quick stop button
├── setup.bat                  ← Original setup wizard
├── modules/
│   ├── usb_sync.bat          ← USB file synchronization
│   ├── git_sync.bat          ← Git auto-commit/push
│   ├── db_deploy.bat         ← MySQL database deployment
│   └── web_deploy.bat        ← Web files to htdocs
├── logs/
│   └── sync_YYYY_MM_DD.log   ← Daily logs
└── README.md                  ← This file
```

---

## 🎮 How to Use

### Starting AutoSync

**Method 1: Double-click** `master_launcher.vbs`
- Runs silently in background
- No console window
- Recommended for daily use

**Method 2: Run** `master_sync.bat`
- Shows console with live status
- Good for troubleshooting
- See exactly what's happening

### Stopping AutoSync

**Method 1: Double-click** `stop_autosync.bat`
- Quick and easy stop

**Method 2: Use launcher with argument**
```
master_launcher.vbs /stop
```

### Restarting AutoSync
```
master_launcher.vbs /restart
```

### Check if Running
```
master_launcher.vbs /status
```

---

## ⚙️ What Happens When USB is Inserted

```
1. USB DETECTED (G:)
   ↓
2. MODULE 1: USB Sync
   - E:\Aplikacje     → USB (MIRROR)
   - E:\Autohotkey    → USB (MIRROR)
   - E:\Scripts       → USB (MIRROR)
   - USB\Projects     → E:\Pliki\Projects (STANDARD)
   ↓
3. MODULE 2: Git Sync
   - Scans E:\Pliki\Projects for Git repos
   - Auto-commits changes with smart messages
   - Auto-pushes to GitHub
   ↓
4. MODULE 3: Database Deploy
   - Scans E:\Pliki\Projects\databases for .sql files
   - Creates databases: {class}_{filename}
   - Imports to E:\xampp MySQL
   ↓
5. MODULE 4: Web Deploy
   - Finds PHP projects in E:\Pliki\Projects\websites
   - Moves to E:\xampp\htdocs\myfiles
   - Names: {class}_{project} or just {project}
   ↓
6. COMPLETE - Wait for USB removal
   ↓
7. USB REMOVED - Loop back to step 1
```

---

## 📝 Configuration (sync_config.ini)

### USB Settings
```ini
[USB]
drive=G:                    # Your USB drive letter
check_interval=5            # Seconds between checks
```

### Local → USB (Mirror Mode)
```ini
[LocalToUSB]
# Exact copy - deletes files on USB if not on local
apps_src=E:\Aplikacje
apps_dst={USB}\Pliki\Inne\Instalki
```

### USB → Local (Standard Mode)
```ini
[USBToLocal]
# Keeps newer files, doesn't delete
db_src={USB}\Pliki\Technik Programista\Bazy Danych
db_dst=E:\Pliki\Projects\databases
```

### Git Settings
```ini
[Git]
root=E:\Pliki\Projects      # Where your Git repos are
auto_commit=true            # Auto-commit changes
auto_push=true              # Auto-push to GitHub
smart_messages=true         # Generate descriptive commits
scan_subdirs=true           # Scan subdirectories for repos
```

### MySQL Settings (FIXED!)
```ini
[MySQL]
bin=E:\xampp\mysql\bin\mysql.exe    # ← Changed from C: to E:
user=root
pass=                               # Empty if no password
sql_base=E:\Pliki\Projects\databases
charset=utf8mb4
```

### Web Deploy (FIXED!)
```ini
[WebDeploy]
source=E:\Pliki\Projects\websites
destination=E:\xampp\htdocs\myfiles  # ← Changed from C: to E:
```

---

## 🤖 Git Smart Messages

Instead of boring "Auto backup 02/02/2026", you get:

```
Auto: 3 modified, 2 added (php, sql files) - 02/02/2026 14:30:22
```

The script analyzes:
- How many files changed (modified, added, deleted)
- What types of files (.php, .sql, .cpp, etc.)
- Timestamp

---

## 💾 Database Auto-Deploy

**Example structure:**
```
databases/
├── klasa1/
│   ├── library.sql    → Database: klasa1_library
│   └── store.sql      → Database: klasa1_store
└── klasa2/
    └── shop.sql       → Database: klasa2_shop
```

Each .sql file creates a database: `{class_folder}_{filename}`

---

## 🌐 Web Auto-Deploy

**Moves PHP projects to htdocs with smart naming:**

Direct in websites folder:
```
websites/myproject/   → htdocs/myfiles/myproject/
```

In class subfolder:
```
websites/klasa2/shop/   → htdocs/myfiles/klasa2_shop/
```

---

## 📊 Logging

All operations logged to `logs/sync_YYYY_MM_DD.log`:

```
[14:30:15] USB DETECTED: G:
[14:30:16] SYNC: G:\Pliki\... -> E:\Pliki\Projects\cpp
[14:30:18] SUCCESS: cpp synced
[14:30:19] Committing: Auto: 2 modified (cpp files) - 02/02/2026 14:30:19
[14:30:22] SUCCESS: Pushed E:\Pliki\Projects
[14:30:25] Database: klasa2_shop deployed
[14:30:27] Web: klasa2_shop moved to htdocs
```

---

## 🔧 Troubleshooting

### "Weird OEA characters in console"
- **Not a problem!** That's just Polish characters in console encoding
- The actual sync works perfectly (check your logs)
- Use `master_launcher.vbs` to avoid seeing it

### Modules not running
- **FIXED!** Update your `master_sync.bat` with the new version
- Old version only had USB sync enabled
- New version calls all 4 modules

### XAMPP paths wrong
- **FIXED!** Update your `sync_config.ini` with the new version
- Changed all `C:\xampp` to `E:\xampp`

### Git push failing
- Check internet connection
- Verify Git credentials: `git config credential.helper store`
- Make sure you've pushed at least once manually

### MySQL errors
- Make sure XAMPP MySQL is running
- Check username/password in config
- Look for SQL syntax errors in log file

---

## 🚀 Auto-Start on Boot

1. Press `Win + R`
2. Type `shell:startup` and press Enter
3. Create shortcut to `master_launcher.vbs`
4. Done! AutoSync starts automatically when Windows boots

---

## ✨ What's New in v2.1

### Added:
- ✅ Enhanced launcher with start/stop/restart
- ✅ Process management functions
- ✅ Status checking
- ✅ Quick stop button

### Fixed:
- ✅ master_sync.bat now calls ALL modules
- ✅ XAMPP paths corrected to E: drive
- ✅ Better error handling
- ✅ Improved logging

### Removed:
- ❌ Scripts/launcher (merged into AutoSync)
- ❌ Duplicate launcher files
- ❌ Unnecessary VBS files

---

## 📋 Quick Command Reference

```bash
# Start (silent)
master_launcher.vbs

# Start (with console)
master_sync.bat

# Stop
stop_autosync.bat
# or
master_launcher.vbs /stop

# Restart
master_launcher.vbs /restart

# Check status
master_launcher.vbs /status
```

---

## 🎯 Migration from Scripts/launcher

**You can safely delete Scripts/launcher!**

Everything is now in AutoSync:
- ✅ Start/stop/restart functionality
- ✅ Process management
- ✅ Better logging
- ✅ All the same features, better integrated

---

Made with ❤️ for seamless automation

**AutoSync v2.1 - Now Actually Running All Modules!** 🎉
