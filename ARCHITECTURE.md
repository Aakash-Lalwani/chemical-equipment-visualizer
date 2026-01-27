# Project Architecture & Technical Details

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                        │
├──────────────────────┬──────────────────────────────────┤
│   React Web App      │     PyQt5 Desktop App            │
│   (Port 3000)        │     (Standalone)                 │
│   - Chart.js         │     - Matplotlib                 │
│   - Axios            │     - Requests                   │
└──────────────────────┴──────────────────────────────────┘
                         ↓ HTTP/REST API ↓
┌─────────────────────────────────────────────────────────┐
│              DJANGO BACKEND (Port 8000)                 │
├─────────────────────────────────────────────────────────┤
│  API Layer (Django REST Framework)                      │
│  - Token Authentication                                 │
│  - Request/Response Serialization                       │
│  - CORS Handling                                        │
├─────────────────────────────────────────────────────────┤
│  Business Logic Layer                                   │
│  - CSV Processing (Pandas)                              │
│  - Analytics Calculation                                │
│  - PDF Generation (ReportLab)                           │
│  - File Management                                      │
├─────────────────────────────────────────────────────────┤
│  Data Access Layer (Django ORM)                         │
│  - Models: Dataset, EquipmentData                       │
│  - Relationships & Queries                              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              DATABASE (SQLite)                          │
│  - User Table                                           │
│  - Dataset Table                                        │
│  - EquipmentData Table                                  │
│  - Token Table                                          │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              FILE SYSTEM                                │
│  - Uploaded CSV files (media/datasets/)                 │
│  - Generated PDFs (temporary)                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow

### Upload CSV Workflow

```
1. User selects CSV file
   ↓
2. Frontend sends POST to /api/upload-csv/
   ↓
3. Django receives file
   ↓
4. Validate file (extension, size)
   ↓
5. Save file to media/datasets/
   ↓
6. Pandas reads CSV
   ↓
7. Validate columns (Equipment Name, Type, Flowrate, Pressure, Temperature)
   ↓
8. Clean data (remove NaN, convert types)
   ↓
9. Calculate analytics:
   - Total count
   - Average flowrate, pressure, temperature
   - Equipment type distribution (count by type)
   ↓
10. Create Dataset record in database
    ↓
11. Create EquipmentData records for each row
    ↓
12. Check dataset count for user
    ↓
13. If > 5, delete oldest datasets and files
    ↓
14. Return serialized dataset with analytics
    ↓
15. Frontend displays dashboard with charts
```

---

## 🔐 Authentication Flow

```
1. User enters username + password
   ↓
2. Frontend sends POST to /api/login/
   ↓
3. Django authenticates via User model
   ↓
4. If valid, get or create Token
   ↓
5. Return token + user info
   ↓
6. Frontend stores token in localStorage
   ↓
7. All future requests include:
   Header: Authorization: Token <token>
   ↓
8. Django validates token on each request
   ↓
9. If valid, allow access; else 401 Unauthorized
```

---

## 🗄️ Database Schema

### User Table (Django built-in)
```sql
- id: INTEGER PRIMARY KEY
- username: VARCHAR(150) UNIQUE
- password: VARCHAR(128) [hashed]
- email: VARCHAR(254)
- is_active: BOOLEAN
- date_joined: DATETIME
```

### Dataset Table
```sql
- id: INTEGER PRIMARY KEY
- user_id: INTEGER FOREIGN KEY → User.id
- uploaded_at: DATETIME
- file: VARCHAR(100) [path to CSV]
- total_equipment: INTEGER
- avg_flowrate: FLOAT
- avg_pressure: FLOAT
- avg_temperature: FLOAT
- equipment_types: TEXT [JSON string]

INDEXES:
- user_id, uploaded_at (for history queries)
```

### EquipmentData Table
```sql
- id: INTEGER PRIMARY KEY
- dataset_id: INTEGER FOREIGN KEY → Dataset.id
- equipment_name: VARCHAR(200)
- equipment_type: VARCHAR(100)
- flowrate: FLOAT
- pressure: FLOAT
- temperature: FLOAT

INDEXES:
- dataset_id (for filtering by dataset)

CASCADE DELETE: When Dataset deleted, all EquipmentData deleted
```

### Token Table (DRF built-in)
```sql
- key: VARCHAR(40) PRIMARY KEY [unique token]
- user_id: INTEGER FOREIGN KEY → User.id
- created: DATETIME
```

---

## 🔧 Technology Choices Explained

### Why Django?
- **Rapid Development:** Built-in admin, ORM, auth
- **Security:** CSRF, XSS, SQL injection protection
- **Scalability:** Can handle large datasets
- **Community:** Extensive documentation and packages

### Why Django REST Framework?
- **Serialization:** Easy JSON conversion
- **Authentication:** Token auth built-in
- **Browsable API:** Test endpoints in browser
- **Validation:** Automatic request validation

### Why React?
- **Component-Based:** Reusable UI pieces
- **Virtual DOM:** Fast updates
- **Ecosystem:** Chart.js, Axios, and more
- **State Management:** Easy data flow

### Why PyQt5?
- **Cross-Platform:** Works on Windows, Mac, Linux
- **Native Look:** Feels like a real desktop app
- **Rich Widgets:** Tables, charts, file dialogs
- **Mature:** Stable and well-documented

### Why SQLite?
- **Simplicity:** No separate database server
- **Portability:** Single file database
- **Sufficient:** Perfect for this project size
- **Django Default:** Works out of the box

### Why Pandas?
- **CSV Reading:** Excellent CSV handling
- **Data Cleaning:** Easy NaN removal, type conversion
- **Analytics:** Built-in mean, count, groupby
- **Performance:** Fast for datasets up to millions of rows

### Why Chart.js (Web)?
- **Easy Integration:** Works great with React
- **Interactive:** Hover tooltips, animations
- **Responsive:** Adapts to screen size
- **Free:** Open source

### Why Matplotlib (Desktop)?
- **Python Native:** Works seamlessly with PyQt5
- **Powerful:** Any chart type imaginable
- **Customizable:** Full control over appearance
- **Embeddable:** Can be embedded in Qt widgets

---

## 🔒 Security Considerations

### Implemented
✅ Token-based authentication  
✅ Password hashing (Django built-in)  
✅ CSRF protection  
✅ SQL injection prevention (ORM)  
✅ File size limits  
✅ File type validation  
✅ User-specific data isolation  

### For Production (Not Implemented)
❌ HTTPS/SSL  
❌ Rate limiting  
❌ Input sanitization for XSS  
❌ Strong password requirements  
❌ Token expiration  
❌ Refresh tokens  
❌ API versioning  
❌ Logging and monitoring  

---

## 📈 Scalability

### Current Limitations
- SQLite: Not for high-concurrency
- File Storage: Local disk (not cloud)
- No Caching: Repeated queries hit database
- Single Server: No load balancing

### How to Scale
1. **Database:** Switch to PostgreSQL/MySQL
2. **File Storage:** Use AWS S3 or Azure Blob
3. **Caching:** Add Redis for query results
4. **Load Balancing:** Multiple Django instances with Nginx
5. **Task Queue:** Celery for async CSV processing
6. **CDN:** Serve static files from CDN
7. **Database Indexing:** Add indexes for common queries

---

## 🧪 Testing Strategy

### Unit Tests (Not Implemented)
- Test CSV validation logic
- Test analytics calculations
- Test API endpoints
- Test serializers

### Integration Tests (Not Implemented)
- Test full upload workflow
- Test authentication flow
- Test PDF generation

### Example Test Cases

```python
# Test CSV with missing columns
def test_upload_csv_missing_columns():
    # Should return 400 error

# Test CSV with invalid data
def test_upload_csv_invalid_data():
    # Should clean data and process valid rows

# Test 5-dataset limit
def test_dataset_limit():
    # Upload 6 datasets, verify only 5 remain

# Test unauthorized access
def test_unauthorized_access():
    # Should return 401 without token
```

---

## 🚀 Deployment

### Development (Current)
- Django runserver (port 8000)
- React dev server (port 3000)
- SQLite database
- Local file storage

### Production (Recommended)

**Backend:**
- Gunicorn/uWSGI WSGI server
- Nginx reverse proxy
- PostgreSQL database
- AWS S3 for files
- Environment variables for secrets

**Frontend:**
- Build with `npm run build`
- Serve static files from Nginx
- Or deploy to Vercel/Netlify

**Desktop:**
- Package with PyInstaller
- Create .exe installer (Windows)
- Create .app bundle (Mac)
- Create .deb/.rpm (Linux)

---

## 📦 Dependencies Explained

### Backend (requirements.txt)
```
Django==5.2.10           # Web framework
djangorestframework      # REST API framework
django-cors-headers      # CORS handling
pandas                   # CSV processing
reportlab                # PDF generation
pillow                   # Image handling (for PDF)
matplotlib               # Charts (for desktop app)
```

### Frontend (package.json)
```
react                    # UI library
react-dom                # React rendering
axios                    # HTTP client
chart.js                 # Charts
react-chartjs-2          # React wrapper for Chart.js
vite                     # Build tool
```

### Desktop (requirements.txt)
```
PyQt5                    # GUI framework
requests                 # HTTP client
matplotlib               # Charts
```

---

## 🎯 Design Patterns Used

### Backend
- **MVC Pattern:** Models, Views, Templates (Django)
- **Repository Pattern:** Models abstract database access
- **Serializer Pattern:** DRF serializers for data transformation
- **Token Authentication:** Security pattern

### Frontend
- **Component-Based Architecture:** Reusable React components
- **Service Layer:** API client abstraction
- **State Management:** Local state with useState
- **Props Down, Events Up:** React data flow

### Desktop
- **Model-View-Controller:** Separation of data, UI, logic
- **Observer Pattern:** Qt signals and slots
- **Singleton Pattern:** API client instance

---

## 🔄 API Response Formats

### Login Response
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  }
}
```

### Upload Response
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "uploaded_at": "2026-01-27T20:00:00Z",
  "file": "/media/datasets/sample_equipment_data.csv",
  "total_equipment": 10,
  "avg_flowrate": 195.23,
  "avg_pressure": 2.54,
  "avg_temperature": 83.45,
  "equipment_types": "{\"Reactor\": 2, \"Pump\": 2, ...}",
  "equipment_records": [
    {
      "id": 1,
      "equipment_name": "Reactor A",
      "equipment_type": "Reactor",
      "flowrate": 150.5,
      "pressure": 2.3,
      "temperature": 120.0
    },
    ...
  ],
  "chart_data": {
    "labels": ["Reactor", "Pump", "Heat Exchanger", ...],
    "values": [2, 2, 2, ...]
  }
}
```

### Error Response
```json
{
  "error": "Missing required columns: Type, Flowrate"
}
```

---

## ✨ Key Features Implementation

### 1. CSV Validation
- Check file extension
- Check file size (max 10MB)
- Validate required columns
- Remove rows with missing data
- Convert numeric columns
- Handle invalid values

### 2. Analytics Calculation
- Count total rows (after cleaning)
- Calculate mean for flowrate, pressure, temperature
- Group by equipment type and count
- Store as JSON string

### 3. History Management (Last 5)
- Query datasets ordered by upload time
- If count > 5, get datasets beyond 5th
- Delete from database (cascade to equipment records)
- Delete physical files from disk

### 4. PDF Generation
- Create PDF document
- Add title and metadata
- Create tables for stats and equipment types
- Add bar chart visualization
- Format with colors and styling
- Return as downloadable file

---

**This architecture supports:**
- Easy maintenance
- Future enhancements
- Testing
- Scalability
- Clean code principles

---

**Ready for submission and presentation! 🎉**
