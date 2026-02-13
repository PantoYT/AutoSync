"""
Presets Manager Dialog
Import and manage task presets
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QLabel, QMessageBox, QFileDialog,
    QGroupBox, QTextEdit
)
from PyQt6.QtCore import Qt
import json
from pathlib import Path


class PresetsDialog(QDialog):
    """Dialog for managing task presets"""
    
    # Built-in preset templates
    BUILT_IN_PRESETS = {
        "USB to Local Sync": {
            "type": "file_transfer",
            "config": {
                "source": "G:\\Pliki\\Technik Programista",
                "destination": "E:\\Pliki\\Projects",
                "operation": "copy",
                "overwrite": True,
                "recursive": True,
                "mirror": False
            },
            "description": "Sync files from USB drive to local projects folder"
        },
        "Auto-commit Projects": {
            "type": "git",
            "config": {
                "repo_path": "E:\\Pliki\\Projects",
                "auto_add": True,
                "auto_commit": True,
                "auto_push": True,
                "smart_message": True,
                "remote": "origin"
            },
            "description": "Automatically commit and push changes in projects folder"
        },
        "Import Databases": {
            "type": "sql",
            "config": {
                "operation": "import",
                "mysql_bin": "E:\\xampp\\mysql\\bin\\mysql.exe",
                "user": "root",
                "password": "",
                "sql_directory": "E:\\Pliki\\Projects\\databases",
                "create_database": True,
                "drop_existing": True
            },
            "description": "Import all SQL files from databases folder"
        },
        "Backup Documents": {
            "type": "file_transfer",
            "config": {
                "source": "C:\\Users\\Documents",
                "destination": "D:\\Backups\\Documents",
                "operation": "copy",
                "overwrite": True,
                "file_patterns": ["*.docx", "*.pdf", "*.xlsx"],
                "mirror": False
            },
            "description": "Backup important documents to external drive"
        },
        "Run Cleanup Script": {
            "type": "script",
            "config": {
                "script_type": "python",
                "script_path": "E:\\Scripts\\cleanup.py",
                "timeout": 300,
                "capture_output": True
            },
            "description": "Run system cleanup script"
        }
    }
    
    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        
        self.config_manager = config_manager
        self.selected_preset = None
        
        self.setWindowTitle("Task Presets")
        self.setMinimumSize(600, 500)
        
        self.setup_ui()
        self.load_presets()
    
    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel(
            "Select a preset to quickly create a pre-configured task.\n"
            "You can customize the preset after creating the task."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Preset list
        list_group = QGroupBox("Available Presets")
        list_layout = QVBoxLayout(list_group)
        
        self.preset_list = QListWidget()
        self.preset_list.currentRowChanged.connect(self.on_preset_selected)
        list_layout.addWidget(self.preset_list)
        
        layout.addWidget(list_group)
        
        # Preset details
        details_group = QGroupBox("Preset Details")
        details_layout = QVBoxLayout(details_group)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(150)
        details_layout.addWidget(self.details_text)
        
        layout.addWidget(details_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        import_btn = QPushButton("Import Preset...")
        import_btn.clicked.connect(self.import_preset_file)
        button_layout.addWidget(import_btn)
        
        export_btn = QPushButton("Export Preset...")
        export_btn.clicked.connect(self.export_preset_file)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()
        
        use_btn = QPushButton("Use Preset")
        use_btn.setObjectName("primaryButton")
        use_btn.clicked.connect(self.use_preset)
        button_layout.addWidget(use_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def load_presets(self):
        """Load available presets"""
        self.preset_list.clear()
        
        # Add built-in presets
        for name in self.BUILT_IN_PRESETS.keys():
            self.preset_list.addItem(f"📋 {name} (Built-in)")
        
        # Add user presets from config
        if self.config_manager:
            user_presets = self.config_manager.get('presets', {})
            for name in user_presets.keys():
                self.preset_list.addItem(f"⭐ {name} (Custom)")
    
    def on_preset_selected(self, row):
        """Handle preset selection"""
        if row < 0:
            self.details_text.clear()
            return
        
        item_text = self.preset_list.item(row).text()
        
        # Extract preset name
        if "(Built-in)" in item_text:
            preset_name = item_text.replace("📋 ", "").replace(" (Built-in)", "")
            preset = self.BUILT_IN_PRESETS.get(preset_name)
        else:
            preset_name = item_text.replace("⭐ ", "").replace(" (Custom)", "")
            user_presets = self.config_manager.get('presets', {})
            preset = user_presets.get(preset_name)
        
        if preset:
            # Display preset details
            details = f"<b>Name:</b> {preset_name}<br><br>"
            details += f"<b>Type:</b> {preset.get('type', 'Unknown')}<br><br>"
            details += f"<b>Description:</b><br>{preset.get('description', 'No description')}<br><br>"
            details += f"<b>Configuration:</b><br>"
            
            config = preset.get('config', {})
            for key, value in config.items():
                details += f"  • {key}: {value}<br>"
            
            self.details_text.setHtml(details)
            self.selected_preset = (preset_name, preset)
        else:
            self.details_text.clear()
            self.selected_preset = None
    
    def use_preset(self):
        """Use the selected preset"""
        if not self.selected_preset:
            QMessageBox.warning(
                self,
                "No Preset Selected",
                "Please select a preset to use"
            )
            return
        
        self.accept()
    
    def import_preset_file(self):
        """Import preset from JSON file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import Preset",
            "",
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    preset_data = json.load(f)
                
                # Validate preset
                if 'name' not in preset_data or 'type' not in preset_data or 'config' not in preset_data:
                    QMessageBox.warning(
                        self,
                        "Invalid Preset",
                        "The preset file is missing required fields (name, type, config)"
                    )
                    return
                
                # Add to user presets
                if self.config_manager:
                    user_presets = self.config_manager.get('presets', {})
                    preset_name = preset_data['name']
                    user_presets[preset_name] = {
                        'type': preset_data['type'],
                        'config': preset_data['config'],
                        'description': preset_data.get('description', '')
                    }
                    self.config_manager.set('presets', user_presets)
                    self.config_manager.save_config(self.config_manager.config)
                
                self.load_presets()
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"Preset '{preset_name}' imported successfully"
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Import Error",
                    f"Failed to import preset: {e}"
                )
    
    def export_preset_file(self):
        """Export selected preset to JSON file"""
        if not self.selected_preset:
            QMessageBox.warning(
                self,
                "No Preset Selected",
                "Please select a preset to export"
            )
            return
        
        preset_name, preset = self.selected_preset
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Preset",
            f"{preset_name}.json",
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if filename:
            try:
                export_data = {
                    'name': preset_name,
                    'type': preset['type'],
                    'config': preset['config'],
                    'description': preset.get('description', '')
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"Preset exported to {filename}"
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to export preset: {e}"
                )
    
    def get_selected_preset(self):
        """Get the selected preset"""
        return self.selected_preset
