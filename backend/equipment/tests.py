"""
Equipment App Tests

WHAT: Automated tests for the equipment app
WHY: Ensures upload, validation, and API endpoints work correctly
HOW: Uses Django TestCase with temporary database and files
"""

import os
import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token
from .models import Dataset, EquipmentData


class UploadCSVTestCase(TestCase):
    """Test CSV upload functionality"""
    
    def setUp(self):
        """Set up test user and client"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        
    def test_upload_valid_csv(self):
        """Test uploading a valid CSV file"""
        # Create a valid CSV file content
        csv_content = b"""Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor A,Reactor,150.5,2.3,120.0
Pump B,Pump,200.0,1.8,85.5
Heat Exchanger C,Heat Exchanger,175.3,3.5,40.2"""
        
        # Create an uploaded file
        csv_file = SimpleUploadedFile(
            "test_equipment.csv",
            csv_content,
            content_type="text/csv"
        )
        
        # Make request with authentication
        response = self.client.post(
            '/api/upload-csv/',
            {'file': csv_file},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        
        # Check response
        self.assertEqual(response.status_code, 201)
        self.assertIn('total_equipment', response.json())
        self.assertEqual(response.json()['total_equipment'], 3)
        
        # Check database
        self.assertEqual(Dataset.objects.count(), 1)
        self.assertEqual(EquipmentData.objects.count(), 3)
        
    def test_upload_csv_case_insensitive_columns(self):
        """Test that column names are case-insensitive"""
        # CSV with lowercase column names
        csv_content = b"""equipment name,type,flowrate,pressure,temperature
Reactor A,Reactor,150.5,2.3,120.0"""
        
        csv_file = SimpleUploadedFile(
            "test_lowercase.csv",
            csv_content,
            content_type="text/csv"
        )
        
        response = self.client.post(
            '/api/upload-csv/',
            {'file': csv_file},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        
        # Should succeed with lowercase columns
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['total_equipment'], 1)
        
    def test_upload_csv_mixed_case_columns(self):
        """Test that mixed case column names work"""
        # CSV with UPPERCASE column names
        csv_content = b"""EQUIPMENT NAME,TYPE,FLOWRATE,PRESSURE,TEMPERATURE
Reactor A,Reactor,150.5,2.3,120.0"""
        
        csv_file = SimpleUploadedFile(
            "test_uppercase.csv",
            csv_content,
            content_type="text/csv"
        )
        
        response = self.client.post(
            '/api/upload-csv/',
            {'file': csv_file},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        
        # Should succeed with uppercase columns
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['total_equipment'], 1)
        
    def test_upload_missing_columns(self):
        """Test that CSV with missing columns is rejected"""
        # CSV missing Temperature column
        csv_content = b"""Equipment Name,Type,Flowrate,Pressure
Reactor A,Reactor,150.5,2.3"""
        
        csv_file = SimpleUploadedFile(
            "test_missing_column.csv",
            csv_content,
            content_type="text/csv"
        )
        
        response = self.client.post(
            '/api/upload-csv/',
            {'file': csv_file},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        
        # Should fail
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        
    def test_upload_non_csv_file(self):
        """Test that non-CSV files are rejected"""
        txt_file = SimpleUploadedFile(
            "test.txt",
            b"This is not a CSV",
            content_type="text/plain"
        )
        
        response = self.client.post(
            '/api/upload-csv/',
            {'file': txt_file},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        
        # Should fail
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        
    def test_upload_without_authentication(self):
        """Test that upload requires authentication"""
        csv_content = b"""Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor A,Reactor,150.5,2.3,120.0"""
        
        csv_file = SimpleUploadedFile(
            "test.csv",
            csv_content,
            content_type="text/csv"
        )
        
        # Make request without token
        response = self.client.post(
            '/api/upload-csv/',
            {'file': csv_file}
        )
        
        # Should be unauthorized
        self.assertEqual(response.status_code, 401)
        
    def test_history_limit_to_five(self):
        """Test that only last 5 datasets are kept per user"""
        # Upload 7 files
        for i in range(7):
            csv_content = f"""Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor {i},Reactor,150.5,2.3,120.0""".encode()
            
            csv_file = SimpleUploadedFile(
                f"test_{i}.csv",
                csv_content,
                content_type="text/csv"
            )
            
            self.client.post(
                '/api/upload-csv/',
                {'file': csv_file},
                HTTP_AUTHORIZATION=f'Token {self.token.key}'
            )
        
        # Should only have 5 datasets
        self.assertEqual(Dataset.objects.filter(user=self.user).count(), 5)


class AuthenticationTestCase(TestCase):
    """Test authentication endpoints"""
    
    def setUp(self):
        self.client = Client()
        
    def test_login_success(self):
        """Test successful login"""
        # Create user
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Login
        response = self.client.post(
            '/api/login/',
            json.dumps({'username': 'testuser', 'password': 'testpass123'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        self.assertIn('user', response.json())
        
    def test_login_invalid_credentials(self):
        """Test login with wrong password"""
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        response = self.client.post(
            '/api/login/',
            json.dumps({'username': 'testuser', 'password': 'wrongpass'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())


class DatasetModelTestCase(TestCase):
    """Test Dataset model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_dataset_creation(self):
        """Test creating a dataset"""
        dataset = Dataset.objects.create(
            user=self.user,
            total_equipment=10,
            avg_flowrate=195.23,
            avg_pressure=2.46,
            avg_temperature=83.33,
            equipment_types='{"Reactor": 2, "Pump": 3}'
        )
        
        self.assertEqual(dataset.user, self.user)
        self.assertEqual(dataset.total_equipment, 10)
        self.assertEqual(str(dataset), f"Dataset {dataset.id} - testuser - {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}")
        
    def test_dataset_ordering(self):
        """Test that datasets are ordered by newest first"""
        import time
        
        # Create 3 datasets with slight delays to ensure different timestamps
        ds1 = Dataset.objects.create(user=self.user, total_equipment=5)
        time.sleep(0.01)  # Small delay to ensure different timestamps
        ds2 = Dataset.objects.create(user=self.user, total_equipment=10)
        time.sleep(0.01)
        ds3 = Dataset.objects.create(user=self.user, total_equipment=15)
        
        # Get all datasets
        datasets = Dataset.objects.all()
        
        # Newest should be first (ds3), oldest last (ds1)
        self.assertEqual(datasets[0].id, ds3.id)
        self.assertEqual(datasets[2].id, ds1.id)
