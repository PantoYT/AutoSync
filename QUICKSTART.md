# Quick Start Guide - Automation Hub

Get up and running in 5 minutes!

## Installation

### Step 1: Install Dependencies

```bash
python setup.py
```

This will:
- Check Python version (3.8+ required)
- Install all required packages
- Create necessary directories
- Initialize configuration

### Step 2: Launch Application

```bash
python main.py
```

## First Steps

### 1. Configure Base Paths

Go to **Settings → Configuration** and set your paths:

- **Scripts Path**: Where your scripts are located
- **Projects Path**: Your project directory
- **Databases Path**: SQL files location
- **XAMPP Path**: If using XAMPP (e.g., `C:\xampp`)

### 2. Create Your First Task

#### Example: File Backup Task

1. Click **"Add Task"** button
2. Fill in task details:
   - **Name**: "Daily Backup"
   - **Type**: File Transfer
   - **Source**: `C:\Users\YourName\Documents`
   - **Destination**: `D:\Backups`
   - **Operation**: Copy
   - **Overwrite**: Yes

3. Click **"Save"**

#### Example: Git Auto-Commit Task

1. Click **"Add Task"**
2. Fill in:
   - **Name**: "Auto-commit Project"
   - **Type**: Git Sync
   - **Repository Path**: `C:\Projects\MyApp`
   - **Auto Add**: ✓
   - **Auto Commit**: ✓
   - **Auto Push**: ✓
   - **Smart Messages**: ✓

3. Click **"Save"**

### 3. Run a Task

- Select task in the table
- Click **▶️ Start** button
- Watch progress in the log panel

### 4. Schedule a Task

- Right-click task → **"Schedule"**
- Choose schedule type:
  - **Interval**: Every 30 minutes
  - **Daily**: At 14:00
  - **Weekly**: Monday at 09:00

## Common Use Cases

### Use Case 1: USB Sync on Connect

**Goal**: Auto-sync files when USB drive is connected

**Setup**:
1. Create File Transfer task
2. Source: USB drive (e.g., `G:\Documents`)
3. Destination: Local backup
4. Schedule: Event-based (manual trigger)

### Use Case 2: Nightly Database Backup

**Goal**: Export MySQL databases every night

**Setup**:
1. Create SQL task
2. Operation: Export
3. Database: your_database
4. Output: `D:\Backups\db_backup.sql`
5. Schedule: Daily at 02:00

### Use Case 3: Auto-commit Work

**Goal**: Auto-commit changes every hour

**Setup**:
1. Create Git Sync task
2. Repository: Your project folder
3. Smart Messages: ✓
4. Schedule: Interval (60 minutes)

## Keyboard Shortcuts

- **Ctrl+N**: New task
- **Ctrl+S**: Start selected task
- **Ctrl+Q**: Stop selected task
- **Ctrl+L**: Clear logs
- **F5**: Refresh task list

## Themes

Change theme in **Settings → Theme**:

- **Dark Blue & Yellow** (default)
- **Black & White**
- **System Default**

## Tips

### Performance
- Start with small file sets to test
- Use file patterns to filter transfers
- Set reasonable timeouts

### Reliability
- Always test tasks manually first
- Monitor logs for errors
- Keep backups of config files

### Organization
- Use descriptive task names
- Group related tasks with prefixes
- Export configs regularly

## Troubleshooting

### Application won't start

```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Tasks fail immediately

1. Check log panel for error messages
2. Verify all paths exist
3. Check file permissions
4. Test operation manually

### Git push fails

- Set up SSH keys
- Or use Git credential manager
- Check network connectivity

## Next Steps

📖 **Read the full README.md** for:
- Detailed task configuration
- Advanced scheduling options
- Security best practices
- Extending the application

🛠️ **Explore the code**:
- `tasks/` - Task implementations
- `gui/` - User interface
- `utils/` - Helper modules

💡 **Get ideas**:
- Check `configs/default_config.json` for examples
- Look at existing Python scripts in uploaded files

## Support

- **Logs**: Check `logs/app_YYYYMMDD.log`
- **Config**: Edit `configs/user_config.json`
- **Documentation**: See README.md

---

**Happy Automating! 🚀**
