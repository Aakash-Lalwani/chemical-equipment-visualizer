"""Quick API Test Script"""
import requests
import time

BASE_URL = 'http://127.0.0.1:8000/api'

print("\n" + "="*60)
print("🚀 BACKEND API TEST")
print("="*60)

# Wait for server to be ready
print("\n⏳ Waiting for server...")
time.sleep(2)

# Test 1: Login
print("\n📝 TEST 1: Login")
try:
    response = requests.post(
        f'{BASE_URL}/login/', 
        json={'username': 'admin', 'password': 'admin123'},
        timeout=3
    )
    if response.status_code == 200:
        data = response.json()
        token = data['token']
        print(f"✅ SUCCESS - Token: {token[:30]}...")
        print(f"   User: {data['user']['username']}")
    else:
        print(f"❌ FAILED - Status {response.status_code}")
        exit()
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit()

# Test 2: Upload History
print("\n📝 TEST 2: Upload History")
try:
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{BASE_URL}/upload-history/', headers=headers, timeout=3)
    if response.status_code == 200:
        datasets = response.json()
        print(f"✅ SUCCESS - Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"   → Dataset {ds['id']}: {ds['total_equipment']} equipment")
    else:
        print(f"❌ FAILED - Status {response.status_code}")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 3: Upload CSV
print("\n📝 TEST 3: CSV Upload")
try:
    csv_path = r'c:\Users\91985\Desktop\FOSSE_2026\sample_equipment_data.csv'
    with open(csv_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f'{BASE_URL}/upload-csv/', 
            headers=headers, 
            files=files,
            timeout=5
        )
    if response.status_code == 201:
        data = response.json()
        print(f"✅ SUCCESS - Dataset ID: {data['id']}")
        print(f"   Total Equipment: {data['total_equipment']}")
        print(f"   Avg Flowrate: {data['avg_flowrate']:.2f}")
        print(f"   Avg Pressure: {data['avg_pressure']:.2f}")
        print(f"   Avg Temperature: {data['avg_temperature']:.2f}")
        dataset_id = data['id']
    else:
        print(f"❌ FAILED - Status {response.status_code}: {response.text[:100]}")
        dataset_id = None
except FileNotFoundError:
    print(f"❌ ERROR: CSV file not found")
    dataset_id = None
except Exception as e:
    print(f"❌ ERROR: {e}")
    dataset_id = None

# Test 4: Get Summary
if dataset_id:
    print("\n📝 TEST 4: Dataset Summary")
    try:
        response = requests.get(
            f'{BASE_URL}/datasets/{dataset_id}/summary/', 
            headers=headers,
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS")
            print(f"   Equipment Records: {len(data['equipment_records'])}")
            print(f"   Chart Labels: {data['chart_data']['labels']}")
        else:
            print(f"❌ FAILED - Status {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

print("\n" + "="*60)
print("✨ ALL TESTS COMPLETE!")
print("="*60 + "\n")
