"""
Configuration Manager
Load/save application and task configurations in JSON format
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class ConfigManager:
    """Manage application configuration"""
    
    def __init__(self, config_dir: str = "configs"):
        """
        Initialize config manager
        
        Args:
            config_dir: Directory for configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.default_config_file = self.config_dir / "default_config.json"
        self.user_config_file = self.config_dir / "user_config.json"
        
        # Current loaded configuration
        self.config: Dict[str, Any] = {}
        
        # Initialize default config if it doesn't exist
        if not self.default_config_file.exists():
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration file"""
        default_config = {
            "app": {
                "name": "Automation Hub",
                "version": "1.0.0",
                "theme": "dark-blue-yellow",
                "auto_start": False,
                "check_updates": True,
                "log_retention_days": 30
            },
            "paths": {
                "scripts": "",
                "projects": "",
                "databases": "",
                "htdocs": "",
                "xampp": ""
            },
            "git": {
                "default_remote": "origin",
                "default_branch": "main",
                "auto_commit": True,
                "auto_push": True,
                "smart_messages": True
            },
            "mysql": {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "",
                "charset": "utf8mb4"
            },
            "presets": {
                "file_transfers": [],
                "git_repos": [],
                "sql_databases": []
            },
            "tasks": [],
            "ui": {
                "window_geometry": {
                    "width": 1200,
                    "height": 800,
                    "x": 100,
                    "y": 100
                },
                "show_tray_icon": True,
                "minimize_to_tray": True,
                "start_minimized": False
            }
        }
        
        self.save_config(default_config, self.default_config_file)
    
    def load_config(self, config_file: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Args:
            config_file: Config file path (defaults to user_config or default_config)
        
        Returns:
            Configuration dictionary
        """
        if config_file is None:
            # Try user config first, fall back to default
            if self.user_config_file.exists():
                config_file = self.user_config_file
            else:
                config_file = self.default_config_file
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return self.config
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def save_config(self, config: Dict[str, Any], config_file: Optional[Path] = None):
        """
        Save configuration to file
        
        Args:
            config: Configuration dictionary
            config_file: Config file path (defaults to user_config)
        """
        if config_file is None:
            config_file = self.user_config_file
        
        try:
            # Add metadata
            config['_metadata'] = {
                'saved_at': datetime.now().isoformat(),
                'version': config.get('app', {}).get('version', '1.0.0')
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.config = config
            return True
            
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get config value by dot-notation path
        
        Args:
            key_path: Dot-separated path (e.g., 'app.theme')
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set config value by dot-notation path
        
        Args:
            key_path: Dot-separated path (e.g., 'app.theme')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to parent
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set value
        config[keys[-1]] = value
    
    def add_task_config(self, task_config: Dict[str, Any]):
        """Add task configuration"""
        if 'tasks' not in self.config:
            self.config['tasks'] = []
        
        self.config['tasks'].append(task_config)
    
    def remove_task_config(self, task_id: str):
        """Remove task configuration by ID"""
        if 'tasks' in self.config:
            self.config['tasks'] = [
                t for t in self.config['tasks'] if t.get('id') != task_id
            ]
    
    def get_task_configs(self) -> list:
        """Get all task configurations"""
        return self.config.get('tasks', [])
    
    def update_task_config(self, task_id: str, task_config: Dict[str, Any]):
        """Update task configuration"""
        if 'tasks' in self.config:
            for i, task in enumerate(self.config['tasks']):
                if task.get('id') == task_id:
                    self.config['tasks'][i] = task_config
                    break
    
    def add_preset(self, preset_type: str, preset: Dict[str, Any]):
        """
        Add a preset
        
        Args:
            preset_type: Type of preset (file_transfers, git_repos, sql_databases)
            preset: Preset configuration
        """
        if 'presets' not in self.config:
            self.config['presets'] = {}
        
        if preset_type not in self.config['presets']:
            self.config['presets'][preset_type] = []
        
        self.config['presets'][preset_type].append(preset)
    
    def get_presets(self, preset_type: str) -> list:
        """Get presets by type"""
        return self.config.get('presets', {}).get(preset_type, [])
    
    def export_config(self, output_file: str) -> bool:
        """
        Export current configuration to file
        
        Args:
            output_file: Output file path
        
        Returns:
            True if successful
        """
        try:
            output_path = Path(output_file)
            return self.save_config(self.config, output_path)
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, input_file: str) -> bool:
        """
        Import configuration from file
        
        Args:
            input_file: Input file path
        
        Returns:
            True if successful
        """
        try:
            input_path = Path(input_file)
            if not input_path.exists():
                return False
            
            imported_config = self.load_config(input_path)
            if imported_config:
                # Merge with current config
                self.config.update(imported_config)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error importing config: {e}")
            return False


# Global config manager instance
_global_config: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get or create global config manager"""
    global _global_config
    if _global_config is None:
        _global_config = ConfigManager()
    return _global_config


def init_config_manager(config_dir: str = "configs") -> ConfigManager:
    """Initialize global config manager"""
    global _global_config
    _global_config = ConfigManager(config_dir)
    return _global_config
