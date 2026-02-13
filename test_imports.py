#!/usr/bin/env python3
"""
Runtime Import Checker
Tests if all modules can be imported without errors
"""

import sys
import importlib
from pathlib import Path

def test_imports():
    """Test importing all modules"""
    print("=" * 60)
    print("TESTING MODULE IMPORTS")
    print("=" * 60)
    print()
    
    # Add project to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    modules_to_test = [
        'utils.logger',
        'utils.config_manager',
        'utils.scheduler',
        'tasks.base_task',
        'tasks.script_task',
        'tasks.file_transfer_task',
        'tasks.git_task',
        'tasks.sql_task',
    ]
    
    # Note: GUI modules require PyQt6 which may not be installed yet
    gui_modules = [
        'gui.theme_manager',
        'gui.task_dialog',
        'gui.main_window',
    ]
    
    success_count = 0
    fail_count = 0
    
    # Test core modules
    print("Testing core modules:")
    for module_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            print(f"  ✓ {module_name}")
            success_count += 1
        except ImportError as e:
            print(f"  ✗ {module_name}: {e}")
            fail_count += 1
        except Exception as e:
            print(f"  ⚠ {module_name}: {e}")
    
    print()
    print("Testing GUI modules (requires PyQt6):")
    for module_name in gui_modules:
        try:
            module = importlib.import_module(module_name)
            print(f"  ✓ {module_name}")
            success_count += 1
        except ImportError as e:
            if 'PyQt6' in str(e):
                print(f"  ⊘ {module_name}: PyQt6 not installed (expected)")
            else:
                print(f"  ✗ {module_name}: {e}")
                fail_count += 1
        except Exception as e:
            print(f"  ⚠ {module_name}: {e}")
            fail_count += 1
    
    print()
    print("=" * 60)
    print(f"Results: {success_count} passed, {fail_count} failed")
    print("=" * 60)
    
    return fail_count == 0


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
