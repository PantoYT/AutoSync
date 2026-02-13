# Automation Hub - Project Overview

## 🎯 Project Description

**Automation Hub** is a professional, modular Python GUI application designed for automating repetitive tasks. Built from scratch with a clean architecture, it provides a user-friendly interface for managing file transfers, Git synchronization, database operations, and script execution.

## 🏗️ Architecture

### Design Principles

1. **Modular** - Each component is independent and reusable
2. **Extensible** - Easy to add new task types
3. **Separation of Concerns** - GUI separated from business logic
4. **Thread-safe** - Tasks run in background without blocking UI
5. **Configuration-driven** - No hard-coded paths

### Core Components

```
┌─────────────────────────────────────────────────────────┐
│                    Main Application                      │
│                      (main.py)                          │
└────────────┬─────────────────────────────┬──────────────┘
             │                             │
    ┌────────▼────────┐          ┌────────▼────────┐
    │   GUI Layer     │          │  Business Logic │
    │   (gui/)        │          │  (tasks/utils/) │
    └────────┬────────┘          └────────┬────────┘
             │                             │
    ┌────────▼────────┐          ┌────────▼────────┐
    │  Main Window    │          │   Task Manager  │
    │  Theme Manager  │          │   Scheduler     │
    │  Log Panel      │          │   Config Mgr    │
    └─────────────────┘          └─────────────────┘
```

### Directory Structure

```
automation_hub/
│
├── gui/                          # User Interface
│   ├── __init__.py
│   ├── main_window.py            # Main application window
│   └── theme_manager.py          # Theme system
│
├── tasks/                        # Task Implementations
│   ├── __init__.py
│   ├── base_task.py              # Abstract base class
│   ├── script_task.py            # Script execution
│   ├── file_transfer_task.py     # File operations
│   ├── git_task.py               # Git synchronization
│   └── sql_task.py               # Database operations
│
├── utils/                        # Utility Modules
│   ├── __init__.py
│   ├── logger.py                 # Centralized logging
│   ├── config_manager.py         # Configuration system
│   └── scheduler.py              # Task scheduling
│
├── configs/                      # Configuration Files
│   ├── default_config.json       # Default settings
│   └── user_config.json          # User preferences
│
├── logs/                         # Application Logs
│   └── app_YYYYMMDD.log
│
├── resources/                    # Resources (icons, etc.)
│
├── main.py                       # Application entry point
├── setup.py                      # Setup script
├── requirements.txt              # Python dependencies
├── README.md                     # Full documentation
└── QUICKSTART.md                 # Quick start guide
```

## 📦 Components

### 1. Task System (`tasks/`)

#### BaseTask (Abstract)
- Provides common functionality for all tasks
- Manages lifecycle: start, pause, stop, reset
- Handles threading for background execution
- Progress tracking and status updates
- Callback system for GUI notifications

#### Task Types

**ScriptTask**
- Execute Python scripts, batch files, or commands
- Configurable timeout and working directory
- Capture and log stdout/stderr

**FileTransferTask**
- Copy or move files/folders
- Pattern matching (include/exclude)
- Mirror mode for exact replication
- Progress tracking per file

**GitTask**
- Automatic git add/commit/push
- Smart commit message generation
- Repository validation
- Remote push with error handling

**SQLTask**
- Import/export MySQL databases
- Batch import from directory
- Auto-create databases
- Character encoding support

### 2. Utilities (`utils/`)

#### Logger
- Centralized logging system
- Multiple outputs: GUI, console, file
- Log levels: DEBUG, INFO, WARNING, ERROR, SUCCESS
- In-memory log storage with configurable size
- Export to TXT/CSV

#### ConfigManager
- JSON-based configuration
- Dot-notation access (e.g., `config.get('app.theme')`)
- Import/export configs
- Preset management
- Auto-save on exit

#### Scheduler
- Multiple schedule types: immediate, interval, daily, weekly, event
- Background execution thread
- Enable/disable schedules
- Next run time calculation
- Event-based triggering

### 3. GUI (`gui/`)

#### MainWindow
- Central application window
- Task table with controls
- Real-time log panel
- Menu and toolbar
- Theme support
- Status bar

#### ThemeManager
- Multiple themes: Dark Blue & Yellow, Black & White, System
- Qt stylesheet generation
- Easy theme switching
- Consistent styling across app

## 🔧 Technical Details

### Threading Model

```
Main Thread (GUI)
  │
  ├─► Task Thread 1 (Background)
  ├─► Task Thread 2 (Background)
  ├─► Task Thread N (Background)
  └─► Scheduler Thread (Background)
```

- GUI runs in main Qt thread
- Each task executes in its own thread
- Scheduler runs in background thread
- Thread-safe communication via signals/callbacks

### Task Lifecycle

```
IDLE → START → RUNNING → [PAUSED] → COMPLETED
                  │                      │
                  └──────► STOPPED ──────┘
                  │                      
                  └──────► FAILED ───────┘
```

### Configuration Flow

```
default_config.json → Merge → user_config.json → Runtime
         ↓                            ↓
    Shipped with app            User modifications
```

### Logging System

```
Task Event → Logger → [Memory Buffer]
                           │
                           ├─► GUI Display
                           ├─► Console Output
                           └─► Log File
```

## 🎨 GUI Features

### Task Table Columns
1. **Task Name** - Descriptive task name
2. **Type** - Task type (Script, File, Git, SQL)
3. **Status** - Current status (Idle, Running, etc.)
4. **Progress** - Progress bar (0-100%)
5. **Next Run** - Scheduled run time
6. **Actions** - Quick action buttons

### Theme System

Themes control:
- Background colors
- Text colors
- Button styles
- Table styling
- Scrollbar appearance
- Menu styling

### Log Panel

Features:
- Color-coded by level
- Auto-scroll to bottom
- Monospace font for readability
- Searchable (future feature)
- Export functionality

## 🔌 Extensibility

### Adding a New Task Type

1. **Create task class**:
```python
from tasks.base_task import BaseTask

class MyTask(BaseTask):
    def __init__(self, name: str, config: dict):
        super().__init__(name, "my_task", config)
    
    def validate(self) -> tuple[bool, str]:
        # Validation logic
        return True, None
    
    def _execute(self) -> bool:
        # Execution logic
        return True
```

2. **Register in task factory** (future: task_factory.py)

3. **Create GUI dialog** for task configuration

4. **Add to task type menu**

### Adding a New Schedule Type

1. Update `ScheduleType` enum
2. Implement in `_update_next_run()` method
3. Add GUI configuration dialog

## 📊 Performance Considerations

- **Memory**: Logs limited to configurable size (default: 2000 entries)
- **Threading**: Tasks run in background, non-blocking
- **File I/O**: Buffered operations for large files
- **Database**: Connection pooling for MySQL operations
- **GUI Updates**: Rate-limited to prevent overwhelming

## 🔒 Security Considerations

### Current State
- Passwords stored in plaintext config (NOT RECOMMENDED)
- File paths validated before operations
- Git operations use system credentials
- MySQL connections use configured credentials

### Recommendations
1. Use OS keyring for password storage
2. Implement encrypted configuration
3. Add user authentication for app access
4. Audit log for security events
5. File permission checks before operations

## 🧪 Testing Strategy (Future)

### Unit Tests
- Task validation
- Configuration management
- Scheduler logic
- Theme switching

### Integration Tests
- Task execution end-to-end
- GUI interactions
- Configuration persistence
- Log export

### Manual Testing Checklist
- [ ] Create each task type
- [ ] Schedule tasks with all schedule types
- [ ] Test pause/resume/stop
- [ ] Theme switching
- [ ] Config import/export
- [ ] Log export
- [ ] Multiple tasks running simultaneously

## 📈 Future Enhancements

### Planned Features
1. **File system monitoring** - Auto-trigger on file changes
2. **Email notifications** - Notify on task completion/failure
3. **Task dependencies** - Run task B after task A
4. **Remote execution** - Execute tasks on remote machines
5. **Web dashboard** - Monitor tasks via web interface
6. **Plugin system** - Load task types from plugins
7. **Task templates** - Shareable task configurations
8. **Docker support** - Run tasks in containers

### Code Improvements
1. **Type hints** - Complete type annotations
2. **Docstrings** - Comprehensive documentation
3. **Error handling** - More specific exceptions
4. **Validation** - Input validation library
5. **Async/await** - For I/O operations
6. **Database** - SQLite for task history

## 🎓 Learning Resources

### Technologies Used
- **PyQt6**: https://doc.qt.io/qtforpython/
- **GitPython**: https://gitpython.readthedocs.io/
- **Threading**: https://docs.python.org/3/library/threading.html
- **JSON**: https://docs.python.org/3/library/json.html

### Design Patterns
- **Observer Pattern**: Task callbacks
- **Strategy Pattern**: Task types
- **Singleton Pattern**: Global managers
- **Factory Pattern**: Task creation (future)
- **Template Method**: Base task execution

## 📝 Code Quality

### Standards
- Follow PEP 8 style guide
- Type hints for function signatures
- Docstrings for public APIs
- Meaningful variable names
- DRY principle (Don't Repeat Yourself)

### Tools (Recommended)
- **Black**: Code formatting
- **Pylint**: Static analysis
- **MyPy**: Type checking
- **Pytest**: Unit testing

## 🤝 Contributing Guidelines

1. **Fork repository**
2. **Create feature branch**
3. **Write tests** for new features
4. **Update documentation**
5. **Submit pull request**

### Commit Message Format
```
type(scope): subject

body

footer
```

Example:
```
feat(tasks): add FTP transfer task

Implements FTP file transfer with SSL support

Closes #123
```

## 📄 License

This project is provided as-is for educational and personal use.

## 🙏 Acknowledgments

Based on requirements and existing automation scripts, this project was built from scratch to provide a clean, modular, and professional automation solution.

---

**Built with Python + PyQt6 = ❤️**
