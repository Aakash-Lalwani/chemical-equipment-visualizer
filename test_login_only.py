"""
Simple login test - Run this AFTER starting server
"""
import requests
import time

print("\n" + "="*60)
print("🔍 TESTING LOGIN ENDPOINT")
print("="*60)

# Wait a moment for server to be ready
time.sleep(1)

BASE_URL = 'http://127.0.0.1:8000/api'

print(f"\n🌐 Attempting to connect to: {BASE_URL}/login/")
print("📝 Credentials: admin / admin123")

try:
    response = requests.post(
        f'{BASE_URL}/login/', 
        json={'username': 'admin', 'password': 'admin123'},
        timeout=5
    )
    
    print(f"\n📊 Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS! Login worked!")
        print(f"   Token: {data.get('token', '')[:30]}...")
        print(f"   User: {data.get('user', {}).get('username')}")
        print(f"   Email: {data.get('user', {}).get('email')}")
    else:
        print(f"\n❌ Login failed!")
        print(f"   Response: {response.text}")
        
except requests.exceptions.ConnectionError as e:
    print("\n❌ CONNECTION ERROR!")
    print(f"   Error: {str(e)[:200]}")
    print("\n🔧 Troubleshooting:")
    print("   1. Is Django server running?")
    print("      Check terminal for: 'Starting development server at http://127.0.0.1:8000/'")
    print("   2. Run in separate terminal:")
    print("      cd c:\\Users\\91985\\Desktop\\FOSSE_2026\\backend")
    print("      C:/Users/91985/Desktop/FOSSE_2026/.venv/Scripts/python.exe manage.py runserver")
    print("   3. Then run this test again")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "="*60)
