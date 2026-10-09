# AegisAI Configuration File
# Edit this file to set up your emergency contacts and email settings

# ==============================================================================
# EMERGENCY CONTACTS CONFIGURATION
# ==============================================================================

# Personal Emergency Contacts (will be notified for all emergencies)
PERSONAL_CONTACTS = [
    'rithwickreddy64@gmail.com',
    
]

# Hospital/Medical Emergency Contacts (notified for serious emergencies)
HOSPITAL_CONTACTS = [
    'sonuakshu.12@gmail.com',
]

# ==============================================================================
# EMAIL CONFIGURATION
# ==============================================================================

# Sender Email (Gmail recommended)
SENDER_EMAIL = 'akshayamorishetty@gmail.com'

# App Password (for Gmail, generate at: https://myaccount.google.com/apppasswords)
# DO NOT use your regular Gmail password
EMAIL_PASSWORD = 'dsaf lbpt bdvx sdpn'

# SMTP Server Settings (default for Gmail)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# ==============================================================================
# DETECTION SENSITIVITY SETTINGS
# ==============================================================================

# Facial Expression Thresholds (0.0 to 1.0, higher = more sensitive)
FEAR_SENSITIVITY = 0.7
SHOCK_SENSITIVITY = 0.75
DISTRESS_SENSITIVITY = 0.7

# Voice Detection Keywords (add more emergency words if needed)
EMERGENCY_KEYWORDS = [
    'help',
    'save',
    'emergency',
    'danger',
    'accident',
    'crash',
    'stop'
]

# Audio sensitivity (0.0 to 1.0, higher = more sensitive)
AUDIO_SENSITIVITY = 0.6

# ==============================================================================
# SYSTEM SETTINGS
# ==============================================================================

# Camera settings
CAMERA_INDEX = 0  # 0 for default camera, change if using external camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Emergency cooldown (seconds before another alert can be sent)
EMERGENCY_COOLDOWN = 30

# Auto-save emergency images
SAVE_EMERGENCY_IMAGES = True
EMERGENCY_IMAGE_PATH = './emergency_captures/'

# ==============================================================================
# VEHICLE INFORMATION (Optional - for emergency alerts)
# ==============================================================================

VEHICLE_INFO = {
    'make': 'Toyota',
    'model': 'Camry',
    'year': '2023',
    'license_plate': 'ABC-1234',
    'color': 'Silver'
}

# GPS Tracking (if available)
ENABLE_GPS = False  # Set to True if you have GPS module
GPS_UPDATE_INTERVAL = 5  # seconds

# ==============================================================================
# LOGGING SETTINGS
# ==============================================================================

ENABLE_LOGGING = True
LOG_FILE_PATH = './aegis_ai.log'
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL