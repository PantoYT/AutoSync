"""
Task Creation Dialog
Dialog for creating and editing tasks
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QPushButton, QTextEdit,
    QFileDialog, QCheckBox, QSpinBox, QLabel,
    QTabWidget, QWidget, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt

from tasks.script_task import ScriptTask
from tasks.file_transfer_task import FileTransferTask
from tasks.git_task import GitTask
from tasks.sql_task import SQLTask


class TaskDialog(QDialog):
    """Dialog for creating/editing tasks"""
    
    def __init__(self, parent=None, task=None, edit_mode=False):
        super().__init__(parent)
        
        self.task = task
        self.edit_mode = edit_mode
        self.task_config = {}
        
        self.setWindowTitle("Edit Task" if edit_mode else "Create New Task")
        self.setMinimumSize(600, 500)
        
        self.setup_ui()
        
        if edit_mode and task:
            self.load_task_data()
    
    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        
        # Basic information
        form_layout = QFormLayout()
        
        # Task name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter task name")
        form_layout.addRow("Task Name:", self.name_edit)
        
        # Task type
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Script Execution",
            "File Transfer",
            "Git Sync",
            "SQL Database"
        ])
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        form_layout.addRow("Task Type:", self.type_combo)
        
        layout.addLayout(form_layout)
        
        # Configuration tabs
        self.tabs = QTabWidget()
        
        # Create configuration tabs for each task type
        self.script_tab = self.create_script_tab()
        self.file_tab = self.create_file_tab()
        self.git_tab = self.create_git_tab()
        self.sql_tab = self.create_sql_tab()
        
        self.tabs.addTab(self.script_tab, "Script Config")
        self.tabs.addTab(self.file_tab, "File Transfer Config")
        self.tabs.addTab(self.git_tab, "Git Config")
        self.tabs.addTab(self.sql_tab, "SQL Config")
        
        layout.addWidget(self.tabs)
        
        # Update visible tab based on type
        self.on_type_changed(0)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Task")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_task)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def create_script_tab(self):
        """Create script execution configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        form = QFormLayout()
        
        # Script type
        self.script_type_combo = QComboBox()
        self.script_type_combo.addItems(["Python Script", "Batch File", "System Command"])
        form.addRow("Script Type:", self.script_type_combo)
        
        # Script path
        path_layout = QHBoxLayout()
        self.script_path_edit = QLineEdit()
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_script)
        path_layout.addWidget(self.script_path_edit)
        path_layout.addWidget(browse_btn)
        form.addRow("Script Path:", path_layout)
        
        # Command (for system commands)
        self.command_edit = QLineEdit()
        self.command_edit.setPlaceholderText("e.g., echo Hello World")
        form.addRow("Command:", self.command_edit)
        
        # Arguments
        self.args_edit = QLineEdit()
        self.args_edit.setPlaceholderText("e.g., --verbose --output file.txt")
        form.addRow("Arguments:", self.args_edit)
        
        # Working directory
        work_layout = QHBoxLayout()
        self.working_dir_edit = QLineEdit()
        work_browse_btn = QPushButton("Browse...")
        work_browse_btn.clicked.connect(self.browse_working_dir)
        work_layout.addWidget(self.working_dir_edit)
        work_layout.addWidget(work_browse_btn)
        form.addRow("Working Dir:", work_layout)
        
        # Timeout
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 3600)
        self.timeout_spin.setValue(300)
        self.timeout_spin.setSuffix(" seconds")
        form.addRow("Timeout:", self.timeout_spin)
        
        # Capture output
        self.capture_output_check = QCheckBox("Capture stdout/stderr")
        self.capture_output_check.setChecked(True)
        form.addRow("", self.capture_output_check)
        
        layout.addLayout(form)
        layout.addStretch()
        
        return widget
    
    def create_file_tab(self):
        """Create file transfer configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        form = QFormLayout()
        
        # Source
        src_layout = QHBoxLayout()
        self.file_source_edit = QLineEdit()
        src_browse_btn = QPushButton("Browse...")
        src_browse_btn.clicked.connect(self.browse_file_source)
        src_layout.addWidget(self.file_source_edit)
        src_layout.addWidget(src_browse_btn)
        form.addRow("Source:", src_layout)
        
        # Destination
        dst_layout = QHBoxLayout()
        self.file_dest_edit = QLineEdit()
        dst_browse_btn = QPushButton("Browse...")
        dst_browse_btn.clicked.connect(self.browse_file_dest)
        dst_layout.addWidget(self.file_dest_edit)
        dst_layout.addWidget(dst_browse_btn)
        form.addRow("Destination:", dst_layout)
        
        # Operation
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Copy", "Move"])
        form.addRow("Operation:", self.operation_combo)
        
        # Options
        self.overwrite_check = QCheckBox("Overwrite existing files")
        self.overwrite_check.setChecked(True)
        form.addRow("", self.overwrite_check)
        
        self.recursive_check = QCheckBox("Recursive (include subdirectories)")
        self.recursive_check.setChecked(True)
        form.addRow("", self.recursive_check)
        
        self.mirror_check = QCheckBox("Mirror mode (delete extras in destination)")
        form.addRow("", self.mirror_check)
        
        # File patterns
        self.file_patterns_edit = QLineEdit()
        self.file_patterns_edit.setPlaceholderText("e.g., *.txt, *.pdf, *.docx")
        form.addRow("Include Patterns:", self.file_patterns_edit)
        
        self.exclude_patterns_edit = QLineEdit()
        self.exclude_patterns_edit.setPlaceholderText("e.g., *.tmp, *.log")
        form.addRow("Exclude Patterns:", self.exclude_patterns_edit)
        
        layout.addLayout(form)
        layout.addStretch()
        
        return widget
    
    def create_git_tab(self):
        """Create Git sync configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        form = QFormLayout()
        
        # Repository path
        repo_layout = QHBoxLayout()
        self.git_repo_edit = QLineEdit()
        repo_browse_btn = QPushButton("Browse...")
        repo_browse_btn.clicked.connect(self.browse_git_repo)
        repo_layout.addWidget(self.git_repo_edit)
        repo_layout.addWidget(repo_browse_btn)
        form.addRow("Repository:", repo_layout)
        
        # Options
        self.git_auto_add_check = QCheckBox("Automatically stage all changes")
        self.git_auto_add_check.setChecked(True)
        form.addRow("", self.git_auto_add_check)
        
        self.git_auto_commit_check = QCheckBox("Automatically commit changes")
        self.git_auto_commit_check.setChecked(True)
        form.addRow("", self.git_auto_commit_check)
        
        self.git_auto_push_check = QCheckBox("Automatically push to remote")
        self.git_auto_push_check.setChecked(True)
        form.addRow("", self.git_auto_push_check)
        
        self.git_smart_msg_check = QCheckBox("Generate smart commit messages")
        self.git_smart_msg_check.setChecked(True)
        form.addRow("", self.git_smart_msg_check)
        
        # Custom commit message
        self.git_commit_msg_edit = QLineEdit()
        self.git_commit_msg_edit.setPlaceholderText("Leave empty for auto-generated message")
        form.addRow("Commit Message:", self.git_commit_msg_edit)
        
        # Remote
        self.git_remote_edit = QLineEdit()
        self.git_remote_edit.setText("origin")
        form.addRow("Remote:", self.git_remote_edit)
        
        # Branch
        self.git_branch_edit = QLineEdit()
        self.git_branch_edit.setPlaceholderText("Leave empty for current branch")
        form.addRow("Branch:", self.git_branch_edit)
        
        layout.addLayout(form)
        layout.addStretch()
        
        return widget
    
    def create_sql_tab(self):
        """Create SQL database configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        form = QFormLayout()
        
        # Operation
        self.sql_operation_combo = QComboBox()
        self.sql_operation_combo.addItems(["Import", "Export"])
        form.addRow("Operation:", self.sql_operation_combo)
        
        # MySQL binary
        mysql_layout = QHBoxLayout()
        self.mysql_bin_edit = QLineEdit()
        self.mysql_bin_edit.setText("C:\\xampp\\mysql\\bin\\mysql.exe")
        mysql_browse_btn = QPushButton("Browse...")
        mysql_browse_btn.clicked.connect(self.browse_mysql)
        mysql_layout.addWidget(self.mysql_bin_edit)
        mysql_layout.addWidget(mysql_browse_btn)
        form.addRow("MySQL Path:", mysql_layout)
        
        # Connection info
        self.sql_user_edit = QLineEdit()
        self.sql_user_edit.setText("root")
        form.addRow("Username:", self.sql_user_edit)
        
        self.sql_pass_edit = QLineEdit()
        self.sql_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Password:", self.sql_pass_edit)
        
        self.sql_host_edit = QLineEdit()
        self.sql_host_edit.setText("localhost")
        form.addRow("Host:", self.sql_host_edit)
        
        self.sql_port_spin = QSpinBox()
        self.sql_port_spin.setRange(1, 65535)
        self.sql_port_spin.setValue(3306)
        form.addRow("Port:", self.sql_port_spin)
        
        # Database name (for export)
        self.sql_database_edit = QLineEdit()
        form.addRow("Database:", self.sql_database_edit)
        
        # SQL file
        sql_file_layout = QHBoxLayout()
        self.sql_file_edit = QLineEdit()
        sql_file_browse = QPushButton("Browse...")
        sql_file_browse.clicked.connect(self.browse_sql_file)
        sql_file_layout.addWidget(self.sql_file_edit)
        sql_file_layout.addWidget(sql_file_browse)
        form.addRow("SQL File:", sql_file_layout)
        
        # SQL directory (for batch import)
        sql_dir_layout = QHBoxLayout()
        self.sql_dir_edit = QLineEdit()
        sql_dir_browse = QPushButton("Browse...")
        sql_dir_browse.clicked.connect(self.browse_sql_dir)
        sql_dir_layout.addWidget(self.sql_dir_edit)
        sql_dir_layout.addWidget(sql_dir_browse)
        form.addRow("SQL Directory:", sql_dir_layout)
        
        # Options
        self.sql_create_db_check = QCheckBox("Create database if not exists")
        self.sql_create_db_check.setChecked(True)
        form.addRow("", self.sql_create_db_check)
        
        self.sql_drop_check = QCheckBox("Drop existing database before import")
        self.sql_drop_check.setChecked(True)
        form.addRow("", self.sql_drop_check)
        
        layout.addLayout(form)
        layout.addStretch()
        
        return widget
    
    def on_type_changed(self, index):
        """Handle task type change"""
        self.tabs.setCurrentIndex(index)
    
    def browse_script(self):
        """Browse for script file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Script",
            "", "All Files (*.*)"
        )
        if file_path:
            self.script_path_edit.setText(file_path)
    
    def browse_working_dir(self):
        """Browse for working directory"""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Working Directory")
        if dir_path:
            self.working_dir_edit.setText(dir_path)
    
    def browse_file_source(self):
        """Browse for file source"""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if dir_path:
            self.file_source_edit.setText(dir_path)
    
    def browse_file_dest(self):
        """Browse for file destination"""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if dir_path:
            self.file_dest_edit.setText(dir_path)
    
    def browse_git_repo(self):
        """Browse for Git repository"""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Git Repository")
        if dir_path:
            self.git_repo_edit.setText(dir_path)
    
    def browse_mysql(self):
        """Browse for MySQL executable"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select MySQL Executable",
            "", "Executable Files (*.exe);;All Files (*.*)"
        )
        if file_path:
            self.mysql_bin_edit.setText(file_path)
    
    def browse_sql_file(self):
        """Browse for SQL file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select SQL File",
            "", "SQL Files (*.sql);;All Files (*.*)"
        )
        if file_path:
            self.sql_file_edit.setText(file_path)
    
    def browse_sql_dir(self):
        """Browse for SQL directory"""
        dir_path = QFileDialog.getExistingDirectory(self, "Select SQL Directory")
        if dir_path:
            self.sql_dir_edit.setText(dir_path)
    
    def load_task_data(self):
        """Load task data for editing"""
        if not self.task:
            return
        
        self.name_edit.setText(self.task.name)
        
        # Set task type
        type_map = {
            "script": 0,
            "file_transfer": 1,
            "git": 2,
            "sql": 3
        }
        self.type_combo.setCurrentIndex(type_map.get(self.task.task_type, 0))
        
        # Load configuration based on type
        config = self.task.config
        
        if self.task.task_type == "script":
            self.script_path_edit.setText(config.get("script_path", ""))
            self.command_edit.setText(config.get("command", ""))
            self.working_dir_edit.setText(config.get("working_dir", ""))
            self.timeout_spin.setValue(config.get("timeout", 300))
            
        elif self.task.task_type == "file_transfer":
            self.file_source_edit.setText(config.get("source", ""))
            self.file_dest_edit.setText(config.get("destination", ""))
            self.overwrite_check.setChecked(config.get("overwrite", True))
            self.mirror_check.setChecked(config.get("mirror", False))
            
        elif self.task.task_type == "git":
            self.git_repo_edit.setText(config.get("repo_path", ""))
            self.git_auto_add_check.setChecked(config.get("auto_add", True))
            self.git_auto_commit_check.setChecked(config.get("auto_commit", True))
            self.git_auto_push_check.setChecked(config.get("auto_push", True))
            
        elif self.task.task_type == "sql":
            self.mysql_bin_edit.setText(config.get("mysql_bin", ""))
            self.sql_user_edit.setText(config.get("user", "root"))
            self.sql_database_edit.setText(config.get("database", ""))
    
    def save_task(self):
        """Save task configuration"""
        task_name = self.name_edit.text().strip()
        if not task_name:
            QMessageBox.warning(self, "Error", "Please enter a task name")
            return
        
        task_type_index = self.type_combo.currentIndex()
        
        # Build configuration based on type
        if task_type_index == 0:  # Script
            script_type_map = {0: "python", 1: "batch", 2: "command"}
            config = {
                "script_type": script_type_map[self.script_type_combo.currentIndex()],
                "script_path": self.script_path_edit.text(),
                "command": self.command_edit.text(),
                "arguments": self.args_edit.text().split() if self.args_edit.text() else [],
                "working_dir": self.working_dir_edit.text(),
                "timeout": self.timeout_spin.value(),
                "capture_output": self.capture_output_check.isChecked()
            }
            self.task_config = ("script", task_name, config)
            
        elif task_type_index == 1:  # File Transfer
            patterns = [p.strip() for p in self.file_patterns_edit.text().split(",") if p.strip()]
            exclude = [p.strip() for p in self.exclude_patterns_edit.text().split(",") if p.strip()]
            
            config = {
                "source": self.file_source_edit.text(),
                "destination": self.file_dest_edit.text(),
                "operation": self.operation_combo.currentText().lower(),
                "overwrite": self.overwrite_check.isChecked(),
                "recursive": self.recursive_check.isChecked(),
                "mirror": self.mirror_check.isChecked(),
                "file_patterns": patterns,
                "exclude_patterns": exclude
            }
            self.task_config = ("file_transfer", task_name, config)
            
        elif task_type_index == 2:  # Git
            config = {
                "repo_path": self.git_repo_edit.text(),
                "auto_add": self.git_auto_add_check.isChecked(),
                "auto_commit": self.git_auto_commit_check.isChecked(),
                "auto_push": self.git_auto_push_check.isChecked(),
                "smart_message": self.git_smart_msg_check.isChecked(),
                "commit_message": self.git_commit_msg_edit.text(),
                "remote": self.git_remote_edit.text() or "origin",
                "branch": self.git_branch_edit.text()
            }
            self.task_config = ("git", task_name, config)
            
        elif task_type_index == 3:  # SQL
            config = {
                "operation": self.sql_operation_combo.currentText().lower(),
                "mysql_bin": self.mysql_bin_edit.text(),
                "user": self.sql_user_edit.text(),
                "password": self.sql_pass_edit.text(),
                "host": self.sql_host_edit.text(),
                "port": self.sql_port_spin.value(),
                "database": self.sql_database_edit.text(),
                "sql_file": self.sql_file_edit.text(),
                "sql_directory": self.sql_dir_edit.text(),
                "create_database": self.sql_create_db_check.isChecked(),
                "drop_existing": self.sql_drop_check.isChecked()
            }
            self.task_config = ("sql", task_name, config)
        
        self.accept()
    
    def get_task_config(self):
        """Get the configured task"""
        return self.task_config
