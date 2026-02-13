"""
Base Task Class
All task types inherit from this base class
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any, Callable
from datetime import datetime
import threading
import uuid


class TaskStatus(Enum):
    """Task execution status"""
    IDLE = "Idle"
    RUNNING = "Running"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    FAILED = "Failed"
    STOPPED = "Stopped"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class BaseTask(ABC):
    """
    Abstract base class for all task types
    
    All tasks must implement:
    - _execute(): Core execution logic
    - validate(): Validate task configuration
    """
    
    def __init__(self, name: str, task_type: str, config: Dict[str, Any]):
        """
        Initialize base task
        
        Args:
            name: Human-readable task name
            task_type: Task type identifier (script, file_transfer, git, sql, etc.)
            config: Task-specific configuration dictionary
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.task_type = task_type
        self.config = config
        
        # Status tracking
        self.status = TaskStatus.IDLE
        self.progress = 0.0
        self.error_message: Optional[str] = None
        
        # Timing
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        
        # Control
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        
        # Callbacks for GUI updates
        self.on_status_change: Optional[Callable] = None
        self.on_progress_update: Optional[Callable] = None
        self.on_log_message: Optional[Callable] = None
        
        # Priority
        self.priority = TaskPriority.NORMAL
        
        # Statistics
        self.run_count = 0
        self.success_count = 0
        self.fail_count = 0
    
    @abstractmethod
    def _execute(self) -> bool:
        """
        Execute the task logic (must be implemented by subclasses)
        
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate task configuration
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    def start(self):
        """Start task execution in a separate thread"""
        if self.status == TaskStatus.RUNNING:
            self.log("Task already running", "WARNING")
            return
        
        if self.status == TaskStatus.PAUSED:
            self.resume()
            return
        
        # Validate before starting
        is_valid, error_msg = self.validate()
        if not is_valid:
            self.log(f"Validation failed: {error_msg}", "ERROR")
            self.set_status(TaskStatus.FAILED)
            self.error_message = error_msg
            return
        
        # Reset control events
        self._stop_event.clear()
        self._pause_event.clear()
        
        # Start execution thread
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def _run(self):
        """Internal run method (executes in thread)"""
        try:
            self.set_status(TaskStatus.RUNNING)
            self.started_at = datetime.now()
            self.last_run = datetime.now()
            self.run_count += 1
            self.error_message = None
            
            self.log(f"Task started: {self.name}", "INFO")
            
            # Execute task
            success = self._execute()
            
            # Check if stopped during execution
            if self._stop_event.is_set():
                self.set_status(TaskStatus.STOPPED)
                self.log("Task stopped by user", "WARNING")
            elif success:
                self.set_status(TaskStatus.COMPLETED)
                self.completed_at = datetime.now()
                self.success_count += 1
                self.progress = 100.0
                self.update_progress(100.0)
                self.log("Task completed successfully", "SUCCESS")
            else:
                self.set_status(TaskStatus.FAILED)
                self.fail_count += 1
                self.log("Task failed", "ERROR")
                
        except Exception as e:
            self.set_status(TaskStatus.FAILED)
            self.fail_count += 1
            self.error_message = str(e)
            self.log(f"Task error: {e}", "ERROR")
    
    def pause(self):
        """Pause task execution"""
        if self.status == TaskStatus.RUNNING:
            self._pause_event.set()
            self.set_status(TaskStatus.PAUSED)
            self.log("Task paused", "INFO")
    
    def resume(self):
        """Resume paused task"""
        if self.status == TaskStatus.PAUSED:
            self._pause_event.clear()
            self.set_status(TaskStatus.RUNNING)
            self.log("Task resumed", "INFO")
    
    def stop(self):
        """Stop task execution"""
        self._stop_event.set()
        self._pause_event.clear()
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
        
        self.set_status(TaskStatus.STOPPED)
        self.log("Task stopped", "WARNING")
    
    def reset(self):
        """Reset task to initial state"""
        if self.status == TaskStatus.RUNNING:
            self.log("Cannot reset running task", "WARNING")
            return
        
        self.status = TaskStatus.IDLE
        self.progress = 0.0
        self.error_message = None
        self.started_at = None
        self.completed_at = None
        
        self.log("Task reset", "INFO")
    
    def is_stopped(self) -> bool:
        """Check if stop was requested"""
        return self._stop_event.is_set()
    
    def is_paused(self) -> bool:
        """Check if task is paused"""
        return self._pause_event.is_set()
    
    def wait_if_paused(self):
        """Wait while task is paused"""
        while self.is_paused() and not self.is_stopped():
            threading.Event().wait(0.1)
    
    def set_status(self, status: TaskStatus):
        """Update task status and notify GUI"""
        self.status = status
        if self.on_status_change:
            self.on_status_change(self)
    
    def update_progress(self, progress: float):
        """Update task progress (0-100)"""
        self.progress = max(0.0, min(100.0, progress))
        if self.on_progress_update:
            self.on_progress_update(self, self.progress)
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message"""
        if self.on_log_message:
            self.on_log_message(self.name, message, level)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize task to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.task_type,
            "status": self.status.value,
            "progress": self.progress,
            "config": self.config,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "run_count": self.run_count,
            "success_count": self.success_count,
            "fail_count": self.fail_count,
            "priority": self.priority.value
        }
    
    def get_status_text(self) -> str:
        """Get formatted status text"""
        return self.status.value
    
    def get_progress_text(self) -> str:
        """Get formatted progress text"""
        if self.progress > 0:
            return f"{self.progress:.1f}%"
        return "-"
    
    def get_next_run_text(self) -> str:
        """Get formatted next run time"""
        if self.next_run:
            return self.next_run.strftime("%Y-%m-%d %H:%M:%S")
        return "-"
