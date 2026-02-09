# AutoSync - Improved Version
## Installation & Usage Guide

---

## 🚀 What's New in This Version

### ✅ Fixed Issues:
- **Crash Recovery**: Automatic cleanup of lockfiles on errors
- **Better Logging**: Detailed progress tracking with timestamps
- **Timeout Protection**: No more infinite hangs on robocopy
- **Error Handling**: Graceful handling of missing folders/drives
- **Progress Indicators**: See exactly what's happening in real-time
- **Summary Statistics**: Know how many operations succeeded/failed

### ✅ New Tools:
- **diagnostic.bat** - Checks your setup and identifies problems
- **quickfix.bat** - Automatically fixes common issues
- **Improved modules** - Better error handling in all sync modules

---

## 📁 File Structure

Your AutoSync folder should look like this:

```
AutoSync/
├── master_sync.bat              ← Main program (or use improved version)
├── master_sync_improved.bat     ← NEW: Improved main program
├── master_launcher.vbs          ← Silent launcher
├── stop_autosync.bat            ← Emergency stop
├── diagnostic.bat               ← NEW: Problem checker
├── quickfix.bat                 ← NEW: Auto-fix tool
├── sync_config.ini              ← Your configuration
├── modules/
│   ├── usb_sync.bat            ← USB sync module (or use improved)
│   ├── usb_sync_improved.bat  ← NEW: Improved USB sync
│   ├── git_sync.bat            ← Git auto-commit/push
│   ├── db_deploy.bat           ← MySQL database deployment
│   └── web_deploy.bat          ← Web project deployment
└── logs/
    └── sync_09_02_2026.log     ← Daily logs
```

---

## 🔧 Installation Steps

### Step 1: Backup Your Current Setup
```batch
REM Just in case, copy your current working files to a backup folder
```

### Step 2: Replace Files

**Option A: Replace Everything (Recommended)**
1. Rename `master_sync.bat` to `master_sync_old.bat`
2. Rename `master_sync_improved.bat` to `master_sync.bat`
3. In the `modules` folder:
   - Rename `usb_sync.bat` to `usb_sync_old.bat`
   - Rename `usb_sync_improved.bat` to `usb_sync.bat`

**Option B: Test First**
1. Keep your old files
2. Run `master_sync_improved.bat` directly to test
3. If it works, replace the old version

### Step 3: Run Diagnostic
```batch
diagnostic.bat
```
This will check:
- ✅ Config file exists
- ✅ Modules are in place
- ✅ USB drive is configured
- ✅ All paths are valid
- ✅ No stale lockfiles

### Step 4: Fix Any Issues
If diagnostic finds problems:
```batch
quickfix.bat
```
This automatically:
- 🧹 Kills hung processes
- 🗑️ Removes lockfiles
- 📁 Creates missing directories
- 🔧 Cleans temp files

---

## 🎯 Usage

### Normal Startup
```batch
REM Double-click:
master_launcher.vbs

REM Or run directly:
master_sync.bat
```

### Stop AutoSync
```batch
REM Double-click:
stop_autosync.bat

REM Or use launcher:
master_launcher.vbs stop
```

### Check Status
```batch
master_launcher.vbs status
```

### Restart AutoSync
```batch
master_launcher.vbs restart
```

---

## 🐛 Troubleshooting

### Problem: "Another instance is running!"
**Solution:**
```batch
quickfix.bat
```
Or manually:
```batch
del "%TEMP%\autosync_master.lock"
```

### Problem: Sync stops in the middle
**Check the log file:**
```batch
notepad logs\sync_09_02_2026.log
```
Look for:
- `ERROR:` - Critical failures
- `WARNING:` - Non-critical issues
- `SUCCESS:` - What worked

**Common causes:**
1. USB drive disconnected mid-sync
2. File/folder locked by another program
3. Permission denied
4. Network drive timeout

### Problem: USB not detected
**Check:**
1. Is USB plugged in?
2. Check drive letter in Windows Explorer
3. Update `sync_config.ini` if drive letter changed
4. Run `diagnostic.bat` to verify

### Problem: Folders not syncing
**Check:**
1. Run `diagnostic.bat` - it will list all paths
2. Verify folders exist on USB:
   ```
   G:\Pliki\Technik Programista\Bazy Danych\klasa1
   G:\Pliki\Technik Programista\Programowanie\cpp\klasa1
   etc.
   ```
3. Check log file for "INFO: not found" messages

---

## 📝 Understanding the Log

### Good Signs ✅
```
[15:56:38] USB DETECTED: G:
[15:56:39] SUCCESS: apps mirrored
[15:56:40] SUCCESS: klasa1 synced (code: 1)
[15:57:00] SYNC CYCLE COMPLETE
Modules run: 4
Successful: 4
Failed: 0
```

### Warning Signs ⚠️
```
[15:56:40] INFO: klasa2 not found (normal if not in that year yet)
[15:56:45] SKIP: Source not found: E:\Missing\Folder
```
These are usually OK - they mean optional folders don't exist yet.

### Error Signs ❌
```
[15:56:50] ERROR: Mirror failed for apps (critical error)
[15:57:00] ERROR: USB drive G: not accessible!
[15:57:10] WARNING: Commit failed for C:\repo
```
These need attention - run `diagnostic.bat` to identify the problem.

---

## 🎓 For First-Year Students (klasa1)

**You're in klasa1, so:**
- ✅ Only `klasa1` folders will sync
- ✅ The script will skip `klasa2-5` (that's normal!)
- ✅ You'll see messages like: `INFO: klasa2 not found (normal)`
- ✅ As you progress to klasa2, just create the folder and it will auto-sync

**Your USB structure should look like:**
```
G:\
└── Pliki\
    └── Technik Programista\
        ├── Bazy Danych\
        │   └── klasa1\          ← Your current year
        ├── Programowanie\
        │   ├── cpp\
        │   │   └── klasa1\      ← Your current year
        │   └── python\
        │       └── klasa1\      ← Your current year
        └── Strony internetowe\
            └── klasa1\          ← Your current year
```

---

## 🔐 Lockfile Explained

### What is it?
A temporary file at: `C:\Users\YourName\AppData\Local\Temp\autosync_master.lock`

### Why does it exist?
Prevents AutoSync from starting twice (would corrupt files!)

### When does it get deleted?
- ✅ Normal shutdown: Auto-deleted
- ❌ Crash/force-close: Left behind (causes "already running" error)

### How to fix?
```batch
del "%TEMP%\autosync_master.lock"
```
Or use `quickfix.bat`

---

## 📊 Robocopy Exit Codes

The improved version shows robocopy codes in logs:

| Code | Meaning |
|------|---------|
| 0 | No files copied (already in sync) ✅ |
| 1 | Files copied successfully ✅ |
| 2 | Extra files detected ✅ |
| 3 | Files copied + extras ✅ |
| 4-7 | Mismatches (usually OK) ⚠️ |
| 8+ | **ERRORS - something failed!** ❌ |

Codes 0-7 are considered **SUCCESS** in the improved version.

---

## 🎮 Quick Command Reference

```batch
REM Start AutoSync
master_sync.bat

REM Stop AutoSync
stop_autosync.bat

REM Check for problems
diagnostic.bat

REM Fix common issues
quickfix.bat

REM Delete lockfile manually
del "%TEMP%\autosync_master.lock"

REM View latest log
notepad logs\sync_09_02_2026.log
```

---

## 💡 Tips

1. **Run diagnostic.bat first** - It will tell you exactly what's wrong
2. **Check logs regularly** - They show what's actually happening
3. **Use quickfix.bat** - It solves 90% of common problems
4. **Don't panic about "klasa2-5 not found"** - That's normal for first-year!
5. **If sync stops mid-way** - Check if USB got disconnected

---

## 🆘 Still Having Issues?

1. Run `diagnostic.bat` and take a screenshot
2. Run `quickfix.bat`
3. Check the latest log file in `logs\` folder
4. Look for ERROR messages (not INFO or WARNING)
5. Verify your USB drive letter hasn't changed

---

## 📞 Need More Help?

The improved version includes much better error messages. When something fails:
1. It tells you EXACTLY what failed
2. It continues with other tasks (doesn't give up entirely)
3. It gives you a summary at the end

**Check the log file** - it has detailed step-by-step information!

---

Made with ❤️ for students who want their files to just... work!