# Automation Hub

**Professional Task Automation & Scheduling System**

A lightweight, modular Python GUI application for automating repetitive tasks including file transfers, Git synchronization, database operations, and script execution.

---

## ✨ Features

### Core Features
- **Lightweight & Fast** - Minimal resource usage, quick launch times
- **Modular Architecture** - Easy to extend with new task types
- **Fully Configurable** - No hard-coded paths, customizable presets
- **Task Scheduling** - Run immediately, at intervals, or triggered by events
- **Centralized Logging** - Live monitoring of all tasks with searchable logs
- **Modern GUI** - Built with PyQt6, multiple themes available
- **Background Execution** - Tasks run in threads, GUI stays responsive

### Task Types
- **Script Execution** - Run Python scripts, batch files, or system commands
- **File Transfer** - Copy/move files with patterns, mirror directories
- **Git Sync** - Automatic commit/push with smart commit messages
- **SQL Operations** - Import/export MySQL databases
- **Extensible** - Easy to add new task types

### Scheduling Options
- **Immediate** - Run once right now
- **Interval** - Every N seconds/minutes/hours
- **Daily** - Run at specific time each day
- **Weekly** - Run on specific day and time
- **Event-based** - Triggered by external events

### GUI Features
- **Task Management** - Start, pause, stop, reset, delete tasks
- **Progress Tracking** - Real-time progress bars for active tasks
- **Log Viewer** - Scrollable, filterable log panel
- **Themes** - Dark Blue & Yellow (default), Black & White, System Default
- **Presets** - Save and reuse common task configurations
- **Settings** - Fully configurable from GUI

---

## 📋 Requirements

- **Python 3.8+**
- **Operating System**: Windows, Linux, or macOS
- **Dependencies**: Listed in `requirements.txt`

---

## 🚀 Installation

### 1. Clone or Download

```bash
git clone <repository-url>
cd automation_hub
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note for Windows users:**
- `pywin32` is required for some features
- Will be installed automatically on Windows

**Note for Git features:**
- Install `GitPython` if you need Git synchronization:
  ```bash
  pip install GitPython
  ```

---

## 🎯 Quick Start

### Basic Usage

1. **Launch the application:**
   ```bash
   python main.py
   ```

2. **Add a task:**
   - Click "Add Task" button in toolbar
   - Select task type (Script, File Transfer, Git, SQL)
   - Configure task settings
   - Save task

3. **Run a task:**
   - Select task in the task table
   - Click "Start" button
   - Monitor progress and logs in real-time

4. **Schedule a task:**
   - Right-click task → "Schedule"
   - Choose schedule type (Interval, Daily, Weekly)
   - Configure schedule parameters

### Example Tasks

#### File Transfer Task
```
Name: Backup Documents
Type: File Transfer
Source: C:\Users\YourName\Documents
Destination: D:\Backups\Documents
Operation: Copy
Overwrite: Yes
Patterns: *.docx, *.pdf
Schedule: Daily at 22:00
```

#### Git Sync Task
```
Name: Auto-commit Projects
Type: Git Sync
Repository: C:\Projects\MyApp
Auto Add: Yes
Auto Commit: Yes
Auto Push: Yes
Smart Messages: Yes
Schedule: Every 30 minutes
```

#### SQL Import Task
```
Name: Import Databases
Type: SQL Database
Operation: Import
MySQL Path: C:\xampp\mysql\bin\mysql.exe
User: root
SQL Directory: G:\Databases
Schedule: On demand
```

---

## 📁 Project Structure

```
automation_hub/
│
├── gui/                          # GUI components
│   ├── main_window.py            # Main application window
│   ├── task_table.py             # Task list with controls
│   ├── log_panel.py              # Log viewer
│   ├── settings_dialog.py        # Settings menu
│   ├── theme_manager.py          # Theme system
│   └── tray_icon.py              # System tray (optional)
│
├── tasks/                        # Task type implementations
│   ├── base_task.py              # Base task class
│   ├── script_task.py            # Script execution
│   ├── file_transfer_task.py     # File operations
│   ├── git_task.py               # Git sync
│   └── sql_task.py               # SQL import/export
│
├── utils/                        # Utility modules
│   ├── logger.py                 # Centralized logging
│   ├── config_manager.py         # Configuration system
│   ├── scheduler.py              # Task scheduling
│   └── thread_manager.py         # Thread management
│
├── configs/                      # Configuration files
│   ├── default_config.json       # Default settings
│   └── user_config.json          # User preferences
│
├── logs/                         # Application logs
│   └── app_YYYYMMDD.log
│
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## ⚙️ Configuration

### Configuration Files

Configuration is stored in JSON format in the `configs/` directory:

- **default_config.json** - Default settings (don't edit directly)
- **user_config.json** - Your customized settings

### Configuration Options

#### Application Settings
```json
{
  "app": {
    "theme": "dark-blue-yellow",
    "auto_start": false,
    "log_retention_days": 30
  }
}
```

#### Path Presets
```json
{
  "paths": {
    "scripts": "C:\\Scripts",
    "projects": "C:\\Projects",
    "databases": "C:\\Databases",
    "htdocs": "C:\\xampp\\htdocs"
  }
}
```

#### MySQL Settings
```json
{
  "mysql": {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "charset": "utf8mb4"
  }
}
```

### Editing Configuration

1. **Via GUI** (Recommended):
   - Menu → Settings → Edit Configuration
   - Change settings in the dialog
   - Click Save

2. **Manually**:
   - Edit `configs/user_config.json`
   - Restart application

---

## 🎨 Themes

### Available Themes

1. **Dark Blue & Yellow** (Default)
   - Dark blue background with yellow accents
   - Easy on the eyes for long sessions

2. **Black & White**
   - High contrast monochrome design
   - Minimal and professional

3. **System Default**
   - Uses your operating system's theme
   - Automatically adapts to system changes

### Changing Theme

- **GUI**: Menu → Settings → Theme → Select theme
- **Config**: Edit `app.theme` in `user_config.json`

---

## 📊 Task Types

### Script Execution

Execute Python scripts, batch files, or system commands.

**Configuration:**
- `script_path`: Path to script file
- `script_type`: 'python', 'batch', or 'command'
- `arguments`: List of command-line arguments
- `working_dir`: Working directory for execution
- `timeout`: Maximum execution time (seconds)
- `capture_output`: Whether to capture stdout/stderr

**Example:**
```python
{
  "name": "Run Cleanup Script",
  "type": "script",
  "config": {
    "script_path": "C:\\Scripts\\cleanup.py",
    "script_type": "python",
    "arguments": ["--verbose"],
    "timeout": 300
  }
}
```

### File Transfer

Copy or move files/folders with advanced filtering.

**Configuration:**
- `source`: Source path (file or directory)
- `destination`: Destination path
- `operation`: 'copy' or 'move'
- `overwrite`: Whether to overwrite existing files
- `mirror`: Mirror mode (delete extras in destination)
- `file_patterns`: Include patterns (e.g., `['*.txt', '*.pdf']`)
- `exclude_patterns`: Exclude patterns

**Example:**
```python
{
  "name": "Backup Projects",
  "type": "file_transfer",
  "config": {
    "source": "C:\\Projects",
    "destination": "D:\\Backups\\Projects",
    "operation": "copy",
    "overwrite": true,
    "file_patterns": ["*.py", "*.md", "*.json"]
  }
}
```

### Git Sync

Automatic Git commit and push with smart commit messages.

**Configuration:**
- `repo_path`: Path to Git repository
- `auto_add`: Automatically stage all changes
- `auto_commit`: Automatically commit changes
- `auto_push`: Automatically push to remote
- `commit_message`: Custom commit message (optional)
- `smart_message`: Generate descriptive commit messages
- `remote`: Remote name (default: origin)
- `branch`: Branch name (default: current branch)

**Example:**
```python
{
  "name": "Auto-commit Website",
  "type": "git",
  "config": {
    "repo_path": "C:\\Projects\\MyWebsite",
    "auto_add": true,
    "auto_commit": true,
    "auto_push": true,
    "smart_message": true
  }
}
```

### SQL Database

Import/export MySQL databases.

**Configuration:**
- `operation`: 'import' or 'export'
- `mysql_bin`: Path to mysql.exe
- `user`: MySQL username
- `password`: MySQL password
- `database`: Database name (for export)
- `sql_file`: Single SQL file path
- `sql_directory`: Directory with SQL files (batch import)
- `create_database`: Create database if not exists
- `drop_existing`: Drop database before import

**Example:**
```python
{
  "name": "Import Databases",
  "type": "sql",
  "config": {
    "operation": "import",
    "mysql_bin": "C:\\xampp\\mysql\\bin\\mysql.exe",
    "user": "root",
    "password": "",
    "sql_directory": "G:\\Databases",
    "drop_existing": true
  }
}
```

---

## 🔄 Scheduling

### Schedule Types

1. **Immediate**
   - Run once, right now
   - No configuration needed

2. **Interval**
   - Run every N seconds/minutes/hours
   - Config: `{"minutes": 30}` or `{"hours": 2}`

3. **Daily**
   - Run at specific time each day
   - Config: `{"time": "14:30"}`

4. **Weekly**
   - Run on specific day and time
   - Config: `{"day": 0, "time": "09:00"}` (0=Monday, 6=Sunday)

5. **Event-based**
   - Triggered manually or by external events
   - Config: `{"event_type": "file_changed"}`

### Setting Up Schedules

1. Right-click task in task table
2. Select "Schedule Task"
3. Choose schedule type
4. Configure parameters
5. Click OK

---

## 📝 Logging

### Log Levels

- **DEBUG** - Detailed diagnostic information
- **INFO** - General information messages
- **WARNING** - Warning messages (non-critical issues)
- **ERROR** - Error messages (task failures)
- **SUCCESS** - Success messages (task completed)

### Log Viewer

The log panel shows real-time logs with:
- Timestamp
- Task name
- Log level
- Message

### Log Files

Logs are saved to `logs/app_YYYYMMDD.log` with:
- Daily rotation
- Configurable retention period
- UTF-8 encoding

### Exporting Logs

1. Menu → Tools → Export Logs
2. Choose format (TXT or CSV)
3. Select task filter (optional)
4. Choose output location

---

## 🛠️ Extending the Application

### Adding a New Task Type

1. **Create task class** in `tasks/`:

```python
from tasks.base_task import BaseTask

class MyCustomTask(BaseTask):
    def __init__(self, name: str, config: dict):
        super().__init__(name, "my_custom", config)
    
    def validate(self) -> tuple[bool, str]:
        # Validate configuration
        return True, None
    
    def _execute(self) -> bool:
        # Execute task logic
        self.log("Task running", "INFO")
        self.update_progress(50.0)
        # ... do work ...
        return True
```

2. **Register in GUI** - Add to task type selection

3. **Create configuration UI** - Add task-specific settings dialog

### Code Style

- Follow PEP 8
- Type hints for function signatures
- Docstrings for classes and methods
- Clear variable names

---

## 🐛 Troubleshooting

### Application Won't Start

**Check Python version:**
```bash
python --version  # Should be 3.8+
```

**Reinstall dependencies:**
```bash
pip install -r requirements.txt --force-reinstall
```

**Check for errors:**
```bash
python main.py
# Look for error messages in console
```

### Tasks Not Executing

1. **Check logs** - View log panel for error messages
2. **Validate configuration** - Ensure all paths exist
3. **Check permissions** - Ensure write access to destinations
4. **Test manually** - Try running the operation manually first

### Git Sync Issues

**GitPython not installed:**
```bash
pip install GitPython
```

**Authentication errors:**
- Set up SSH keys for passwordless authentication
- Or use Git credential manager

**Push failures:**
- Check network connectivity
- Verify remote URL
- Ensure you have push permissions

### SQL Import Errors

**MySQL not found:**
- Verify `mysql.exe` path in configuration
- Ensure XAMPP/MySQL is installed

**Permission denied:**
- Check MySQL user permissions
- Verify password is correct

**Character encoding issues:**
- Ensure SQL files are UTF-8 encoded
- Try `charset: utf8mb4` in configuration

---

## 💡 Tips & Best Practices

### Performance
- Use file patterns to limit transfer scope
- Set reasonable timeouts for long-running tasks
- Schedule heavy tasks during off-peak hours

### Reliability
- Test tasks manually before scheduling
- Use try/dry-run options when available
- Monitor logs regularly
- Keep backups of configuration

### Security
- Don't store passwords in plaintext config
- Use environment variables for sensitive data
- Restrict file permissions on config directory
- Review logs for security issues

### Organization
- Use descriptive task names
- Group related tasks with prefixes
- Document custom configurations
- Export/backup configurations regularly

---

## 🔐 Security Notes

### Sensitive Data

- Passwords in config files are stored in plaintext
- **Recommendation**: Use OS keyring or environment variables
- Restrict read permissions on `configs/` directory

### File Operations

- Always verify source/destination paths
- Test with dry-run or small datasets first
- Be cautious with mirror mode (deletes files!)

### Script Execution

- Only run scripts from trusted sources
- Review scripts before adding to automation
- Use timeout limits to prevent runaway scripts

---

## 📄 License

This project is provided as-is for educational and personal use.

---

## 🤝 Contributing

To add features or fix bugs:

1. Create a new branch
2. Make your changes
3. Test thoroughly
4. Submit pull request with description

---

## 📧 Support

For issues, questions, or suggestions:

- Check logs in `logs/` directory
- Review configuration in `configs/`
- Consult this README
- Check inline code documentation

---

## 🗺️ Roadmap

### Planned Features
- [ ] File system monitoring triggers
- [ ] Email notifications
- [ ] Task dependencies (run after another task)
- [ ] Remote task execution
- [ ] Web dashboard
- [ ] Plugin system
- [ ] Task templates/marketplace
- [ ] Docker container support

---

## 📚 Additional Resources

### Documentation
- Qt Documentation: https://doc.qt.io/qtforpython/
- Python Threading: https://docs.python.org/3/library/threading.html
- GitPython: https://gitpython.readthedocs.io/

### Example Configurations

See `configs/default_config.json` for example task configurations and presets.

---

**Made with ❤️ for automating the boring stuff!**
