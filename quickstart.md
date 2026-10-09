# AegisAI - Quick Start Guide

## 🎯 Get Started in 5 Minutes

### Option 1: Easy Way (Recommended for Beginners)

#### Windows Users:
1. **Double-click** `start_aegis_windows.bat`
2. Follow on-screen prompts
3. Done! 🎉

#### Mac/Linux Users:
1. **Right-click** `start_aegis.sh` → Open Terminal
2. Type: `bash start_aegis.sh`
3. Done! 🎉

---

### Option 2: Manual Way (For Advanced Users)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure settings
# Edit config.py with your email and contacts

# 3. Run the app
python aegis_ai_enhanced.py
```

---

## ⚙️ Initial Setup (IMPORTANT!)

### Before First Run:

**1. Configure Email (Required for alerts)**
   - Open `config.py` in any text editor
   - Find this section:
   ```python
   SENDER_EMAIL = 'akshayamorishetty@gmail.com'
   EMAIL_PASSWORD = 'dsaf lbpt bdvx sdpn'
   ```
   - Replace with YOUR Gmail address
   - For password, use Gmail App Password (see instructions below)

**2. Add Emergency Contacts**
   ```python
   PERSONAL_CONTACTS = [
       'sonuakshu.12@gmail.com',
       'friend@gmail.com'
   ]
   
   HOSPITAL_CONTACTS = [
       'emergency@hospital.com'
   ]
   ```

**3. Test Everything**
   - Launch the app
   - Click "TEST ALERT SYSTEM"
   - Check if emergency contacts receive email

---

## 📧 Gmail App Password Setup

**Why?** Gmail doesn't allow apps to use your regular password for security.

**Steps:**
1. Go to: https://myaccount.google.com/
2. Click **Security** (left sidebar)
3. Enable **2-Step Verification** (if not already)
4. Go back to **Security**
5. Click **App Passwords**
6. Select **Mail** and **Other (Custom name)**
7. Type "AegisAI"
8. Click **Generate**
9. Copy the 16-character password
10. Paste it in `config.py` as `EMAIL_PASSWORD`

**Important:** Use the 16-character code, NOT your regular password!

---

## 🎮 Using AegisAI

### Interface Overview:
```
┌─────────────────────────────────────────┐
│  🛡️ AegisAI Detection System           │
├─────────────────────┬───────────────────┤
│                     │  🚨 Emergency     │
│   📹 Camera Feed    │     ● NORMAL      │
│                     │                   │
│   [Live Video]      │  😊 Emotion       │
│                     │     Neutral       │
│                     │                   │
│                     │  🎤 Voice         │
│                     │     Listening...  │
│                     │                   │
│                     │  📝 System Log    │
│                     │  [Recent events]  │
│                     │                   │
│                     │  [⏸ PAUSE]        │
│                     │  [📧 TEST]        │
└─────────────────────┴───────────────────┘
```

### What Triggers Emergency:

**Facial Expressions:**
- Wide open eyes + open mouth = Fear
- Very wide eyes = Shock
- Wide open mouth = Distress

**Voice Commands:**
- "Help!"
- "Save me!"
- "Emergency!"
- "Danger!"
- Any loud screaming

### When Emergency Detected:
1. ⚠️ Screen flashes red border
2. 📸 Captures photo
3. 📧 Sends email to all contacts
4. 🔊 Shows alert on screen

---

## 🧪 Testing Your Setup

### Test 1: Camera
✅ Do you see yourself on screen?
✅ Is there a green mesh on your face?

### Test 2: Emotion Detection
- Make different faces
- Watch the emotion label change
- Try: Happy, Surprised, Fear (wide eyes + mouth)

### Test 3: Voice Recognition
- Say "Hello" → Should appear in voice box
- Say "Help" → Should trigger emergency!

### Test 4: Email Alerts
- Click "TEST ALERT SYSTEM"
- Check email inbox
- ✅ Should receive test alert

---

## 🚗 In-Car Setup

### Mounting:
1. Position device facing driver
2. Mount at dashboard level
3. Angle for clear face view
4. Ensure stable power (car charger)

### Before Driving:
- ✅ Test camera view
- ✅ Test voice detection
- ✅ Verify alerts work
- ✅ Inform emergency contacts

### During Drive:
- Keep app running
- Ensure good lighting
- Minimize background noise
- Don't cover camera

---

## ❓ Common Questions

**Q: Will it drain my battery?**
A: Yes, use car charger or power bank for long trips

**Q: What if I don't have internet?**
A: Email alerts won't work, but detection still runs

**Q: Can I adjust sensitivity?**
A: Yes! Edit thresholds in config.py

**Q: Will it work at night?**
A: Works best with cabin light on

**Q: What about false alarms?**
A: There's a 30-second cooldown between alerts

**Q: Is my data private?**
A: Yes! Nothing leaves your computer except email alerts

---

## 🐛 Quick Fixes

**Camera not working?**
```bash
# Check camera permissions
# Windows: Settings → Privacy → Camera
# Mac: System Preferences → Security → Camera
# Allow access for Terminal/Python
```

**Voice not detected?**
```bash
# Check microphone permissions
# Speak louder and clearer
# Reduce background noise
```

**Email not sending?**
```bash
# Double-check config.py
# Verify App Password (not regular password!)
# Check internet connection
```

**App won't start?**
```bash
# Make sure you installed dependencies:
pip install -r requirements.txt

# Try launcher:
python launcher.py
```

---

## 🎓 Tips for Best Results

### Lighting:
- ✅ Face the window/light
- ✅ Turn on cabin light at night
- ❌ Avoid backlighting

### Positioning:
- ✅ Camera at eye level
- ✅ 1-2 feet away from face
- ✅ Clear, unobstructed view

### Voice:
- ✅ Speak clearly
- ✅ Minimize background noise
- ✅ Radio/music at low volume

### General:
- ✅ Update emergency contacts regularly
- ✅ Test monthly
- ✅ Keep device charged
- ✅ Inform passengers about system

---

## 📞 Need Help?

1. Check **README.md** for detailed guide
2. Review error messages in system log
3. Look at **Troubleshooting** section in README
4. Verify all configuration settings

---

## ✅ Daily Checklist

Before Each Trip:
- [ ] AegisAI running
- [ ] Camera showing video
- [ ] Face detection working
- [ ] Voice detection active
- [ ] Internet connected
- [ ] Device charging
- [ ] Emergency contacts updated

---

## 🔐 Safety Reminders

- ⚠️ This is an **assistance tool**, not replacement for 911
- ⚠️ Always drive safely and attentively
- ⚠️ Inform emergency contacts they may receive alerts
- ⚠️ Test regularly to ensure functionality
- ⚠️ Keep emergency numbers accessible

---

## 🎉 You're All Set!

**Ready to go?** Just run:
- Windows: `start_aegis_windows.bat`
- Mac/Linux: `bash start_aegis.sh`
- Or: `python aegis_ai_enhanced.py`

**Stay safe on the road!** 🛡️🚗

---

*AegisAI - Your AI Safety Guardian*