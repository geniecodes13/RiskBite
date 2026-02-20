"""
Explainer Service
Provides human-friendly explanations for ingredients by fetching descriptions from ingredients database.
"""
import re
from app.data.ingredients import INGREDIENTS_DB


class ExplainerService:
    """Service to explain ingredients using descriptions from INGREDIENTS_DB"""

    @staticmethod
    def explain(ingredient: str) -> str:
        """
        Explain an ingredient by looking up description in INGREDIENTS_DB.
        Falls back to generic message if not found.
        
        Args:
            ingredient: The ingredient name to explain
            
        Returns:
            Description/explanation text for the ingredient
        """
        if not ingredient:
            return "No explanation available."

        ing = ingredient.lower().strip()

        # Try exact match first
        if ing in INGREDIENTS_DB:
            return INGREDIENTS_DB[ing].get("description", "This ingredient is commonly used in foods.")

        # Try partial matches
        for db_ingredient, data in INGREDIENTS_DB.items():
            if db_ingredient in ing or ing in db_ingredient:
                return data.get("description", "This ingredient is commonly used in foods.")

        # Generic fallback for numeric INS/E codes
        m = re.search(r"\b(?:ins|e)\s*-?\s*(\d{2,4})\b", ing)
        if m:
            num = m.group(1)
            return f"For more information about INS/E{num}, you can search the browser."

        # Generic friendly fallback
        return "For more information, you can search the browser."
