"""
Git Sync Task
Automatic git add/commit/push with smart commit messages
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from git import Repo, InvalidGitRepositoryError, GitCommandError
    
try:
    from git import Repo, InvalidGitRepositoryError, GitCommandError
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    # Define dummy classes for type hints
    Repo = None
    InvalidGitRepositoryError = Exception
    GitCommandError = Exception

from .base_task import BaseTask


class GitTask(BaseTask):
    """Git repository synchronization"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize Git task
        
        Config keys:
            - repo_path: Path to git repository
            - auto_add: Automatically stage all changes
            - auto_commit: Automatically commit changes
            - auto_push: Automatically push to remote
            - commit_message: Custom commit message (optional)
            - smart_message: Generate smart commit messages
            - remote: Remote name (default: origin)
            - branch: Branch name (default: current branch)
        """
        super().__init__(name, "git", config)
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate Git configuration"""
        if not GIT_AVAILABLE:
            return False, "GitPython not installed. Install with: pip install GitPython"
        
        repo_path = self.config.get("repo_path")
        if not repo_path:
            return False, "Repository path is required"
        
        path = Path(repo_path)
        if not path.exists():
            return False, f"Repository not found: {repo_path}"
        
        if not (path / ".git").exists():
            return False, f"Not a git repository: {repo_path}"
        
        return True, None
    
    def _generate_smart_message(self, repo: Repo) -> str:
        """Generate a smart commit message based on changes"""
        try:
            # Get changed files
            changed_files = [item.a_path for item in repo.index.diff("HEAD")]
            untracked = repo.untracked_files
            
            # Count changes
            modified = len(changed_files)
            added = len(untracked)
            
            # Determine file types
            extensions = set()
            for file in changed_files + untracked:
                ext = Path(file).suffix
                if ext:
                    extensions.add(ext[1:])  # Remove the dot
            
            # Build message
            parts = []
            if modified > 0:
                parts.append(f"{modified} modified")
            if added > 0:
                parts.append(f"{added} added")
            
            message = "Auto: " + ", ".join(parts)
            
            if extensions:
                ext_list = ", ".join(sorted(extensions))
                message += f" ({ext_list} files)"
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            message += f" - {timestamp}"
            
            return message
            
        except Exception as e:
            self.log(f"Error generating smart message: {e}", "WARNING")
            return f"Auto backup - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    def _execute(self) -> bool:
        """Execute Git sync"""
        try:
            repo_path = self.config.get("repo_path")
            auto_add = self.config.get("auto_add", True)
            auto_commit = self.config.get("auto_commit", True)
            auto_push = self.config.get("auto_push", True)
            smart_message = self.config.get("smart_message", True)
            commit_message = self.config.get("commit_message")
            remote_name = self.config.get("remote", "origin")
            branch_name = self.config.get("branch")
            
            self.log(f"Checking repository: {repo_path}", "INFO")
            self.update_progress(10.0)
            
            # Open repository
            try:
                repo = Repo(repo_path)
            except InvalidGitRepositoryError:
                self.error_message = "Not a valid git repository"
                return False
            
            # Check for changes
            if repo.is_dirty(untracked_files=True):
                self.log("Changes detected", "INFO")
            else:
                self.log("No changes to commit", "INFO")
                return True
            
            self.update_progress(20.0)
            
            # Stage changes
            if auto_add:
                self.log("Staging changes...", "INFO")
                repo.git.add(A=True)
                self.update_progress(40.0)
            
            # Commit changes
            if auto_commit:
                if not commit_message and smart_message:
                    commit_message = self._generate_smart_message(repo)
                elif not commit_message:
                    commit_message = f"Auto backup - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                
                self.log(f"Committing: {commit_message}", "INFO")
                try:
                    repo.index.commit(commit_message)
                    self.update_progress(70.0)
                except Exception as e:
                    if "nothing to commit" in str(e).lower():
                        self.log("Nothing to commit (already committed)", "INFO")
                        return True
                    raise
            
            # Push to remote
            if auto_push:
                self.log(f"Pushing to {remote_name}...", "INFO")
                try:
                    origin = repo.remote(name=remote_name)
                    
                    # Get current branch if not specified
                    if not branch_name:
                        branch_name = repo.active_branch.name
                    
                    push_info = origin.push(branch_name)
                    
                    # Check push result
                    if push_info:
                        for info in push_info:
                            if info.flags & info.ERROR:
                                self.error_message = f"Push error: {info.summary}"
                                self.log(self.error_message, "ERROR")
                                return False
                    
                    self.log(f"Successfully pushed to {remote_name}/{branch_name}", "SUCCESS")
                    self.update_progress(100.0)
                    
                except GitCommandError as e:
                    self.error_message = f"Push failed: {str(e)}"
                    self.log(self.error_message, "WARNING")
                    self.log("Changes are committed locally", "INFO")
                    return True  # Still success if committed locally
            
            return True
            
        except Exception as e:
            self.error_message = str(e)
            self.log(f"Git sync error: {e}", "ERROR")
            return False
