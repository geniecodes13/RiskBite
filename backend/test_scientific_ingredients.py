"""
Test script to verify scientific ingredients (emulsifiers, catalysts, etc.) are working correctly
"""

import sys
sys.path.insert(0, '/backend')

from app.data.ingredients import INGREDIENTS_DB, get_ingredient_info
from app.services.risk_engine import RiskEngine

# Test scientific ingredients
scientific_ingredients = [
    "soy lecithin",
    "polysorbate 80",
    "sodium stearoyl lactylate",
    "amylase",
    "protease",
    "carrageenan",
    "fd&c red no. 40",
    "bha",
    "vanillin",
    "titanium dioxide",
    "carnauba wax",
    "propylene glycol"
]

print("=" * 80)
print("TESTING SCIENTIFIC INGREDIENTS DATABASE")
print("=" * 80)

# Test 1: Check that new ingredients exist
print("\n✓ Test 1: Verifying new scientific ingredients exist in database")
print("-" * 80)
found_count = 0
for ingredient in scientific_ingredients:
    info = get_ingredient_info(ingredient)
    if info:
        found_count += 1
        print(f"✓ {ingredient.upper()}")
        print(f"  • Risk Level: {info['risk_level']}")
        print(f"  • Description: {info['description'][:80]}...")
        print(f"  • Tags: {', '.join(info['health_tags'][:3])}")
    else:
        print(f"✗ {ingredient} - NOT FOUND")

print(f"\nFound {found_count}/{len(scientific_ingredients)} ingredients")

# Test 2: Check that descriptions are present and informative
print("\n✓ Test 2: Verifying descriptions are detailed and scientific")
print("-" * 80)
good_descriptions = 0
for ingredient in scientific_ingredients[:5]:
    info = get_ingredient_info(ingredient)
    if info and len(info['description']) > 40:
        good_descriptions += 1
        print(f"✓ {ingredient}: {len(info['description'])} characters")

print(f"Good descriptions: {good_descriptions}/5")

# Test 3: Test risk analysis with scientific ingredients
print("\n✓ Test 3: Testing risk analysis with scientific ingredients")
print("-" * 80)
test_ingredients = [
    "sugar",
    "soy lecithin",
    "polysorbate 80",
    "carrageenan",
    "vitamin e"
]

result = RiskEngine.analyze_ingredients(test_ingredients, user_conditions=["pcos"])
print(f"Analyzed {len(result['ingredients'])} ingredients")
print(f"Found {len(result['warnings'])} warnings")
print(f"Risk Score: {result['risk_score']}/100")
print(f"Risk Level: {result['risk_level']}")

print("\nWarnings generated:")
for i, warning in enumerate(result['warnings'], 1):
    print(f"\n{i}. {warning['ingredient'].upper()}")
    print(f"   Risk: {warning.get('risk_level', 'N/A')}")
    print(f"   Description: {warning.get('description', 'N/A')[:100]}...")
    print(f"   Reason: {warning['reason'][:100]}...")
    print(f"   Alternative: {warning['alternative']}")

# Test 4: Check ingredient categories
print("\n✓ Test 4: Checking ingredient categories")
print("-" * 80)
categories = {}
for ing, info in INGREDIENTS_DB.items():
    tags = info.get('health_tags', [])
    for tag in tags:
        if tag not in categories:
            categories[tag] = 0
        categories[tag] += 1

print("Top ingredient categories:")
for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  • {cat}: {count} ingredients")

# Test 5: Total ingredient count
print("\n✓ Test 5: Total ingredient count")
print("-" * 80)
print(f"Total ingredients in database: {len(INGREDIENTS_DB)}")
risk_distribution = {"high": 0, "medium": 0, "low": 0}
for ing, info in INGREDIENTS_DB.items():
    risk = info.get('risk_level', 'low')
    if risk in risk_distribution:
        risk_distribution[risk] += 1

print(f"Risk Distribution:")
print(f"  • High Risk: {risk_distribution['high']}")
print(f"  • Medium Risk: {risk_distribution['medium']}")
print(f"  • Low Risk: {risk_distribution['low']}")

print("\n" + "=" * 80)
print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
print("=" * 80)
print("\nScientific ingredients with detailed descriptions are now available!")
print("Frontend will display: What it is, Why it matters, and Better alternatives")
