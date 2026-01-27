"""
Database models for equipment data.

WHAT: These are Python classes that represent database tables.
WHY: Django uses these to create and manage the database automatically.
HOW: Each class attribute becomes a column in the database.
"""

from django.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    """
    Stores information about each uploaded CSV dataset.
    
    Fields:
    - user: Who uploaded this dataset
    - uploaded_at: When it was uploaded
    - file: The CSV file itself
    - total_equipment: Total number of equipment in the CSV
    - avg_flowrate: Average flowrate calculated from the CSV
    - avg_pressure: Average pressure calculated from the CSV
    - avg_temperature: Average temperature calculated from the CSV
    - equipment_types: JSON string of equipment type distribution
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="The user who uploaded this dataset"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the dataset was uploaded"
    )
    file = models.FileField(
        upload_to='datasets/',
        help_text="The uploaded CSV file"
    )
    
    # Calculated analytics
    total_equipment = models.IntegerField(
        default=0,
        help_text="Total number of equipment entries"
    )
    avg_flowrate = models.FloatField(
        default=0.0,
        help_text="Average flowrate across all equipment"
    )
    avg_pressure = models.FloatField(
        default=0.0,
        help_text="Average pressure across all equipment"
    )
    avg_temperature = models.FloatField(
        default=0.0,
        help_text="Average temperature across all equipment"
    )
    equipment_types = models.TextField(
        default='{}',
        help_text="JSON string containing equipment type distribution"
    )
    
    class Meta:
        ordering = ['-uploaded_at']  # Newest first
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'
    
    def __str__(self):
        """String representation of the dataset"""
        return f"Dataset {self.id} - {self.user.username} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class EquipmentData(models.Model):
    """
    Stores individual equipment records from the CSV.
    
    Fields:
    - dataset: Link to the parent Dataset
    - equipment_name: Name of the equipment
    - equipment_type: Type/category of equipment
    - flowrate: Flowrate value
    - pressure: Pressure value
    - temperature: Temperature value
    """
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='equipment_records',
        help_text="The dataset this equipment belongs to"
    )
    equipment_name = models.CharField(
        max_length=200,
        help_text="Name of the equipment"
    )
    equipment_type = models.CharField(
        max_length=100,
        help_text="Type/category of equipment"
    )
    flowrate = models.FloatField(
        help_text="Flowrate value"
    )
    pressure = models.FloatField(
        help_text="Pressure value"
    )
    temperature = models.FloatField(
        help_text="Temperature value"
    )
    
    class Meta:
        ordering = ['equipment_name']
        verbose_name = 'Equipment Data'
        verbose_name_plural = 'Equipment Data'
    
    def __str__(self):
        """String representation of the equipment"""
        return f"{self.equipment_name} ({self.equipment_type})"
