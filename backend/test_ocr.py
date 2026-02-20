from app.services.ocr_service import OCRService

# Load a test image as bytes
with open("test.jpg", "rb") as f:
    image_bytes = f.read()

# Run OCR
text = OCRService.extract_text_from_image(image_bytes)

print("OCR OUTPUT:")
print(text)
