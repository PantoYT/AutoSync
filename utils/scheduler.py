"""
Task Scheduler
Handles background task scheduling with various trigger types
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable
from enum import Enum


class ScheduleType(Enum):
    """Task schedule types"""
    IMMEDIATE = "immediate"
    INTERVAL = "interval"
    DAILY = "daily"
    WEEKLY = "weekly"
    CRON = "cron"
    EVENT = "event"


class TaskScheduler:
    """Manage task scheduling and execution"""
    
    def __init__(self):
        """Initialize scheduler"""
        self.schedules: Dict[str, Dict[str, Any]] = {}
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # Callbacks
        self.on_task_triggered: Optional[Callable] = None
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            return
        
        self.running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._thread.start()
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        self._stop_event.set()
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running and not self._stop_event.is_set():
            try:
                current_time = datetime.now()
                
                # Check all schedules
                for task_id, schedule in list(self.schedules.items()):
                    if not schedule.get('enabled', True):
                        continue
                    
                    next_run = schedule.get('next_run')
                    if next_run and current_time >= next_run:
                        # Trigger task
                        if self.on_task_triggered:
                            self.on_task_triggered(task_id)
                        
                        # Update next run time
                        self._update_next_run(task_id, schedule)
                
                # Sleep for a short interval
                time.sleep(1)
                
            except Exception as e:
                print(f"Scheduler error: {e}")
    
    def add_schedule(
        self,
        task_id: str,
        schedule_type: ScheduleType,
        config: Dict[str, Any]
    ):
        """
        Add a task schedule
        
        Args:
            task_id: Task identifier
            schedule_type: Type of schedule
            config: Schedule configuration
                - For IMMEDIATE: no config needed
                - For INTERVAL: {'seconds': int} or {'minutes': int} or {'hours': int}
                - For DAILY: {'time': 'HH:MM'}
                - For WEEKLY: {'day': 0-6, 'time': 'HH:MM'} (0=Monday)
                - For CRON: {'expression': 'cron_expr'}
                - For EVENT: {'event_type': str}
        """
        schedule = {
            'type': schedule_type,
            'config': config,
            'enabled': True,
            'created_at': datetime.now()
        }
        
        # Calculate first run time
        if schedule_type == ScheduleType.IMMEDIATE:
            schedule['next_run'] = datetime.now()
        else:
            self._update_next_run(task_id, schedule)
        
        self.schedules[task_id] = schedule
    
    def _update_next_run(self, task_id: str, schedule: Dict[str, Any]):
        """Update next run time for a schedule"""
        schedule_type = schedule['type']
        config = schedule['config']
        current_time = datetime.now()
        
        if schedule_type == ScheduleType.IMMEDIATE:
            # One-time immediate execution
            schedule['enabled'] = False
            schedule['next_run'] = None
        
        elif schedule_type == ScheduleType.INTERVAL:
            # Interval-based scheduling
            seconds = config.get('seconds', 0)
            minutes = config.get('minutes', 0)
            hours = config.get('hours', 0)
            
            total_seconds = seconds + (minutes * 60) + (hours * 3600)
            schedule['next_run'] = current_time + timedelta(seconds=total_seconds)
        
        elif schedule_type == ScheduleType.DAILY:
            # Daily at specific time
            time_str = config.get('time', '00:00')
            hour, minute = map(int, time_str.split(':'))
            
            next_run = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If time has passed today, schedule for tomorrow
            if next_run <= current_time:
                next_run += timedelta(days=1)
            
            schedule['next_run'] = next_run
        
        elif schedule_type == ScheduleType.WEEKLY:
            # Weekly on specific day and time
            target_day = config.get('day', 0)  # 0=Monday
            time_str = config.get('time', '00:00')
            hour, minute = map(int, time_str.split(':'))
            
            # Calculate days until target day
            current_day = current_time.weekday()
            days_ahead = target_day - current_day
            
            if days_ahead < 0:  # Target day already passed this week
                days_ahead += 7
            elif days_ahead == 0:  # Target day is today
                target_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if target_time <= current_time:
                    days_ahead = 7
            
            next_run = current_time + timedelta(days=days_ahead)
            next_run = next_run.replace(hour=hour, minute=minute, second=0, microsecond=0)
            schedule['next_run'] = next_run
        
        elif schedule_type == ScheduleType.EVENT:
            # Event-based scheduling (set by external trigger)
            schedule['next_run'] = None
    
    def remove_schedule(self, task_id: str):
        """Remove a task schedule"""
        if task_id in self.schedules:
            del self.schedules[task_id]
    
    def enable_schedule(self, task_id: str):
        """Enable a task schedule"""
        if task_id in self.schedules:
            self.schedules[task_id]['enabled'] = True
    
    def disable_schedule(self, task_id: str):
        """Disable a task schedule"""
        if task_id in self.schedules:
            self.schedules[task_id]['enabled'] = False
    
    def trigger_event(self, task_id: str):
        """Manually trigger an event-based task"""
        if task_id in self.schedules:
            schedule = self.schedules[task_id]
            if schedule['type'] == ScheduleType.EVENT:
                schedule['next_run'] = datetime.now()
    
    def get_next_run(self, task_id: str) -> Optional[datetime]:
        """Get next run time for a task"""
        if task_id in self.schedules:
            return self.schedules[task_id].get('next_run')
        return None
    
    def get_schedule_info(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get schedule information"""
        return self.schedules.get(task_id)
    
    def get_all_schedules(self) -> Dict[str, Dict[str, Any]]:
        """Get all schedules"""
        return self.schedules.copy()


# Global scheduler instance
_global_scheduler: Optional[TaskScheduler] = None


def get_scheduler() -> TaskScheduler:
    """Get or create global scheduler"""
    global _global_scheduler
    if _global_scheduler is None:
        _global_scheduler = TaskScheduler()
    return _global_scheduler


def init_scheduler() -> TaskScheduler:
    """Initialize global scheduler"""
    global _global_scheduler
    _global_scheduler = TaskScheduler()
    return _global_scheduler
