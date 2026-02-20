"""
Risk Engine - Analyzes ingredients and generates personalized health warnings
"""

import logging
from typing import List, Tuple, Dict, Optional
from app.data.ingredients import INGREDIENTS_DB, get_ingredient_info, get_risk_score_for_ingredient

logger = logging.getLogger(__name__)


class WarningGenerator:
    """Generates personalized health warnings for ingredients"""

    def __init__(self, ingredients: List[str], user_conditions: Optional[List[str]] = None):
        """
        Initialize warning generator
        
        Args:
            ingredients: List of ingredients to analyze
            user_conditions: List of user health conditions (e.g., ['diabetes', 'peanut_allergy'])
        """
        self.ingredients = ingredients
        self.user_conditions = user_conditions or []
        self.warnings = []
        self.risk_scores = []

    def generate_warnings(self) -> List[Dict]:
        """
        Generate personalized warnings for each ingredient
        
        Returns:
            List of warning dictionaries
        """
        warnings = []
        
        for ingredient in self.ingredients:
            ingredient_info = get_ingredient_info(ingredient)
            
            if not ingredient_info:
                logger.debug(f"No info found for ingredient: {ingredient}")
                continue
            
            # Check if ingredient is relevant to user's conditions
            if self._is_relevant_to_user(ingredient_info):
                warning = self._create_warning(ingredient, ingredient_info)
                if warning:
                    warnings.append(warning)
        
        self.warnings = warnings
        return warnings

    def _is_relevant_to_user(self, ingredient_info: Dict) -> bool:
        """
        Check if ingredient warning is relevant to user's health conditions
        
        Args:
            ingredient_info: Ingredient information dictionary
            
        Returns:
            True if relevant to user, False otherwise
        """
        if not self.user_conditions:
            # Show all medium/high risk if no conditions specified
            return ingredient_info["risk_level"] in ["medium", "high"]
        
        ingredient_tags = ingredient_info["health_tags"]
        
        # Check for condition matches
        condition_mapping = {
            # Diseases
            "diabetes": ["diabetes"],
            "cold": ["cold", "immune_support"],
            "fever": ["cold", "immune_support"],
            "hypertension": ["hypertension", "heart_disease", "sodium"],
            "heart_disease": ["heart_disease", "saturated_fat"],
            "thyroid": ["thyroid", "iodine"],
            "pcos": ["pcos", "hormonal_balance", "insulin_resistance"],
            "obesity": ["weight_gain", "high_calorie"],
            "ibs": ["digestive", "fiber_content"],
            "crohn_disease": ["crohn", "digestive", "inflammatory"],
            "gerd": ["gerd", "acid_forming"],
            
            # Allergies
            "peanut_allergy": ["peanut_allergy", "allergen"],
            "nut_allergy": ["nut_allergy", "allergen"],
            "shellfish_allergy": ["shellfish_allergy", "allergen"],
            "egg_allergy": ["egg_allergy", "allergen"],
            "soy_allergy": ["soy_allergy", "allergen"],
            "gluten_sensitivity": ["gluten_sensitivity", "celiac"],
            "lactose_intolerance": ["lactose_intolerance", "digestive"],
            
            # Dietary
            "vegan": ["vegan", "animal_product"],
            "pescatarian": ["fish", "vegan"],  # Pescatarians avoid meat but eat fish
        }
        
        for condition in self.user_conditions:
            tags_to_match = condition_mapping.get(condition, [condition])
            for tag in tags_to_match:
                if tag in ingredient_tags:
                    return True
        
        # Always show high risk regardless of conditions
        if ingredient_info["risk_level"] == "high":
            return True
        
        return False

    def _create_warning(self, ingredient: str, ingredient_info: Dict) -> Optional[Dict]:
        """
        Create a warning dictionary for an ingredient
        
        Args:
            ingredient: Ingredient name
            ingredient_info: Ingredient information
            
        Returns:
            Warning dictionary or None
        """
        reason = self._personalize_reason(ingredient_info)
        
        if not reason:
            return None
        
        return {
            "ingredient": ingredient,
            "reason": reason,
            "description": ingredient_info.get("description", ""),
            "risk_level": ingredient_info.get("risk_level", "medium"),
            "alternative": ingredient_info["safe_alternative"],
            "why": ingredient_info.get("why", "")
        }

    def _personalize_reason(self, ingredient_info: Dict) -> str:
        """
        Create personalized reason based on user conditions
        
        Args:
            ingredient_info: Ingredient information
            
        Returns:
            Personalized reason string
        """
        reason = ingredient_info["description"]
        
        # Enhance reason based on user conditions
        ingredient_tags = ingredient_info["health_tags"]
        
        for condition in self.user_conditions:
            # Diseases
            if condition == "diabetes" and "diabetes" in ingredient_tags:
                return f"{reason} This is particularly problematic for your diabetes management."
            elif condition == "hypertension" and "hypertension" in ingredient_tags:
                return f"{reason} This can worsen your high blood pressure."
            elif condition == "heart_disease" and "heart_disease" in ingredient_tags:
                return f"{reason} This is risky for your heart condition."
            elif condition == "thyroid" and "thyroid" in ingredient_tags:
                return f"{reason} This may interfere with your thyroid function."
            elif condition == "pcos" and "pcos" in ingredient_tags:
                return f"{reason} This can trigger hormonal imbalances related to your PCOS."
            elif condition == "cold" and "immune_support" in ingredient_tags:
                return f"{reason} Avoid this while you have cold symptoms."
            elif condition == "fever" and "immune_support" in ingredient_tags:
                return f"{reason} This is not recommended during fever."
            elif condition == "obesity" and ("weight_gain" in ingredient_tags or "high_calorie" in ingredient_tags):
                return f"{reason} This can contribute to weight gain."
            elif condition == "ibs" and "digestive" in ingredient_tags:
                return f"{reason} This can trigger your IBS symptoms."
            elif condition == "crohn_disease" and "inflammatory" in ingredient_tags:
                return f"{reason} This may aggravate your Crohn's disease."
            elif condition == "gerd" and "acid_forming" in ingredient_tags:
                return f"{reason} This can trigger acid reflux."
            
            # Allergies
            elif condition == "peanut_allergy" and "peanut_allergy" in ingredient_tags:
                return f"{reason} This can trigger your peanut allergy."
            elif condition == "nut_allergy" and "nut_allergy" in ingredient_tags:
                return f"{reason} This can trigger your nut allergy."
            elif condition == "shellfish_allergy" and "shellfish_allergy" in ingredient_tags:
                return f"{reason} This can trigger your shellfish allergy."
            elif condition == "egg_allergy" and "egg_allergy" in ingredient_tags:
                return f"{reason} This can trigger your egg allergy."
            elif condition == "soy_allergy" and "soy_allergy" in ingredient_tags:
                return f"{reason} This can trigger your soy allergy."
            elif condition == "gluten_sensitivity" and "gluten_sensitivity" in ingredient_tags:
                return f"{reason} This is unsuitable for your gluten sensitivity."
            elif condition == "lactose_intolerance" and "lactose_intolerance" in ingredient_tags:
                return f"{reason} This will cause digestive issues due to your lactose intolerance."
            
            # Dietary
            elif condition == "vegan" and "vegan" in ingredient_tags:
                return f"{reason} This product is not suitable for your vegan diet."
            elif condition == "pescatarian" and "animal_product" in ingredient_tags:
                if "fish" not in ingredient_tags:  # Pescatarians eat fish
                    return f"{reason} This is animal product not suitable for pescatarian diet."
        
        return reason

    def calculate_risk_score(self) -> Tuple[int, str]:
        """
        Calculate overall risk score (0-100) and risk level
        
        Returns:
            Tuple of (risk_score, risk_level)
        """
        if not self.ingredients:
            return 0, "Low"
        
        total_score = 0
        high_risk_count = 0
        
        for ingredient in self.ingredients:
            ingredient_info = get_ingredient_info(ingredient)
            if not ingredient_info:
                continue
            
            score = get_risk_score_for_ingredient(ingredient)
            total_score += score
            
            if ingredient_info["risk_level"] == "high":
                high_risk_count += 1
        
        # Calculate average
        avg_score = total_score // len(self.ingredients) if self.ingredients else 0
        
        # Determine risk level
        if high_risk_count >= 3 or avg_score >= 60:
            risk_level = "High"
        elif high_risk_count >= 1 or avg_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return avg_score, risk_level

    def generate_summary(self, risk_level: str, warning_count: int) -> str:
        """
        Generate friendly summary of scan results
        
        Args:
            risk_level: Overall risk level
            warning_count: Number of warnings found
            
        Returns:
            Summary string
        """
        if warning_count == 0:
            return "Great news! This product contains no problematic ingredients for your health conditions."
        
        if risk_level == "High":
            return f"⚠️ We found {warning_count} ingredients of concern. We strongly recommend looking for an alternative product."
        elif risk_level == "Medium":
            return f"We found {warning_count} ingredient(s) that may require caution. Consider safer alternatives if available."
        else:
            return f"This product is generally safe, though we found {warning_count} ingredient(s) to be aware of."


class RiskEngine:
    """Main risk analysis engine"""

    @staticmethod
    def analyze_ingredients(
        ingredients: List[str],
        user_conditions: Optional[List[str]] = None
    ) -> Dict:
        """
        Analyze ingredients and generate risk assessment
        
        Args:
            ingredients: List of ingredient names
            user_conditions: List of user health conditions
            
        Returns:
            Dictionary with risk analysis results
        """
        # Generate warnings
        warning_gen = WarningGenerator(ingredients, user_conditions)
        warnings = warning_gen.generate_warnings()
        
        # Calculate risk score
        risk_score, risk_level = warning_gen.calculate_risk_score()
        
        # Generate summary
        summary = warning_gen.generate_summary(risk_level, len(warnings))
        
        return {
            "ingredients": ingredients,
            "warnings": warnings,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "summary": summary
        }
