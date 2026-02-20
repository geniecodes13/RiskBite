"""
Pydantic models for request/response validation
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from typing import Dict


# ==================== Request Models ====================

class HealthCondition(BaseModel):
    """User health conditions and preferences"""
    diabetes: bool = False
    peanut_allergy: bool = False
    gluten_sensitivity: bool = False
    lactose_intolerance: bool = False
    nut_allergy: bool = False
    shellfish_allergy: bool = False
    vegan: bool = False
    pescatarian: bool = False


class ScanRequest(BaseModel):
    """Request payload for product scanning"""
    conditions: Optional[List[str]] = Field(
        default=None,
        description="List of user health conditions (e.g., ['diabetes', 'peanut_allergy'])"
    )


# ==================== Response Models ====================

class WarningResponse(BaseModel):
    """Single ingredient warning"""
    ingredient: str = Field(description="Name of the flagged ingredient")
    reason: str = Field(description="Why this ingredient is problematic")
    alternative: str = Field(description="Recommended safer alternative")


class ScanResponse(BaseModel):
    """Response from product scan endpoint"""
    ingredients: List[str] = Field(description="Extracted ingredients from product label")
    risk_level: str = Field(description="Overall risk level: Low, Medium, or High")
    risk_score: int = Field(description="Risk score 0-100")
    warnings: List[WarningResponse] = Field(description="List of ingredient warnings")
    explanations: Optional[Dict[str, str]] = Field(
        default=None,
        description="Mapping of ingredient -> simple explanation (plain language)"
    )
    extracted_text: Optional[str] = Field(
        default=None,
        description="Raw OCR extracted text from the product label"
    )
    summary: Optional[str] = Field(description="Friendly summary of the scan")


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    version: str
