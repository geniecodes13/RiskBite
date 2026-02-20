import requests

# Test OAuth endpoint
r = requests.get('http://localhost:8000/auth/google/login', allow_redirects=False)
print('Status:', r.status_code)
print('Location:', r.headers.get('location'))
