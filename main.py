"""
Automation Hub - Main Application
Professional task automation and scheduling system
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Import utilities
from utils import init_logger, init_config_manager, init_scheduler, get_logger
from gui.main_window import MainWindow


def main():
    """Main application entry point"""
    
    # Initialize application
    app = QApplication(sys.argv)
    app.setApplicationName("Automation Hub")
    app.setOrganizationName("AutomationHub")
    
    # High DPI support is automatic in Qt6
    
    # Initialize core systems
    logger = init_logger("logs", max_memory_logs=2000)
    config = init_config_manager("configs")
    scheduler = init_scheduler()
    
    # Load configuration
    config.load_config()
    
    # Log startup
    logger.log("System", "=" * 60, "INFO")
    logger.log("System", "Automation Hub Starting", "INFO")
    logger.log("System", "=" * 60, "INFO")
    
    try:
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Start scheduler
        scheduler.start()
        logger.log("System", "Scheduler started", "SUCCESS")
        
        # Run application
        exit_code = app.exec()
        
        # Cleanup
        logger.log("System", "Application shutting down", "INFO")
        scheduler.stop()
        config.save_config(config.config)
        
        return exit_code
        
    except Exception as e:
        logger.log("System", f"Fatal error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
