"""
CSV Processing Utilities.

WHAT: Functions to read, validate, and analyze CSV files.
WHY: We need to extract data and calculate statistics from uploaded CSVs.
HOW: Use Pandas to read CSV and calculate averages.
"""

import pandas as pd
import json
from typing import Dict, Tuple, List


def process_csv_file(file_path: str) -> Tuple[bool, Dict, str]:
    """
    Process a CSV file and extract equipment data with analytics.
    
    Args:
        file_path: Path to the CSV file
    
    Returns:
        Tuple of (success, data_dict, error_message)
        - success: Boolean indicating if processing was successful
        - data_dict: Dictionary containing analytics and equipment records
        - error_message: Error message if processing failed
    
    Example:
        success, data, error = process_csv_file('/path/to/file.csv')
        if success:
            print(f"Total equipment: {data['total_equipment']}")
    """
    try:
        # Read CSV file using Pandas
        df = pd.read_csv(file_path)
        
        # Normalize column names to be case-insensitive
        # Strip whitespace and convert to lowercase for matching
        df.columns = df.columns.str.strip()
        
        # Create mapping of lowercase column names to actual column names
        column_mapping = {col.lower(): col for col in df.columns}
        
        # Define required columns (lowercase for comparison)
        required_columns_lower = ['equipment name', 'type', 'flowrate', 'pressure', 'temperature']
        
        # Check for required columns (case-insensitive)
        missing_columns = []
        for req_col in required_columns_lower:
            if req_col not in column_mapping:
                missing_columns.append(req_col.replace('equipment name', 'Equipment Name').title())
        
        if missing_columns:
            return False, {}, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Rename columns to standardized format
        standard_names = {
            'equipment name': 'Equipment Name',
            'type': 'Type',
            'flowrate': 'Flowrate',
            'pressure': 'Pressure',
            'temperature': 'Temperature'
        }
        
        # Build rename mapping from actual columns to standard names
        rename_mapping = {}
        for lower_col, actual_col in column_mapping.items():
            if lower_col in standard_names:
                rename_mapping[actual_col] = standard_names[lower_col]
        
        df = df.rename(columns=rename_mapping)
        
        # Now work with standardized column names
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        
        # Remove rows with any missing values
        df_clean = df.dropna(subset=required_columns)
        
        if len(df_clean) == 0:
            return False, {}, "No valid data rows found in CSV file"
        
        # Convert numeric columns to float, replacing any invalid values with NaN
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        for col in numeric_columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Remove rows where numeric conversion failed
        df_clean = df_clean.dropna(subset=numeric_columns)
        
        if len(df_clean) == 0:
            return False, {}, "No valid numeric data found in CSV file"
        
        # Calculate analytics
        total_equipment = len(df_clean)
        avg_flowrate = float(df_clean['Flowrate'].mean())
        avg_pressure = float(df_clean['Pressure'].mean())
        avg_temperature = float(df_clean['Temperature'].mean())
        
        # Calculate equipment type distribution
        type_counts = df_clean['Type'].value_counts().to_dict()
        equipment_types = json.dumps(type_counts)
        
        # Prepare equipment records as list of dictionaries
        equipment_records = []
        for _, row in df_clean.iterrows():
            equipment_records.append({
                'equipment_name': str(row['Equipment Name']),
                'equipment_type': str(row['Type']),
                'flowrate': float(row['Flowrate']),
                'pressure': float(row['Pressure']),
                'temperature': float(row['Temperature'])
            })
        
        # Prepare result dictionary
        result = {
            'total_equipment': total_equipment,
            'avg_flowrate': round(avg_flowrate, 2),
            'avg_pressure': round(avg_pressure, 2),
            'avg_temperature': round(avg_temperature, 2),
            'equipment_types': equipment_types,
            'equipment_records': equipment_records
        }
        
        return True, result, ""
    
    except FileNotFoundError:
        return False, {}, "File not found"
    
    except pd.errors.EmptyDataError:
        return False, {}, "CSV file is empty"
    
    except pd.errors.ParserError:
        return False, {}, "Invalid CSV format"
    
    except Exception as e:
        return False, {}, f"Error processing CSV: {str(e)}"


def validate_csv_size(file_size: int, max_size_mb: int = 10) -> Tuple[bool, str]:
    """
    Validate if CSV file size is within acceptable limits.
    
    Args:
        file_size: Size of file in bytes
        max_size_mb: Maximum allowed size in megabytes (default: 10MB)
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Example:
        is_valid, error = validate_csv_size(file.size, max_size_mb=10)
        if not is_valid:
            return Response({'error': error}, status=400)
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file_size > max_size_bytes:
        return False, f"File size exceeds {max_size_mb}MB limit"
    
    return True, ""


def get_equipment_type_chart_data(equipment_types_json: str) -> Dict:
    """
    Convert equipment types JSON string to chart-friendly format.
    
    Args:
        equipment_types_json: JSON string of equipment type distribution
    
    Returns:
        Dictionary with 'labels' and 'values' arrays for Chart.js
    
    Example:
        chart_data = get_equipment_type_chart_data(dataset.equipment_types)
        # Returns: {'labels': ['Reactor', 'Pump'], 'values': [3, 5]}
    """
    try:
        types_dict = json.loads(equipment_types_json)
        return {
            'labels': list(types_dict.keys()),
            'values': list(types_dict.values())
        }
    except:
        return {'labels': [], 'values': []}
