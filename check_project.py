#!/usr/bin/env python3
"""
Comprehensive Python Project Checker
Checks for import issues, missing dependencies, and common errors
"""

import sys
import ast
import importlib.util
from pathlib import Path
import re

class ProjectChecker:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.issues = []
        self.warnings = []
        
    def check_all(self):
        """Run all checks"""
        print("=" * 60)
        print("AUTOMATION HUB - PROJECT VALIDATION")
        print("=" * 60)
        print()
        
        # Find all Python files
        py_files = list(self.project_root.rglob("*.py"))
        py_files = [f for f in py_files if '__pycache__' not in str(f)]
        
        print(f"Found {len(py_files)} Python files")
        print()
        
        # Check each file
        for py_file in sorted(py_files):
            self.check_file(py_file)
        
        # Print results
        self.print_results()
        
        return len(self.issues) == 0
    
    def check_file(self, filepath):
        """Check a single Python file"""
        rel_path = filepath.relative_to(self.project_root)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content, str(filepath))
            
            # Extract imports
            imports = self.extract_imports(tree)
            
            # Check for common issues
            self.check_imports(rel_path, imports, content)
            self.check_qt_usage(rel_path, content)
            self.check_string_formatting(rel_path, content)
            
            print(f"✓ {rel_path}")
            
        except SyntaxError as e:
            self.issues.append(f"{rel_path}: SYNTAX ERROR at line {e.lineno}: {e.msg}")
            print(f"✗ {rel_path}: SYNTAX ERROR")
        except Exception as e:
            self.issues.append(f"{rel_path}: ERROR: {e}")
            print(f"✗ {rel_path}: ERROR")
    
    def extract_imports(self, tree):
        """Extract all imports from AST"""
        imports = {
            'modules': set(),
            'from_imports': {},
            'names': set()
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports['modules'].add(alias.name)
                    imports['names'].add(alias.asname if alias.asname else alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                if module not in imports['from_imports']:
                    imports['from_imports'][module] = set()
                
                for alias in node.names:
                    imports['from_imports'][module].add(alias.name)
                    imports['names'].add(alias.asname if alias.asname else alias.name)
        
        return imports
    
    def check_imports(self, filepath, imports, content):
        """Check for import issues"""
        # Check for PyQt6 imports
        if 'PyQt6' in str(filepath):
            return
        
        # Common PyQt6 classes that need to be imported
        qt_classes = [
            'QDialog', 'QMainWindow', 'QWidget', 'QPushButton',
            'QLabel', 'QLineEdit', 'QTextEdit', 'QTableWidget',
            'QVBoxLayout', 'QHBoxLayout', 'QFormLayout',
            'QMessageBox', 'QFileDialog', 'QProgressBar',
            'QComboBox', 'QCheckBox', 'QSpinBox', 'QTabWidget'
        ]
        
        for qt_class in qt_classes:
            if qt_class in content and qt_class not in imports['names']:
                # Check if it's in a comment or string
                if f"'{qt_class}'" not in content and f'"{qt_class}"' not in content:
                    self.warnings.append(
                        f"{filepath}: Uses {qt_class} but may not import it"
                    )
    
    def check_qt_usage(self, filepath, content):
        """Check for Qt-specific issues"""
        # Check for QDialog.DialogCode usage without QDialog import
        if 'QDialog.DialogCode' in content or 'DialogCode' in content:
            if 'from PyQt6.QtWidgets import' in content:
                imports_line = [line for line in content.split('\n') 
                               if 'from PyQt6.QtWidgets import' in line]
                if imports_line and 'QDialog' not in imports_line[0]:
                    self.issues.append(
                        f"{filepath}: Uses QDialog.DialogCode but QDialog not imported"
                    )
        
        # Check for deprecated Qt attributes
        deprecated = {
            'AA_UseHighDpiPixmaps': 'Removed in Qt6 - High DPI is automatic',
            'AA_EnableHighDpiScaling': 'Removed in Qt6 - High DPI is automatic'
        }
        
        for dep, msg in deprecated.items():
            if dep in content:
                self.issues.append(f"{filepath}: Uses deprecated {dep} - {msg}")
    
    def check_string_formatting(self, filepath, content):
        """Check for string formatting issues"""
        # Check for f-string syntax errors (basic check)
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'f"' in line or "f'" in line:
                # Basic check for unmatched braces
                open_braces = line.count('{')
                close_braces = line.count('}')
                # Account for escaped braces
                open_braces -= line.count('{{')
                close_braces -= line.count('}}')
                
                if open_braces != close_braces:
                    self.warnings.append(
                        f"{filepath}:{i}: Possible f-string brace mismatch"
                    )
    
    def print_results(self):
        """Print check results"""
        print()
        print("=" * 60)
        print("RESULTS")
        print("=" * 60)
        print()
        
        if self.issues:
            print(f"❌ CRITICAL ISSUES ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  - {issue}")
            print()
        
        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
            print()
        
        if not self.issues and not self.warnings:
            print("✅ ALL CHECKS PASSED!")
            print()
        
        print("=" * 60)


def main():
    project_root = Path(__file__).parent
    
    checker = ProjectChecker(project_root)
    success = checker.check_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
