"""
Integration Test Script for RISKbite 4.0
Tests user auth, health history, and OAuth flow
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "TestPass123!"

def log_test(test_name: str, status: str, details: str = ""):
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"STATUS: {status}")
    if details:
        print(f"DETAILS: {details}")
    print('='*60)

def test_health_check():
    """Test if backend is running"""
    try:
        resp = requests.get(f"{BASE_URL}/", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            log_test("Backend Health Check", "✅ PASS", f"Status: {data.get('status')}")
            return True
        else:
            log_test("Backend Health Check", "❌ FAIL", f"Status code: {resp.status_code}")
            return False
    except Exception as e:
        log_test("Backend Health Check", "❌ FAIL", f"Connection error: {str(e)}")
        return False

def test_register_user(email: str = TEST_EMAIL, password: str = TEST_PASSWORD):
    """Test user registration"""
    try:
        payload = {"email": email, "password": password}
        resp = requests.post(f"{BASE_URL}/auth/register", json=payload, timeout=5)
        
        if resp.status_code == 200:
            data = resp.json()
            log_test("User Registration", "✅ PASS", f"User ID: {data.get('user_id')}, Email: {data.get('email')}")
            return True, data.get('user_id')
        elif resp.status_code == 400 and "already registered" in resp.text:
            log_test("User Registration", "⚠️  INFO", "User already exists (will use existing account)")
            # Try to get user ID from login instead
            return test_login_user(email, password)
        else:
            log_test("User Registration", "❌ FAIL", f"Status: {resp.status_code}, Response: {resp.text}")
            return False, None
    except Exception as e:
        log_test("User Registration", "❌ FAIL", f"Error: {str(e)}")
        return False, None

def test_login_user(email: str = TEST_EMAIL, password: str = TEST_PASSWORD):
    """Test user login"""
    try:
        payload = {"email": email, "password": password}
        resp = requests.post(f"{BASE_URL}/auth/login", json=payload, timeout=5)
        
        if resp.status_code == 200:
            data = resp.json()
            log_test("User Login", "✅ PASS", f"User ID: {data.get('user_id')}, Email: {data.get('email')}")
            return True, data.get('user_id')
        else:
            log_test("User Login", "❌ FAIL", f"Status: {resp.status_code}, Response: {resp.text}")
            return False, None
    except Exception as e:
        log_test("User Login", "❌ FAIL", f"Error: {str(e)}")
        return False, None

def test_save_health_history(user_id: int):
    """Test saving health history"""
    try:
        health_data = {
            "data": {
                "diabetes": True,
                "allergies": ["peanuts", "shellfish"],
                "bloodType": "O+",
                "medications": ["Metformin"]
            }
        }
        resp = requests.post(
            f"{BASE_URL}/health/{user_id}",
            json=health_data,
            timeout=5
        )
        
        if resp.status_code == 200:
            data = resp.json()
            log_test("Save Health History", "✅ PASS", f"History ID: {data.get('history_id')}")
            return True
        else:
            log_test("Save Health History", "❌ FAIL", f"Status: {resp.status_code}, Response: {resp.text}")
            return False
    except Exception as e:
        log_test("Save Health History", "❌ FAIL", f"Error: {str(e)}")
        return False

def test_get_health_history(user_id: int):
    """Test retrieving health history"""
    try:
        resp = requests.get(f"{BASE_URL}/health/{user_id}", timeout=5)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('ok') and data.get('history'):
                log_test("Get Health History", "✅ PASS", f"Retrieved: {json.dumps(data.get('history'), indent=2)}")
                return True
            elif data.get('ok'):
                log_test("Get Health History", "⚠️  INFO", "No health history saved yet")
                return True
            else:
                log_test("Get Health History", "❌ FAIL", f"Response: {data}")
                return False
        else:
            log_test("Get Health History", "❌ FAIL", f"Status: {resp.status_code}")
            return False
    except Exception as e:
        log_test("Get Health History", "❌ FAIL", f"Error: {str(e)}")
        return False

def test_oauth_configured():
    """Check if OAuth is properly configured"""
    try:
        resp = requests.get(f"{BASE_URL}/auth/google/login", timeout=5, allow_redirects=False)
        
        if resp.status_code in [307, 302]:  # Redirect to Google
            log_test("OAuth Configuration", "✅ PASS", "OAuth is configured and redirects to Google")
            return True
        elif resp.status_code == 500:
            log_test("OAuth Configuration", "❌ FAIL", "OAuth not configured - check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env")
            return False
        else:
            log_test("OAuth Configuration", "⚠️  INFO", f"Unexpected status: {resp.status_code}")
            return True
    except Exception as e:
        log_test("OAuth Configuration", "❌ FAIL", f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run complete integration test suite"""
    print("\n" + "="*60)
    print("🧪 RISKbite 4.0 Integration Test Suite")
    print("="*60)
    
    results = {}
    
    # Test 1: Health check
    results["health_check"] = test_health_check()
    if not results["health_check"]:
        print("\n❌ Backend is not running. Start it with:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return results
    
    # Test 2: OAuth config
    results["oauth_config"] = test_oauth_configured()
    
    # Test 3: Register/Login
    success, user_id = test_register_user()
    results["registration"] = success
    
    if not success or user_id is None:
        print("\n⚠️  Registration failed, trying login...")
        success, user_id = test_login_user()
        results["login"] = success
    
    if user_id:
        # Test 4: Save health history
        results["save_health"] = test_save_health_history(user_id)
        
        # Test 5: Get health history
        results["get_health"] = test_get_health_history(user_id)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    total_tests = len([v for v in results.values() if v is not None])
    passed_tests = len([v for v in results.values() if v is True])
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Application is ready to use.")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Check details above.")
    
    print("="*60)

if __name__ == "__main__":
    run_all_tests()
