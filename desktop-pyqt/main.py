"""
Chemical Equipment Visualizer - Desktop Application (PyQt5)
PHASE 3 IMPROVED - Professional UI/UX

WHAT: Desktop version of the equipment visualizer
WHY: Some users prefer desktop applications
HOW: Uses PyQt5 for GUI and requests for API calls

UX IMPROVEMENTS:
✅ Modern Qt stylesheets (matching web design)
✅ Gradient stat cards
✅ Better spacing and layout
✅ Professional colors and fonts
✅ Improved charts with styling
"""

import sys
import os
import json
import requests
import configparser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                              QFileDialog, QTableWidget, QTableWidgetItem, 
                              QMessageBox, QTabWidget, QListWidget, QListWidgetItem,
                              QTextEdit, QGroupBox, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Import custom styles
try:
    from styles import MAIN_STYLESHEET, LOGIN_STYLESHEET, get_stat_card_stylesheet, STAT_GRADIENTS, COLORS
except ImportError:
    # Fallback if styles.py not found
    MAIN_STYLESHEET = ""
    LOGIN_STYLESHEET = ""
    COLORS = {}

# API Configuration
# Load from config.ini if it exists, otherwise use localhost
def load_config():
    """Load configuration from config.ini"""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    
    if os.path.exists(config_path):
        config.read(config_path)
        return config.get('API', 'backend_url', fallback='http://localhost:8000/api')
    else:
        return os.environ.get('BACKEND_URL', 'http://localhost:8000/api')

API_BASE_URL = load_config()


class APIClient:
    """
    API Client for backend communication
    
    WHAT: Handles all API requests to the Django backend
    WHY: Centralizes API logic
    HOW: Uses requests library to make HTTP calls
    """
    
    def __init__(self):
        self.token = None
        self.session = requests.Session()
    
    def set_token(self, token):
        """Set authentication token"""
        self.token = token
        self.session.headers.update({'Authorization': f'Token {token}'})
    
    def login(self, username, password):
        """Login user and get token"""
        url = f'{API_BASE_URL}/login/'
        response = requests.post(url, json={'username': username, 'password': password})
        response.raise_for_status()
        data = response.json()
        self.set_token(data['token'])
        return data
    
    def upload_csv(self, file_path):
        """Upload CSV file"""
        url = f'{API_BASE_URL}/upload-csv/'
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(url, files=files)
        response.raise_for_status()
        return response.json()
    
    def get_upload_history(self):
        """Get upload history"""
        url = f'{API_BASE_URL}/upload-history/'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_dataset_summary(self, dataset_id):
        """Get dataset summary"""
        url = f'{API_BASE_URL}/datasets/{dataset_id}/summary/'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def download_pdf(self, dataset_id, save_path):
        """Download PDF report"""
        url = f'{API_BASE_URL}/datasets/{dataset_id}/download-pdf/'
        response = self.session.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return save_path


class LoginWindow(QWidget):
    """
    Login Window
    
    WHAT: Window for user authentication
    WHY: Users need to log in to use the app
    HOW: Collects credentials and calls API
    """
    
    login_successful = pyqtSignal(object)  # Signal when login succeeds
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Login - Equipment Visualizer')
        self.setFixedSize(460, 520)
        
        # Apply gradient background
        self.setStyleSheet(LOGIN_STYLESHEET)
        
        # Main layout with margins
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Center the login card
        main_layout.addStretch()
        
        # Login card container
        card = QWidget()
        card.setObjectName('loginCard')
        card_layout = QVBoxLayout()
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(40, 40, 40, 40)
        
        # App Icon
        icon_label = QLabel('⚗️')
        icon_label.setObjectName('appIcon')
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)
        
        # Title
        title = QLabel('Welcome Back')
        title.setObjectName('loginTitle')
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel('Sign in to Equipment Visualizer')
        subtitle.setObjectName('loginSubtitle')
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(10)
        
        # Username
        username_label = QLabel('👤 Username')
        card_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setMinimumHeight(40)
        card_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel('🔒 Password')
        card_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.password_input)
        
        card_layout.addSpacing(10)
        
        # Login button
        self.login_btn = QPushButton('🚀 Sign In')
        self.login_btn.setMinimumHeight(44)
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)
        
        # Demo credentials info
        demo_widget = QWidget()
        demo_layout = QVBoxLayout()
        demo_layout.setContentsMargins(12, 12, 12, 12)
        demo_widget.setStyleSheet(f'''
            QWidget {{
                background-color: #fef3c7;
                border: 1px solid #fbbf24;
                border-radius: 6px;
            }}
        ''')
        
        demo_title = QLabel('🎯 Demo Account')
        demo_title.setStyleSheet('font-weight: 600; color: #92400e; background: transparent;')
        demo_layout.addWidget(demo_title)
        
        demo_text = QLabel('Username: <b>admin</b><br>Password: <b>admin123</b>')
        demo_text.setStyleSheet('color: #92400e; font-size: 12px; background: transparent;')
        demo_layout.addWidget(demo_text)
        
        demo_widget.setLayout(demo_layout)
        card_layout.addWidget(demo_widget)
        
        # Status label
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        card_layout.addWidget(self.status_label)
        
        card.setLayout(card_layout)
        main_layout.addWidget(card)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.status_label.setText('⚠️ Please enter both username and password')
            self.status_label.setObjectName('errorLabel')
            self.status_label.setStyle(self.status_label.style())
            return
        
        self.login_btn.setEnabled(False)
        self.status_label.setText('🔄 Signing in...')
        self.status_label.setObjectName('infoLabel')
        self.status_label.setStyle(self.status_label.style())
        
        try:
            user_data = self.api_client.login(username, password)
            self.login_successful.emit(user_data)
            self.close()
        except requests.exceptions.RequestException as e:
            error_msg = '⚠️ Invalid credentials or server error'
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = '⚠️ ' + error_data.get('error', error_msg)
                except:
                    pass
            
            self.status_label.setText(error_msg)
            self.status_label.setObjectName('errorLabel')
            self.status_label.setStyle(self.status_label.style())
            self.login_btn.setEnabled(True)


class ChartWidget(QWidget):
    """
    Chart Widget using Matplotlib - PHASE 3 IMPROVED
    
    WHAT: Displays charts in the PyQt5 window
    WHY: Users need to see visual data
    HOW: Embeds Matplotlib figure in Qt widget with professional styling
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(10, 5), facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def plot_bar_chart(self, labels, values, title='Equipment Type Distribution'):
        """Plot a professional bar chart matching web design"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Use primary blue color
        bars = ax.bar(labels, values, color='#3b82f6', edgecolor='#2563eb', linewidth=1.5)
        
        # Styling
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color='#1f2937')
        ax.set_xlabel('Equipment Type', fontsize=12, fontweight='600', color='#1f2937')
        ax.set_ylabel('Count', fontsize=12, fontweight='600', color='#1f2937')
        
        # Grid for readability
        ax.grid(axis='y', alpha=0.2, linestyle='--')
        ax.set_axisbelow(True)
        
        # Rotate x labels
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Styling for axes
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e5e7eb')
        ax.spines['bottom'].set_color('#e5e7eb')
        
        # Tick colors
        ax.tick_params(colors='#6b7280', which='both')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_pie_chart(self, labels, values, title='Equipment Type Distribution'):
        """Plot a professional pie chart matching web design"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Professional color palette
        colors = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#ec4899']
        
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        
        # Style the text
        for text in texts:
            text.set_color('#1f2937')
            text.set_fontsize(11)
            text.set_fontweight('600')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color='#1f2937')
        
        self.figure.tight_layout()
        self.canvas.draw()


class MainWindow(QMainWindow):
    """
    Main Application Window
    
    WHAT: Main window with all features
    WHY: Central hub for all functionality
    HOW: Organizes components in tabs
    """
    
    def __init__(self, api_client, user_data):
        super().__init__()
        self.api_client = api_client
        self.user_data = user_data
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f'Equipment Visualizer - {self.user_data["user"]["username"]}')
        self.setGeometry(100, 100, 1300, 850)
        
        # Apply main stylesheet
        self.setStyleSheet(MAIN_STYLESHEET)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        # Header
        header_widget = QWidget()
        header_widget.setStyleSheet(f'''
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #667eea, stop:1 #764ba2);
                padding: 20px;
            }}
        ''')
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        # Logo and title
        logo_layout = QHBoxLayout()
        logo = QLabel('⚗️')
        logo.setStyleSheet('font-size: 32px; background: transparent;')
        logo_layout.addWidget(logo)
        
        title_widget = QWidget()
        title_widget.setStyleSheet('background: transparent;')
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)
        
        app_title = QLabel('Chemical Equipment Visualizer')
        app_title.setStyleSheet('color: white; font-size: 18px; font-weight: 700; background: transparent;')
        title_layout.addWidget(app_title)
        
        subtitle = QLabel('Desktop Application')
        subtitle.setStyleSheet('color: rgba(255, 255, 255, 0.8); font-size: 12px; background: transparent;')
        title_layout.addWidget(subtitle)
        
        title_widget.setLayout(title_layout)
        logo_layout.addWidget(title_widget)
        logo_layout.addStretch()
        
        header_layout.addLayout(logo_layout)
        header_layout.addStretch()
        
        # User info
        user_info = QLabel(f'👤 {self.user_data["user"]["username"]}')
        user_info.setStyleSheet('''
            color: white;
            font-size: 14px;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
        ''')
        header_layout.addWidget(user_info)
        
        header_widget.setLayout(header_layout)
        main_layout.addWidget(header_widget)
        
        # Content area with padding
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_widget.setLayout(content_layout)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        content_layout.addWidget(self.tabs)
        
        # Upload tab
        self.upload_tab = self.create_upload_tab()
        self.tabs.addTab(self.upload_tab, '📄 Upload CSV')
        
        # Dashboard tab
        self.dashboard_tab = self.create_dashboard_tab()
        self.tabs.addTab(self.dashboard_tab, '📊 Dashboard')
        
        # History tab
        self.history_tab = self.create_history_tab()
        self.tabs.addTab(self.history_tab, '📜 History')
        
        main_layout.addWidget(content_widget)
    
    def create_upload_tab(self):
        """Create upload tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Instructions card
        instructions_group = QGroupBox()
        instructions_layout = QVBoxLayout()
        
        icon_label = QLabel('📂')
        icon_label.setStyleSheet('font-size: 64px; background: transparent;')
        icon_label.setAlignment(Qt.AlignCenter)
        instructions_layout.addWidget(icon_label)
        
        title = QLabel('Upload Equipment Data')
        title.setObjectName('headerLabel')
        title.setAlignment(Qt.AlignCenter)
        instructions_layout.addWidget(title)
        
        desc = QLabel('Select a CSV file containing equipment parameters to analyze and visualize')
        desc.setObjectName('subtitleLabel')
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        instructions_layout.addWidget(desc)
        
        instructions_group.setLayout(instructions_layout)
        layout.addWidget(instructions_group)
        
        # File selection card
        file_group = QGroupBox('Selected File')
        file_layout = QVBoxLayout()
        
        self.file_path_label = QLabel('No file selected')
        self.file_path_label.setObjectName('subtitleLabel')
        self.file_path_label.setAlignment(Qt.AlignCenter)
        file_layout.addWidget(self.file_path_label)
        
        browse_btn = QPushButton('📁 Browse Files')
        browse_btn.setObjectName('secondaryButton')
        browse_btn.setMinimumHeight(44)
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Upload button
        self.upload_btn = QPushButton('🚀 Upload & Process CSV')
        self.upload_btn.setMinimumHeight(50)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        layout.addWidget(self.upload_btn)
        
        # Status
        self.upload_status = QLabel('')
        self.upload_status.setAlignment(Qt.AlignCenter)
        self.upload_status.setWordWrap(True)
        layout.addWidget(self.upload_status)
        
        # Requirements info
        req_group = QGroupBox('📋 CSV Requirements')
        req_layout = QVBoxLayout()
        req_text = QLabel(
            '• Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature<br>'
            '• File format: .csv (Comma Separated Values)<br>'
            '• Maximum file size: 10MB'
        )
        req_text.setObjectName('subtitleLabel')
        req_layout.addWidget(req_text)
        req_group.setLayout(req_layout)
        layout.addWidget(req_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_dashboard_tab(self):
        """Create dashboard tab with gradient stat cards"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Stats cards in grid
        stats_widget = QWidget()
        stats_layout = QGridLayout()
        stats_layout.setSpacing(16)
        
        self.stat_cards = {}
        stats_config = [
            ('Total Equipment', '⚙️', 'purple'),
            ('Avg Flowrate', '💧', 'pink'),
            ('Avg Pressure', '📊', 'blue'),
            ('Avg Temperature', '🌡️', 'orange'),
        ]
        
        for i, (stat_name, icon, gradient) in enumerate(stats_config):
            card = QGroupBox()
            if gradient in STAT_GRADIENTS:
                card.setStyleSheet(get_stat_card_stylesheet(*STAT_GRADIENTS[gradient]))
            
            card_layout = QVBoxLayout()
            card_layout.setSpacing(12)
            
            icon_label = QLabel(icon)
            icon_label.setStyleSheet('font-size: 32px; background: transparent;')
            card_layout.addWidget(icon_label)
            
            label = QLabel(stat_name)
            label.setStyleSheet('font-size: 13px; opacity: 0.9; background: transparent;')
            card_layout.addWidget(label)
            
            value = QLabel('--')
            value.setStyleSheet('font-size: 28px; font-weight: 700; background: transparent;')
            card_layout.addWidget(value)
            
            self.stat_cards[stat_name] = value
            
            card.setLayout(card_layout)
            stats_layout.addWidget(card, i // 2, i % 2)
        
        stats_widget.setLayout(stats_layout)
        layout.addWidget(stats_widget)
        
        # Charts group
        charts_group = QGroupBox('📈 Data Visualizations')
        charts_layout = QVBoxLayout()
        
        self.bar_chart = ChartWidget()
        charts_layout.addWidget(self.bar_chart)
        
        charts_group.setLayout(charts_layout)
        layout.addWidget(charts_group)
        
        # Data table
        table_group = QGroupBox('🗂️ Equipment Records')
        table_layout = QVBoxLayout()
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.data_table.horizontalHeader().setStretchLastSection(True)
        table_layout.addWidget(self.data_table)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_history_tab(self):
        """Create history tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(16)
        
        # Header with refresh button
        header_layout = QHBoxLayout()
        header_label = QLabel('📜 Upload History')
        header_label.setObjectName('headerLabel')
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        refresh_btn = QPushButton('🔄 Refresh')
        refresh_btn.setObjectName('secondaryButton')
        refresh_btn.clicked.connect(self.load_history)
        header_layout.addWidget(refresh_btn)
        layout.addLayout(header_layout)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.history_item_clicked)
        layout.addWidget(self.history_list)
        
        # Action buttons
        btn_group = QGroupBox('Actions')
        btn_layout = QHBoxLayout()
        
        view_btn = QPushButton('👁️ View Dataset')
        view_btn.setMinimumHeight(40)
        view_btn.clicked.connect(self.view_selected_dataset)
        btn_layout.addWidget(view_btn)
        
        pdf_btn = QPushButton('📥 Download PDF')
        pdf_btn.setObjectName('successButton')
        pdf_btn.setMinimumHeight(40)
        pdf_btn.clicked.connect(self.download_selected_pdf)
        btn_layout.addWidget(pdf_btn)
        
        btn_group.setLayout(btn_layout)
        layout.addWidget(btn_group)
        
        widget.setLayout(layout)
        
        # Load history on init
        self.load_history()
        
        return widget
    
    def browse_file(self):
        """Browse for CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if file_path:
            self.selected_file = file_path
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  # KB
            self.file_path_label.setText(f'📄 {file_name} ({file_size:.2f} KB)')
            self.file_path_label.setObjectName('successLabel')
            self.file_path_label.setStyle(self.file_path_label.style())
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        """Upload selected file"""
        if not hasattr(self, 'selected_file'):
            return
        
        self.upload_btn.setEnabled(False)
        self.upload_status.setText('🔄 Uploading and processing...')
        self.upload_status.setObjectName('infoLabel')
        self.upload_status.setStyle(self.upload_status.style())
        
        try:
            result = self.api_client.upload_csv(self.selected_file)
            self.upload_status.setText(f'✅ Success! {result["total_equipment"]} equipment records processed.')
            self.upload_status.setObjectName('successLabel')
            self.upload_status.setStyle(self.upload_status.style())
            
            # Load the dataset
            self.current_dataset = self.api_client.get_dataset_summary(result['id'])
            self.update_dashboard()
            
            # Switch to dashboard tab
            self.tabs.setCurrentIndex(1)
            
            # Refresh history
            self.load_history()
        except Exception as e:
            self.upload_status.setText(f'⚠️ Error: {str(e)}')
            self.upload_status.setObjectName('errorLabel')
            self.upload_status.setStyle(self.upload_status.style())
        finally:
            self.upload_btn.setEnabled(True)
    
    def update_dashboard(self):
        """Update dashboard with current dataset"""
        if not self.current_dataset:
            return
        
        # Update stats
        self.stat_cards['Total Equipment'].setText(str(self.current_dataset['total_equipment']))
        self.stat_cards['Avg Flowrate'].setText(f"{self.current_dataset['avg_flowrate']:.2f}")
        self.stat_cards['Avg Pressure'].setText(f"{self.current_dataset['avg_pressure']:.2f}")
        self.stat_cards['Avg Temperature'].setText(f"{self.current_dataset['avg_temperature']:.2f}")
        
        # Update chart
        if 'chart_data' in self.current_dataset:
            chart_data = self.current_dataset['chart_data']
            self.bar_chart.plot_bar_chart(chart_data['labels'], chart_data['values'])
        
        # Update table
        records = self.current_dataset.get('equipment_records', [])
        self.data_table.setRowCount(len(records))
        
        for i, record in enumerate(records):
            self.data_table.setItem(i, 0, QTableWidgetItem(record['equipment_name']))
            self.data_table.setItem(i, 1, QTableWidgetItem(record['equipment_type']))
            self.data_table.setItem(i, 2, QTableWidgetItem(str(record['flowrate'])))
            self.data_table.setItem(i, 3, QTableWidgetItem(str(record['pressure'])))
            self.data_table.setItem(i, 4, QTableWidgetItem(str(record['temperature'])))
    
    def load_history(self):
        """Load upload history"""
        try:
            history = self.api_client.get_upload_history()
            self.history_list.clear()
            
            for dataset in history:
                # Format date
                from datetime import datetime
                try:
                    dt = datetime.fromisoformat(dataset['uploaded_at'].replace('Z', '+00:00'))
                    date_str = dt.strftime('%b %d, %Y %I:%M %p')
                except:
                    date_str = dataset['uploaded_at']
                
                item_text = f"📊 Dataset #{dataset['id']} • {date_str} • {dataset['total_equipment']} equipment"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, dataset['id'])
                self.history_list.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'⚠️ Failed to load history: {str(e)}')
    
    def history_item_clicked(self, item):
        """Handle history item click"""
        self.selected_dataset_id = item.data(Qt.UserRole)
    
    def view_selected_dataset(self):
        """View selected dataset from history"""
        if not hasattr(self, 'selected_dataset_id'):
            QMessageBox.warning(self, 'Warning', '⚠️ Please select a dataset first')
            return
        
        try:
            self.current_dataset = self.api_client.get_dataset_summary(self.selected_dataset_id)
            self.update_dashboard()
            self.tabs.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'⚠️ Failed to load dataset: {str(e)}')
    
    def download_selected_pdf(self):
        """Download PDF for selected dataset"""
        if not hasattr(self, 'selected_dataset_id'):
            QMessageBox.warning(self, 'Warning', '⚠️ Please select a dataset first')
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, 
            'Save PDF', 
            f'equipment_report_{self.selected_dataset_id}.pdf',
            'PDF Files (*.pdf)'
        )
        
        if save_path:
            try:
                self.api_client.download_pdf(self.selected_dataset_id, save_path)
                QMessageBox.information(self, 'Success', f'✅ PDF saved successfully!\n\nLocation: {save_path}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'⚠️ Failed to download PDF: {str(e)}')


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Create API client
    api_client = APIClient()
    
    # Show login window
    login_window = LoginWindow(api_client)
    
    def on_login_success(user_data):
        """Handle successful login"""
        main_window = MainWindow(api_client, user_data)
        main_window.show()
    
    login_window.login_successful.connect(on_login_success)
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
