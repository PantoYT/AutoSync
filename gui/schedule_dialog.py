"""
Schedule Dialog
Configure task scheduling options
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QComboBox, QSpinBox, QTimeEdit,
    QLabel, QCheckBox, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, QTime

from utils.scheduler import ScheduleType


class ScheduleDialog(QDialog):
    """Dialog for scheduling tasks"""
    
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        
        self.task = task
        self.schedule_config = None
        
        self.setWindowTitle(f"Schedule Task: {task.name if task else 'Task'}")
        self.setMinimumSize(450, 400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        
        # Schedule type selection
        type_group = QGroupBox("Schedule Type")
        type_layout = QVBoxLayout(type_group)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Run Immediately (Once)",
            "Interval (Repeat Every...)",
            "Daily (Every Day at...)",
            "Weekly (Specific Day)",
            "On Startup (Auto-run)"
        ])
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        type_layout.addWidget(self.type_combo)
        
        layout.addWidget(type_group)
        
        # Configuration panels
        self.config_group = QGroupBox("Configuration")
        self.config_layout = QVBoxLayout(self.config_group)
        
        # Interval panel
        self.interval_panel = self.create_interval_panel()
        self.config_layout.addWidget(self.interval_panel)
        
        # Daily panel
        self.daily_panel = self.create_daily_panel()
        self.config_layout.addWidget(self.daily_panel)
        
        # Weekly panel
        self.weekly_panel = self.create_weekly_panel()
        self.config_layout.addWidget(self.weekly_panel)
        
        # Startup panel
        self.startup_panel = self.create_startup_panel()
        self.config_layout.addWidget(self.startup_panel)
        
        layout.addWidget(self.config_group)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)
        
        self.enabled_check = QCheckBox("Schedule enabled")
        self.enabled_check.setChecked(True)
        options_layout.addWidget(self.enabled_check)
        
        self.run_once_check = QCheckBox("Run immediately, then start schedule")
        options_layout.addWidget(self.run_once_check)
        
        layout.addWidget(options_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Schedule")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_schedule)
        
        remove_btn = QPushButton("Remove Schedule")
        remove_btn.setObjectName("dangerButton")
        remove_btn.clicked.connect(self.remove_schedule)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(remove_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        # Show appropriate panel
        self.on_type_changed(0)
    
    def create_interval_panel(self):
        """Create interval configuration panel"""
        panel = QGroupBox("Interval Settings")
        layout = QFormLayout(panel)
        
        # Hours
        self.interval_hours = QSpinBox()
        self.interval_hours.setRange(0, 23)
        self.interval_hours.setValue(0)
        layout.addRow("Hours:", self.interval_hours)
        
        # Minutes
        self.interval_minutes = QSpinBox()
        self.interval_minutes.setRange(0, 59)
        self.interval_minutes.setValue(30)
        layout.addRow("Minutes:", self.interval_minutes)
        
        # Seconds
        self.interval_seconds = QSpinBox()
        self.interval_seconds.setRange(0, 59)
        self.interval_seconds.setValue(0)
        layout.addRow("Seconds:", self.interval_seconds)
        
        info = QLabel("Task will run repeatedly at this interval")
        info.setStyleSheet("color: gray; font-size: 9pt;")
        layout.addRow("", info)
        
        return panel
    
    def create_daily_panel(self):
        """Create daily configuration panel"""
        panel = QGroupBox("Daily Settings")
        layout = QFormLayout(panel)
        
        self.daily_time = QTimeEdit()
        self.daily_time.setTime(QTime(9, 0))
        self.daily_time.setDisplayFormat("HH:mm")
        layout.addRow("Time:", self.daily_time)
        
        info = QLabel("Task will run every day at this time")
        info.setStyleSheet("color: gray; font-size: 9pt;")
        layout.addRow("", info)
        
        return panel
    
    def create_weekly_panel(self):
        """Create weekly configuration panel"""
        panel = QGroupBox("Weekly Settings")
        layout = QFormLayout(panel)
        
        self.weekly_day = QComboBox()
        self.weekly_day.addItems([
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ])
        layout.addRow("Day:", self.weekly_day)
        
        self.weekly_time = QTimeEdit()
        self.weekly_time.setTime(QTime(9, 0))
        self.weekly_time.setDisplayFormat("HH:mm")
        layout.addRow("Time:", self.weekly_time)
        
        info = QLabel("Task will run every week on this day")
        info.setStyleSheet("color: gray; font-size: 9pt;")
        layout.addRow("", info)
        
        return panel
    
    def create_startup_panel(self):
        """Create startup configuration panel"""
        panel = QGroupBox("Startup Settings")
        layout = QVBoxLayout(panel)
        
        info = QLabel(
            "Task will run automatically when the application starts.\n\n"
            "Useful for tasks that should always run, like file monitoring "
            "or periodic backups."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: gray;")
        layout.addWidget(info)
        
        self.startup_delay = QSpinBox()
        self.startup_delay.setRange(0, 300)
        self.startup_delay.setValue(5)
        self.startup_delay.setSuffix(" seconds")
        
        delay_layout = QFormLayout()
        delay_layout.addRow("Delay after startup:", self.startup_delay)
        layout.addLayout(delay_layout)
        
        return panel
    
    def on_type_changed(self, index):
        """Handle schedule type change"""
        # Hide all panels
        self.interval_panel.hide()
        self.daily_panel.hide()
        self.weekly_panel.hide()
        self.startup_panel.hide()
        
        # Show selected panel
        if index == 0:  # Immediate
            pass
        elif index == 1:  # Interval
            self.interval_panel.show()
        elif index == 2:  # Daily
            self.daily_panel.show()
        elif index == 3:  # Weekly
            self.weekly_panel.show()
        elif index == 4:  # Startup
            self.startup_panel.show()
    
    def save_schedule(self):
        """Save schedule configuration"""
        schedule_type_index = self.type_combo.currentIndex()
        
        # Build configuration based on type
        if schedule_type_index == 0:  # Immediate
            self.schedule_config = {
                'type': ScheduleType.IMMEDIATE,
                'config': {},
                'enabled': self.enabled_check.isChecked(),
                'run_once': True
            }
        
        elif schedule_type_index == 1:  # Interval
            hours = self.interval_hours.value()
            minutes = self.interval_minutes.value()
            seconds = self.interval_seconds.value()
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if total_seconds == 0:
                QMessageBox.warning(
                    self,
                    "Invalid Interval",
                    "Please set an interval greater than 0"
                )
                return
            
            self.schedule_config = {
                'type': ScheduleType.INTERVAL,
                'config': {
                    'hours': hours,
                    'minutes': minutes,
                    'seconds': seconds
                },
                'enabled': self.enabled_check.isChecked(),
                'run_once': self.run_once_check.isChecked()
            }
        
        elif schedule_type_index == 2:  # Daily
            time = self.daily_time.time()
            time_str = time.toString("HH:mm")
            
            self.schedule_config = {
                'type': ScheduleType.DAILY,
                'config': {
                    'time': time_str
                },
                'enabled': self.enabled_check.isChecked(),
                'run_once': self.run_once_check.isChecked()
            }
        
        elif schedule_type_index == 3:  # Weekly
            day = self.weekly_day.currentIndex()
            time = self.weekly_time.time()
            time_str = time.toString("HH:mm")
            
            self.schedule_config = {
                'type': ScheduleType.WEEKLY,
                'config': {
                    'day': day,
                    'time': time_str
                },
                'enabled': self.enabled_check.isChecked(),
                'run_once': self.run_once_check.isChecked()
            }
        
        elif schedule_type_index == 4:  # Startup
            delay = self.startup_delay.value()
            
            self.schedule_config = {
                'type': 'startup',
                'config': {
                    'delay': delay
                },
                'enabled': self.enabled_check.isChecked(),
                'run_once': False
            }
        
        self.accept()
    
    def remove_schedule(self):
        """Remove task schedule"""
        reply = QMessageBox.question(
            self,
            "Remove Schedule",
            "Are you sure you want to remove the schedule for this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.schedule_config = None
            self.accept()
    
    def get_schedule_config(self):
        """Get the schedule configuration"""
        return self.schedule_config
