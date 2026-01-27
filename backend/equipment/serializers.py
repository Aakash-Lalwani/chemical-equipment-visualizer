"""
Serializers for Equipment API.

WHAT: Serializers convert model instances to JSON and vice versa.
WHY: APIs communicate using JSON, not Python objects.
HOW: Define which fields to include and how to validate them.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, EquipmentData


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EquipmentDataSerializer(serializers.ModelSerializer):
    """Serializer for individual equipment records"""
    class Meta:
        model = EquipmentData
        fields = [
            'id',
            'equipment_name',
            'equipment_type',
            'flowrate',
            'pressure',
            'temperature'
        ]


class DatasetSerializer(serializers.ModelSerializer):
    """Serializer for Dataset with related equipment records"""
    user = UserSerializer(read_only=True)
    equipment_records = EquipmentDataSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id',
            'user',
            'uploaded_at',
            'file',
            'total_equipment',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'equipment_types',
            'equipment_records'
        ]
        read_only_fields = [
            'uploaded_at',
            'total_equipment',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'equipment_types'
        ]


class DatasetListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing datasets (without equipment records)"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id',
            'user',
            'uploaded_at',
            'total_equipment',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'equipment_types'
        ]
