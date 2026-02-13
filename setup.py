"""
Setup and Installation Script
Helps users set up the Automation Hub application
"""

import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher is required")
        return False
    
    print("✓ Python version is compatible")
    return True


def install_dependencies():
    """Install required dependencies"""
    print_header("Installing Dependencies")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ ERROR: requirements.txt not found")
        return False
    
    print("Installing packages from requirements.txt...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("\n✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR: Failed to install dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    base_dir = Path(__file__).parent
    
    directories = [
        base_dir / "configs",
        base_dir / "logs",
        base_dir / "resources"
    ]
    
    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True)
            print(f"✓ Created: {directory.name}/")
        else:
            print(f"  Already exists: {directory.name}/")
    
    print("\n✓ Directories created")
    return True


def run_initial_setup():
    """Run initial application setup"""
    print_header("Running Initial Setup")
    
    try:
        # Import configuration manager
        sys.path.insert(0, str(Path(__file__).parent))
        from utils.config_manager import ConfigManager
        
        config = ConfigManager()
        config.load_config()
        
        print("✓ Configuration system initialized")
        print(f"✓ Config file: {config.user_config_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Setup failed: {e}")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")
    
    print("Next steps:")
    print("\n1. Launch the application:")
    print("   python main.py")
    
    print("\n2. Or create a virtual environment (recommended):")
    print("   python -m venv venv")
    print("   venv\\Scripts\\activate  # Windows")
    print("   source venv/bin/activate  # Linux/macOS")
    print("   python main.py")
    
    print("\n3. Read the documentation:")
    print("   Open README.md for detailed usage instructions")
    
    print("\n4. Configure the application:")
    print("   - Set paths in Settings menu")
    print("   - Add your first task")
    print("   - Schedule tasks as needed")
    
    print("\n" + "=" * 60)
    print("  Thank you for using Automation Hub!")
    print("=" * 60 + "\n")


def main():
    """Main setup function"""
    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  AUTOMATION HUB - SETUP & INSTALLATION  ".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60 + "\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Ask user if they want to proceed
    print("\nThis script will:")
    print("  1. Install required Python packages")
    print("  2. Create necessary directories")
    print("  3. Initialize configuration")
    
    response = input("\nContinue with setup? (Y/n): ").strip().lower()
    if response and response not in ('y', 'yes'):
        print("\nSetup cancelled.")
        sys.exit(0)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Run initial setup
    if not run_initial_setup():
        sys.exit(1)
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
