# 🥗 RISKbite - AI-Powered Ingredient Scanner

> **Smart ingredient analysis for your health** 🎯
> 
> Scan product labels → Extract ingredients → Get personalized health warnings

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)](QUICKSTART.md)
[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org)
[![React](https://img.shields.io/badge/react-18+-61dafb)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-009688)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🎯 Problem Statement

Consumers struggle to understand ingredient labels on packaged products due to:
- 🤔 Complex chemical names
- 📝 Unclear health implications
- 👨‍👩‍👧 Confusion about personal health conditions
- ⚠️ Hidden allergens and risky ingredients

**RISKbite solves this** with AI-powered scanning and personalized warnings.

---

## ✨ Features

### 📷 Product Label Scanning
- **Drag-and-drop** image upload
- **AI-powered OCR** (Tesseract)
- **Instant text extraction** from product images
- **Scan history** tracking for each user

### 🔐 Authentication & User Management
- **Email/Password registration** and login
- **Google OAuth** integration for seamless sign-in
- **Session management** with secure cookies
- **Password hashing** with Argon2 algorithm

### 🧠 Intelligent Analysis
- **133+ ingredient database** with risk levels(currently exculde emulsifiers and other catalysts)
- **Ingredient normalization** (handles variants)
- **Risk scoring** algorithm (0-100)
- **Natural language health parsing** - users can type their conditions in plain English

### ❤️ Personalized Warnings
- **21+ health conditions** (Diabetes, Allergies, Gluten, Lactose, Vegan, etc.)
- **Condition-based filtering**
- **Friendly explanations** for each issue
- **Safe alternatives** for risky ingredients

### 📋 Health History
- **Save health profile** with natural language input
- **Automatic condition extraction** from text
- **Persistent user preferences** across sessions
- **Scan history** with past results

### 🎨 Beautiful UI
- **Color-coded risk badges** (🔴 High, 🟡 Medium, 🟢 Low)
- **Loading states** and smooth animations
- **Fully responsive** (mobile-friendly)
- **Error handling** with clear messages
- **Landing, Login, Dashboard, and Scan pages**

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Tesseract OCR (instructions below)

### 1️⃣ Install Tesseract

**Windows:**
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Run installer and note the path

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 2️⃣ Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
python run_server.py
```

Server running at: **http://localhost:8000**

### 3️⃣ Setup Frontend
```bash
npm install
npm run dev
```

Frontend at: **http://localhost:**

### 4️⃣ Start Scanning! 🎉

Open http://localhost:5173 and start uploading product images!

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICKSTART.md](QUICKSTART.md)** | 5-minute setup guide |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Full project overview |
| **[backend/README.md](backend/README.md)** | Backend installation & usage |
| **[backend/ARCHITECTURE.md](backend/ARCHITECTURE.md)** | Technical deep dive |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Frontend (React + Turquoise Theme)                  │
│  • Landing Page                                                         │
│  • Login/Register (Email + Google OAuth)                               │
│  • Dashboard with Health History                                       │
│  • Scan Page with Image Upload                                         │
└────────────────┬────────────────────────────────────────────────────────┘
                 │ HTTP API
                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Backend (FastAPI + Python)                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    API Endpoints                                 │   │
│  │  • /auth/register, /auth/login, /auth/google/* (OAuth)          │   │
│  │  • /scan (product scanning)                                     │   │
│  │  • /health/{user_id} (health history)                          │   │
│  │  • /parse-health (natural language parsing)                     │   │
│  │  • /scans/{user_id} (scan history)                             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│  ┌───────────────────────────────┐  ┌──────────────────────────────┐   │
│  │ OCR Service (Tesseract)       │  │ Auth Services               │   │
│  ├───────────────────────────────┤  │ • Argon2 Password Hashing   │   │
│  │ Parser Service (Ingredients)  │  │ • Google OAuth             │   │
│  ├───────────────────────────────┤  │ • Session Management        │   │
│  │ Risk Engine (Analysis)        │  └──────────────────────────────┘   │
│  ├───────────────────────────────┤                                    │
│  │ Explainer Service              │  ┌──────────────────────────────┐   │
│  ├───────────────────────────────┤  │ Health Parser Service        │   │
│  │ Health Parser Service         │  │ • Natural Language Parsing   │   │
│  └───────────────────────────────┘  │ • Condition Extraction       │   │
│           ↓                         └──────────────────────────────┘   │
│  ┌─────────────────────────────┐                                     │
│  │ Ingredients Database        │                                     │
│  │ (133+ items)                │                                     │
│  └─────────────────────────────┘                                     │
│           ↓                                                           │
│  ┌─────────────────────────────┐                                     │
│  │ SQLite Database             │                                     │
│  │ • users                    │                                     │
│  │ • health_history           │                                     │
│  │ • scans                    │                                     │
│  └─────────────────────────────┘                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 What's Included

### Frontend
- ✅ 3 React components (HealthForm, ImageUpload, ResultCard)
- ✅ API service layer with error handling
- ✅ Pink theme with modern styling
- ✅ Responsive design
- ✅ Loading states and animations

### Backend
- ✅ FastAPI with 2 endpoints
- ✅ Tesseract OCR integration
- ✅ Ingredient parser (normalizes, cleans)
- ✅ Risk analysis engine
- ✅ 100+ ingredient knowledge base
- ✅ Pydantic validation
- ✅ CORS middleware
- ✅ Error handling

### Documentation
- ✅ Quick start guide
- ✅ Architecture documentation
- ✅ Deployment guide
- ✅ API examples
- ✅ Code comments

---

## 🎯 Example Usage

### Frontend: Upload Image
1. Select health conditions (e.g., Diabetes, Peanut Allergy)
2. Upload or drag-drop product image
3. Wait for results (~3-8 seconds)
4. View personalized warnings

### API: Scan Product
```bash
curl -X POST http://localhost:8000/scan \
  -F "image=@cereal_box.jpg" \
  -F 'conditions=["diabetes", "peanut_allergy"]'
```

### Response
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

## 🧠 Supported Health Conditions

- 🩺 **Diabetes** - High sugar ingredients
- 🥜 **Peanut Allergy** - Peanut-related items
- 🌳 **Nut Allergy** - Tree nuts
- 🦐 **Shellfish Allergy** - Crustaceans
- 🌾 **Gluten Sensitivity** - Wheat, barley, rye
- 🥛 **Lactose Intolerance** - Milk products
- 🥗 **Vegan** - Animal products
- 🐟 **Pescatarian** - Meat (fish ok)

---

## 📊 Ingredient Database

**100+ ingredients** covering:

| Category | Count | Examples |
|----------|-------|----------|
| Sugars | 10+ | Sugar, HFCS, Fructose, Glucose |
| Fats | 6+ | Palm Oil, Trans Fats |
| Sodium | 9+ | Sodium Benzoate, Nitrate |
| Allergens | 20+ | Peanuts, Shellfish, Gluten |
| Additives | 12+ | Artificial Colors, Preservatives |
| Animal Products | 8+ | Gelatin, Milk, Beef |
| Other | 25+ | Lecithin, Guar Gum, etc. |

---

## 🔧 Tech Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **CSS3** - Styling (pink theme)
- **Fetch API** - HTTP client

### Backend
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pytesseract** - OCR wrapper
- **Pillow** - Image processing
- **Pydantic** - Data validation

### Deployment
- **Docker** - Containerization
- **Heroku** - PaaS option
- **AWS EC2** - VM option
- **Railway** - Simple deployment

---

## 📈 Performance

| Operation | Duration |
|-----------|----------|
| OCR (clear label) | 2-3 sec |
| OCR (blurry) | 5-8 sec |
| Ingredient Parsing | ~50 ms |
| Risk Analysis | ~100 ms |
| **Total Response** | **2-8 sec** |

---

## 🚀 Deployment Options

### Local Development
```bash
python run_server.py  # Backend
npm run dev           # Frontend
```

### Docker
```bash
docker-compose up
```

### Cloud (Heroku)
```bash
heroku create
heroku buildpacks:add https://github.com/heroku-community/heroku-buildpack-tesseract
git push heroku main
```

### Cloud (AWS, Railway, Vercel)
See [DEPLOYMENT.md](backend/DEPLOYMENT.md) for details

---

## 📸 Screenshots

### Frontend
```
┌─────────────────────────────┐
│  🥗 RISKbite               │
│  Smart ingredient analysis │
└─────────────────────────────┘
│ ❤️ Health Conditions       │
│ ☑ Diabetes                 │
│ ☑ Peanut Allergy           │
│ ☑ Gluten Sensitivity       │
└─────────────────────────────┘
│ 📷 Upload Product Label    │
│ [Drag & Drop Area]         │
│ [🔍 Scan Label]            │
└─────────────────────────────┘
```

### Results
```
┌─────────────────────────────┐
│ 🔴 High Risk               │
│ ⚠️ We found 2 issues       │
└─────────────────────────────┘
│ ⛔ Sugar                    │
│ Reason: High glycemic...   │
│ ✅ Alternative: Stevia     │
├─────────────────────────────┤
│ ⛔ Peanut Oil              │
│ Reason: Can trigger...     │
│ ✅ Alternative: Sunflower │
└─────────────────────────────┘
```

---

## 🔐 Security

- ✅ Input validation (image file types)
- ✅ CORS protection
- ✅ Error message sanitization
- ✅ No persistent image storage
- ✅ Size limits (10 MB default)

---

## 🆘 Troubleshooting

### Backend Issues
- **"Tesseract not found"** → Install from: https://github.com/UB-Mannheim/tesseract/wiki
- **"Module not found"** → Run: `pip install -r requirements.txt`
- **"CORS error"** → Check CORS_ORIGINS in backend

### Frontend Issues
- **"Cannot reach backend"** → Ensure backend is running on :8000
- **"Image upload fails"** → Use clear product label image
- **"No results"** → Check browser console for errors

See [backend/README.md#troubleshooting](backend/README.md#troubleshooting) for more help.

---

## 🤝 Contributing

Want to improve RISKbite?

1. Add more ingredients to `ingredients.py`
2. Improve OCR preprocessing
3. Add ML-based alternative extraction
4. Implement product history
5. Add database integration

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎉 Next Steps

1. **Quick Start** → [QUICKSTART.md](QUICKSTART.md)
2. **Full Setup** → [backend/README.md](backend/README.md)
3. **Understand Code** → [ARCHITECTURE.md](backend/ARCHITECTURE.md)
4. **Deploy** → [DEPLOYMENT.md](backend/DEPLOYMENT.md)

---

## 📞 Support

- 📖 Check documentation files above
- 🐛 Review [Troubleshooting](backend/README.md#troubleshooting)
- 💬 See code comments
- 📚 Check example code

---

## 🌟 Credits

Built for the hackathon with ❤️

**Tech Stack:** React, FastAPI, Tesseract, Python

**Features:** OCR, AI Analysis, Personalization

**Theme:** Pink & Modern 🌸

---

## 🚀 Version

**v1.0.0** - Hackathon Ready

---

**Let's make ingredient transparency mainstream! 🥗**

[Get Started →](QUICKSTART.md)
