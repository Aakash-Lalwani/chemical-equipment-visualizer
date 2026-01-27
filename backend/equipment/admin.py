"""
Django Admin configuration for equipment models.

WHAT: This registers our models in Django's admin panel.
WHY: So we can view and manage data through a web interface.
HOW: We use @admin.register decorator to register models.
"""

from django.contrib import admin
from .models import Dataset, EquipmentData


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    """Admin interface for Dataset model"""
    list_display = ['id', 'user', 'uploaded_at', 'total_equipment', 'avg_flowrate', 'avg_pressure', 'avg_temperature']
    list_filter = ['uploaded_at', 'user']
    search_fields = ['user__username']
    readonly_fields = ['uploaded_at']
    
    def has_add_permission(self, request):
        """Disable manual addition through admin"""
        return False


@admin.register(EquipmentData)
class EquipmentDataAdmin(admin.ModelAdmin):
    """Admin interface for EquipmentData model"""
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['equipment_type', 'dataset']
    search_fields = ['equipment_name', 'equipment_type']
    
    def has_add_permission(self, request):
        """Disable manual addition through admin"""
        return False
