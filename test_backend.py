"""
Quick Backend Test Script

WHAT: Tests if all backend components are working
WHY: Quick verification before demo
HOW: Makes API calls to test endpoints

Run this to verify backend is working properly.
"""

import requests
import json

# Configuration
BASE_URL = 'http://localhost:8000/api'
USERNAME = 'admin'
PASSWORD = 'admin123'

def print_result(test_name, success, message=''):
    """Print test result"""
    status = '✅ PASS' if success else '❌ FAIL'
    print(f'{status} - {test_name}')
    if message:
        print(f'     {message}')

def test_backend():
    """Run all backend tests"""
    print('\n' + '='*60)
    print('BACKEND API TESTS')
    print('='*60 + '\n')
    
    token = None
    dataset_id = None
    
    # Test 1: Server is running
    try:
        response = requests.get(f'{BASE_URL}/login/', timeout=2)
        print_result('Server Running', response.status_code in [200, 405], 
                    f'Status: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print_result('Server Running', False, 'Backend not running! Start with: python manage.py runserver')
        return
    
    # Test 2: Login
    try:
        response = requests.post(f'{BASE_URL}/login/', 
                                json={'username': USERNAME, 'password': PASSWORD})
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print_result('Login', True, f'Token: {token[:20]}...')
        else:
            print_result('Login', False, f'Status: {response.status_code}')
            return
    except Exception as e:
        print_result('Login', False, str(e))
        return
    
    # Test 3: Upload History (should work even if empty)
    try:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(f'{BASE_URL}/upload-history/', headers=headers)
        if response.status_code == 200:
            history = response.json()
            print_result('Get History', True, f'Found {len(history)} datasets')
            if len(history) > 0:
                dataset_id = history[0]['id']
        else:
            print_result('Get History', False, f'Status: {response.status_code}')
    except Exception as e:
        print_result('Get History', False, str(e))
    
    # Test 4: Get Dataset Summary (if we have a dataset)
    if dataset_id:
        try:
            headers = {'Authorization': f'Token {token}'}
            response = requests.get(f'{BASE_URL}/datasets/{dataset_id}/summary/', 
                                  headers=headers)
            if response.status_code == 200:
                data = response.json()
                print_result('Get Dataset Summary', True, 
                           f'Total equipment: {data["total_equipment"]}')
            else:
                print_result('Get Dataset Summary', False, 
                           f'Status: {response.status_code}')
        except Exception as e:
            print_result('Get Dataset Summary', False, str(e))
    else:
        print_result('Get Dataset Summary', None, 
                    'Skipped - No datasets available (upload one first)')
    
    # Test 5: Invalid Token (should fail)
    try:
        headers = {'Authorization': 'Token invalid123'}
        response = requests.get(f'{BASE_URL}/upload-history/', headers=headers)
        if response.status_code == 401:
            print_result('Invalid Token Rejected', True, 'Unauthorized as expected')
        else:
            print_result('Invalid Token Rejected', False, 
                        'Security issue: Invalid token was accepted!')
    except Exception as e:
        print_result('Invalid Token Rejected', False, str(e))
    
    print('\n' + '='*60)
    print('TESTS COMPLETE')
    print('='*60)
    print('\nNext steps:')
    print('1. Upload a CSV file using the web or desktop app')
    print('2. Verify charts and data display correctly')
    print('3. Download a PDF report')
    print('4. Check upload history\n')

if __name__ == '__main__':
    test_backend()
