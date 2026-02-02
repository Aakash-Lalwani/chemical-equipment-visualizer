"""
Desktop App Configuration Template

SETUP INSTRUCTIONS:
1. Copy this file to 'config.py' in the same directory
2. Update BACKEND_URL with your actual backend server URL
3. DO NOT commit config.py to git (it's in .gitignore)

Security Note:
- Authentication tokens are stored in memory only during app session
- For production use, consider using the 'keyring' library for secure token storage
"""

# Backend API Base URL
# Development (local backend):
BACKEND_URL = 'http://localhost:8000/api'

# Production (deployed backend):
# BACKEND_URL = 'https://your-backend.railway.app/api'

# Optional: Enable debug logging
DEBUG = True
