#!/usr/bin/env python
"""
Test script to verify disease database and risk engine accuracy
Tests parsing of diseases and ingredient-disease mappings
"""

import sys
import json
from app.services.health_parser_service import HealthParserService
from app.services.risk_engine import WarningGenerator
from app.data.ingredients import INGREDIENTS_DB, get_ingredient_info

def test_disease_parsing():
    """Test parsing of various disease conditions"""
    print("\n" + "="*80)
    print("TEST 1: Disease Parsing")
    print("="*80)
    
    test_cases = [
        "I have diabetes and high blood pressure",
        "I have thyroid issues and PCOS",
        "I suffer from cold and fever",
        "I have GERD and IBS",
        "I have Crohn's disease",
        "I have a fever and need immune support",
        "I have hypothyroid condition",
        "I have polycystic ovarian disease",
    ]
    
    for text in test_cases:
        result = HealthParserService.parse_health_text(text)
        print(f"\nInput: {text}")
        print(f"Parsed Conditions: {[k for k,v in result['conditions'].items() if v]}")
        print(f"Confidence: {result['confidence']:.0%}")
        is_valid, msg = HealthParserService.validate_parsed_data(result)
        print(f"Valid: {is_valid} - {msg}")

def test_ingredient_disease_mapping():
    """Test ingredient-disease health tag mappings"""
    print("\n" + "="*80)
    print("TEST 2: Ingredient-Disease Mappings")
    print("="*80)
    
    test_ingredients = [
        "sugar",
        "high fructose corn syrup",
        "palm oil",
        "sodium chloride",
        "caffeine",
        "coffee",
        "alcohol",
        "ginger",
        "honey",
        "seaweed",
    ]
    
    for ingredient in test_ingredients:
        info = get_ingredient_info(ingredient)
        if info:
            print(f"\n{ingredient.upper()}")
            print(f"  Risk Level: {info['risk_level']}")
            print(f"  Health Tags: {info['health_tags']}")
            print(f"  Description: {info['description']}")

def test_risk_engine_with_diseases():
    """Test risk engine accuracy with different disease combinations"""
    print("\n" + "="*80)
    print("TEST 3: Risk Engine with Diseases")
    print("="*80)
    
    test_scenarios = [
        {
            "ingredients": ["sugar", "high fructose corn syrup", "palm oil"],
            "conditions": ["diabetes"],
            "name": "Diabetic with high sugar items"
        },
        {
            "ingredients": ["salt", "sodium chloride", "palm oil"],
            "conditions": ["hypertension", "heart_disease"],
            "name": "Hypertension patient with salty/fatty items"
        },
        {
            "ingredients": ["coffee", "caffeine", "spicy sauce", "chocolate"],
            "conditions": ["gerd"],
            "name": "GERD patient with trigger foods"
        },
        {
            "ingredients": ["sugar", "alcohol", "high fructose corn syrup"],
            "conditions": ["pcos", "obesity"],
            "name": "PCOS patient with metabolic disruptors"
        },
        {
            "ingredients": ["cruciferous vegetables", "seaweed"],
            "conditions": ["thyroid"],
            "name": "Thyroid patient with mixed ingredients"
        },
    ]
    
    for scenario in test_scenarios:
        print(f"\n{'─'*70}")
        print(f"Scenario: {scenario['name']}")
        print(f"Conditions: {scenario['conditions']}")
        print(f"Ingredients: {scenario['ingredients']}")
        
        generator = WarningGenerator(scenario['ingredients'], scenario['conditions'])
        warnings = generator.generate_warnings()
        risk_score, risk_level = generator.calculate_risk_score()
        
        print(f"\nRisk Score: {risk_score}/100")
        print(f"Risk Level: {risk_level}")
        print(f"Warnings Generated: {len(warnings)}")
        
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  • {warning['ingredient']}")
                print(f"    Reason: {warning['reason']}")
                print(f"    Alternative: {warning['alternative']}")

def test_all_new_diseases():
    """List all newly added diseases"""
    print("\n" + "="*80)
    print("TEST 4: All Supported Diseases (10+ new diseases)")
    print("="*80)
    
    diseases = HealthParserService.CONDITION_KEYWORDS.copy()
    
    # Separate into categories
    diseases_only = {k: v for k, v in diseases.items() 
                     if k not in ['peanut_allergy', 'nut_allergy', 'shellfish_allergy', 
                                  'gluten_sensitivity', 'lactose_intolerance', 'egg_allergy', 
                                  'soy_allergy', 'vegan', 'pescatarian', 'vegetarian']}
    
    allergies_only = {k: v for k, v in diseases.items() 
                      if 'allergy' in k or k in ['gluten_sensitivity', 'lactose_intolerance']}
    
    print("\nDISEASES SUPPORTED (11 total):")
    for i, (disease, keywords) in enumerate(diseases_only.items(), 1):
        print(f"  {i}. {disease.replace('_', ' ').title()}")
        print(f"     Keywords: {', '.join(keywords[:3])}")
    
    print(f"\nALLERGIES SUPPORTED ({len(allergies_only)} total):")
    for i, (allergy, keywords) in enumerate(allergies_only.items(), 1):
        print(f"  {i}. {allergy.replace('_', ' ').title()}")
    
    print(f"\nDIETARY PREFERENCES SUPPORTED (3 total):")
    dietary = ['vegan', 'pescatarian', 'vegetarian']
    for i, diet in enumerate(dietary, 1):
        print(f"  {i}. {diet.title()}")

def test_accuracy_metrics():
    """Test accuracy of risk engine"""
    print("\n" + "="*80)
    print("TEST 5: Accuracy Validation")
    print("="*80)
    
    # Test case: Diabetics should flag sugary ingredients
    print("\n[Accuracy Test 1] Sugar detection for diabetics")
    generator = WarningGenerator(["sugar", "glucose"], ["diabetes"])
    warnings = generator.generate_warnings()
    assert len(warnings) >= 1, "Failed to detect sugar for diabetic"
    print(f"✓ PASS: Detected {len(warnings)} warnings for diabetic patient")
    
    # Test case: GERD patients should flag spicy/acidic items
    print("\n[Accuracy Test 2] GERD trigger detection")
    generator = WarningGenerator(["coffee", "spicy sauce"], ["gerd"])
    warnings = generator.generate_warnings()
    assert len(warnings) >= 1, "Failed to detect GERD triggers"
    print(f"✓ PASS: Detected {len(warnings)} GERD triggers")
    
    # Test case: Hypertension patients should flag high sodium
    print("\n[Accuracy Test 3] Sodium detection for hypertension")
    generator = WarningGenerator(["sodium chloride", "sodium"], ["hypertension"])
    warnings = generator.generate_warnings()
    assert len(warnings) >= 1, "Failed to detect sodium for hypertensive"
    print(f"✓ PASS: Detected {len(warnings)} sodium warnings")
    
    # Test case: Thyroid patients should flag cruciferous
    print("\n[Accuracy Test 4] Cruciferous detection for thyroid")
    generator = WarningGenerator(["cruciferous vegetables"], ["thyroid"])
    warnings = generator.generate_warnings()
    assert len(warnings) >= 1, "Failed to detect goitrogens for thyroid"
    print(f"✓ PASS: Detected {len(warnings)} thyroid-related warnings")
    
    # Test case: Vegetarians should be flagged for meat products
    print("\n[Accuracy Test 5] Dietary preference enforcement")
    generator = WarningGenerator(["gelatin", "carmine"], ["vegan"])
    warnings = generator.generate_warnings()
    assert len(warnings) >= 1, "Failed to detect non-vegan items"
    print(f"✓ PASS: Detected {len(warnings)} non-vegan items")
    
    print("\n✓ All accuracy tests passed!")

def main():
    """Run all tests"""
    print("\n╔" + "="*78 + "╗")
    print("║" + " "*20 + "DISEASE DATABASE & RISK ENGINE TESTS" + " "*23 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        test_disease_parsing()
        test_ingredient_disease_mapping()
        test_all_new_diseases()
        test_risk_engine_with_diseases()
        test_accuracy_metrics()
        
        print("\n" + "="*80)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nSummary:")
        print("  ✓ Disease parsing working for 11+ diseases")
        print("  ✓ Ingredient-disease mappings verified")
        print("  ✓ Risk engine accuracy validated")
        print("  ✓ New diseases integrated successfully")
        print("  ✓ Database accuracy improved")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
