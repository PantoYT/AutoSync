# AutoSync v2.0 - Automatic USB Backup & Deployment System

Complete automation for USB backups, Git synchronization, database deployment, and web file management.

## 🚀 Features

- **Bidirectional USB Sync**: E: ↔ USB automatic synchronization
- **Smart Git Auto-Commit**: Intelligent commit messages based on file changes
- **Database Auto-Deploy**: Scan .sql files and auto-create MySQL databases
- **Web Auto-Deploy**: Move PHP projects to htdocs with class-based naming
- **Runs Forever**: Background monitoring loop that never stops
- **Portable**: Copy entire folder to new PC and run setup
- **Detailed Logging**: Every operation logged with timestamps

## 📁 Project Structure

```
AutoSync/
├── master_launcher.vbs       ← Double-click this to start!
├── master_sync.bat            ← Main orchestrator
├── sync_config.ini            ← All your settings
├── setup.bat                  ← First-time setup wizard
├── modules/
│   ├── usb_sync.bat          ← USB file synchronization
│   ├── git_sync.bat          ← Git auto-commit/push
│   ├── db_deploy.bat         ← MySQL database deployment
│   └── web_deploy.bat        ← Web files to htdocs
├── logs/
│   └── sync_YYYY_MM_DD.log   ← Daily logs
└── README.md                  ← This file
```

## ⚙️ First Time Setup

### Option 1: Use Setup Wizard (Recommended)
1. Double-click `setup.bat`
2. Follow the wizard prompts
3. Configuration saved automatically

### Option 2: Manual Configuration
Edit `sync_config.ini` with your paths:

```ini
[USB]
drive=G:                       # Your USB drive letter

[LocalToUSB]
apps_src=E:\Aplikacje         # Files to backup TO USB
apps_dst={USB}\Pliki\...      # Destination on USB

[USBToLocal]
db_src={USB}\Pliki\...        # Files to sync FROM USB
db_dst=E:\Pliki\Projects\...  # Destination on local drive

[Git]
root=E:\Pliki\Projects        # Where your Git repos are
auto_commit=true              # Auto-commit changes
auto_push=true                # Auto-push to GitHub
smart_messages=true           # Generate descriptive commits

[MySQL]
bin=C:\xampp\mysql\bin\mysql.exe
user=root
pass=                         # Empty if no password

[WebDeploy]
source=E:\Pliki\Projects\websites
destination=C:\xampp\htdocs\myfiles
```

## 🎮 How to Use

### Starting AutoSync

**Method 1**: Double-click `master_launcher.vbs`
- Runs silently in background
- No console window

**Method 2**: Run `master_sync.bat`
- Shows console with status updates
- Useful for troubleshooting

### Auto-Start on Boot
Run `setup.bat` and choose "Yes" when asked about auto-start, or:
1. Press `Win + R`
2. Type `shell:startup` and press Enter
3. Create shortcut to `master_launcher.vbs`

### How It Works

```
1. Script starts → Waits for USB insertion
                          ↓
2. USB detected → Runs all sync modules:
                  • USB Sync (E: ↔ USB)
                  • Git Sync (commit/push)
                  • Database Deploy (.sql → MySQL)
                  • Web Deploy (PHP → htdocs)
                          ↓
3. Sync complete → Monitors USB for removal
                          ↓
4. USB removed → Back to step 1 (forever loop)
```

## 📊 Sync Behavior

### LOCAL → USB (Mirror Mode)
- **Apps, AutoHotkey, Scripts**: `/MIR` flag
- Exact copy - deletes files on USB if not on local
- Perfect for backups

### USB → LOCAL (Standard Mode)
- **Databases, Projects, Web files**: `/E` flag
- Keeps newer files, doesn't delete
- Safe for working files

## 🤖 Git Smart Messages

Instead of "Auto backup 01/27/2026", you get:

```
Auto: 3 modified, 2 added (php, sql files) - 01/27/2026 14:30:22
```

The script analyzes:
- How many files changed
- What types of files (.php, .sql, .cpp, etc.)
- What operations (modified, added, deleted)

## 💾 Database Auto-Deploy

Scans for `.sql` files in your projects and:

1. Finds: `E:\Pliki\Projects\databases\klasa2\shop.sql`
2. Creates database: `klasa2_shop`
3. Imports all tables/data automatically

**Naming Convention**: `{class_folder}_{filename}`

Example structure:
```
databases/
├── klasa1/
│   ├── library.sql    → Database: klasa1_library
│   └── store.sql      → Database: klasa1_store
└── klasa2/
    └── shop.sql       → Database: klasa2_shop
```

## 🌐 Web Auto-Deploy

Moves PHP projects to htdocs with smart naming:

**If directly in websites/**
```
websites/myproject/   → htdocs/myfiles/myproject/
```

**If in class subfolder:**
```
websites/klasa2/shop/   → htdocs/myfiles/klasa2_shop/
```

All `.php` projects are automatically detected and moved.

## 📝 Logging

All operations logged to `logs/sync_YYYY_MM_DD.log`:

```
[14:30:15] USB DETECTED: G:
[14:30:16] SYNC: G:\Pliki\... -> E:\Pliki\Projects\cpp
[14:30:18] SUCCESS: cpp synced
[14:30:19] Committing: Auto: 2 modified (cpp files) - 01/27/2026 14:30:19
[14:30:22] SUCCESS: Pushed E:\Pliki\Projects
[14:30:25] Database: klasa2_shop deployed
```

## 🔧 Troubleshooting

### Script not starting
- Check `logs/` folder for error messages
- Run `master_sync.bat` (not VBS) to see console output

### USB not detected
- Verify drive letter in `sync_config.ini`
- Check if USB is formatted and accessible

### Git push failing
- Check internet connection
- Verify Git credentials are configured
- Run `git config credential.helper store` in your repos

### MySQL import errors
- Verify MySQL is running (XAMPP Control Panel)
- Check username/password in config
- Look for SQL syntax errors in log file

### Files not syncing
- Check source/destination paths in config
- Verify you have write permissions
- Look for robocopy errors in log

## 🎯 Common Scenarios

### New Computer Setup
1. Copy entire `AutoSync/` folder to new PC
2. Run `setup.bat`
3. Enter your paths
4. Done!

### Adding New Sync Paths
1. Open `sync_config.ini`
2. Add new entries under `[LocalToUSB]` or `[USBToLocal]`
3. Follow existing format
4. Restart AutoSync

### Changing USB Drive Letter
1. Edit `sync_config.ini`
2. Change `drive=G:` to new letter
3. No restart needed - detects automatically

### Disable Auto-Push (Local Commits Only)
1. Edit `sync_config.ini`
2. Set `auto_push=false`
3. Commits stay local until you manually push

## 🔒 Safety Features

- **Error Handling**: Failed operations don't stop entire script
- **Detailed Logs**: Every action recorded with timestamps
- **Robocopy Retry**: 3 retries with 5-second wait on errors
- **Git Check**: Only commits if changes detected
- **MySQL Safety**: Drops database before recreating (clean imports)

## 💡 Tips & Best Practices

1. **Check logs regularly** - Look for patterns of failures
2. **Test on small folders first** - Before adding large directories
3. **Backup your config** - Copy `sync_config.ini` to USB
4. **Use Git branches** - For experimental features
5. **Schedule daily log reviews** - Catch issues early

## 📋 Config File Reference

### Path Placeholders
- `{USB}` - Automatically replaced with USB drive letter
- Example: `{USB}\Pliki\Inne` → `G:\Pliki\Inne`

### Boolean Settings
- `true` / `false` (case insensitive)
- Controls features like auto-commit, auto-push, smart messages

### Intervals
- `check_interval` - Seconds between USB checks (default: 5)
- Lower = more responsive, higher = less CPU usage

## 🆘 Support

If you encounter issues:
1. Check the log file in `logs/` folder
2. Run `master_sync.bat` to see live output
3. Verify paths in `sync_config.ini`
4. Ensure all required software is installed (Git, MySQL)

## 📜 Version History

**v2.0** (Current)
- Modular architecture
- Smart Git messages
- Portable configuration
- Setup wizard
- Improved logging

**v1.0** (Legacy)
- Basic USB sync
- Hardcoded paths
- Manual Git commits

---

**Made with ❤️ for seamless automation**
