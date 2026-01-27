# 🔌 API Testing Guide

Quick reference for testing all backend endpoints.

---

## 🌐 Base URL
```
http://localhost:8000/api
```

---

## 🔐 Authentication Endpoints

### 1. Login (POST)
**Endpoint:** `/api/login/`  
**Method:** POST  
**Auth Required:** No

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Success Response (200):**
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

**Error Response (401):**
```json
{
  "error": "Invalid credentials"
}
```

**Test with cURL:**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Test with PowerShell:**
```powershell
$body = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/login/" -Method Post -Body $body -ContentType "application/json"
```

---

### 2. Register (POST)
**Endpoint:** `/api/register/`  
**Method:** POST  
**Auth Required:** No

**Request Body:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123"
}
```

**Success Response (201):**
```json
{
  "token": "abc123...",
  "user": {
    "id": 2,
    "username": "newuser",
    "email": "user@example.com"
  }
}
```

---

## 📤 Upload Endpoints

### 3. Upload CSV (POST)
**Endpoint:** `/api/upload-csv/`  
**Method:** POST  
**Auth Required:** Yes (Token)

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: multipart/form-data
```

**Request Body:**
Form-data with file field:
- Key: `file`
- Value: (CSV file)

**Success Response (201):**
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
    }
  ]
}
```

**Error Responses:**
```json
// 400 - No file provided
{"error": "No file provided"}

// 400 - Invalid file type
{"error": "File must be a CSV"}

// 400 - Missing columns
{"error": "Missing required columns: Type, Flowrate"}

// 400 - File too large
{"error": "File size exceeds 10MB limit"}

// 401 - Unauthorized
{"detail": "Authentication credentials were not provided."}
```

**Test with PowerShell:**
```powershell
$token = "YOUR_TOKEN_HERE"
$file = "c:\Users\91985\Desktop\FOSSE_2026\sample_equipment_data.csv"

$headers = @{
    "Authorization" = "Token $token"
}

$form = @{
    file = Get-Item -Path $file
}

Invoke-RestMethod -Uri "http://localhost:8000/api/upload-csv/" -Method Post -Headers $headers -Form $form
```

---

## 📋 History & Dataset Endpoints

### 4. Get Upload History (GET)
**Endpoint:** `/api/upload-history/`  
**Method:** GET  
**Auth Required:** Yes (Token)

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Success Response (200):**
```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com"
    },
    "uploaded_at": "2026-01-27T20:00:00Z",
    "total_equipment": 10,
    "avg_flowrate": 195.23,
    "avg_pressure": 2.54,
    "avg_temperature": 83.45,
    "equipment_types": "{\"Reactor\": 2, \"Pump\": 2}"
  }
]
```

**Test with PowerShell:**
```powershell
$token = "YOUR_TOKEN_HERE"
$headers = @{
    "Authorization" = "Token $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/upload-history/" -Method Get -Headers $headers
```

---

### 5. Get Dataset Summary (GET)
**Endpoint:** `/api/datasets/<id>/summary/`  
**Method:** GET  
**Auth Required:** Yes (Token)

**Example:** `/api/datasets/1/summary/`

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Success Response (200):**
```json
{
  "id": 1,
  "user": {...},
  "uploaded_at": "2026-01-27T20:00:00Z",
  "file": "/media/datasets/sample.csv",
  "total_equipment": 10,
  "avg_flowrate": 195.23,
  "avg_pressure": 2.54,
  "avg_temperature": 83.45,
  "equipment_types": "{...}",
  "equipment_records": [...],
  "chart_data": {
    "labels": ["Reactor", "Pump", "Heat Exchanger"],
    "values": [2, 2, 2]
  }
}
```

**Error Response (404):**
```json
{"error": "Dataset not found"}
```

**Test with PowerShell:**
```powershell
$token = "YOUR_TOKEN_HERE"
$datasetId = 1
$headers = @{
    "Authorization" = "Token $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/datasets/$datasetId/summary/" -Method Get -Headers $headers
```

---

### 6. Download PDF (GET)
**Endpoint:** `/api/datasets/<id>/download-pdf/`  
**Method:** GET  
**Auth Required:** Yes (Token)

**Example:** `/api/datasets/1/download-pdf/`

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Success Response (200):**
- Content-Type: application/pdf
- Binary PDF data

**Test with Browser:**
```
http://localhost:8000/api/datasets/1/download-pdf/
```
(Will prompt to download PDF)

**Test with PowerShell:**
```powershell
$token = "YOUR_TOKEN_HERE"
$datasetId = 1
$headers = @{
    "Authorization" = "Token $token"
}

Invoke-WebRequest -Uri "http://localhost:8000/api/datasets/$datasetId/download-pdf/" -Method Get -Headers $headers -OutFile "report.pdf"
```

---

### 7. Delete Dataset (DELETE)
**Endpoint:** `/api/datasets/<id>/delete/`  
**Method:** DELETE  
**Auth Required:** Yes (Token)

**Example:** `/api/datasets/1/delete/`

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Success Response (200):**
```json
{"message": "Dataset deleted successfully"}
```

**Error Response (404):**
```json
{"error": "Dataset not found"}
```

**Test with PowerShell:**
```powershell
$token = "YOUR_TOKEN_HERE"
$datasetId = 1
$headers = @{
    "Authorization" = "Token $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/datasets/$datasetId/delete/" -Method Delete -Headers $headers
```

---

## 🔨 Testing with Python Requests

Save this as `test_api.py`:

```python
import requests

BASE_URL = 'http://localhost:8000/api'

# 1. Login
response = requests.post(f'{BASE_URL}/login/', 
                        json={'username': 'admin', 'password': 'admin123'})
print('Login:', response.status_code)
token = response.json()['token']
print('Token:', token)

# Setup headers
headers = {'Authorization': f'Token {token}'}

# 2. Get History
response = requests.get(f'{BASE_URL}/upload-history/', headers=headers)
print('History:', response.status_code)
print('Datasets:', len(response.json()))

# 3. Upload CSV
with open('sample_equipment_data.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post(f'{BASE_URL}/upload-csv/', 
                            headers=headers, files=files)
    print('Upload:', response.status_code)
    dataset_id = response.json()['id']
    print('Dataset ID:', dataset_id)

# 4. Get Summary
response = requests.get(f'{BASE_URL}/datasets/{dataset_id}/summary/', 
                       headers=headers)
print('Summary:', response.status_code)
print('Total Equipment:', response.json()['total_equipment'])

# 5. Download PDF
response = requests.get(f'{BASE_URL}/datasets/{dataset_id}/download-pdf/', 
                       headers=headers)
print('PDF:', response.status_code)
with open(f'report_{dataset_id}.pdf', 'wb') as f:
    f.write(response.content)
    print('PDF saved!')
```

Run with:
```powershell
python test_api.py
```

---

## 🌐 Testing with Browser (Django Admin)

**URL:** http://localhost:8000/admin/

**Login:**
- Username: admin
- Password: admin123

**Can view:**
- Datasets
- Equipment Data
- Users
- Tokens

---

## 📊 Expected Status Codes

| Status | Meaning | When |
|--------|---------|------|
| 200 | OK | Successful GET/DELETE |
| 201 | Created | Successful POST (created) |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing/invalid token |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Backend error |

---

## 🧪 Quick Test Checklist

Test each endpoint:

- [ ] POST /api/login/ → Get token
- [ ] GET /api/upload-history/ → List datasets
- [ ] POST /api/upload-csv/ → Upload file
- [ ] GET /api/datasets/1/summary/ → View details
- [ ] GET /api/datasets/1/download-pdf/ → Download PDF
- [ ] DELETE /api/datasets/1/delete/ → Remove dataset
- [ ] POST /api/register/ → Create user

---

## 🐛 Common Issues

### "Authentication credentials were not provided"
**Fix:** Add Authorization header:
```
Authorization: Token YOUR_TOKEN_HERE
```

### "Invalid token"
**Fix:** Login again to get fresh token

### "Dataset not found"
**Fix:** Check dataset ID exists in history

### "Missing required columns"
**Fix:** CSV must have: Equipment Name, Type, Flowrate, Pressure, Temperature

---

## 📝 Sample CSV Format

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor A,Reactor,150.5,2.3,120.0
Pump B,Pump,175.3,3.5,40.2
Heat Exchanger C,Heat Exchanger,200.0,1.8,85.5
```

**Required Columns:**
1. Equipment Name (text)
2. Type (text)
3. Flowrate (number)
4. Pressure (number)
5. Temperature (number)

---

## ✅ Success Indicators

When everything works:
- ✅ Login returns token
- ✅ Upload returns dataset ID
- ✅ History shows datasets
- ✅ Summary includes chart_data
- ✅ PDF downloads successfully
- ✅ Delete removes dataset

---

## 🔍 Debugging Tips

1. **Check Django logs** in the terminal
2. **Use Django admin** to see database
3. **Check media folder** for uploaded files
4. **Verify token** is correct
5. **Test with Postman/Insomnia** for complex requests

---

**Happy Testing! 🧪**
