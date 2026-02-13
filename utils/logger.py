"""
Centralized Logging System
Handles logging to GUI, console, and file
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable
from collections import deque


class LogLevel:
    """Log level constants"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class CentralLogger:
    """Centralized logging manager"""
    
    def __init__(self, log_dir: str = "logs", max_memory_logs: int = 1000):
        """
        Initialize logger
        
        Args:
            log_dir: Directory for log files
            max_memory_logs: Maximum number of logs to keep in memory
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory log storage (for GUI display)
        self.memory_logs = deque(maxlen=max_memory_logs)
        
        # Callback for GUI updates
        self.on_log_added: Optional[Callable] = None
        
        # Setup file logging
        self.setup_file_logging()
    
    def setup_file_logging(self):
        """Setup file logging"""
        log_file = self.log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Configure root logger
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('AutomationHub')
    
    def log(self, task_name: str, message: str, level: str = LogLevel.INFO):
        """
        Log a message
        
        Args:
            task_name: Name of the task generating the log
            message: Log message
            level: Log level (DEBUG, INFO, WARNING, ERROR, SUCCESS)
        """
        timestamp = datetime.now()
        
        # Create log entry
        log_entry = {
            'timestamp': timestamp,
            'task': task_name,
            'message': message,
            'level': level
        }
        
        # Add to memory
        self.memory_logs.append(log_entry)
        
        # Log to file
        log_text = f"[{task_name}] {message}"
        
        if level == LogLevel.DEBUG:
            self.logger.debug(log_text)
        elif level == LogLevel.INFO:
            self.logger.info(log_text)
        elif level == LogLevel.WARNING:
            self.logger.warning(log_text)
        elif level == LogLevel.ERROR:
            self.logger.error(log_text)
        elif level == LogLevel.SUCCESS:
            self.logger.info(f"✓ {log_text}")
        
        # Notify GUI
        if self.on_log_added:
            self.on_log_added(log_entry)
    
    def get_recent_logs(self, count: int = 100) -> list:
        """Get recent log entries"""
        return list(self.memory_logs)[-count:]
    
    def get_logs_for_task(self, task_name: str, count: int = 100) -> list:
        """Get logs for a specific task"""
        task_logs = [log for log in self.memory_logs if log['task'] == task_name]
        return task_logs[-count:]
    
    def clear_memory_logs(self):
        """Clear in-memory logs"""
        self.memory_logs.clear()
        self.log("System", "Memory logs cleared", LogLevel.INFO)
    
    def format_log_entry(self, log_entry: dict) -> str:
        """Format a log entry for display"""
        timestamp = log_entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        task = log_entry['task']
        level = log_entry['level']
        message = log_entry['message']
        
        return f"[{timestamp}] [{task}] [{level}] {message}"
    
    def export_logs(self, output_file: str, task_name: Optional[str] = None):
        """
        Export logs to file
        
        Args:
            output_file: Output file path
            task_name: Optional task name filter
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if task_name:
                logs = self.get_logs_for_task(task_name)
            else:
                logs = list(self.memory_logs)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"Automation Hub Log Export\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                if task_name:
                    f.write(f"Task Filter: {task_name}\n")
                f.write(f"Total Entries: {len(logs)}\n")
                f.write("=" * 80 + "\n\n")
                
                for log_entry in logs:
                    f.write(self.format_log_entry(log_entry) + "\n")
            
            self.log("System", f"Logs exported to {output_file}", LogLevel.SUCCESS)
            return True
            
        except Exception as e:
            self.log("System", f"Failed to export logs: {e}", LogLevel.ERROR)
            return False


# Global logger instance
_global_logger: Optional[CentralLogger] = None


def get_logger() -> CentralLogger:
    """Get or create global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = CentralLogger()
    return _global_logger


def init_logger(log_dir: str = "logs", max_memory_logs: int = 1000) -> CentralLogger:
    """Initialize global logger"""
    global _global_logger
    _global_logger = CentralLogger(log_dir, max_memory_logs)
    return _global_logger
