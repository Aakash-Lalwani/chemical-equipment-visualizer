# Chemical Equipment Parameter Visualizer

A comprehensive full-stack application for analyzing and visualizing chemical equipment parameters. Built with Django REST Framework backend, React frontend, and PyQt5 desktop application.

![React](https://img.shields.io/badge/React-18-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-Desktop-orange.svg)
![WCAG 2.1 AA](https://img.shields.io/badge/Accessibility-WCAG%202.1%20AA-brightgreen.svg)

## Overview

This project provides a complete solution for managing and analyzing chemical equipment data through multiple interfaces. The system allows users to upload CSV files containing equipment parameters and generates comprehensive visualizations and statistical analyses.

**Key Capabilities:**
- Multi-platform support (Web and Desktop applications)
- Real-time data processing and validation
- Interactive data visualizations with Chart.js and Matplotlib
- RESTful API architecture
- Token-based authentication
- PDF report generation
- WCAG 2.1 AA accessibility compliance

## Features

### Data Management
- CSV file upload with validation and parsing
- Support for multiple equipment types and parameters
- Automatic data storage with SQLite database
- Historical dataset management
- Dataset deletion with cascading cleanup

### Data Analysis
- Automatic calculation of summary statistics (averages, totals, distributions)
- Equipment type categorization and counting
- Parameter analysis (flowrate, pressure, temperature)
- Data integrity validation

### Visualization
- Bar charts for equipment type distribution
- Pie charts for proportional analysis
- Interactive data tables with sorting
- Summary statistics cards
- PDF report generation with embedded charts

### User Experience
- Responsive web interface built with React
- Native desktop application using PyQt5
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Inline help and tooltips
- Form validation with clear error messages

### Technical Features
- RESTful API architecture
- Token-based authentication
- CORS-enabled backend
- File upload with progress tracking
- Automatic old dataset cleanup
- Cross-platform desktop support

## Technology Stack

### Backend
- Django 5.2 - Web framework
- Django REST Framework - API development
- SQLite - Database
- Pandas - Data processing
- ReportLab - PDF generation
- Python 3.10+

### Web Frontend
- React 18 - UI library
- Vite - Build tool
- Chart.js - Data visualization
- Axios - HTTP client
- CSS3 - Styling

### Desktop Application
- PyQt5 - GUI framework
- Matplotlib - Charting library
- Requests - API communication
- Python 3.10+

## Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 16+ (optional, for web frontend)
- Git

---

## Quick Start

Use this one-command launcher (Windows):

```bash
.\RUN_ALL.bat
```

This script automatically starts:
- Django backend server
- React frontend (if Node.js installed)
- PyQt5 desktop application

**Default credentials:** `admin` / `admin123`

---

## Setup Instructions

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd chemical-equipment-visualizer
```

2. Create and activate virtual environment:
```bash
# Windows
cd backend
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

3. Copy environment configuration:
```powershell
# Windows
copy .env.example .env
# Edit .env file with your actual configuration

# Linux/Mac
cp .env.example .env
# Edit .env file with your actual configuration
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run database migrations:
```bash
python manage.py migrate
```

6. Create admin user (credentials for demo):
```bash
python manage.py createsuperuser
# Username: admin
# Password: admin123
# Email: (press Enter to skip)
```

7. Start the development server:
```bash
python manage.py runserver
```

The backend API will be available on the development server.

**Test it:** Navigate to the admin panel and login with your credentials.

### Web Frontend Setup (Optional)

1. Navigate to frontend directory:
```bash
cd frontend-react
```

2. Copy environment configuration:
```powershell
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

3. Install dependencies:
```bash
npm install
```

4. Start development server:
```bash
npm run dev
```

The web interface will be available on the Vite development server.

**Test it:** Open the application in your browser and you should see the login page.

### Desktop Application Setup

1. Ensure backend is running first

2. Copy configuration file:
```powershell
# Windows
cd desktop-pyqt
copy config.example.py config.py
# Edit config.py if needed to change backend URL
```

3. Run the application:
```bash
# Windows (from project root)
backend\.venv\Scripts\python.exe desktop-pyqt\main.py

# Linux/Mac
python desktop-pyqt/main.py
```

**Note:** Desktop app uses the same backend Python environment for simplicity.

---

## Usage

### Getting Started

1. Start the backend server (see Installation section)
2. Access the web interface or launch the desktop application
3. Log in with your credentials (default: `admin` / `admin123`)
4. Upload a CSV file containing equipment data
5. View automatically generated visualizations and statistics
6. Access historical datasets through the History tab
7. Download PDF reports as needed

### Sample Data

A sample CSV file (`sample_equipment_data.csv`) is included in the project root for testing:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor A,Reactor,150.5,2.3,120.0
Heat Exchanger B,Heat Exchanger,200.0,1.8,85.5
Pump C,Pump,175.3,3.5,40.2
...
```

**Expected Results:**
- Total Equipment: 10
- Average Flowrate: 195.23
- Average Pressure: 2.46
- Average Temperature: 83.33
- Equipment Types: Reactor (2), Heat Exchanger (2), Pump (2), Column (1), Compressor (1), Mixer (1), Separator (1)

### CSV File Format

The application expects CSV files with the following structure:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor A,Reactor,150.5,2.3,120.0
Pump B,Pump,200.0,1.8,85.5
Heat Exchanger C,Heat Exchanger,175.3,3.5,40.2
```

**Required Columns:**
- **Equipment Name** (or equipment name, EQUIPMENT NAME): Equipment identifier
- **Type** (or type, TYPE): Category/type of equipment  
- **Flowrate** (or flowrate, FLOWRATE): Numerical flow rate value
- **Pressure** (or pressure, PRESSURE): Numerical pressure value
- **Temperature** (or temperature, TEMPERATURE): Numerical temperature value

**Note:** Column names are **case-insensitive**. The system accepts uppercase, lowercase, or mixed case.

**File Requirements:**
- File extension: `.csv`
- Maximum file size: 10MB
- Encoding: UTF-8 (recommended)

**Data Validation:**
- Numeric columns are automatically coerced to numbers
- Rows with invalid/missing data are dropped (warning shown with count)
- At least one valid data row required
- First row must contain column headers
- All columns are required

Sample data files are provided in the `sample_equipment_data.csv` file.

## API Documentation

Base URL: `/api/`

### Authentication Endpoints

**POST /api/login/**
- Request body: `{"username": "string", "password": "string"}`
- Response: `{"token": "string", "user_id": integer}`
- Description: Authenticate user and receive authentication token

### Dataset Endpoints

**POST /api/upload-csv/**
- Headers: `Authorization: Token <token>`
- Request: Multipart form data with CSV file
- Response: Dataset object with analytics
- Description: Upload and process CSV file

**GET /api/upload-history/**
- Headers: `Authorization: Token <token>`
- Response: Array of dataset objects
- Description: Retrieve user's upload history

**GET /api/dataset-summary/<id>/**
- Headers: `Authorization: Token <token>`
- Response: Detailed dataset with equipment records
- Description: Get complete dataset information

**GET /api/download-pdf/<id>/**
- Headers: `Authorization: Token <token>`
- Response: PDF file
- Description: Generate and download PDF report

**DELETE /api/delete-dataset/<id>/**
- Headers: `Authorization: Token <token>`
- Response: Success message
- Description: Delete dataset and associated data

## Project Structure

```
chemical-equipment-visualizer/
├── backend/
│   ├── config/              # Django project settings
│   ├── equipment/           # Main application
│   │   ├── models.py        # Database models
│   │   ├── views.py         # API views
│   │   ├── serializers.py   # DRF serializers
│   │   ├── utils.py         # CSV processing utilities
│   │   └── pdf_generator.py # PDF report generation
│   ├── media/               # Uploaded files
│   ├── db.sqlite3          # SQLite database
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
│
├── frontend-react/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── CSVUpload.jsx
│   │   │   ├── History.jsx
│   │   │   └── Tooltip.jsx
│   │   ├── styles/         # CSS files
│   │   │   ├── global.css
│   │   │   └── Tooltip.css
│   │   ├── services/       # API client
│   │   │   └── api.js
│   │   ├── utils/          # Utility functions
│   │   │   └── keyboardShortcuts.js
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── package.json        # npm dependencies
│   └── vite.config.js      # Vite configuration
│
├── desktop-pyqt/
│   ├── main.py            # Desktop application
│   ├── styles.py          # Qt stylesheets
│   └── requirements.txt   # PyQt5 dependencies
│
├── sample_equipment_data.csv  # Sample dataset
├── RUN_ALL.bat               # Windows launch script
└── README.md                 # This file
```

## Development

### Architecture Overview

The application follows a three-tier architecture:

1. **Backend (Django REST Framework)**
   - Handles authentication and authorization
   - Processes CSV files using Pandas
   - Calculates statistical summaries
   - Generates PDF reports
   - Provides RESTful API endpoints

2. **Web Frontend (React)**
   - Single-page application
   - Component-based architecture
   - State management with React hooks
   - Chart rendering with Chart.js
   - Responsive design

3. **Desktop Application (PyQt5)**
   - Native GUI application
   - Direct API communication
   - Matplotlib chart integration
   - Cross-platform compatibility

### Key Implementation Details

**CSV Processing**
- Pandas DataFrame for efficient data manipulation
- Column validation and type checking
- Statistical calculations (mean, sum, count)
- Equipment type aggregation

**Authentication**
- Token-based authentication using Django REST Framework tokens
- Token storage in localStorage (web) and memory (desktop)
- Protected API endpoints require valid tokens

**Data Visualization**
- Chart.js for web interface (bar and pie charts)
- Matplotlib for desktop application and PDF generation
- Consistent color schemes across platforms
- Responsive chart sizing

**PDF Generation**
- ReportLab library for PDF creation
- Dynamic table generation from dataset
- Embedded matplotlib charts
- Professional formatting

## Testing

### Running Tests

The application includes comprehensive testing capabilities:

**Backend Testing**
```bash
cd backend
python manage.py test
```

**Frontend Testing**
```bash
cd frontend-react
npm test
```

### Manual Testing Checklist

1. Authentication
   - User can log in with valid credentials
   - Invalid credentials are rejected
   - Token is properly stored and used for API requests

2. CSV Upload
   - Valid CSV files are accepted and processed
   - Invalid files are rejected with clear error messages
   - File size limits are enforced
   - Progress indication works correctly

3. Data Visualization
   - Charts render correctly with uploaded data
   - Statistics are calculated accurately
   - Tables display all records
   - Color schemes are consistent

4. History Management
   - All uploaded datasets are listed
   - Dataset details can be viewed
   - PDF reports download correctly
   - Datasets can be deleted

5. Accessibility
   - Keyboard navigation works throughout the application
   - Screen readers can access all content
   - Color contrast meets WCAG standards
   - Focus indicators are visible

## Troubleshooting

### Common Issues

**Backend won't start**
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is already in use
- Run migrations: `python manage.py migrate`

**Frontend build errors**
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version (requires 16+)
- Verify API base URL in configuration

**Desktop application issues**
- Ensure backend is running before starting desktop app
- Verify PyQt5 is properly installed
- Check network connectivity to backend server

**CSV upload failures**
- Verify CSV format matches required structure
- Check file size (must be under 10MB)
- Ensure all required columns are present
- Validate data types in columns

**PDF generation errors**
- Ensure ReportLab is installed
- Check file system permissions
- Verify matplotlib is working correctly

---

## Testing & Validation

### Automated Validation

```powershell
# Windows
.\scripts\validate_project.ps1

# This checks:
# - Required files exist
# - CSV format is valid
# - Backend dependencies installed
# - Django checks pass
# - Tests pass
# - Frontend builds successfully
```

### Run Django Tests

```bash
cd backend
.venv\Scripts\activate  # Windows
python manage.py test

# Expected output:
# Creating test database...
# ......................
# Ran 12 tests in X.XXs
# OK
```

### Manual Testing

**Functional Tests:**
- Backend admin panel loads successfully
- Frontend application loads successfully
- User authentication with default credentials (admin/admin123)
- CSV file upload functionality (sample_equipment_data.csv)
- Dashboard displays correct statistics (Total: 10, Avg Flowrate: ~195.23)
- Bar chart displays 7 equipment types
- History tab shows uploaded datasets
- PDF report generation and download
- Desktop application launches and displays data

---

## Deployment

### Backend Deployment

1. **Configure environment variables:**
```env
SECRET_KEY=<generate-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-production-domain
CORS_ALLOWED_ORIGINS=your-frontend-domain
```

2. **Deploy with required files:**
```bash
# Ensure these files exist:
# - Procfile
# - runtime.txt (Python version)
# - Configuration file (optional)
```

3. **Run migrations after deployment:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Frontend Deployment

1. **Update environment variable:**
```env
VITE_API_URL=your-backend-api-url
```

2. **Build and deploy:**
```bash
npm run build
```

3. **Build settings:**
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

---

## Project Structure

```
FOSSE_2026/
├── backend/                 # Django REST API
│   ├── config/             # Django settings
│   ├── equipment/          # Main app (models, views, utils)
│   ├── media/              # Uploaded CSV files
│   ├── .env.example        # Environment template
│   └── requirements.txt    # Python dependencies
├── frontend-react/         # React web application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API client
│   │   └── config.js       # Configuration
│   ├── .env.example        # Environment template
│   └── package.json        # Node dependencies
├── desktop-pyqt/           # PyQt5 desktop application
│   ├── main.py             # Entry point
│   ├── config.example.py   # Configuration template
│   └── requirements.txt    # Python dependencies
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD
├── scripts/
│   └── validate_project.ps1  # Validation script
├── sample_equipment_data.csv  # Sample data for demo
├── DEMO_INSTRUCTIONS.md    # Video demo guide
├── README.md               # This file
└── RUN_ALL.bat             # Quick launcher (Windows)
```

---

## Troubleshooting

### Common Issues

**Backend won't start:**
```powershell
# Check Python version (needs 3.10+)
python --version

# Recreate virtual environment
cd backend
rmdir /s .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Run checks
python manage.py check
```

**ModuleNotFoundError:**
```bash
# Make sure venv is activated (prompt should show (.venv))
.venv\Scripts\activate
pip install -r requirements.txt
```

**Database errors:**
```bash
# Delete and recreate database
cd backend
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**CORS errors in browser console:**
```python
# backend/config/settings.py should include:
CORS_ALLOWED_ORIGINS = [
    # Add your frontend development server URLs
]
# Restart backend after changes
```

**Frontend "Cannot find module" errors:**
```bash
cd frontend-react
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Desktop app won't launch:**
```powershell
# Check PyQt5 installation
backend\.venv\Scripts\python.exe -c "import PyQt5; print('OK')"

# If error, reinstall
backend\.venv\Scripts\pip.exe install PyQt5 --force-reinstall

# Check backend URL in config.ini or config.py
```

**CSV upload fails:**
```
Common causes:
1. Column names incorrect (must have: Equipment Name, Type, Flowrate, Pressure, Temperature)
2. File too large (max 10MB)
3. Missing required columns
4. Invalid numeric data in Flowrate/Pressure/Temperature columns

Solution: Use sample_equipment_data.csv as template
```

**PDF download fails:**
```bash
# Check ReportLab installation
pip show reportlab

# Reinstall if needed
pip install reportlab --upgrade
```

### Getting Help

1. Check this README thoroughly
2. Review DEMO_INSTRUCTIONS.md
3. Run validation script: `.\scripts\validate_project.ps1`
4. Check Django logs in terminal
5. Check browser console for frontend errors

---

### Performance Optimization

- For large datasets, consider implementing pagination
- Enable database query optimization
- Use caching for frequently accessed data
- Optimize image compression in PDF reports
## Security Considerations

**Important: This application is configured for development use.**

For production deployment, implement the following security measures:

1. Change Django SECRET_KEY in settings.py
2. Set DEBUG = False in production
3. Configure ALLOWED_HOSTS properly
4. Use environment variables for sensitive data
5. Implement HTTPS/SSL
6. Add rate limiting to API endpoints
7. Strengthen password requirements
8. Enable CSRF protection
9. Implement proper CORS configuration
10. Regular security audits and dependency updates

## Future Enhancements

Potential improvements for future versions:

- Advanced filtering and search capabilities
- Export to multiple formats (Excel, JSON)
- Real-time data updates with WebSockets
- User profile management
- Role-based access control
- Email notifications for dataset processing
- Additional chart types (line charts, scatter plots)
- Mobile application development
- Docker containerization
- Automated testing suite
- CI/CD pipeline integration

## License

This project is available under the MIT License.

## Contact

For questions or issues, please open an issue on the GitHub repository.

---

Last Updated: January 2026
