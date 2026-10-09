#!/usr/bin/env python3
"""
AegisAI Launcher
Simple launcher with system check and error handling
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required = ['cv2', 'mediapipe', 'PIL', 'speech_recognition', 'numpy', 'tkinter']
    missing = []
    
    print("\nChecking dependencies...")
    for package in required:
        try:
            if package == 'cv2':
                __import__('cv2')
            elif package == 'PIL':
                __import__('PIL')
            elif package == 'tkinter':
                __import__('tkinter')
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT FOUND")
            missing.append(package)
    
    if missing:
        print("\n❌ Missing dependencies detected!")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies installed")
    return True

def check_config():
    """Check if config file exists and is configured"""
    if not os.path.exists('config.py'):
        print("\n⚠️  WARNING: config.py not found")
        print("   Using default configuration")
        return True
    
    print("✓ Configuration file found")
    
    # Check if config is setup
    try:
        import config
        if config.SENDER_EMAIL == 'your_email@gmail.com':
            print("\n⚠️  WARNING: Email not configured in config.py")
            print("   Emergency alerts will NOT be sent")
            response = input("   Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return False
    except Exception as e:
        print(f"\n⚠️  Warning reading config: {e}")
    
    return True

def launch_app():
    """Launch the main application"""
    print("\n" + "="*50)
    print("🛡️  Launching AegisAI Emergency Detection System")
    print("="*50 + "\n")
    
    try:
        if os.path.exists('aegis_ai_enhanced.py'):
            print("Starting enhanced version...")
            import aegis_ai_enhanced
            aegis_ai_enhanced.main()
        elif os.path.exists('aegis_ai_main.py'):
            print("Starting basic version...")
            import aegis_ai_main
            aegis_ai_main.main()
        else:
            print("❌ ERROR: Main application file not found")
            print("   Please ensure aegis_ai_enhanced.py or aegis_ai_main.py exists")
            return False
    except KeyboardInterrupt:
        print("\n\n⏹️  AegisAI stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nFor help, see README.md or check the troubleshooting section")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("="*50)
    print("   AegisAI Emergency Detection System")
    print("   System Pre-Flight Check")
    print("="*50 + "\n")
    
    # Run checks
    if not check_python_version():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    if not check_dependencies():
        print("\n📦 Install dependencies:")
        print("   pip install -r requirements.txt")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    if not check_config():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("\n✓ All system checks passed!")
    input("Press Enter to launch AegisAI...")
    
    # Launch
    success = launch_app()
    
    if not success:
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)