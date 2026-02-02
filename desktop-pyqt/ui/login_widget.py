"""
Modern Login Widget

Clean, professional login screen without visual artifacts
"""

import os
import requests
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont

from .style_tokens import *


class ModernLoginWidget(QWidget):
    """
    Modern login widget with clean design
    
    Features:
    - No gradient artifacts (solid background)
    - Centered card layout
    - Professional typography
    - Clear visual feedback
    - Demo credentials display
    """
    
    loginSuccess = pyqtSignal(str)  # Emits token on successful login
    
    def __init__(self, api_url="http://127.0.0.1:8000", parent=None):
        super().__init__(parent)
        self.api_url = api_url
        self.setObjectName("ModernLoginWidget")
        self.setup_ui()
        self.load_stylesheet()
        
    def setup_ui(self):
        """Build the login interface"""
        # Main layout - center everything
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Horizontal centering container
        h_container = QHBoxLayout()
        h_container.addStretch()
        
        # Login card
        self.card = QFrame()
        self.card.setObjectName("loginCard")
        self.card.setFixedWidth(420)
        self.card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(SPACING_MD)
        card_layout.setContentsMargins(SPACING_2XL, SPACING_2XL, SPACING_2XL, SPACING_2XL)
        
        # App icon/logo
        logo = QLabel("⚙️")
        logo.setObjectName("appLogo")
        logo.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(logo)
        
        # Title
        title = QLabel("Equipment Visualizer")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Sign in to access your dashboard")
        subtitle.setObjectName("loginSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(SPACING_LG)
        
        # Demo credentials box
        demo_box = QFrame()
        demo_box.setObjectName("demoBox")
        demo_layout = QVBoxLayout(demo_box)
        demo_layout.setContentsMargins(SPACING_MD, SPACING_SM, SPACING_MD, SPACING_SM)
        
        demo_title = QLabel("🎯 Demo Credentials")
        demo_title.setObjectName("demoTitle")
        demo_layout.addWidget(demo_title)
        
        demo_text = QLabel("Username: <b>admin</b> | Password: <b>admin123</b>")
        demo_text.setObjectName("demoText")
        demo_layout.addWidget(demo_text)
        
        card_layout.addWidget(demo_box)
        
        card_layout.addSpacing(SPACING_MD)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setObjectName("inputLabel")
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setText("admin")  # Pre-fill demo
        card_layout.addWidget(self.username_input)
        
        card_layout.addSpacing(SPACING_SM)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setObjectName("inputLabel")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText("admin123")  # Pre-fill demo
        self.password_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.password_input)
        
        card_layout.addSpacing(SPACING_LG)
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.setObjectName("primaryButton")
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_button)
        
        # Status message label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        card_layout.addWidget(self.status_label)
        
        h_container.addWidget(self.card)
        h_container.addStretch()
        
        main_layout.addStretch()
        main_layout.addLayout(h_container)
        main_layout.addStretch()
        
    def load_stylesheet(self):
        """Load QSS stylesheet"""
        qss_path = os.path.join(os.path.dirname(__file__), 'modern_login.qss')
        try:
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Warning: Could not load stylesheet: {e}")
            
    def show_status(self, message, status_type="info"):
        """
        Display status message
        
        Args:
            message: Text to display
            status_type: 'error', 'success', or 'info'
        """
        self.status_label.setText(message)
        
        if status_type == "error":
            self.status_label.setObjectName("errorLabel")
        elif status_type == "success":
            self.status_label.setObjectName("successLabel")
        else:
            self.status_label.setObjectName("infoLabel")
        
        # Reapply stylesheet for object name change
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_label.show()
        
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_status("⚠️ Please enter both username and password", "error")
            return
        
        # Disable button and show loading state
        self.login_button.setEnabled(False)
        self.login_button.setText("Signing in...")
        self.show_status("🔄 Connecting to server...", "info")
        
        try:
            # Call login API
            response = requests.post(
                f"{self.api_url}/api/login/",
                json={"username": username, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('token')
                if token:
                    self.show_status("✅ Login successful!", "success")
                    self.loginSuccess.emit(token)
                else:
                    self.show_status("❌ Invalid response from server", "error")
                    self.reset_button()
            else:
                error_msg = response.json().get('error', 'Invalid credentials')
                self.show_status(f"❌ {error_msg}", "error")
                self.reset_button()
                
        except requests.exceptions.ConnectionError:
            self.show_status("❌ Cannot connect to server. Is the backend running?", "error")
            self.reset_button()
        except requests.exceptions.Timeout:
            self.show_status("❌ Request timeout. Server is not responding.", "error")
            self.reset_button()
        except Exception as e:
            self.show_status(f"❌ Error: {str(e)}", "error")
            self.reset_button()
            
    def reset_button(self):
        """Reset login button to normal state"""
        self.login_button.setEnabled(True)
        self.login_button.setText("Sign In")
