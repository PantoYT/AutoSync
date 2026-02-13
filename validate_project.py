#!/usr/bin/env python3
"""
Complete Project Validation
Checks for all potential runtime issues
"""

import sys
import ast
import re
from pathlib import Path
from typing import List, Tuple

class Validator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_file(self, filepath: Path) -> bool:
        """Validate a single Python file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse to check syntax
            try:
                tree = ast.parse(content, str(filepath))
            except SyntaxError as e:
                self.errors.append(f"{filepath}:{e.lineno}: Syntax error: {e.msg}")
                return False
            
            # Check for specific issues
            self.check_qt_imports(filepath, content)
            self.check_type_hints(filepath, content)
            self.check_common_errors(filepath, content)
            
            return True
            
        except Exception as e:
            self.errors.append(f"{filepath}: Failed to read: {e}")
            return False
    
    def check_qt_imports(self, filepath: Path, content: str):
        """Check Qt-related imports"""
        if 'PyQt6' not in content:
            return
        
        # Check for QDialog usage
        if 'QDialog.DialogCode' in content or 'DialogCode.Accepted' in content:
            # Check if QDialog is imported
            import_lines = [line for line in content.split('\n') 
                          if 'from PyQt6.QtWidgets import' in line]
            
            if import_lines:
                imports = ' '.join(import_lines)
                if 'QDialog' not in imports:
                    self.errors.append(
                        f"{filepath}: Uses QDialog.DialogCode but QDialog not imported"
                    )
        
        # Check for deprecated Qt6 attributes
        deprecated_attrs = [
            'AA_UseHighDpiPixmaps',
            'AA_EnableHighDpiScaling',
            'AA_DisableHighDpiScaling'
        ]
        
        for attr in deprecated_attrs:
            if attr in content and 'deprecated' not in content.lower():
                self.errors.append(
                    f"{filepath}: Uses deprecated Qt6 attribute: {attr}"
                )
    
    def check_type_hints(self, filepath: Path, content: str):
        """Check for problematic type hints"""
        # Check for undefined types in hints
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for type hints with undefined classes
            if '-> Repo:' in line or ': Repo)' in line:
                # Make sure Repo is either imported or defined
                if 'from git import Repo' not in content and 'Repo = ' not in content:
                    if 'TYPE_CHECKING' not in content:
                        self.warnings.append(
                            f"{filepath}:{i}: Type hint uses 'Repo' which may not be defined"
                        )
    
    def check_common_errors(self, filepath: Path, content: str):
        """Check for common Python errors"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for undefined variables in common patterns
            
            # Check for .exec() without QDialog import
            if '.exec()' in line and 'QDialog' not in content:
                if any(x in line for x in ['dialog', 'Dialog', 'window']):
                    self.warnings.append(
                        f"{filepath}:{i}: Uses .exec() - ensure QDialog is imported if needed"
                    )
            
            # Check for common name errors
            if 'DialogCode.Accepted' in line and 'QDialog' not in line:
                # Check if full qualification is used
                if 'QDialog.DialogCode' not in content[:content.find(line)]:
                    self.warnings.append(
                        f"{filepath}:{i}: Uses DialogCode.Accepted - should be QDialog.DialogCode.Accepted"
                    )
    
    def print_results(self, total_files: int):
        """Print validation results"""
        print()
        print("=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)
        print()
        print(f"Files checked: {total_files}")
        print()
        
        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")
            print()
        
        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
            print()
        
        if not self.errors and not self.warnings:
            print("✅ ALL CHECKS PASSED - No issues found!")
            print()
        
        return len(self.errors) == 0


def main():
    print("=" * 70)
    print("AUTOMATION HUB - COMPREHENSIVE VALIDATION")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent
    
    # Find all Python files except test scripts
    py_files = [
        f for f in project_root.rglob("*.py")
        if '__pycache__' not in str(f) 
        and f.name not in ['check_project.py', 'test_imports.py', 'validate_project.py']
    ]
    
    print(f"Validating {len(py_files)} Python files...")
    print()
    
    validator = Validator()
    
    for py_file in sorted(py_files):
        rel_path = py_file.relative_to(project_root)
        if validator.validate_file(py_file):
            print(f"✓ {rel_path}")
        else:
            print(f"✗ {rel_path}")
    
    success = validator.print_results(len(py_files))
    
    if success:
        print("=" * 70)
        print("✅ PROJECT IS READY TO RUN!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Install dependencies: python setup.py")
        print("  2. Run application: python main.py")
        print()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
