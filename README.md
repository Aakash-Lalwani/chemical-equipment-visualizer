# Chemical Equipment Parameter Visualizer

A comprehensive full-stack application for analyzing and visualizing chemical equipment parameters. Built with Django REST Framework backend, React frontend, and PyQt5 desktop application.

[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![PyQt5](https://img.shields.io/badge/PyQt5-Desktop-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![WCAG 2.1 AA](https://img.shields.io/badge/Accessibility-WCAG%202.1%20AA-brightgreen.svg)](https://www.w3.org/WAI/WCAG21/quickref/)

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

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Aakash-Lalwani/chemical-equipment-visualizer.git
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

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
python manage.py migrate
```

5. Create admin user:
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://127.0.0.1:8000/`

### Web Frontend Setup (Optional)

1. Navigate to frontend directory:
```bash
cd frontend-react
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

The web interface will be available at `http://localhost:5173/`

### Desktop Application Setup

1. Ensure backend is running

2. Install PyQt5 dependencies:
```bash
pip install -r desktop-pyqt/requirements.txt
```

3. Run the application:
```bash
python desktop-pyqt/main.py
```

## Usage

### Getting Started

1. Start the backend server (see Installation section)
2. Access the web interface at `http://localhost:5173/` or launch the desktop application
3. Log in with your credentials
4. Upload a CSV file containing equipment data
5. View automatically generated visualizations and statistics
6. Access historical datasets through the History tab
7. Download PDF reports as needed

### CSV File Format

The application expects CSV files with the following structure:

```csv
Equipment_ID,Equipment_Type,Flowrate,Pressure,Temperature
EQ001,Pump,3.2,12.5,25.0
EQ002,Valve,2.8,10.0,22.5
EQ003,Heat_Exchanger,4.1,15.2,30.0
```

**Required Columns:**
- Equipment_ID: Unique identifier for each equipment
- Equipment_Type: Category or type of equipment
- Flowrate: Numerical flow rate value
- Pressure: Numerical pressure value
- Temperature: Numerical temperature value

**File Requirements:**
- File extension: .csv
- Maximum file size: 10MB
- First row must contain column headers
- All columns are required

Sample data files are provided in the `sample_equipment_data.csv` file.

## API Documentation

Base URL: `http://127.0.0.1:8000/api/`

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
- Check network connectivity to localhost:8000

**CSV upload failures**
- Verify CSV format matches required structure
- Check file size (must be under 10MB)
- Ensure all required columns are present
- Validate data types in columns

**PDF generation errors**
- Ensure ReportLab is installed
- Check file system permissions
- Verify matplotlib is working correctly

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
