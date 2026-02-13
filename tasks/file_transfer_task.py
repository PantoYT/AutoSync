"""
File Transfer Task
Copy/move files and folders with presets
"""

import shutil
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from .base_task import BaseTask


class FileTransferTask(BaseTask):
    """Copy or move files/folders"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize file transfer task
        
        Config keys:
            - source: Source path (file or directory)
            - destination: Destination path
            - operation: 'copy' or 'move'
            - overwrite: Whether to overwrite existing files
            - recursive: Whether to copy directories recursively
            - mirror: Mirror mode (delete files not in source)
            - file_patterns: List of file patterns to include (e.g., ['*.txt', '*.py'])
            - exclude_patterns: List of patterns to exclude
        """
        super().__init__(name, "file_transfer", config)
        self._total_files = 0
        self._processed_files = 0
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate file transfer configuration"""
        source = self.config.get("source")
        if not source:
            return False, "Source path is required"
        
        source_path = Path(source)
        if not source_path.exists():
            return False, f"Source not found: {source}"
        
        destination = self.config.get("destination")
        if not destination:
            return False, "Destination path is required"
        
        operation = self.config.get("operation", "copy")
        if operation not in ("copy", "move"):
            return False, f"Invalid operation: {operation} (must be 'copy' or 'move')"
        
        return True, None
    
    def _count_files(self, path: Path, patterns: List[str]) -> int:
        """Count files to process"""
        count = 0
        if path.is_file():
            return 1
        
        if patterns:
            for pattern in patterns:
                count += len(list(path.rglob(pattern)))
        else:
            count += sum(1 for _ in path.rglob("*") if _.is_file())
        
        return count
    
    def _should_process_file(self, file_path: Path) -> bool:
        """Check if file should be processed based on patterns"""
        file_patterns = self.config.get("file_patterns", [])
        exclude_patterns = self.config.get("exclude_patterns", [])
        
        # Check exclude patterns first
        if exclude_patterns:
            for pattern in exclude_patterns:
                if file_path.match(pattern):
                    return False
        
        # Check include patterns
        if file_patterns:
            for pattern in file_patterns:
                if file_path.match(pattern):
                    return True
            return False
        
        return True
    
    def _copy_file(self, src: Path, dst: Path) -> bool:
        """Copy a single file"""
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            self.log(f"Failed to copy {src.name}: {e}", "WARNING")
            return False
    
    def _move_file(self, src: Path, dst: Path) -> bool:
        """Move a single file"""
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            return True
        except Exception as e:
            self.log(f"Failed to move {src.name}: {e}", "WARNING")
            return False
    
    def _execute(self) -> bool:
        """Execute file transfer"""
        try:
            source = Path(self.config.get("source"))
            destination = Path(self.config.get("destination"))
            operation = self.config.get("operation", "copy")
            overwrite = self.config.get("overwrite", True)
            mirror = self.config.get("mirror", False)
            
            self.log(f"Starting {operation} from {source} to {destination}", "INFO")
            
            # Count files
            file_patterns = self.config.get("file_patterns", [])
            self._total_files = self._count_files(source, file_patterns)
            self._processed_files = 0
            
            self.log(f"Found {self._total_files} file(s) to process", "INFO")
            self.update_progress(5.0)
            
            # Single file transfer
            if source.is_file():
                if not self._should_process_file(source):
                    self.log("File excluded by pattern", "INFO")
                    return True
                
                dst_file = destination if destination.suffix else destination / source.name
                
                if dst_file.exists() and not overwrite:
                    self.log("File exists and overwrite is disabled", "WARNING")
                    return True
                
                self.update_progress(50.0)
                
                if operation == "copy":
                    success = self._copy_file(source, dst_file)
                else:
                    success = self._move_file(source, dst_file)
                
                if success:
                    self.log(f"Successfully {operation}ed file", "SUCCESS")
                    return True
                else:
                    return False
            
            # Directory transfer
            elif source.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
                
                # Get all files to process
                if file_patterns:
                    files_to_process = []
                    for pattern in file_patterns:
                        files_to_process.extend(source.rglob(pattern))
                else:
                    files_to_process = [f for f in source.rglob("*") if f.is_file()]
                
                # Filter by exclude patterns
                files_to_process = [f for f in files_to_process if self._should_process_file(f)]
                
                self._total_files = len(files_to_process)
                success_count = 0
                fail_count = 0
                
                for file_path in files_to_process:
                    if self.is_stopped():
                        self.log("Transfer stopped by user", "WARNING")
                        return False
                    
                    self.wait_if_paused()
                    
                    # Calculate relative path
                    rel_path = file_path.relative_to(source)
                    dst_file = destination / rel_path
                    
                    # Check overwrite
                    if dst_file.exists() and not overwrite:
                        self._processed_files += 1
                        continue
                    
                    # Transfer file
                    if operation == "copy":
                        if self._copy_file(file_path, dst_file):
                            success_count += 1
                        else:
                            fail_count += 1
                    else:
                        if self._move_file(file_path, dst_file):
                            success_count += 1
                        else:
                            fail_count += 1
                    
                    self._processed_files += 1
                    
                    # Update progress
                    if self._total_files > 0:
                        progress = (self._processed_files / self._total_files) * 90.0 + 5.0
                        self.update_progress(progress)
                
                # Mirror mode: delete files not in source
                if mirror and operation == "copy":
                    self.log("Mirror mode: removing extra files", "INFO")
                    for dst_file in destination.rglob("*"):
                        if dst_file.is_file():
                            rel_path = dst_file.relative_to(destination)
                            src_file = source / rel_path
                            if not src_file.exists():
                                try:
                                    dst_file.unlink()
                                    self.log(f"Removed: {rel_path}", "INFO")
                                except Exception as e:
                                    self.log(f"Failed to remove {rel_path}: {e}", "WARNING")
                
                self.log(f"Transfer complete: {success_count} success, {fail_count} failed", "SUCCESS")
                return fail_count == 0
            
            return True
            
        except Exception as e:
            self.error_message = str(e)
            self.log(f"File transfer error: {e}", "ERROR")
            return False
