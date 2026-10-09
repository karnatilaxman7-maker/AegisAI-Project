"""
AegisAI: Intelligent Multimodal Emergency Detection System (Enhanced Version)
Real-time emergency detection through facial expressions and voice analysis
"""

import cv2
import mediapipe as mp
import numpy as np
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import sounddevice as sd
import speech_recognition as sr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import queue
import time
import os
import logging

# Import configuration
try:
    import config
    CONFIG_LOADED = True
except ImportError:
    CONFIG_LOADED = False
    print("Warning: config.py not found. Using default settings.")

class AegisAI:
    def __init__(self, root):
        self.root = root
        self.root.title("AegisAI - Emergency Detection System v2.0")
        self.root.geometry("1400x750")
        self.root.configure(bg="#1a1a2e")
        
        # Setup logging
        self.setup_logging()
        
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Emergency detection states
        self.emergency_detected = False
        self.last_emergency_time = 0
        self.fear_detected = False
        self.voice_emergency = False
        self.current_emotion = "Neutral"
        self.audio_text = "Initializing..."
        self.emergency_count = 0
        
        # Camera
        self.cap = None
        self.running = False
        
        # Load configuration
        self.load_configuration()
        
        # Emergency image directory
        if self.save_images:
            os.makedirs(self.image_path, exist_ok=True)
        
        # Audio queue for speech recognition
        self.audio_queue = queue.Queue()
        
        # Build UI
        self.build_ui()
        
        # Start systems
        self.start_camera()
        self.start_audio_monitoring()
        
        self.log("AegisAI System Initialized")
        
    def setup_logging(self):
        """Setup logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('aegis_ai.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AegisAI')
    
    def log(self, message, level='info'):
        """Log message"""
        if level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)
    
    def load_configuration(self):
        """Load configuration from config file or use defaults"""
        if CONFIG_LOADED:
            self.emergency_contacts = {
                'personal': config.PERSONAL_CONTACTS,
                'hospital': config.HOSPITAL_CONTACTS
            }
            self.email_config = {
                'sender': config.SENDER_EMAIL,
                'password': config.EMAIL_PASSWORD,
                'smtp_server': config.SMTP_SERVER,
                'smtp_port': config.SMTP_PORT
            }
            self.emergency_keywords = config.EMERGENCY_KEYWORDS
            self.cooldown_period = config.EMERGENCY_COOLDOWN
            self.save_images = config.SAVE_EMERGENCY_IMAGES
            self.image_path = config.EMERGENCY_IMAGE_PATH
            self.vehicle_info = config.VEHICLE_INFO
        else:
            # Default configuration
            self.emergency_contacts = {
                'personal': ['emergency1@example.com'],
                'hospital': ['hospital@example.com']
            }
            self.email_config = {
                'sender': 'your_email@gmail.com',
                'password': 'your_app_password',
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587
            }
            self.emergency_keywords = ['help', 'save', 'emergency', 'danger', 'accident']
            self.cooldown_period = 30
            self.save_images = True
            self.image_path = './emergency_captures/'
            self.vehicle_info = {}
        
    def build_ui(self):
        """Build the enhanced user interface"""
        # Title Frame
        title_frame = tk.Frame(self.root, bg="#0f3460", height=70)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🛡️ AegisAI Emergency Detection System v2.0",
            font=("Helvetica", 22, "bold"),
            fg="#e94560",
            bg="#0f3460"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Status indicator
        self.system_status_indicator = tk.Label(
            title_frame,
            text="● SYSTEM ACTIVE",
            font=("Helvetica", 12, "bold"),
            fg="#00ff00",
            bg="#0f3460"
        )
        self.system_status_indicator.pack(side=tk.RIGHT, padx=20)
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg="#1a1a2e")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left Panel - Video Feed
        left_panel = tk.Frame(content_frame, bg="#16213e", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        video_header = tk.Frame(left_panel, bg="#0f3460", height=40)
        video_header.pack(fill=tk.X)
        video_header.pack_propagate(False)
        
        video_label = tk.Label(video_header, text="📹 Live Camera Feed", 
                              font=("Helvetica", 13, "bold"), 
                              fg="#ffffff", bg="#0f3460")
        video_label.pack(pady=8)
        
        self.video_canvas = tk.Label(left_panel, bg="#000000")
        self.video_canvas.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        # Right Panel - Status Information
        right_panel = tk.Frame(content_frame, bg="#16213e", width=400, relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        right_panel.pack_propagate(False)
        
        status_header = tk.Frame(right_panel, bg="#0f3460", height=40)
        status_header.pack(fill=tk.X)
        status_header.pack_propagate(False)
        
        status_title = tk.Label(status_header, text="📊 System Dashboard", 
                               font=("Helvetica", 13, "bold"), 
                               fg="#ffffff", bg="#0f3460")
        status_title.pack(pady=8)
        
        # Emergency Status with larger alert
        emergency_frame = tk.LabelFrame(right_panel, text="🚨 Emergency Alert Status", 
                                       font=("Helvetica", 11, "bold"),
                                       fg="#e94560", bg="#16213e", bd=2)
        emergency_frame.pack(fill=tk.X, padx=15, pady=15)
        
        self.emergency_status = tk.Label(emergency_frame, text="● NORMAL", 
                                        font=("Helvetica", 20, "bold"),
                                        fg="#00ff00", bg="#16213e")
        self.emergency_status.pack(pady=15)
        
        self.emergency_count_label = tk.Label(emergency_frame, 
                                             text="Alerts Today: 0",
                                             font=("Helvetica", 9),
                                             fg="#a8a8a8", bg="#16213e")
        self.emergency_count_label.pack(pady=5)
        
        # Emotion Detection
        emotion_frame = tk.LabelFrame(right_panel, text="😊 Facial Emotion Analysis", 
                                     font=("Helvetica", 11, "bold"),
                                     fg="#ffffff", bg="#16213e", bd=2)
        emotion_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(emotion_frame, text="Current Emotion:", 
                font=("Helvetica", 9), fg="#a8a8a8", bg="#16213e").pack(anchor=tk.W, padx=10, pady=5)
        
        self.emotion_label = tk.Label(emotion_frame, text="Neutral", 
                                     font=("Helvetica", 16, "bold"),
                                     fg="#ffffff", bg="#16213e")
        self.emotion_label.pack(padx=10, pady=8)
        
        self.emotion_confidence = tk.Label(emotion_frame, text="Confidence: --", 
                                          font=("Helvetica", 8),
                                          fg="#a8a8a8", bg="#16213e")
        self.emotion_confidence.pack(pady=2)
        
        # Voice Detection
        voice_frame = tk.LabelFrame(right_panel, text="🎤 Voice Analysis", 
                                   font=("Helvetica", 11, "bold"),
                                   fg="#ffffff", bg="#16213e", bd=2)
        voice_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(voice_frame, text="Audio Monitor:", 
                font=("Helvetica", 9), fg="#a8a8a8", bg="#16213e").pack(anchor=tk.W, padx=10, pady=5)
        
        self.voice_label = tk.Label(voice_frame, text="Listening...", 
                                   font=("Helvetica", 10),
                                   fg="#00ff00", bg="#16213e", wraplength=350,
                                   justify=tk.LEFT)
        self.voice_label.pack(padx=10, pady=8)
        
        # System Log
        log_frame = tk.LabelFrame(right_panel, text="📝 System Log", 
                                 font=("Helvetica", 11, "bold"),
                                 fg="#ffffff", bg="#16213e", bd=2)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=8, 
            bg="#0a0a0a", 
            fg="#00ff00",
            font=("Courier", 8),
            wrap=tk.WORD
        )
        self.log_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.add_log_entry("System initialized successfully")
        
        # Control Buttons
        button_frame = tk.Frame(right_panel, bg="#16213e")
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        self.start_btn = tk.Button(button_frame, text="⏸ PAUSE MONITORING", 
                                   command=self.toggle_system,
                                   font=("Helvetica", 10, "bold"),
                                   bg="#e94560", fg="#ffffff",
                                   activebackground="#c93550",
                                   relief=tk.RAISED, bd=3,
                                   cursor="hand2",
                                   height=2)
        self.start_btn.pack(fill=tk.X, pady=5)
        
        test_btn = tk.Button(button_frame, text="📧 TEST ALERT SYSTEM", 
                           command=self.test_alert,
                           font=("Helvetica", 10, "bold"),
                           bg="#0f3460", fg="#ffffff",
                           activebackground="#0d2d50",
                           relief=tk.RAISED, bd=3,
                           cursor="hand2",
                           height=2)
        test_btn.pack(fill=tk.X, pady=5)
        
        settings_btn = tk.Button(button_frame, text="⚙ SETTINGS", 
                                command=self.open_settings,
                                font=("Helvetica", 10, "bold"),
                                bg="#16213e", fg="#ffffff",
                                activebackground="#0f1419",
                                relief=tk.RAISED, bd=3,
                                cursor="hand2")
        settings_btn.pack(fill=tk.X, pady=5)
        
    def add_log_entry(self, message):
        """Add entry to system log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        
    def start_camera(self):
        """Initialize and start camera feed"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.add_log_entry("ERROR: Camera not accessible")
                self.log("Camera initialization failed", 'error')
                messagebox.showerror("Camera Error", "Cannot access camera. Please check connections.")
                return
            
            self.running = True
            self.add_log_entry("Camera initialized successfully")
            self.update_frame()
        except Exception as e:
            self.log(f"Camera error: {e}", 'error')
            self.add_log_entry(f"ERROR: {str(e)}")
        
    def update_frame(self):
        """Update video frame and detect emotions"""
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Flip for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process face mesh
                results = self.face_mesh.process(rgb_frame)
                
                # Detect emotion
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        # Draw face mesh (subtle)
                        self.mp_drawing.draw_landmarks(
                            frame,
                            face_landmarks,
                            self.mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=self.mp_drawing.DrawingSpec(
                                color=(0, 255, 100), thickness=1, circle_radius=1
                            )
                        )
                        
                        # Analyze emotion
                        emotion, confidence = self.analyze_facial_expression(face_landmarks)
                        self.current_emotion = emotion
                        
                        # Check for fear/emergency
                        if emotion in ["Fear", "Shock", "Distress"] and confidence > 0.6:
                            if not self.fear_detected:
                                self.fear_detected = True
                                self.trigger_emergency("Facial Expression", frame)
                        else:
                            self.fear_detected = False
                        
                        # Display emotion on frame
                        emotion_color = (0, 255, 0) if emotion == "Neutral" else (0, 165, 255)
                        if emotion in ["Fear", "Shock", "Distress"]:
                            emotion_color = (0, 0, 255)
                        
                        cv2.putText(frame, f"{emotion} ({int(confidence*100)}%)", (10, 35),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1.0, emotion_color, 2)
                else:
                    cv2.putText(frame, "No Face Detected", (10, 35),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                
                # Add emergency overlay if detected
                if self.emergency_detected:
                    # Flashing red border
                    if int(time.time() * 3) % 2 == 0:
                        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), 
                                    (0, 0, 255), 15)
                    cv2.putText(frame, "!!! EMERGENCY DETECTED !!!", (50, 70),
                              cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3)
                
                # Add timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, timestamp, (10, frame.shape[0] - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Convert to PhotoImage for Tkinter
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = img.resize((700, 520), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image=img)
                
                self.video_canvas.configure(image=photo)
                self.video_canvas.image = photo
                
                # Update UI
                self.update_status_ui()
        
        # Schedule next update
        if self.running:
            self.root.after(30, self.update_frame)
    
    def analyze_facial_expression(self, face_landmarks):
        """Analyze facial landmarks to detect emotion with confidence"""
        landmarks = face_landmarks.landmark
        
        # Extract key points for emotion detection
        left_eye_top = landmarks[159].y
        left_eye_bottom = landmarks[145].y
        right_eye_top = landmarks[386].y
        right_eye_bottom = landmarks[374].y
        
        mouth_top = landmarks[13].y
        mouth_bottom = landmarks[14].y
        mouth_left = landmarks[61].x
        mouth_right = landmarks[291].x
        
        left_eyebrow = landmarks[70].y
        right_eyebrow = landmarks[300].y
        
        # Calculate metrics
        eye_openness = (left_eye_bottom - left_eye_top + right_eye_bottom - right_eye_top) / 2
        mouth_openness = mouth_bottom - mouth_top
        mouth_width = mouth_right - mouth_left
        eyebrow_height = (left_eyebrow + right_eyebrow) / 2
        
        # Emotion classification with confidence
        confidence = 0.5
        
        if eye_openness > 0.027 and mouth_openness > 0.045:
            emotion = "Fear"
            confidence = min(0.95, eye_openness * 30 + mouth_openness * 15)
        elif eye_openness > 0.032:
            emotion = "Shock"
            confidence = min(0.95, eye_openness * 25)
        elif mouth_openness > 0.055:
            emotion = "Distress"
            confidence = min(0.95, mouth_openness * 15)
        elif mouth_width > 0.26 and mouth_openness > 0.025:
            emotion = "Happy"
            confidence = 0.7
        elif eyebrow_height < 0.34:
            emotion = "Surprised"
            confidence = 0.6
        else:
            emotion = "Neutral"
            confidence = 0.8
        
        return emotion, confidence
    
    def start_audio_monitoring(self):
        """Start audio monitoring in separate thread"""
        audio_thread = threading.Thread(target=self.monitor_audio, daemon=True)
        audio_thread.start()
        self.add_log_entry("Audio monitoring started")
    
    def monitor_audio(self):
        """Monitor audio for emergency keywords"""
        recognizer = sr.Recognizer()
        
        try:
            microphone = sr.Microphone()
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.add_log_entry("Microphone calibrated")
            
            while self.running:
                try:
                    with microphone as source:
                        audio = recognizer.listen(source, timeout=3, phrase_time_limit=6)
                    
                    try:
                        text = recognizer.recognize_google(audio).lower()
                        self.audio_text = f'Heard: "{text}"'
                        
                        # Check for emergency keywords
                        detected_keywords = [kw for kw in self.emergency_keywords if kw in text]
                        if detected_keywords:
                            self.voice_emergency = True
                            self.add_log_entry(f"EMERGENCY KEYWORD: {detected_keywords[0]}")
                            self.trigger_emergency("Voice Command", None, text)
                        else:
                            self.voice_emergency = False
                            
                    except sr.UnknownValueError:
                        self.audio_text = "Listening... (no speech)"
                    except sr.RequestError as e:
                        self.audio_text = f"Audio service error: {e}"
                        self.log(f"Speech recognition error: {e}", 'error')
                        
                except Exception as e:
                    time.sleep(0.5)
                    
        except Exception as e:
            self.add_log_entry(f"Audio initialization error: {str(e)}")
            self.audio_text = "Audio system unavailable"
            self.log(f"Audio monitoring error: {e}", 'error')
    
    def trigger_emergency(self, trigger_type, frame=None, audio_text=None):
        """Trigger emergency alert with cooldown"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_emergency_time < self.cooldown_period:
            self.add_log_entry(f"Emergency detected but in cooldown period")
            return
        
        if not self.emergency_detected:
            self.emergency_detected = True
            self.last_emergency_time = current_time
            self.emergency_count += 1
            
            self.add_log_entry(f"🚨 EMERGENCY TRIGGERED: {trigger_type}")
            self.log(f"Emergency triggered: {trigger_type}", 'critical')
            
            # Save emergency frame if available
            emergency_image = None
            if frame is not None and self.save_images:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = os.path.join(self.image_path, f"emergency_{timestamp}.jpg")
                cv2.imwrite(image_path, frame)
                emergency_image = image_path
                self.add_log_entry(f"Emergency image saved: {image_path}")
            
            # Send emergency alerts
            threading.Thread(
                target=self.send_emergency_alert,
                args=(trigger_type, emergency_image, audio_text),
                daemon=True
            ).start()
            
            # Auto-reset after 10 seconds
            threading.Timer(10.0, self.reset_emergency).start()
    
    def send_emergency_alert(self, trigger_type, image_path=None, audio_text=None):
        """Send emergency alert via email"""
        try:
            self.add_log_entry("Sending emergency alerts...")
            
            # Determine severity and recipients
            is_serious = (trigger_type == "Facial Expression" and audio_text is not None) or \
                        trigger_type == "Voice Command"
            recipients = self.emergency_contacts['personal'].copy()
            
            if is_serious:
                recipients.extend(self.emergency_contacts['hospital'])
            
            # Create message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            subject = f"🚨 EMERGENCY ALERT - {trigger_type} - {timestamp}"
            
            vehicle_details = ""
            if self.vehicle_info:
                vehicle_details = f"""
Vehicle Information:
  Make: {self.vehicle_info.get('make', 'N/A')}
  Model: {self.vehicle_info.get('model', 'N/A')}
  Year: {self.vehicle_info.get('year', 'N/A')}
  License: {self.vehicle_info.get('license_plate', 'N/A')}
  Color: {self.vehicle_info.get('color', 'N/A')}
"""
            
            body = f"""
⚠️ EMERGENCY DETECTED BY AegisAI SYSTEM ⚠️

═══════════════════════════════════════════
ALERT DETAILS
═══════════════════════════════════════════
Timestamp: {timestamp}
Trigger Type: {trigger_type}
Severity: {'HIGH - Medical Emergency' if is_serious else 'MEDIUM'}
Detected Emotion: {self.current_emotion}
{f'Voice Detected: "{audio_text}"' if audio_text else ''}

{vehicle_details}

Location: [GPS coordinates would appear here if enabled]

═══════════════════════════════════════════

This is an automated emergency alert from the AegisAI 
in-vehicle safety system. Please respond immediately.

If this is a false alarm, please contact the vehicle occupant.

---
AegisAI Emergency Detection System v2.0
Powered by AI & Computer Vision
            """
            
            # Send email
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender']
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach image if available
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data, name=os.path.basename(image_path))
                    msg.attach(image)
            
            # Send via SMTP
            server = smtplib.SMTP(self.email_config['smtp_server'], 
                                 self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['sender'], self.email_config['password'])
            server.send_message(msg)
            server.quit()
            
            self.add_log_entry(f"✓ Alert sent to {len(recipients)} contacts")
            self.log(f"Emergency alert sent to {len(recipients)} recipients", 'info')
            
        except Exception as e:
            self.add_log_entry(f"✗ Alert failed: {str(e)}")
            self.log(f"Error sending emergency alert: {e}", 'error')
            messagebox.showerror("Alert Error", f"Failed to send emergency alert:\n{str(e)}")
    
    def reset_emergency(self):
        """Reset emergency state"""
        self.emergency_detected = False
        self.add_log_entry("Emergency state reset")
    
    def update_status_ui(self):
        """Update status labels in UI"""
        # Emergency status
        if self.emergency_detected:
            self.emergency_status.config(text="⚠️ EMERGENCY!", fg="#ff0000")
        else:
            self.emergency_status.config(text="● NORMAL", fg="#00ff00")
        
        # Emergency count
        self.emergency_count_label.config(text=f"Alerts Today: {self.emergency_count}")
        
        # Emotion
        emotion_colors = {
            "Fear": "#ff0000",
            "Shock": "#ff4500",
            "Distress": "#ff6347",
            "Happy": "#00ff00",
            "Surprised": "#ffff00",
            "Neutral": "#ffffff"
        }
        self.emotion_label.config(
            text=self.current_emotion,
            fg=emotion_colors.get(self.current_emotion, "#ffffff")
        )
        
        # Voice
        voice_color = "#ff0000" if self.voice_emergency else "#00ff00"
        self.voice_label.config(text=self.audio_text, fg=voice_color)
    
    def toggle_system(self):
        """Toggle system on/off"""
        if self.running:
            self.running = False
            self.start_btn.config(text="▶ RESUME MONITORING", bg="#00aa00")
            self.system_status_indicator.config(text="⏸ SYSTEM PAUSED", fg="#ffff00")
            self.add_log_entry("System paused by user")
        else:
            self.running = True
            self.start_btn.config(text="⏸ PAUSE MONITORING", bg="#e94560")
            self.system_status_indicator.config(text="● SYSTEM ACTIVE", fg="#00ff00")
            self.add_log_entry("System resumed by user")
            self.update_frame()
    
    def test_alert(self):
        """Test emergency alert system"""
        response = messagebox.askyesno(
            "Test Alert",
            "This will send a test emergency alert to all configured contacts.\n\nProceed?"
        )
        if response:
            self.add_log_entry("Sending test alert...")
            self.trigger_emergency("System Test", None, "This is a test alert")
            messagebox.showinfo("Test Alert", "Test alert sent successfully!\nCheck recipient inboxes.")
    
    def open_settings(self):
        """Open settings dialog"""
        messagebox.showinfo(
            "Settings",
            "To configure AegisAI:\n\n" +
            "1. Edit the 'config.py' file\n" +
            "2. Set your emergency contacts\n" +
            "3. Configure email settings\n" +
            "4. Adjust sensitivity thresholds\n" +
            "5. Restart the application\n\n" +
            "See config.py for detailed instructions."
        )
    
    def cleanup(self):
        """Cleanup resources"""
        self.running = False
        self.add_log_entry("Shutting down system...")
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.log("AegisAI system shutdown", 'info')

def main():
    """Main entry point"""
    root = tk.Tk()
    app = AegisAI(root)
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Stop AegisAI Emergency Detection System?"):
            app.cleanup()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()