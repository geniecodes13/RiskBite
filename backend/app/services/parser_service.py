"""
Parser Service - Extracts and normalizes ingredient lists from OCR text
"""

import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class ParserService:
    """Service for parsing ingredient text from OCR results"""

    # Keywords that precede ingredient lists
    INGREDIENT_KEYWORDS = [
        'ingredients',
        'ingredients:',
        'contains:',
        'contains',
        'product contains',
        'ingredient list',
        'may contain',
        'may contain:',
        'produced with',
        'produced in facility with'
    ]

    # Common separators between ingredients
    SEPARATORS = [',', '|', ';', '\n', '\t']

    @staticmethod
    def extract_ingredients_section(text: str) -> str:
        """
        Extract the ingredients section from OCR text
        
        Args:
            text: Full OCR text from product label
            
        Returns:
            Ingredient section text
        """
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Find where ingredients section starts
        ingredient_start = -1
        for keyword in ParserService.INGREDIENT_KEYWORDS:
            idx = text_lower.find(keyword)
            if idx != -1:
                ingredient_start = idx + len(keyword)
                break
        
        if ingredient_start == -1:
            logger.warning("Ingredient section not found in OCR text")
            return text  # Fall back to full text
        
        # Extract from ingredient start to potential nutrition section
        ingredient_text = text[ingredient_start:]
        
        # Try to find where ingredients end (usually before "Nutrition Facts" or similar)
        end_keywords = ['nutrition', 'nutritional information', 'allergen', 'storage', 'directions']
        end_idx = len(ingredient_text)
        
        for keyword in end_keywords:
            idx = ingredient_text.lower().find(keyword)
            if idx != -1 and idx > 0:
                end_idx = min(end_idx, idx)
        
        return ingredient_text[:end_idx]

    @staticmethod
    def parse_ingredients(text: str) -> List[str]:
        """
        Parse and normalize ingredient list from text
        
        Args:
            text: Ingredient section text
            
        Returns:
            List of cleaned ingredient names
        """
        # Extract ingredients section
        ingredients_section = ParserService.extract_ingredients_section(text)
        
        # Split by common separators
        ingredients = []
        current_ingredient = ""
        
        for char in ingredients_section:
            if char in ParserService.SEPARATORS:
                if current_ingredient.strip():
                    ingredients.append(current_ingredient.strip())
                current_ingredient = ""
            else:
                current_ingredient += char
        
        # Add last ingredient
        if current_ingredient.strip():
            ingredients.append(current_ingredient.strip())
        
        # Clean and normalize ingredients
        cleaned = []
        for ingredient in ingredients:
            cleaned_ing = ParserService.clean_ingredient_name(ingredient)
            if cleaned_ing and len(cleaned_ing) > 2:  # Ignore very short strings
                cleaned.append(cleaned_ing)
        
        logger.info(f"Parsed {len(cleaned)} ingredients from text")
        return cleaned

    @staticmethod
    def clean_ingredient_name(ingredient: str) -> str:
        """
        Clean and normalize ingredient name
        
        Args:
            ingredient: Raw ingredient name
            
        Returns:
            Cleaned ingredient name
        """
        # Convert to lowercase
        ingredient = ingredient.lower().strip()
        
        # Remove common prefixes/suffixes
        prefixes = ['contains: ', 'may contain: ', 'produced with ', 'includes ']
        for prefix in prefixes:
            if ingredient.startswith(prefix):
                ingredient = ingredient[len(prefix):]
        
        # Remove parenthetical info (but keep it for context)
        # e.g., "soy (from soy lecithin)" -> "soy lecithin"
        ingredient = re.sub(r'\(.*?\)', '', ingredient)
        
        # Remove percentage signs and numbers at the end
        ingredient = re.sub(r'\s*\d+%?\s*$', '', ingredient)
        
        # Remove multiple spaces
        ingredient = re.sub(r'\s+', ' ', ingredient).strip()
        
        # Remove special characters except for common ones like hyphens
        ingredient = re.sub(r'[^a-z0-9\s\-]', '', ingredient)
        
        return ingredient.strip()

    @staticmethod
    def match_ingredient_variants(ingredient: str) -> str:
        """
        Match ingredient variants to standardized names
        
        Args:
            ingredient: Raw ingredient name
            
        Returns:
            Standardized ingredient name
        """
        # Dictionary of ingredient variants -> standard names
        variants = {
            'hfcs': 'high fructose corn syrup',
            'corn syrup': 'high fructose corn syrup',
            'msg': 'monosodium glutamate',
            'salt': 'sodium chloride',
            'sodium': 'sodium chloride',
            'butter': 'milk',
            'cheese': 'milk',
            'yogurt': 'milk',
            'cream': 'milk',
            'wheat flour': 'wheat',
            'whole wheat': 'wheat',
            'artificial flavor': 'artificial colors',
            'beef broth': 'beef',
            'chicken broth': 'chicken',
            'artificial sweetener': 'aspartame',
            'seed oil': 'palm oil',
        }
        
        ingredient_lower = ingredient.lower()
        
        # Check for exact and partial matches
        for variant, standard in variants.items():
            if variant in ingredient_lower:
                return standard
        
        return ingredient

    @staticmethod
    def extract_allergen_info(text: str) -> List[str]:
        """
        Extract allergen information from text
        
        Args:
            text: Full OCR text
            
        Returns:
            List of detected allergens
        """
        allergens = []
        known_allergens = [
            'peanuts', 'tree nuts', 'milk', 'eggs', 'shellfish',
            'fish', 'wheat', 'gluten', 'sesame', 'soy', 'sulfites'
        ]
        
        text_lower = text.lower()
        for allergen in known_allergens:
            if allergen in text_lower:
                allergens.append(allergen)
        
        return allergens
