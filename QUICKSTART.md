# 🚀 RISKbite - Complete Hackathon Setup Guide

## ⚡ Quick Start (5 minutes)

### Step 1: Install Tesseract OCR (Required)

**Windows:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer: `tesseract-ocr-w64-setup-v5.x.x.exe`
3. Note installation path (usually `C:\Program Files\Tesseract-OCR`)

**macOS:**
```bash
brew install tesseract

```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### Step 2: Setup Backend

```bash
# Navigate to backend
cd backend

# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start server
python run_server.py  # Windows
# or
bash run_server.sh  # macOS/Linux
```

**Server will start at:** http://localhost:8000

### Step 3: 

**Frontend will be at:** http://localhost:5173 (or similar)

---

## 🔑 OAuth Configuration (Required)

### Step 1: Add your Google OAuth credentials

1. Open `backend/.env`
2. Add your credentials:
```
GOOGLE_CLIENT_ID=126543276755-jc4d1niu399o4jidcc1o1ogk17o8kc5h.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=YOUR_SECRET_HERE
FRONTEND_URL=http://localhost:5173
```

3. **Get your Client Secret:**
   - Go to https://console.cloud.google.com
   - Navigate to APIs & Services → Credentials
   - Find your OAuth 2.0 Client ID
   - Click it and copy the Client Secret
   - Paste into `.env`

### Step 2: Restart Backend
```powershell
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ Backend running successfully!

---

## 🎯 Feature Testing Checklist

### ✅ Authentication
- [x] Email/Password Registration
- [x] Email/Password Login  
- [x] Google OAuth Login
- [x] User not found error handling
- [x] Password hashing (bcrypt)

### ✅ Health History
- [x] Save user health data
- [x] Retrieve last saved health record
- [x] JSON-based storage
- [x] User-specific database entries

### ✅ Product Scanning (Original Feature)
- [x] Image upload
- [x] OCR text extraction
- [x] Ingredient parsing
- [x] Risk analysis
- [x] Health condition filtering

### ✅ Navigation
- [x] Login page
- [x] Home (scanning) page
- [x] Health History page
- [x] User session display
- [x] Logout button

---

## 📖 User Flows

### Flow 1: Google OAuth Login
```
[Login Page] → [Continue with Google] → [Google Consent] 
→ [User Found?] → [Success/Register]
```

### Flow 2: Email/Password Registration → Login
```
[Login Page] → [Email + Password] → [Register]
→ [Account Created] → [Login with Same Credentials]
```

### Flow 3: Health History Management
```
[Main Page] → [Health History Button] → [JSON Editor]
→ [Save] → [Database Updated]
```

---

## 🚨 Important Notes

1. **KEEP `.env` SECRET** - Never commit to git
2. **First Google login:** Will show "User not found" - Register with email/password first
3. **Database:** Auto-created as `backend/riskbite.db`
4. **Reset DB:** Delete `riskbite.db` and restart backend
5. **CORS:** Open in dev mode, restrict in production

---

## ✨ Files Changed

### Backend
- `app/main.py` → Added OAuth + DB routes
- `requirements.txt` → Added authlib, sqlalchemy, passlib

### Frontend  
- `App.jsx` → Added navigation + view switching
- `App.css` → Professional styling
- `components/Login.jsx` → NEW - Auth UI
- `components/HealthHistory.jsx` → NEW - Health form

---

**Status:** ✅ READY TO USE
**Backend:** http://localhost:8000
**Frontend:** http://localhost:5173

## 📁 Project Structure

```
RISKbite2.0/
├── backend/                      ← FastAPI server
│   ├── app/
│   │   ├── main.py              ← Main endpoints
│   │   ├── models.py            ← Pydantic models
│   │   ├── services/
│   │   │   ├── ocr_service.py   ← Text extraction
│   │   │   ├── parser_service.py ← Ingredient parsing
│   │   │   └── risk_engine.py   ← Analysis logic
│   │   └── data/
│   │       └── ingredients.py   ← 100+ ingredients database
│   ├── requirements.txt
│   ├── run_server.py/.sh
│   └── README.md
├── src/                          ← React frontend
│   ├── app.jsx                  ← Main app
│   ├── components/              ← React components
│   ├── services/
│   │   └── api.js               ← API calls
│   └── style.css
└── public/
    └── index.html
```

---

## 🔧 Troubleshooting

### Issue: "Tesseract not found"
```
Solution: Install Tesseract (see Step 1)
On Windows, add to environment:
set PYTESSERACT_LOCATION=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Issue: "Module not found: fastapi"
```
Solution: Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: CORS errors (frontend can't connect)
```
Solution: Backend should allow your frontend URL
Check app/main.py for CORS configuration
Make sure frontend can reach http://localhost:8000
```

### Issue: OCR returns empty text
```
Solution: Use a clearer product label image
- Better lighting
- Higher resolution
- Larger text
- Straight angle
```

---

## 📚 API Endpoints

### Health Check
```bash
curl http://localhost:8000/
```
Response: `{"status": "healthy", "message": "...", "version": "1.0.0"}`

### Scan Product
```bash
curl -X POST http://localhost:8000/scan \
  -F "image=@product.jpg" \
  -F 'conditions=["diabetes", "peanut_allergy"]'
```

Response:
```json
{
  "ingredients": ["sugar", "peanut oil"],
  "risk_level": "High",
  "risk_score": 85,
  "warnings": [
    {
      "ingredient": "sugar",
      "reason": "High glycemic index – not suitable for diabetics...",
      "alternative": "Stevia or Erythritol"
    }
  ],
  "summary": "⚠️ We found 2 ingredients of concern..."
}
```

---

## 🧪 Testing

### Test with API Docs (Swagger UI)
1. Server running? Visit: http://localhost:8000/docs
2. Click "Try it out" on `/scan` endpoint
3. Upload a product image
4. Enter conditions as: `["diabetes", "peanut_allergy"]`
5. Click "Execute"

### Test with cURL
```bash
# Simple scan
curl -X POST http://localhost:8000/scan \
  -F "image=@cereal.jpg" \
  -F 'conditions=[]'

# With diabetes
curl -X POST http://localhost:8000/scan \
  -F "image=@candy.jpg" \
  -F 'conditions=["diabetes"]'

# With multiple conditions
curl -X POST http://localhost:8000/scan \
  -F "image=@snack.jpg" \
  -F 'conditions=["diabetes", "peanut_allergy", "gluten_sensitivity"]'
```

---

## 📋 Supported Health Conditions

```json
[
  "diabetes",
  "peanut_allergy",
  "nut_allergy",
  "shellfish_allergy",
  "gluten_sensitivity",
  "lactose_intolerance",
  "vegan",
  "pescatarian"
]
```

---

## 🎯 What Backend Does

1. **Receives Image**
   - Validates file is image
   - Extracts bytes

2. **OCR Processing** (Tesseract)
   - Converts image to text
   - Extracts ingredient label

3. **Ingredient Parsing**
   - Locates "Ingredients:" section
   - Splits into individual items
   - Cleans and normalizes names

4. **Risk Analysis**
   - Looks up each ingredient
   - Matches to user conditions
   - Calculates risk score (0-100)
   - Generates personalized warnings

5. **Response**
   - Returns structured JSON
   - Frontend displays results

---

## 💡 Example Ingredients Database

Backend includes 100+ ingredients:

**High Risk:**
- Sugar, Fructose, HFCS
- Trans fats, Palm oil
- Sodium nitrate
- Artificial colors
- Peanuts, Shellfish, Milk
- Gluten, Wheat

**Medium Risk:**
- Glucose, Sodium benzoate
- Artificial sweeteners
- Preservatives

**Low Risk:**  
- Xantitol, Citric acid
- Lecithin, Guar gum

Each ingredient has:
- Risk level
- Health tags (diabetes, allergen, etc.)
- Description
- Safe alternatives

---

## 🎬 Demo Flow

```
1. User opens frontend (http://localhost:5173)
2. User selects health conditions (Diabetes, Peanut Allergy)
3. User uploads product image
4. Frontend sends POST to http://localhost:8000/scan
5. Backend:
   - Extracts text via OCR
   - Parses ingredients
   - Analyzes risks
   - Generates warnings
6. Frontend displays:
   - Risk badge (🔴 High / 🟡 Medium / 🟢 Low)
   - Extracted ingredients
   - Personalized warnings
   - Safe alternatives
   - Summary
7. User can "Scan Another Product"
```

---

## 🚀 Performance Tips

- **OCR Speed:** Clear labels = faster (2-3 sec). Blurry = slower (5-8 sec)
- **Use GPU:** For production, consider GPU acceleration
- **Caching:** Cache ingredient lookups
- **Pre-processing:** Enhance images before OCR

---

## 📞 Need Help?

1. Check [backend/README.md](backend/README.md) for detailed setup
2. Check [backend/ARCHITECTURE.md](backend/ARCHITECTURE.md) for code docs
3. Check FastAPI docs: http://localhost:8000/docs
4. Check error messages in server logs

---

## ✅ Hackathon Checklist

- [ ] Tesseract installed & working
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Health check passes: `curl http://localhost:8000/`
- [ ] Can upload image to http://localhost:8000/docs
- [ ] Frontend connects to backend (no CORS errors)
- [ ] Full scan works end-to-end
- [ ] Multiple conditions work
- [ ] Error handling works (bad image, etc.)
- [ ] Results display correctly in frontend

---

## 🎉 Ready to Demo!

Your RISKbite system is now ready for:
- Live hackathon demos
- Investor presentations
- User testing
- Feedback collection

Good luck! 🥗

---

**Questions?** See backend/README.md or ARCHITECTURE.md
