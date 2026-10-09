# AegisAI Emergency Detection System - Installation Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Hardware
- **Camera**: Built-in webcam or USB camera
- **Microphone**: Built-in or external microphone
- **RAM**: Minimum 4GB (8GB recommended)
- **Processor**: Dual-core CPU or better

### Software
- **Python**: Version 3.8 - 3.11 (recommended: 3.10)
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux

---

## 📦 Installation Steps

### Step 1: Install Python
If you don't have Python installed:

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer and **check "Add Python to PATH"**
3. Verify: Open Command Prompt and type `python --version`

**macOS:**
```bash
# Using Homebrew
brew install python@3.10
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-dev
```

### Step 2: Install System Dependencies

**Windows:**
- No additional system dependencies needed

**macOS:**
```bash
brew install portaudio
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev
sudo apt-get install python3-tk
sudo apt-get install libopencv-dev
```

### Step 3: Create Project Directory
```bash
# Create and navigate to project folder
mkdir AegisAI
cd AegisAI

# Copy all project files here:
# - aegis_ai_enhanced.py
# - config.py
# - requirements.txt
# - README.md (this file)
```

### Step 4: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv aegis_env

# Activate it:
# Windows:
aegis_env\Scripts\activate

# macOS/Linux:
source aegis_env/bin/activate
```

### Step 5: Install Python Dependencies

**Method 1: Using requirements.txt (Recommended)**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Method 2: Manual Installation**
```bash
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.8
pip install Pillow==10.1.0
pip install SpeechRecognition==3.10.0
pip install numpy==1.24.3
pip install sounddevice==0.4.6
```

**For PyAudio (audio input):**

**Windows:**
```bash
pip install pyaudio
# If that fails:
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
pip install pyaudio
```

**Linux:**
```bash
pip install pyaudio
# If that fails, install from apt:
sudo apt-get install python3-pyaudio
```

---

## ⚙️ Configuration

### Step 1: Edit config.py

Open `config.py` in a text editor and configure:

#### 1. Emergency Contacts
```python
PERSONAL_CONTACTS = [
    'your_family@gmail.com',
    'friend@gmail.com'
]

HOSPITAL_CONTACTS = [
    'hospital@example.com'
]
```

#### 2. Email Settings (CRITICAL!)

**For Gmail:**
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Navigate to Security → 2-Step Verification (enable if not already)
3. Go to Security → App Passwords
4. Generate new app password for "Mail"
5. Copy the 16-character password

**Update config.py:**
```python
SENDER_EMAIL = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_16_char_app_password'  # NOT your regular password!
```

#### 3. Vehicle Information (Optional)
```python
VEHICLE_INFO = {
    'make': 'Toyota',
    'model': 'Camry',
    'year': '2023',
    'license_plate': 'ABC-1234',
    'color': 'Silver'
}
```

#### 4. Adjust Sensitivity (Optional)
```python
FEAR_SENSITIVITY = 0.7  # 0.0-1.0, higher = more sensitive
EMERGENCY_KEYWORDS = ['help', 'save', 'emergency', 'danger']
```

---

## 🚀 Running the Application

### Method 1: Run Enhanced Version (Recommended)
```bash
# Make sure virtual environment is activated
python aegis_ai_enhanced.py
```

### Method 2: Run Basic Version
```bash
python aegis_ai_main.py
```

### First Time Setup Checklist
Before running, verify:
- ✅ Camera is connected and working
- ✅ Microphone is connected and working
- ✅ config.py is configured with valid email
- ✅ Emergency contacts are set
- ✅ Internet connection is available (for email)

---

## 🔧 Troubleshooting

### Camera Issues

**Problem: "Camera not accessible"**
```bash
# Check camera:
# Windows: Device Manager → Cameras
# macOS: System Preferences → Security → Camera
# Linux: ls /dev/video*

# Grant camera permissions to Terminal/Python
```

**Problem: Black screen or no video**
- Try changing camera index in config.py: `CAMERA_INDEX = 1`
- Restart application
- Check if another app is using camera

### Audio Issues

**Problem: "Audio system unavailable"**
```bash
# Test microphone:
# Windows: Settings → Sound → Input
# macOS: System Preferences → Sound → Input
# Linux: arecord -l

# Reinstall PyAudio:
pip uninstall pyaudio
pip install pyaudio
```

**Problem: Speech recognition not working**
- Check internet connection (Google Speech API needs internet)
- Speak clearly and loudly
- Check microphone permissions
- Try adjusting `AUDIO_SENSITIVITY` in config.py

### Email Issues

**Problem: "Authentication failed"**
- ✅ Using App Password (NOT regular password)?
- ✅ 2-Step Verification enabled on Gmail?
- ✅ App Password copied correctly (no spaces)?

**Problem: "SMTP connection failed"**
- Check internet connection
- Firewall may be blocking port 587
- Try alternative SMTP settings

**Problem: Emails not received**
- Check spam/junk folders
- Verify email addresses in config.py
- Test with "Test Alert" button

### Performance Issues

**Problem: Laggy video or slow detection**
```python
# In config.py, reduce camera resolution:
CAMERA_WIDTH = 480
CAMERA_HEIGHT = 360
```

**Problem: High CPU usage**
- Close other applications
- Reduce MediaPipe accuracy (in code)
- Use lighter Python version

### Import Errors

**Problem: "ModuleNotFoundError"**
```bash
# Reinstall specific module:
pip install --force-reinstall [module_name]

# Or reinstall everything:
pip install -r requirements.txt --force-reinstall
```

### Common Errors

**"No module named 'cv2'"**
```bash
pip install opencv-python
```

**"No module named 'mediapipe'"**
```bash
pip install mediapipe
```

**"tkinter not found"**
```bash
# Windows/macOS: Reinstall Python with tkinter
# Linux:
sudo apt-get install python3-tk
```

---

## 📊 Testing the System

### 1. Test Camera
- Launch application
- Verify video feed appears
- Check face mesh overlay appears

### 2. Test Emotion Detection
- Make exaggerated facial expressions
- Watch emotion label change
- Try fear/shock face (wide eyes + open mouth)

### 3. Test Voice Detection
- Say "help" loudly
- Say "emergency"
- Check if system detects keywords

### 4. Test Emergency Alert
- Click "TEST ALERT SYSTEM" button
- Check if email is sent
- Verify recipients receive it

---

## 🎯 Usage Tips

### For Best Detection:
1. **Lighting**: Good front lighting on face
2. **Position**: Face camera directly, 1-2 feet away
3. **Voice**: Speak clearly, loudly
4. **Environment**: Minimize background noise

### In Vehicle Setup:
1. Mount device facing driver seat
2. Position at dashboard level
3. Ensure stable power supply
4. Test before first drive

### Emergency Testing:
- Practice emergency scenarios
- Test with passengers
- Verify alert delivery
- Update contacts regularly

---

## 📞 Support

### Getting Help:
1. Check this README
2. Review error messages in system log
3. Check Python/package versions
4. Verify configuration settings

### Report Issues:
- Include error messages
- Specify OS and Python version
- Describe steps to reproduce

---

## 🔐 Security Notes

### Email Security:
- ⚠️ NEVER share your App Password
- ⚠️ NEVER commit config.py with credentials to Git
- Use environment variables for production
- Rotate App Passwords periodically

### Privacy:
- Emergency images stored locally
- No data sent to third parties (except email)
- Configure data retention as needed

---

## 📝 Quick Start Commands

```bash
# Full setup from scratch:
python -m venv aegis_env
source aegis_env/bin/activate  # or aegis_env\Scripts\activate on Windows
pip install -r requirements.txt
# Edit config.py with your settings
python aegis_ai_enhanced.py
```

---

## ✅ Pre-Flight Checklist

Before each use:
- [ ] Camera working
- [ ] Microphone working
- [ ] Internet connected
- [ ] Config updated
- [ ] Test alert sent successfully
- [ ] Emergency contacts notified of system activation

---

**🛡️ AegisAI - Your AI Safety Guardian**

*Stay Safe. Drive Protected.*