"""
SQL Database Task
Import/export SQL databases with MySQL support
"""

import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from .base_task import BaseTask


class SQLTask(BaseTask):
    """SQL database import/export operations"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize SQL task
        
        Config keys:
            - operation: 'import' or 'export'
            - mysql_bin: Path to mysql executable
            - user: MySQL username
            - password: MySQL password
            - host: MySQL host (default: localhost)
            - port: MySQL port (default: 3306)
            - database: Database name (for export)
            - sql_file: SQL file path (for import/export)
            - sql_directory: Directory with SQL files (for batch import)
            - charset: Character set (default: utf8mb4)
            - create_database: Create database if not exists (import only)
            - drop_existing: Drop database before import
        """
        super().__init__(name, "sql", config)
        self._total_files = 0
        self._processed_files = 0
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate SQL configuration"""
        operation = self.config.get("operation", "import")
        if operation not in ("import", "export"):
            return False, f"Invalid operation: {operation}"
        
        mysql_bin = self.config.get("mysql_bin")
        if not mysql_bin:
            return False, "MySQL binary path is required"
        
        if not Path(mysql_bin).exists():
            return False, f"MySQL not found: {mysql_bin}"
        
        user = self.config.get("user")
        if not user:
            return False, "MySQL user is required"
        
        if operation == "import":
            sql_file = self.config.get("sql_file")
            sql_dir = self.config.get("sql_directory")
            
            if not sql_file and not sql_dir:
                return False, "SQL file or directory is required for import"
            
            if sql_file and not Path(sql_file).exists():
                return False, f"SQL file not found: {sql_file}"
            
            if sql_dir and not Path(sql_dir).exists():
                return False, f"SQL directory not found: {sql_dir}"
        
        elif operation == "export":
            database = self.config.get("database")
            if not database:
                return False, "Database name is required for export"
            
            sql_file = self.config.get("sql_file")
            if not sql_file:
                return False, "SQL file path is required for export"
        
        return True, None
    
    def _build_mysql_args(self) -> List[str]:
        """Build common MySQL arguments"""
        args = [self.config.get("mysql_bin")]
        
        user = self.config.get("user")
        args.extend(["-u", user])
        
        password = self.config.get("password", "")
        if password:
            args.append(f"-p{password}")
        
        host = self.config.get("host", "localhost")
        args.extend(["-h", host])
        
        port = self.config.get("port", 3306)
        args.extend(["-P", str(port)])
        
        return args
    
    def _execute_mysql_command(self, command: str, database: Optional[str] = None) -> bool:
        """Execute a MySQL command"""
        try:
            args = self._build_mysql_args()
            
            if database:
                args.append(database)
            
            args.extend(["-e", command])
            
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                self.log(f"MySQL error: {result.stderr}", "ERROR")
                return False
            
            return True
            
        except Exception as e:
            self.log(f"MySQL command error: {e}", "ERROR")
            return False
    
    def _import_sql_file(self, sql_file: Path, database: str) -> bool:
        """Import a single SQL file"""
        try:
            self.log(f"Importing {sql_file.name} into {database}", "INFO")
            
            # Drop and create database if requested
            if self.config.get("drop_existing", True):
                self.log(f"Dropping database {database}", "INFO")
                if not self._execute_mysql_command(f"DROP DATABASE IF EXISTS `{database}`"):
                    return False
            
            if self.config.get("create_database", True):
                charset = self.config.get("charset", "utf8mb4")
                self.log(f"Creating database {database}", "INFO")
                if not self._execute_mysql_command(
                    f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET {charset}"
                ):
                    return False
            
            # Import SQL file
            args = self._build_mysql_args()
            args.append(database)
            
            with open(sql_file, 'r', encoding='utf-8') as f:
                result = subprocess.run(
                    args,
                    stdin=f,
                    capture_output=True,
                    text=True,
                    check=False
                )
            
            if result.returncode != 0:
                self.error_message = f"Import failed: {result.stderr}"
                self.log(self.error_message, "ERROR")
                return False
            
            self.log(f"Successfully imported {database}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Import error: {e}", "ERROR")
            return False
    
    def _export_database(self, database: str, output_file: Path) -> bool:
        """Export a database to SQL file"""
        try:
            self.log(f"Exporting {database} to {output_file}", "INFO")
            
            # Use mysqldump
            mysqldump = Path(self.config.get("mysql_bin")).parent / "mysqldump"
            if not mysqldump.exists():
                mysqldump = Path(str(mysqldump) + ".exe")
            
            if not mysqldump.exists():
                self.error_message = "mysqldump not found"
                return False
            
            args = [str(mysqldump)]
            
            user = self.config.get("user")
            args.extend(["-u", user])
            
            password = self.config.get("password", "")
            if password:
                args.append(f"-p{password}")
            
            host = self.config.get("host", "localhost")
            args.extend(["-h", host])
            
            port = self.config.get("port", 3306)
            args.extend(["-P", str(port)])
            
            args.append(database)
            
            # Execute export
            with open(output_file, 'w', encoding='utf-8') as f:
                result = subprocess.run(
                    args,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )
            
            if result.returncode != 0:
                self.error_message = f"Export failed: {result.stderr}"
                self.log(self.error_message, "ERROR")
                return False
            
            self.log(f"Successfully exported to {output_file}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Export error: {e}", "ERROR")
            return False
    
    def _get_database_name(self, sql_file: Path, sql_dir: Path) -> str:
        """Generate database name from file structure"""
        try:
            rel_path = sql_file.relative_to(sql_dir)
            parts = rel_path.parts
            
            if len(parts) > 1:
                # Include parent folder in database name
                class_name = parts[0]
                db_name = f"{class_name}_{sql_file.stem}"
            else:
                db_name = sql_file.stem
            
            # Clean database name
            db_name = db_name.replace(" ", "_").replace("-", "_")
            
            return db_name
            
        except Exception:
            return sql_file.stem
    
    def _execute(self) -> bool:
        """Execute SQL operation"""
        try:
            operation = self.config.get("operation", "import")
            
            if operation == "import":
                return self._execute_import()
            elif operation == "export":
                return self._execute_export()
            
            return False
            
        except Exception as e:
            self.error_message = str(e)
            self.log(f"SQL task error: {e}", "ERROR")
            return False
    
    def _execute_import(self) -> bool:
        """Execute import operation"""
        sql_file = self.config.get("sql_file")
        sql_dir = self.config.get("sql_directory")
        
        self.update_progress(10.0)
        
        # Single file import
        if sql_file:
            sql_path = Path(sql_file)
            database = self.config.get("database", sql_path.stem)
            
            self.update_progress(30.0)
            success = self._import_sql_file(sql_path, database)
            
            if success:
                self.update_progress(100.0)
            
            return success
        
        # Directory import
        elif sql_dir:
            sql_dir_path = Path(sql_dir)
            sql_files = list(sql_dir_path.rglob("*.sql"))
            
            if not sql_files:
                self.log("No SQL files found", "WARNING")
                return True
            
            self._total_files = len(sql_files)
            self._processed_files = 0
            
            self.log(f"Found {self._total_files} SQL file(s)", "INFO")
            
            success_count = 0
            fail_count = 0
            
            for sql_file in sql_files:
                if self.is_stopped():
                    self.log("Import stopped by user", "WARNING")
                    return False
                
                self.wait_if_paused()
                
                database = self._get_database_name(sql_file, sql_dir_path)
                
                if self._import_sql_file(sql_file, database):
                    success_count += 1
                else:
                    fail_count += 1
                
                self._processed_files += 1
                progress = (self._processed_files / self._total_files) * 90.0 + 10.0
                self.update_progress(progress)
            
            self.log(f"Import complete: {success_count} success, {fail_count} failed", "SUCCESS")
            return fail_count == 0
        
        return False
    
    def _execute_export(self) -> bool:
        """Execute export operation"""
        database = self.config.get("database")
        sql_file = Path(self.config.get("sql_file"))
        
        # Create output directory
        sql_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.update_progress(30.0)
        success = self._export_database(database, sql_file)
        
        if success:
            self.update_progress(100.0)
        
        return success
