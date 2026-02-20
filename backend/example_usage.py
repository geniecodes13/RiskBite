"""
Example usage of RISKbite backend
This shows how to use the API programmatically
"""

import requests
import json

# Backend URL
API_URL = "http://localhost:8000"

def health_check():
    """Check if backend is running"""
    response = requests.get(f"{API_URL}/")
    print("Health Check Response:")
    print(json.dumps(response.json(), indent=2))
    print()


def scan_product(image_path, conditions=None):
    """
    Scan a product label
    
    Args:
        image_path: Path to product image
        conditions: List of health conditions (e.g., ['diabetes', 'peanut_allergy'])
    """
    if not conditions:
        conditions = []
    
    print(f"Scanning: {image_path}")
    print(f"Conditions: {conditions}\n")
    
    with open(image_path, "rb") as img:
        files = {
            "image": img,
        }
        data = {
            "conditions": json.dumps(conditions)
        }
        
        response = requests.post(
            f"{API_URL}/scan",
            files=files,
            data=data
        )
    
    if response.status_code == 200:
        result = response.json()
        print("Scan Results:")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Risk Score: {result['risk_score']}/100")
        print(f"  Ingredients: {len(result['ingredients'])} found")
        
        if result['warnings']:
            print(f"\n  ⚠️  {len(result['warnings'])} warnings:")
            for warning in result['warnings']:
                print(f"\n    • {warning['ingredient']}")
                print(f"      Reason: {warning['reason']}")
                print(f"      Alternative: {warning['alternative']}")
        
        print(f"\n  Summary: {result['summary']}")
    else:
        print(f"Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    
    print("\n" + "="*60 + "\n")


def test_scenarios():
    """Test different scenarios"""
    
    print("="*60)
    print("RISKbite Backend - Test Scenarios")
    print("="*60)
    print()
    
    # Test 1: Health check
    print("TEST 1: Health Check")
    print("-" * 60)
    health_check()
    
    # Test 2: Scan without conditions (all ingredients)
    print("TEST 2: Scan Without Conditions")
    print("-" * 60)
    print("This would scan and show all risky ingredients")
    print("Example: scan_product('cereal_label.jpg')\n")
    
    # Test 3: Scan with diabetes condition
    print("TEST 3: Scan With Diabetes")
    print("-" * 60)
    print("This would highlight sugar and high-glycemic ingredients")
    print("Example: scan_product('snack_label.jpg', ['diabetes'])\n")
    
    # Test 4: Scan with multiple conditions
    print("TEST 4: Scan With Multiple Conditions")
    print("-" * 60)
    print("This would show warnings for all matching conditions")
    print("Example: scan_product('label.jpg', ['diabetes', 'peanut_allergy', 'gluten_sensitivity'])\n")


if __name__ == "__main__":
    print("\n🥗 RISKbite Backend - API Examples\n")
    
    # Show what you can do
    test_scenarios()
    
    # Uncomment to test with real images:
    # health_check()
    # scan_product("path/to/product_image.jpg", ["diabetes"])
    # scan_product("path/to/product_image.jpg", ["diabetes", "peanut_allergy"])
