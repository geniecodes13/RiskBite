"""
Health Parser Service
Converts humanised natural language health information into structured data
"""

import re
import logging
from typing import Dict, List, Set

logger = logging.getLogger(__name__)


class HealthParserService:
    """Parse natural language health descriptions into structured data"""

    # Keyword mappings for conditions and preferences
    CONDITION_KEYWORDS = {
        # ===== COMMON DISEASES =====
        "diabetes": ["diabetes", "diabetic", "blood sugar", "glucose", "type 2 diabetes", "type 1 diabetes", "pre-diabetic"],
        "cold": ["cold", "common cold", "runny nose", "congestion", "nasal congestion"],
        "fever": ["fever", "high temperature", "elevated temperature", "febrile"],
        "hypertension": ["hypertension", "high blood pressure", "bp high", "elevated bp", "high tension"],
        "heart_disease": ["heart disease", "cardiac", "heart condition", "coronary", "heart attack history"],
        
        # ===== ALLERGIES =====
        "peanut_allergy": ["peanut", "peanuts", "peanut allergy"],
        "nut_allergy": ["nut", "nuts", "nut allergy", "tree nut", "almond", "cashew", "walnut"],
        "shellfish_allergy": ["shellfish", "shrimp", "crustacean", "lobster", "crab", "prawn"],
        "gluten_sensitivity": ["gluten", "celiac", "coeliac", "gluten-free", "gluten free"],
        "lactose_intolerance": ["lactose", "lactose intolerance", "lactose-free", "dairy", "milk intolerance"],
        "egg_allergy": ["egg allergy", "eggs", "egg intolerance"],
        "soy_allergy": ["soy", "soy allergy", "soya"],
        
        # ===== METABOLIC & HORMONAL =====
        "thyroid": ["thyroid", "thyroid disease", "hypothyroid", "hyperthyroid", "thyroid condition"],
        "pcos": ["pcos", "polycystic", "polycystic ovarian", "pcod"],
        "obesity": ["obesity", "obese", "overweight", "weight gain prone"],
        
        # ===== DIGESTIVE =====
        "ibs": ["ibs", "irritable bowel", "IBS", "bowel syndrome"],
        "crohn_disease": ["crohn", "crohns", "crohn's disease", "inflammatory bowel"],
        "gerd": ["gerd", "acid reflux", "heartburn", "reflux"],
        
        # ===== DIETARY PREFERENCES =====
        "vegan": ["vegan", "plant-based", "no animal products", "no meat no dairy"],
        "pescatarian": ["pescatarian", "pescetarian", "fish only", "vegetarian but eat fish"],
        "vegetarian": ["vegetarian", "no meat", "meat-free", "no flesh"],
    }

    DENIAL_KEYWORDS = ["no", "don't", "dont", "not", "none", "never", "without", "excluding", "except"]

    @staticmethod
    def parse_health_text(text: str) -> Dict:
        """
        Parse natural language health information into structured format
        
        Args:
            text: Natural language description of health conditions
            
        Returns:
            Dictionary with parsed health information
        """
        if not text or not isinstance(text, str):
            return {
                "conditions": {},
                "allergies": [],
                "dietary_preferences": [],
                "raw_input": text,
                "confidence": 0.0
            }

        # Normalize text
        text_lower = text.lower()
        text_clean = text_lower.replace("-", " ")

        # Initialize result
        result = {
            "conditions": {},
            "allergies": [],
            "dietary_preferences": [],
            "raw_input": text,
            "confidence": 0.0
        }

        # Track what was found
        found_items = []

        # Parse each condition/preference
        for condition, keywords in HealthParserService.CONDITION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_clean:
                    # Check if negated
                    if HealthParserService._is_negated(text_clean, keyword):
                        result["conditions"][condition] = False
                    else:
                        result["conditions"][condition] = True
                    found_items.append(condition)
                    break

        # Categorize into allergies and dietary preferences
        allergies = {"peanut_allergy", "nut_allergy", "shellfish_allergy", "gluten_sensitivity", "lactose_intolerance", "egg_allergy", "soy_allergy"}
        dietary = {"vegan", "pescatarian", "vegetarian"}
        diseases = {"diabetes", "cold", "fever", "hypertension", "heart_disease", "thyroid", "pcos", "obesity", "ibs", "crohn_disease", "gerd"}

        for condition, value in result["conditions"].items():
            if value:  # Only include if True
                if condition in allergies:
                    result["allergies"].append(condition.replace("_", " ").title())
                elif condition in dietary:
                    result["dietary_preferences"].append(condition.replace("_", " ").title())
                # Diseases are kept in conditions dictionary with their original keys

        # Calculate confidence based on number of recognized items
        word_count = len(text_clean.split())
        unique_keywords_found = len(set(found_items))
        result["confidence"] = min(1.0, unique_keywords_found / max(word_count / 5, 1))

        logger.info(f"Parsed health text. Found conditions: {found_items}, Confidence: {result['confidence']:.2%}")

        return result

    @staticmethod
    def _is_negated(text: str, keyword: str) -> bool:
        """Check if a keyword is negated in the text"""
        # Find the keyword position
        keyword_pos = text.find(keyword)
        if keyword_pos == -1:
            return False

        # Look back up to 20 characters for negation keywords
        search_start = max(0, keyword_pos - 20)
        preceding_text = text[search_start:keyword_pos]

        for denial in HealthParserService.DENIAL_KEYWORDS:
            if denial in preceding_text:
                return True

        return False

    @staticmethod
    def validate_parsed_data(parsed: Dict) -> tuple[bool, str]:
        """
        Validate parsed health data
        
        Returns:
            Tuple of (is_valid, message)
        """
        if not isinstance(parsed, dict):
            return False, "Parsed data must be a dictionary"

        if "conditions" not in parsed or not isinstance(parsed["conditions"], dict):
            return False, "Missing or invalid 'conditions' field"

        # Check if any conditions are True (valid)
        has_conditions = any(v for v in parsed["conditions"].values() if v)
        if not has_conditions:
            return False, "No health conditions recognized in the input"

        if parsed.get("confidence", 0) < 0.3:
            return False, f"Low confidence in parsing ({parsed['confidence']:.0%}). Please be more specific."

        return True, "Valid health data"
