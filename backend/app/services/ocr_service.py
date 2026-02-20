"""
OCR Service - Extracts text from product label images using Tesseract
"""

"""
OCR Service - Extracts text from product label images using Tesseract
"""

import os
import io
import logging
import shutil
from typing import Optional

import pytesseract
from PIL import Image, ImageEnhance

logger = logging.getLogger(__name__)

# ==================== Tesseract Configuration ====================

TESSERACT_ENV = os.environ.get("TESSERACT_CMD") or os.environ.get("TESSERACT_PATH")

# Candidate locations to check for the tesseract executable
_candidates = []
if TESSERACT_ENV:
    _candidates.append(TESSERACT_ENV)

_candidates.extend([
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
])

# If tesseract is on PATH, shutil.which will find it
which_path = shutil.which("tesseract")
if which_path:
    _candidates.append(which_path)

# Configure pytesseract using the first valid candidate
configured = False
for _p in _candidates:
    try:
        if _p and os.path.exists(_p):
            pytesseract.pytesseract.tesseract_cmd = _p
            logger.info(f"Tesseract OCR path configured: {_p}")
            configured = True
            break
    except Exception:
        continue

if not configured:
    logger.warning(
        "Tesseract executable not found. Install Tesseract or set the TESSERACT_CMD/TESSERACT_PATH environment variable."
    )

# Allow a mock OCR mode for development/testing when Tesseract isn't available.
MOCK_OCR = os.environ.get("MOCK_OCR", "0") in ["1", "true", "True"]
if MOCK_OCR:
    logger.info("MOCK_OCR is enabled - OCRService will return canned text for testing")


class OCRService:
    """Service for optical character recognition on product labels"""

    @staticmethod
    def extract_text_from_image(image_bytes: bytes) -> str:
        """
        Extract text from product label image using Tesseract OCR
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Extracted text (empty string if extraction fails)
        """
        try:
            # If Tesseract not configured and MOCK_OCR enabled, return sample ingredients
            if not configured and MOCK_OCR:
                sample = (
                    "Ingredients: sugar, water, high fructose corn syrup, peanuts, milk, salt"
                )
                logger.info("MOCK_OCR: returning sample ingredient text")
                return sample
            # Preprocess image first
            processed_bytes = OCRService.preprocess_for_ocr(image_bytes)

            # Load image
            image = Image.open(io.BytesIO(processed_bytes))
            image = image.convert("RGB")

            # OCR config optimized for labels
            custom_config = r"--oem 3 --psm 6"

            extracted_text = pytesseract.image_to_string(
                image,
                config=custom_config
            )

            extracted_text = extracted_text.strip()
            logger.info(f"OCR extraction successful ({len(extracted_text)} chars)")

            return extracted_text

        except pytesseract.TesseractNotFoundError:
            logger.error("Tesseract OCR not installed or not in PATH")
            return ""

        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}", exc_info=True)
            return ""

    @staticmethod
    def preprocess_for_ocr(image_bytes: bytes) -> bytes:
        """
        Preprocess image to improve OCR accuracy
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Preprocessed image bytes
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))

            # Convert to grayscale
            image = image.convert("L")

            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)

            # Optional resize (helps small text)
            image = image.resize(
                (image.width * 2, image.height * 2),
                Image.Resampling.LANCZOS
            )

            output = io.BytesIO()
            image.save(output, format="PNG")
            return output.getvalue()

        except Exception as e:
            logger.warning(f"OCR preprocessing failed, using original image: {str(e)}")
            return image_bytes

'''
import os
import pytesseract

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if not os.path.exists(TESSERACT_PATH):
    raise RuntimeError(f"Tesseract not found at {TESSERACT_PATH}")

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


'pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe C"' # Ensure Tesseract is in PATH
from PIL import Image
import io
import logging
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)


class OCRService:
    """Service for optical character recognition on product labels"""

    @staticmethod
    def extract_text_from_image(image_bytes: bytes) -> Optional[str]:
        """
        Extract text from product label image using Tesseract OCR
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Extracted text from image or None if extraction fails
        """
        try:
            # Open image from bytes
            image = Image.open(io.BytesIO(image_bytes))
            
            # Optional: Resize image for better OCR results
            # image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)
            
            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(image)
            
            logger.info(f"OCR extraction successful. Extracted {len(extracted_text)} characters")
            return extracted_text
            
        except pytesseract.TesseractNotFoundError:
            logger.error("Tesseract not installed. Please install it first.")
            raise RuntimeError(
                "Tesseract OCR not installed. Please install: "
                "https://github.com/UB-Mannheim/tesseract/wiki"
            )
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return None

    @staticmethod
    def preprocess_for_ocr(image_bytes: bytes) -> bytes:
        """
        Preprocess image to improve OCR accuracy
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Preprocessed image bytes
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to grayscale for better OCR
            image = image.convert('L')
            
            # Optional: Enhance contrast
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2)
            
            # Convert back to bytes
            output = io.BytesIO()
            image.save(output, format='PNG')
            return output.getvalue()
            
        except Exception as e:
            logger.warning(f"Preprocessing failed, using original: {str(e)}")
            return image_bytes
'''