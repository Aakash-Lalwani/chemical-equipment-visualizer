"""
API Views for Equipment Management.

WHAT: These are the functions that handle API requests.
WHY: When someone calls our API, these functions run and return responses.
HOW: We use Django REST Framework's APIView and viewsets.
"""

import os
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from .models import Dataset, EquipmentData
from .serializers import DatasetSerializer, DatasetListSerializer, EquipmentDataSerializer
from .utils import process_csv_file, validate_csv_size, get_equipment_type_chart_data
from .pdf_generator import generate_pdf_report


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint - Returns authentication token.
    
    WHAT: User sends username and password, gets back a token.
    WHY: Token is used to authenticate future API calls.
    HOW: Check credentials, create/retrieve token, return it.
    
    Request Body:
        {
            "username": "admin",
            "password": "admin123"
        }
    
    Response:
        {
            "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
            "user": {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com"
            }
        }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register new user endpoint.
    
    Request Body:
        {
            "username": "newuser",
            "email": "user@example.com",
            "password": "password123"
        }
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=email or '',
        password=password
    )
    
    # Create token
    token = Token.objects.create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv_view(request):
    """
    Upload CSV file and process it.
    
    WHAT: Accept CSV file, validate it, calculate analytics, save to database.
    WHY: This is the core feature - uploading and analyzing equipment data.
    HOW: 
        1. Validate file exists and size is OK
        2. Save file temporarily
        3. Process with Pandas
        4. Save to database
        5. Keep only last 5 datasets
    
    Request:
        POST with multipart/form-data
        Field: 'file' (CSV file)
    
    Response:
        {
            "id": 1,
            "total_equipment": 10,
            "avg_flowrate": 195.23,
            ...
        }
    """
    # Check if file is provided
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file = request.FILES['file']
    
    # Validate file extension
    if not file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be a CSV'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file size
    is_valid, error_msg = validate_csv_size(file.size, max_size_mb=10)
    if not is_valid:
        return Response(
            {'error': error_msg},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create dataset instance
    dataset = Dataset.objects.create(
        user=request.user,
        file=file
    )
    
    # Get file path
    file_path = dataset.file.path
    
    # Process CSV file
    success, data, error_msg = process_csv_file(file_path)
    
    if not success:
        dataset.delete()  # Clean up
        return Response(
            {'error': error_msg},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update dataset with analytics
    dataset.total_equipment = data['total_equipment']
    dataset.avg_flowrate = data['avg_flowrate']
    dataset.avg_pressure = data['avg_pressure']
    dataset.avg_temperature = data['avg_temperature']
    dataset.equipment_types = data['equipment_types']
    dataset.save()
    
    # Save equipment records
    for record in data['equipment_records']:
        EquipmentData.objects.create(
            dataset=dataset,
            **record
        )
    
    # Keep only last 5 datasets per user
    user_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
    if user_datasets.count() > 5:
        # Delete oldest datasets
        datasets_to_delete = user_datasets[5:]
        for old_dataset in datasets_to_delete:
            # Delete associated file
            if old_dataset.file:
                if os.path.exists(old_dataset.file.path):
                    os.remove(old_dataset.file.path)
            old_dataset.delete()
    
    # Return serialized data
    serializer = DatasetSerializer(dataset)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_summary_view(request, dataset_id):
    """
    Get detailed summary of a specific dataset.
    
    WHAT: Returns all data about a dataset including equipment records.
    WHY: To view details of a previously uploaded dataset.
    HOW: Retrieve dataset by ID and serialize it.
    
    URL: /api/datasets/<id>/summary/
    
    Response:
        {
            "id": 1,
            "user": {...},
            "total_equipment": 10,
            "equipment_records": [...]
        }
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = DatasetSerializer(dataset)
    
    # Add chart data
    response_data = serializer.data
    response_data['chart_data'] = get_equipment_type_chart_data(dataset.equipment_types)
    
    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upload_history_view(request):
    """
    Get list of all uploaded datasets for the current user.
    
    WHAT: Returns last 5 datasets uploaded by the user.
    WHY: To see history of uploads.
    HOW: Query datasets filtered by user.
    
    URL: /api/upload-history/
    
    Response:
        [
            {
                "id": 1,
                "uploaded_at": "2026-01-27T10:30:00Z",
                "total_equipment": 10,
                ...
            },
            ...
        ]
    """
    datasets = Dataset.objects.filter(user=request.user)[:5]
    serializer = DatasetListSerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset_view(request, dataset_id):
    """
    Delete a specific dataset.
    
    URL: /api/datasets/<id>/delete/
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Delete file
    if dataset.file:
        if os.path.exists(dataset.file.path):
            os.remove(dataset.file.path)
    
    dataset.delete()
    
    return Response(
        {'message': 'Dataset deleted successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_pdf_view(request, dataset_id):
    """
    Download PDF report for a specific dataset.
    
    WHAT: Generates and returns a PDF report.
    WHY: Users want downloadable reports with charts and statistics.
    HOW: Use ReportLab to create a formatted PDF.
    
    URL: /api/datasets/<id>/download-pdf/
    
    Response:
        PDF file download
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return generate_pdf_report(dataset)
