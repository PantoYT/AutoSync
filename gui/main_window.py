"""
Main Window
Central GUI for the Automation Hub application
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QTextEdit,
    QSplitter, QStatusBar, QMenuBar, QMenu, QToolBar,
    QLabel, QProgressBar, QMessageBox, QFileDialog, QDialog
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction

from utils import get_logger, get_config_manager, get_scheduler
from gui.theme_manager import get_theme_manager
from gui.task_dialog import TaskDialog
from gui.schedule_dialog import ScheduleDialog
from gui.presets_dialog import PresetsDialog
from tasks.script_task import ScriptTask
from tasks.file_transfer_task import FileTransferTask
from tasks.git_task import GitTask
from tasks.sql_task import SQLTask


class MainWindow(QMainWindow):
    """Main application window"""
    
    # Signals
    task_updated = pyqtSignal(object)
    log_added = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        
        self.logger = get_logger()
        self.config = get_config_manager()
        self.scheduler = get_scheduler()
        self.theme_manager = get_theme_manager()
        
        self.tasks = {}
        
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(1000)  # Update every second
    
    def setup_ui(self):
        """Setup user interface"""
        self.setWindowTitle("Automation Hub")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create splitter for task table and log panel
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Task table
        self.task_table = self.create_task_table()
        splitter.addWidget(self.task_table)
        
        # Log panel
        self.log_panel = self.create_log_panel()
        splitter.addWidget(self.log_panel)
        
        splitter.setSizes([500, 300])
        
        main_layout.addWidget(splitter)
        
        # Create status bar
        self.create_status_bar()
        
        # Create menu bar
        self.create_menu_bar()
    
    def create_toolbar(self):
        """Create toolbar with action buttons"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Add Task button
        add_action = QAction("➕ Add Task", self)
        add_action.triggered.connect(self.add_task)
        toolbar.addAction(add_action)
        
        # Preset button
        preset_action = QAction("📋 From Preset", self)
        preset_action.setToolTip("Create task from preset")
        preset_action.triggered.connect(self.add_from_preset)
        toolbar.addAction(preset_action)
        
        toolbar.addSeparator()
        
        # Individual task controls
        start_action = QAction("▶️ Start", self)
        start_action.setToolTip("Start selected task")
        start_action.triggered.connect(self.start_selected_task)
        toolbar.addAction(start_action)
        
        pause_action = QAction("⏸️ Pause", self)
        pause_action.setToolTip("Pause selected task")
        pause_action.triggered.connect(self.pause_selected_task)
        toolbar.addAction(pause_action)
        
        stop_action = QAction("⏹️ Stop", self)
        stop_action.setToolTip("Stop selected task")
        stop_action.triggered.connect(self.stop_selected_task)
        toolbar.addAction(stop_action)
        
        toolbar.addSeparator()
        
        # Batch controls
        start_all_action = QAction("▶️▶️ Start All", self)
        start_all_action.setToolTip("Start all idle tasks")
        start_all_action.triggered.connect(self.start_all_tasks)
        toolbar.addAction(start_all_action)
        
        stop_all_action = QAction("⏹️⏹️ Stop All", self)
        stop_all_action.setToolTip("Stop all running tasks")
        stop_all_action.triggered.connect(self.stop_all_tasks)
        toolbar.addAction(stop_all_action)
        
        toolbar.addSeparator()
        
        # Delete button
        delete_action = QAction("🗑️ Delete", self)
        delete_action.setToolTip("Delete selected task")
        delete_action.triggered.connect(self.delete_selected_task)
        toolbar.addAction(delete_action)
    
    def create_task_table(self):
        """Create task table widget"""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Task Name", "Type", "Status", "Progress", "Next Run", "Controls"
        ])
        
        # Set column widths
        table.setColumnWidth(0, 200)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 100)
        table.setColumnWidth(3, 150)
        table.setColumnWidth(4, 150)
        table.setColumnWidth(5, 280)
        
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        return table
    
    def create_log_panel(self):
        """Create log panel widget"""
        log_widget = QTextEdit()
        log_widget.setReadOnly(True)
        log_widget.setMaximumHeight(300)
        
        # Set font to monospace for logs
        from PyQt6.QtGui import QFont
        font = QFont("Consolas", 9)
        log_widget.setFont(font)
        
        return log_widget
    
    def create_status_bar(self):
        """Create status bar"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        self.status_label = QLabel("Ready")
        status_bar.addWidget(self.status_label)
        
        status_bar.addPermanentWidget(QLabel("Tasks: 0"))
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        import_action = QAction("Import Config", self)
        import_action.triggered.connect(self.import_config)
        file_menu.addAction(import_action)
        
        export_action = QAction("Export Config", self)
        export_action.triggered.connect(self.export_config)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        clear_logs_action = QAction("Clear Logs", self)
        clear_logs_action.triggered.connect(self.clear_logs)
        tools_menu.addAction(clear_logs_action)
        
        export_logs_action = QAction("Export Logs", self)
        export_logs_action.triggered.connect(self.export_logs)
        tools_menu.addAction(export_logs_action)
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        
        theme_menu = settings_menu.addMenu("Theme")
        
        for theme_name in self.theme_manager.get_available_themes():
            theme_action = QAction(theme_name, self)
            theme_action.triggered.connect(lambda checked, t=theme_name: self.change_theme(t))
            theme_menu.addAction(theme_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.logger.on_log_added = self.on_log_added
        
        # Connect scheduler to task execution
        self.scheduler.on_task_triggered = self.on_task_triggered
    
    def on_task_triggered(self, task_id):
        """Handle scheduler triggering a task"""
        task = self.tasks.get(task_id)
        if task:
            self.logger.log("Scheduler", f"Triggering scheduled task: {task.name}", "INFO")
            task.start()
            
            # Update next run time
            next_run = self.scheduler.get_next_run(task_id)
            if next_run:
                task.next_run = next_run
                self.update_task_next_run(task_id, next_run)
    
    def apply_theme(self):
        """Apply current theme"""
        theme_name = self.config.get('app.theme', 'dark-blue-yellow')
        stylesheet = self.theme_manager.get_stylesheet(theme_name)
        self.setStyleSheet(stylesheet)
    
    def add_task(self):
        """Add a new task"""
        dialog = TaskDialog(self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_config = dialog.get_task_config()
            if task_config:
                task_type, task_name, config = task_config
                
                # Create task instance
                task = self.create_task_instance(task_type, task_name, config)
                
                if task:
                    # Add to tasks dictionary
                    self.tasks[task.id] = task
                    
                    # Setup callbacks
                    task.on_status_change = self.on_task_status_changed
                    task.on_progress_update = self.on_task_progress_updated
                    task.on_log_message = self.logger.log
                    
                    # Add to table
                    self.add_task_to_table(task)
                    
                    # Save to config
                    self.config.add_task_config(task.to_dict())
                    
                    self.logger.log("GUI", f"Task created: {task_name}", "SUCCESS")
    
    def add_from_preset(self):
        """Create task from preset"""
        dialog = PresetsDialog(self, self.config)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            preset_data = dialog.get_selected_preset()
            
            if preset_data:
                preset_name, preset = preset_data
                
                # Create task from preset
                task_name = preset_name
                task_type = preset['type']
                config = preset['config'].copy()
                
                # Create task instance
                task = self.create_task_instance(task_type, task_name, config)
                
                if task:
                    # Add to tasks dictionary
                    self.tasks[task.id] = task
                    
                    # Setup callbacks
                    task.on_status_change = self.on_task_status_changed
                    task.on_progress_update = self.on_task_progress_updated
                    task.on_log_message = self.logger.log
                    
                    # Add to table
                    self.add_task_to_table(task)
                    
                    # Save to config
                    self.config.add_task_config(task.to_dict())
                    
                    self.logger.log("GUI", f"Task created from preset: {task_name}", "SUCCESS")
    
    def create_task_instance(self, task_type, task_name, config):
        """Create task instance based on type"""
        try:
            if task_type == "script":
                return ScriptTask(task_name, config)
            elif task_type == "file_transfer":
                return FileTransferTask(task_name, config)
            elif task_type == "git":
                return GitTask(task_name, config)
            elif task_type == "sql":
                return SQLTask(task_name, config)
            else:
                self.logger.log("GUI", f"Unknown task type: {task_type}", "ERROR")
                return None
        except Exception as e:
            self.logger.log("GUI", f"Error creating task: {e}", "ERROR")
            QMessageBox.critical(self, "Error", f"Failed to create task: {e}")
            return None
    
    def add_task_to_table(self, task):
        """Add task to the table"""
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)
        
        # Task name
        self.task_table.setItem(row, 0, QTableWidgetItem(task.name))
        
        # Task type
        type_names = {
            "script": "Script",
            "file_transfer": "File Transfer",
            "git": "Git Sync",
            "sql": "SQL Database"
        }
        self.task_table.setItem(row, 1, QTableWidgetItem(type_names.get(task.task_type, task.task_type)))
        
        # Status
        self.task_table.setItem(row, 2, QTableWidgetItem(task.status.value))
        
        # Progress bar
        progress_widget = QWidget()
        progress_layout = QHBoxLayout(progress_widget)
        progress_layout.setContentsMargins(4, 4, 4, 4)
        
        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setMaximum(100)
        progress_layout.addWidget(progress_bar)
        
        self.task_table.setCellWidget(row, 3, progress_widget)
        
        # Next run
        self.task_table.setItem(row, 4, QTableWidgetItem("-"))
        
        # Control buttons
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        control_layout.setContentsMargins(2, 2, 2, 2)
        control_layout.setSpacing(2)
        
        # Start button
        start_btn = QPushButton("▶")
        start_btn.setToolTip("Start task")
        start_btn.setFixedSize(30, 30)
        start_btn.setObjectName("successButton")
        start_btn.clicked.connect(lambda: self.start_task_by_id(task.id))
        control_layout.addWidget(start_btn)
        
        # Pause button
        pause_btn = QPushButton("⏸")
        pause_btn.setToolTip("Pause task")
        pause_btn.setFixedSize(30, 30)
        pause_btn.setObjectName("warningButton")
        pause_btn.clicked.connect(lambda: self.pause_task_by_id(task.id))
        control_layout.addWidget(pause_btn)
        
        # Stop button
        stop_btn = QPushButton("⏹")
        stop_btn.setToolTip("Stop task")
        stop_btn.setFixedSize(30, 30)
        stop_btn.setObjectName("dangerButton")
        stop_btn.clicked.connect(lambda: self.stop_task_by_id(task.id))
        control_layout.addWidget(stop_btn)
        
        # Reset button
        reset_btn = QPushButton("↻")
        reset_btn.setToolTip("Reset task")
        reset_btn.setFixedSize(30, 30)
        reset_btn.clicked.connect(lambda: self.reset_task_by_id(task.id))
        control_layout.addWidget(reset_btn)
        
        # Schedule button
        schedule_btn = QPushButton("⏰")
        schedule_btn.setToolTip("Schedule task")
        schedule_btn.setFixedSize(30, 30)
        schedule_btn.clicked.connect(lambda: self.schedule_task_by_id(task.id))
        control_layout.addWidget(schedule_btn)
        
        # Delete button
        delete_btn = QPushButton("🗑")
        delete_btn.setToolTip("Delete task")
        delete_btn.setFixedSize(30, 30)
        delete_btn.setObjectName("dangerButton")
        delete_btn.clicked.connect(lambda: self.delete_task_by_id(task.id))
        control_layout.addWidget(delete_btn)
        
        control_layout.addStretch()
        
        self.task_table.setCellWidget(row, 5, control_widget)
        
        # Store task ID in the first column item
        self.task_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, task.id)
    
    def start_task_by_id(self, task_id):
        """Start task by ID"""
        task = self.tasks.get(task_id)
        if task:
            task.start()
            self.logger.log("GUI", f"Starting task: {task.name}", "INFO")
    
    def pause_task_by_id(self, task_id):
        """Pause task by ID"""
        task = self.tasks.get(task_id)
        if task:
            task.pause()
            self.logger.log("GUI", f"Pausing task: {task.name}", "INFO")
    
    def stop_task_by_id(self, task_id):
        """Stop task by ID"""
        task = self.tasks.get(task_id)
        if task:
            task.stop()
            self.logger.log("GUI", f"Stopping task: {task.name}", "INFO")
    
    def reset_task_by_id(self, task_id):
        """Reset task by ID"""
        task = self.tasks.get(task_id)
        if task:
            task.reset()
            self.logger.log("GUI", f"Resetting task: {task.name}", "INFO")
    
    def schedule_task_by_id(self, task_id):
        """Schedule task by ID"""
        task = self.tasks.get(task_id)
        if not task:
            return
        
        dialog = ScheduleDialog(self, task)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            schedule_config = dialog.get_schedule_config()
            
            if schedule_config is None:
                # Remove schedule
                self.scheduler.remove_schedule(task_id)
                task.next_run = None
                self.logger.log("GUI", f"Schedule removed for task: {task.name}", "INFO")
            else:
                # Add/update schedule
                self.scheduler.add_schedule(
                    task_id,
                    schedule_config['type'],
                    schedule_config['config']
                )
                
                # Run immediately if requested
                if schedule_config.get('run_once', False):
                    task.start()
                
                # Update next run time
                next_run = self.scheduler.get_next_run(task_id)
                task.next_run = next_run
                
                # Update table
                self.update_task_next_run(task_id, next_run)
                
                schedule_type_names = {
                    'immediate': 'Immediate',
                    'interval': 'Interval',
                    'daily': 'Daily',
                    'weekly': 'Weekly',
                    'startup': 'On Startup'
                }
                
                type_name = schedule_type_names.get(
                    schedule_config['type'].value if hasattr(schedule_config['type'], 'value') else schedule_config['type'],
                    'Scheduled'
                )
                
                self.logger.log("GUI", f"Task scheduled: {task.name} ({type_name})", "SUCCESS")
    
    def update_task_next_run(self, task_id, next_run):
        """Update next run time in table"""
        for row in range(self.task_table.rowCount()):
            item = self.task_table.item(row, 0)
            if item and item.data(Qt.ItemDataRole.UserRole) == task_id:
                if next_run:
                    next_run_text = next_run.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    next_run_text = "-"
                self.task_table.setItem(row, 4, QTableWidgetItem(next_run_text))
                break
    
    def edit_task_by_id(self, task_id):
        """Edit task by ID"""
        task = self.tasks.get(task_id)
        if task:
            QMessageBox.information(
                self,
                "Edit Task",
                f"Task editing for '{task.name}' will be implemented.\n"
                "You can delete and recreate the task for now."
            )
    
    def delete_task_by_id(self, task_id):
        """Delete task by ID"""
        task = self.tasks.get(task_id)
        if not task:
            return
        
        reply = QMessageBox.question(
            self,
            "Delete Task",
            f"Are you sure you want to delete task '{task.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Stop task if running
            if task.status.value == "Running":
                task.stop()
            
            # Find and remove from table
            for row in range(self.task_table.rowCount()):
                item = self.task_table.item(row, 0)
                if item and item.data(Qt.ItemDataRole.UserRole) == task_id:
                    self.task_table.removeRow(row)
                    break
            
            # Remove from tasks dict
            del self.tasks[task_id]
            
            # Remove from config
            self.config.remove_task_config(task_id)
            
            self.logger.log("GUI", f"Task deleted: {task.name}", "INFO")
    
    def on_task_status_changed(self, task):
        """Handle task status change"""
        # Find task in table and update status
        for row in range(self.task_table.rowCount()):
            item = self.task_table.item(row, 0)
            if item and item.data(Qt.ItemDataRole.UserRole) == task.id:
                self.task_table.setItem(row, 2, QTableWidgetItem(task.status.value))
                break
    
    def on_task_progress_updated(self, task, progress):
        """Handle task progress update"""
        # Find task in table and update progress bar
        for row in range(self.task_table.rowCount()):
            item = self.task_table.item(row, 0)
            if item and item.data(Qt.ItemDataRole.UserRole) == task.id:
                widget = self.task_table.cellWidget(row, 3)
                if widget:
                    progress_bar = widget.findChild(QProgressBar)
                    if progress_bar:
                        progress_bar.setValue(int(progress))
                break
    
    def start_selected_task(self):
        """Start the selected task"""
        selected_rows = self.task_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        item = self.task_table.item(row, 0)
        if item:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            self.start_task_by_id(task_id)
    
    def pause_selected_task(self):
        """Pause the selected task"""
        selected_rows = self.task_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        item = self.task_table.item(row, 0)
        if item:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            self.pause_task_by_id(task_id)
    
    def stop_selected_task(self):
        """Stop the selected task"""
        selected_rows = self.task_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        item = self.task_table.item(row, 0)
        if item:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            self.stop_task_by_id(task_id)
    
    def start_all_tasks(self):
        """Start all tasks"""
        for task in self.tasks.values():
            if task.status.value == "Idle":
                task.start()
        self.logger.log("GUI", "Starting all idle tasks", "INFO")
    
    def stop_all_tasks(self):
        """Stop all running tasks"""
        for task in self.tasks.values():
            if task.status.value == "Running":
                task.stop()
        self.logger.log("GUI", "Stopping all running tasks", "INFO")
    
    def delete_selected_task(self):
        """Delete the selected task"""
        selected_rows = self.task_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        item = self.task_table.item(row, 0)
        if item:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            self.delete_task_by_id(task_id)
    
    def on_log_added(self, log_entry: dict):
        """Handle new log entry"""
        formatted_log = self.logger.format_log_entry(log_entry)
        
        # Color code by level
        level = log_entry['level']
        if level == "ERROR":
            color = "red"
        elif level == "WARNING":
            color = "orange"
        elif level == "SUCCESS":
            color = "green"
        else:
            color = "white"
        
        self.log_panel.append(f'<span style="color:{color};">{formatted_log}</span>')
        
        # Auto-scroll to bottom
        self.log_panel.verticalScrollBar().setValue(
            self.log_panel.verticalScrollBar().maximum()
        )
    
    def update_ui(self):
        """Update UI elements"""
        # Update status bar
        self.status_label.setText(f"Tasks: {len(self.tasks)}")
    
    def clear_logs(self):
        """Clear log panel"""
        self.log_panel.clear()
        self.logger.clear_memory_logs()
    
    def export_logs(self):
        """Export logs to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Logs",
            "",
            "Text Files (*.txt);;CSV Files (*.csv)"
        )
        
        if filename:
            self.logger.export_logs(filename)
            QMessageBox.information(self, "Success", f"Logs exported to {filename}")
    
    def import_config(self):
        """Import configuration from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import Configuration",
            "",
            "JSON Files (*.json)"
        )
        
        if filename:
            if self.config.import_config(filename):
                QMessageBox.information(self, "Success", "Configuration imported successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to import configuration")
    
    def export_config(self):
        """Export configuration to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Configuration",
            "",
            "JSON Files (*.json)"
        )
        
        if filename:
            if self.config.export_config(filename):
                QMessageBox.information(self, "Success", f"Configuration exported to {filename}")
            else:
                QMessageBox.warning(self, "Error", "Failed to export configuration")
    
    def change_theme(self, theme_name: str):
        """Change application theme"""
        self.theme_manager.set_theme(theme_name)
        self.config.set('app.theme', theme_name)
        self.apply_theme()
        self.logger.log("GUI", f"Theme changed to: {theme_name}", "INFO")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Automation Hub",
            "<h2>Automation Hub</h2>"
            "<p>Version 1.0.0</p>"
            "<p>Professional task automation and scheduling system</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Script execution</li>"
            "<li>File transfer</li>"
            "<li>Git synchronization</li>"
            "<li>SQL database operations</li>"
            "<li>Flexible scheduling</li>"
            "</ul>"
        )
    
    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Save configuration
            self.config.save_config(self.config.config)
            self.logger.log("GUI", "Application closing", "INFO")
            event.accept()
        else:
            event.ignore()
