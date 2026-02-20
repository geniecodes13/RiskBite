#!/usr/bin/env python
"""Integration test for health history with humanised language"""

import json
import sys
from app.services.health_parser_service import HealthParserService

print("\n" + "=" * 80)
print("RISKbite Health History - Humanised Language Integration Test")
print("=" * 80)

# Test 1: Health Parser Service
print("\n[TEST 1] Health Parser Service")
print("-" * 80)

test_cases = [
    ("I have diabetes, I'm allergic to peanuts and shellfish, I'm lactose intolerant",
     {"diabetes": True, "peanut_allergy": True, "shellfish_allergy": True, "lactose_intolerance": True}),
    ("I'm vegan and have gluten sensitivity",
     {"vegan": True, "gluten_sensitivity": True}),
    ("I'm pescatarian",
     {"pescatarian": True}),
]

all_passed = True

for input_text, expected_conditions in test_cases:
    print(f"\nInput: {input_text}")
    result = HealthParserService.parse_health_text(input_text)
    is_valid, message = HealthParserService.validate_parsed_data(result)
    
    if not is_valid:
        print(f"  ❌ FAILED: {message}")
        all_passed = False
        continue
    
    # Check if expected conditions are found
    parsed_conditions = result.get("conditions", {})
    conditions_match = all(
        parsed_conditions.get(key) == value 
        for key, value in expected_conditions.items()
    )
    
    if conditions_match:
        print(f"  ✓ PASSED")
        print(f"    - Confidence: {result['confidence']:.0%}")
        print(f"    - Conditions found: {len([v for v in parsed_conditions.values() if v])} positive")
    else:
        print(f"  ❌ FAILED: Expected conditions don't match")
        print(f"    Expected: {expected_conditions}")
        print(f"    Got: {parsed_conditions}")
        all_passed = False

# Test 2: Validation
print("\n[TEST 2] Validation Logic")
print("-" * 80)

# Test with empty input
empty_result = HealthParserService.parse_health_text("")
is_valid, msg = HealthParserService.validate_parsed_data(empty_result)
if not is_valid and "No health conditions" in msg:
    print("✓ PASSED: Empty input properly rejected")
else:
    print(f"❌ FAILED: Empty input validation - {msg}")
    all_passed = False

# Test with input that has no recognizable health conditions
no_health_text = "something random that has no health info"
no_health_result = HealthParserService.parse_health_text(no_health_text)
is_valid, msg = HealthParserService.validate_parsed_data(no_health_result)
if not is_valid and "No health conditions" in msg:
    print("✓ PASSED: Input with no health conditions properly rejected")
else:
    print(f"❌ FAILED: No health conditions validation - {msg}")
    all_passed = False

# Test 3: Negation Detection
print("\n[TEST 3] Negation Detection")
print("-" * 80)

negation_text = "I don't have diabetes, but I'm allergic to peanuts"
neg_result = HealthParserService.parse_health_text(negation_text)
if not neg_result["conditions"].get("diabetes") and neg_result["conditions"].get("peanut_allergy"):
    print("✓ PASSED: Negation properly detected")
else:
    print(f"❌ FAILED: Negation detection")
    print(f"   Parsed: {neg_result['conditions']}")
    all_passed = False

# Summary
print("\n" + "=" * 80)
if all_passed:
    print("✓ ALL TESTS PASSED")
    print("\nImplementation Summary:")
    print("- Frontend component updated to accept humanised language")
    print("- New /parse-health endpoint created for natural language processing")
    print("- Health history stored with parsed structured data")
    print("- Confidence scoring and validation implemented")
    sys.exit(0)
else:
    print("❌ SOME TESTS FAILED")
    sys.exit(1)
