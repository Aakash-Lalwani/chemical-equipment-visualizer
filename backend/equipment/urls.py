"""
URL Configuration for Equipment API.

WHAT: Maps URLs to view functions.
WHY: Django needs to know which function handles which URL.
HOW: Define urlpatterns list with path() functions.

URL Structure:
    /api/login/ -> login_view
    /api/register/ -> register_view
    /api/upload-csv/ -> upload_csv_view
    /api/upload-history/ -> upload_history_view
    /api/datasets/<id>/summary/ -> dataset_summary_view
    /api/datasets/<id>/delete/ -> delete_dataset_view
    /api/datasets/<id>/download-pdf/ -> download_pdf_view
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    
    # CSV upload
    path('upload-csv/', views.upload_csv_view, name='upload-csv'),
    
    # Dataset management
    path('upload-history/', views.upload_history_view, name='upload-history'),
    path('datasets/<int:dataset_id>/summary/', views.dataset_summary_view, name='dataset-summary'),
    path('datasets/<int:dataset_id>/delete/', views.delete_dataset_view, name='dataset-delete'),
    path('datasets/<int:dataset_id>/download-pdf/', views.download_pdf_view, name='download-pdf'),
]
