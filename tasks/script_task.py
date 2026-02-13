"""
Script Execution Task
Executes Python scripts, batch files, or system commands
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from .base_task import BaseTask


class ScriptTask(BaseTask):
    """Execute scripts or system commands"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize script task
        
        Config keys:
            - script_path: Path to script file
            - script_type: 'python', 'batch', 'command'
            - arguments: List of command-line arguments
            - working_dir: Working directory for execution
            - timeout: Execution timeout in seconds
            - capture_output: Whether to capture stdout/stderr
        """
        super().__init__(name, "script", config)
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate script configuration"""
        script_type = self.config.get("script_type", "python")
        
        if script_type in ("python", "batch"):
            script_path = self.config.get("script_path")
            if not script_path:
                return False, "Script path is required"
            
            path = Path(script_path)
            if not path.exists():
                return False, f"Script not found: {script_path}"
            
            if not path.is_file():
                return False, f"Not a file: {script_path}"
        
        elif script_type == "command":
            command = self.config.get("command")
            if not command:
                return False, "Command is required"
        else:
            return False, f"Invalid script type: {script_type}"
        
        return True, None
    
    def _execute(self) -> bool:
        """Execute the script"""
        try:
            script_type = self.config.get("script_type", "python")
            timeout = self.config.get("timeout", 300)
            capture_output = self.config.get("capture_output", True)
            working_dir = self.config.get("working_dir")
            
            # Build command
            if script_type == "python":
                script_path = self.config.get("script_path")
                cmd = [sys.executable, script_path]
            elif script_type == "batch":
                script_path = self.config.get("script_path")
                cmd = [script_path]
            elif script_type == "command":
                command = self.config.get("command")
                cmd = command if isinstance(command, list) else [command]
            else:
                self.error_message = f"Unknown script type: {script_type}"
                return False
            
            # Add arguments
            arguments = self.config.get("arguments", [])
            if arguments:
                cmd.extend(arguments)
            
            self.log(f"Executing: {' '.join(cmd)}", "INFO")
            self.update_progress(10.0)
            
            # Execute
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
                check=False
            )
            
            self.update_progress(90.0)
            
            # Log output
            if capture_output and result.stdout:
                self.log(f"Output: {result.stdout[:500]}", "INFO")
            
            if result.returncode == 0:
                self.log(f"Script completed with exit code 0", "SUCCESS")
                return True
            else:
                self.error_message = f"Exit code: {result.returncode}"
                if capture_output and result.stderr:
                    self.error_message += f"\n{result.stderr[:500]}"
                self.log(f"Script failed: {self.error_message}", "ERROR")
                return False
                
        except subprocess.TimeoutExpired:
            self.error_message = f"Script timeout after {timeout} seconds"
            self.log(self.error_message, "ERROR")
            return False
        except Exception as e:
            self.error_message = str(e)
            self.log(f"Script execution error: {e}", "ERROR")
            return False
