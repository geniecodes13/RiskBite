#!/usr/bin/env python
"""Quick test for health parser service"""

from app.services.health_parser_service import HealthParserService
import json

# Test cases
test_inputs = [
    "I have diabetes, I am allergic to peanuts and shellfish, and I am lactose intolerant",
    "I'm vegan and have a gluten sensitivity",
    "I'm pescatarian and allergic to shellfish",
    "No allergies, just prefer vegetarian food",
]

print("=" * 80)
print("Health Parser Service - Test Results")
print("=" * 80)

for test_input in test_inputs:
    print(f"\nInput: {test_input}")
    print("-" * 80)
    
    result = HealthParserService.parse_health_text(test_input)
    is_valid, message = HealthParserService.validate_parsed_data(result)
    
    print(f"Valid: {is_valid} ({message})")
    print(f"Confidence: {result['confidence']:.0%}")
    print("Parsed Data:")
    print(json.dumps({k: v for k, v in result.items() if k != 'raw_input'}, indent=2))

print("\n" + "=" * 80)
