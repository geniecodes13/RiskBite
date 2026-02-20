# RISKbite Backend - Setup & Installation Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Tesseract OCR installed on your system

### 1. Install Tesseract OCR

#### **Windows:**
```bash
# Option 1: Use installers
https://github.com/UB-Mannheim/tesseract/wiki

# Download and run: tesseract-ocr-w64-setup-v5.x.x.exe
# Note the installation path (C:\Program Files\Tesseract-OCR)

# Then set environment variable:
set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

#### **macOS:**
```bash
brew install tesseract
```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

### 2. Set Up Python Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment (.env)

```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your settings (optional for local development)
```

### 4. Run the Server

```bash
# From backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or simply:
python app/main.py
```

Server will start at: **http://localhost:8000**

## 📚 API Documentation

Once running, visit:
- **API Docs (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

## 🔌 Example API Usage

### Health Check
```bash
curl http://localhost:8000/
```

### Scan Product
```bash
curl -X POST http://localhost:8000/scan \
  -F "image=@product_label.jpg" \
  -F "conditions=['diabetes', 'peanut_allergy']"
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app & endpoints
│   ├── models.py              # Pydantic request/response models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ocr_service.py     # Text extraction from images
│   │   ├── parser_service.py  # Ingredient parsing & cleaning
│   │   └── risk_engine.py     # Risk analysis & warning generation
│   └── data/
│       ├── __init__.py
│       └── ingredients.py     # Ingredient knowledge base (100+ items)
├── requirements.txt            # Python dependencies
├── .env.example               # Environment configuration
└── README.md                  # This file
```

## 🛠️ Key Components

### 1. **OCR Service** (`ocr_service.py`)
- Extracts text from product label images
- Uses Tesseract OCR
- Includes image preprocessing

### 2. **Parser Service** (`parser_service.py`)
- Locates ingredient section in raw text
- Splits and cleans ingredient names
- Normalizes ingredient variants

### 3. **Risk Engine** (`risk_engine.py`)
- Matches ingredients against knowledge base
- Calculates overall risk score (0-100)
- Generates personalized warnings based on user conditions
- Creates friendly summaries

### 4. **Ingredient Database** (`ingredients.py`)
- 100+ ingredients with:
  - Risk level (low/medium/high)
  - Health tags (diabetes, allergen, etc.)
  - Human-readable descriptions
  - Safe alternatives

## 🧪 Testing the API

### Test with Postman or cURL:

**1. Health Check:**
```bash
curl -X GET http://localhost:8000/
```

**2. Scan Product (with conditions):**
```bash
curl -X POST http://localhost:8000/scan \
  -F "image=@test_label.jpg" \
  -F 'conditions=["diabetes", "peanut_allergy"]'
```

**3. Response Example:**
```json
{
  "ingredients": ["sugar", "sodium benzoate", "peanut oil"],
  "risk_level": "High",
  "risk_score": 85,
  "warnings": [
    {
      "ingredient": "sugar",
      "reason": "High glycemic index – not suitable for diabetics. This is particularly problematic for your diabetes management.",
      "alternative": "Stevia, Erythritol, Monk Fruit"
    },
    {
      "ingredient": "peanut oil",
      "reason": "Contains peanuts which trigger allergic reactions. This can trigger your peanut allergy.",
      "alternative": "Sunflower seed butter"
    }
  ],
  "summary": "⚠️ We found 2 ingredients of concern. We strongly recommend looking for an alternative product."
}
```

## 🚨 Troubleshooting

### Issue: Tesseract not found
```
pytesseract.TesseractNotInstalledError: tesseract is not installed
```
**Solution:** Install Tesseract OCR (see section 1 above)

### Issue: CORS errors (frontend can't reach backend)
**Solution:** Ensure `CORS_ORIGINS` in `.env` includes your frontend URL

### Issue: Image extraction returns empty
**Possible causes:**
- Image too small or blurry
- Label text too small
- Poor lighting in image
**Solution:** Try with clearer, well-lit product label image

### Issue: Module not found errors
**Solution:**
```bash
# Make sure you're in virtual environment
source venv/bin/activate  # or activate on Windows
pip install -r requirements.txt
```

## 📊 Performance Notes

- **OCR Processing:** ~2-5 seconds per image (depends on image quality)
- **Ingredient Analysis:** ~100ms
- **Total response time:** 2-6 seconds

## 🔐 Security Considerations (Production)

1. **Image Size Limits:** Add file size validation
2. **Rate Limiting:** Implement request throttling
3. **Authentication:** Add API key or JWT auth
4. **CORS:** Specify exact allowed origins
5. **Input Validation:** Sanitize all inputs
6. **Logging:** Implement structured logging with sensitive data masking

## 📈 Future Enhancements

- [ ] Database integration for ingredient tracking
- [ ] ML-based ingredient recognition (instead of just OCR)
- [ ] Batch processing for multiple products
- [ ] User authentication & history
- [ ] Alternative product recommendations
- [ ] Nutritional information extraction
- [ ] Multi-language support

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review FastAPI docs: https://fastapi.tiangolo.com/
3. Check Tesseract docs: https://github.com/UB-Mannheim/tesseract/wiki

---

**Happy Hacking! 🚀**
