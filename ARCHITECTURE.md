#  RISKbite - System Architecture

##  High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                                 │
│                    (React Vite - Port 5173)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────┐  ┌──────────────────┐  ┌─────────────────────┐ │
│  │   Login Page      │  │  Home Page       │  │ Health History      │ │
│  │                   │  │                  │  │ Page                │ │
│  ├───────────────────┤  ├──────────────────┤  ├─────────────────────┤ │
│  │ • Email/Password  │  │ • Image Upload   │  │ • JSON Editor       │ │
│  │ • Google OAuth    │  │ • Health Form    │  │ • Save Button       │ │
│  │ • Register        │  │ • Results Card   │  │ • Last Saved Record │ │
│  │ • Error Messages  │  │ • Navigation     │  │ • Status Messages   │ │
│  └───────────────────┘  └──────────────────┘  └─────────────────────┘ │
│                                                                         │
└────────────┬────────────────────────────────────────────────────────┬──┘
             │                                                        │
             │ HTTPS/API Calls                                        │ HTTPS/API Calls
             │                                                        │
             ▼                                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        BACKEND API                                      │
│                  (FastAPI - Port 8000)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │          AUTHENTICATION ENDPOINTS                               │ │
│  ├──────────────────────────────────────────────────────────────────┤ │
│  │ • POST /auth/register          - Create account                 │ │
│  │ • POST /auth/login             - Login with email/password      │ │
│  │ • GET  /auth/google/login      - Start OAuth flow              │ │
│  │ • GET  /auth/google/callback   - OAuth callback                │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │        HEALTH HISTORY ENDPOINTS                                 │ │
│  ├──────────────────────────────────────────────────────────────────┤ │
│  │ • POST /health/{user_id}      - Save health data                │ │
│  │ • GET  /health/{user_id}      - Get latest health history       │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │        PRODUCT SCANNING ENDPOINTS                               │ │
│  ├──────────────────────────────────────────────────────────────────┤ │
│  │ • POST /scan                   - Scan product (original)         │ │
│  │ • GET  /                       - Health check                    │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │         CORE SERVICES                                           │ │
│  ├──────────────────────────────────────────────────────────────────┤ │
│  │ • Password Hashing (Argon2)                                     │ │
│  │ • OAuth Handler (Google)                                        │ │
│  │ • OCR Service (Tesseract)                                       │ │
│  │ • Parser Service                                                │ │
│  │ • Risk Engine                                                   │ │
│  │ • Explainer Service                                             │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└───────────────┬────────────────────────────────┬───────────────────────┘
                │                                │
                │ SQL Queries                    │ OAuth Request to Google
                │                                │
                ▼                                ▼
    ┌──────────────────┐        ┌──────────────────────────────┐
    │   SQLite DB      │        │  Google OAuth Server         │
    │  (riskbite.db)   │        │  (Google Cloud Platform)     │
    └──────────────────┘        └──────────────────────────────┘
    │ • users table    │
    │ • health_history │
    └──────────────────┘
```

---

##  Authentication Flow

### Google OAuth Flow
```
User Browser                     Frontend (5173)              Backend (8000)              Google
   │                               │                              │                        │
   ├──1. Click "Continue Google"──►│                              │                        │
   │                               │                              │                        │
   │                               ├─2. GET /auth/google/login──► │                        │
   │                               │                              │                        │
   │                               │                              ├─3. Redirect to Google OAuth ───► │
   │◄─────────────────────────────────────────────────────────────────────────────────────┤
   │         User signs in to Google                                                        │
   │────────────────────────────────────────────────────────────────────────────────────► │
   │                               │                              │                        │
   │                               │                              │◄─4. Auth Code/Token ──│
   │                               │                              │                        │
   │                               │◄─5. Redirect with user info ─┤                        │
   │◄─ User logged in (email shown) ─┤                              │                        │
   │                               │                              │                        │
   │                               │                              │                        │
```

### Email/Password Flow
```
User enters email + password
         │
         ▼
   Click "Register"  OR  Click "Login"
         │                     │
         ├──────┬──────┬───────┘
         │      │      │
    Validate  Hash  Query DB
         │      │      │
         └──────┼──────┘
                ▼
           Check Results
         ____|____
        │         │
      Valid    Invalid
        │         │
      Save    Error Msg
        │
        ▼
    Logged In 
```

---

##  Database Schema

### Users Table
```
┌──────────────────────────────────┐
│         users                    │
├──────────────────────────────────┤
│ id (PK)              INTEGER     │ ← Primary Key
│ email (UNIQUE)       VARCHAR     │ ← User's email
│ hashed_password      VARCHAR     │ ← Argon2 hashed
│ created_at          DATETIME     │ ← Account creation time
└──────────────────────────────────┘
         △
         │ One-to-Many
         │
┌──────────────────────────────────┐
│     health_history               │
├──────────────────────────────────┤
│ id (PK)              INTEGER     │
│ user_id (FK)  ───────VARCHAR     │ → users.id
│ data (JSON)          TEXT        │ → Health data
│ created_at          DATETIME     │ → Save time
└──────────────────────────────────┘
```

---

##  API Request/Response Flow

### Registration Request
```
POST /auth/register

Request:
┌──────────────────────────────────┐
│ {                                │
│   "email": "user@gmail.com",     │
│   "password": "SecurePass123!"   │
│ }                                │
└──────────────────────────────────┘
           │
           ▼ Frontend sends
    ┌──────────────────────────────┐
    │ Backend Processing:          │
    │ 1. Validate email format     │
    │ 2. Check if email exists     │
    │ 3. Hash password (Argon2)    │
    │ 4. Save to database          │
    └──────────────────────────────┘
           │
           ▼
Response 200 OK:
┌──────────────────────────────────┐
│ {                                │
│   "ok": true,                    │
│   "user_id": 1,                  │
│   "email": "user@gmail.com"      │
│ }                                │
└──────────────────────────────────┘
```

### Health History Save
```
POST /health/1

Request:
┌─────────────────────────────────────┐
│ {                                   │
│   "data": {                         │
│     "age": 35,                      │
│     "diabetes": true,               │
│     "allergies": ["peanuts"]        │
│   }                                 │
│ }                                   │
└─────────────────────────────────────┘
           │
           ▼ Frontend sends
    ┌──────────────────────────────┐
    │ Backend Processing:          │
    │ 1. Verify user_id exists     │
    │ 2. Convert to JSON string    │
    │ 3. Add timestamp             │
    │ 4. Save to database          │
    └──────────────────────────────┘
           │
           ▼
Response 200 OK:
┌──────────────────────────────────┐
│ {                                │
│   "ok": true,                    │
│   "history_id": 1                │
│ }                                │
└──────────────────────────────────┘
```

---

##  Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Layer 1: Input Validation                                  │
│ ├─ Email format check                                      │
│ ├─ Password strength validation                            │
│ └─ JSON validation for health data                         │
│                                                             │
│ Layer 2: Password Security                                 │
│ ├─ Argon2 hashing algorithm                                │
│ ├─ Salt automatically added                                │
│ ├─ Constant-time comparison                                │
│ └─ Never stored in plain text                              │
│                                                             │
│ Layer 3: OAuth Security                                    │
│ ├─ Authlib handles token exchange                          │
│ ├─ Secure redirect URIs                                    │
│ ├─ State parameter verification                            │
│ └─ Token expiration handling                               │
│                                                             │
│ Layer 4: Database Security                                 │
│ ├─ SQL Injection prevention (SQLAlchemy ORM)               │
│ ├─ Foreign key constraints                                 │
│ ├─ User_id verification for data access                    │
│ └─ Proper indexing                                         │
│                                                             │
│ Layer 5: Environment Security                              │
│ ├─ .env file (not versioned)                               │
│ ├─ Credentials not in code                                 │
│ ├─ CORS properly configured                                │
│ └─ HTTPS ready (requires cert in production)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

##  Data Flow Diagram

```
User Input
    │
    ├─ Email/Password
    │      │
    │      ▼
    │  Frontend Validation
    │      │
    │      ▼
    │  HTTPS POST to API
    │      │
    │      ▼
    │  Backend Receives
    │      │
    │      ├─ Validate Format
    │      │
    │      ├─ Check Duplicates (for register)
    │      │
    │      ├─ Hash Password (Argon2)
    │      │
    │      ├─ Store in SQLite
    │      │
    │      ▼
    │  Response to Frontend
    │      │
    │      ▼
    │  User Logged In 
    │
    │
    ├─ Health Data (JSON)
    │      │
    │      ▼
    │  Textarea Input
    │      │
    │      ▼
    │  Parse JSON
    │      │
    │      ▼
    │  POST to /health/{user_id}
    │      │
    │      ▼
    │  Backend Receives
    │      │
    │      ├─ Verify user_id
    │      │
    │      ├─ Stringify JSON
    │      │
    │      ├─ Add timestamp
    │      │
    │      ├─ Store in health_history
    │      │
    │      ▼
    │  Response ("Saved")
    │      │
    │      ▼
    │  Display Last Saved 
```

---

##  Deployment Architecture (Production Ready)

```
┌────────────────────────────────────────────────────────────────┐
│                    PRODUCTION SETUP                            │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ User Browser                                             │ │
│  └──────────────────────────────────────────────────────────┘ │
│                          │                                     │
│                   HTTPS / TLS                                  │
│                          │                                     │
│      ┌───────────────────┴────────────────────┐              │
│      │                                        │              │
│      ▼                                        ▼              │
│  ┌─────────────────┐                  ┌──────────────────┐  │
│  │ Frontend CDN    │                  │ Load Balancer    │  │
│  │ (Netlify/Vercel)│                  │ (AWS/Nginx)      │  │
│  └─────────────────┘                  └──────────────────┘  │
│                                               │               │
│                                               ▼               │
│                                   ┌──────────────────────┐    │
│                                   │ Backend Instances    │    │
│                                   │ (Replicated)         │    │
│                                   ├──────────────────────┤    │
│                                   │ API Server 1         │    │
│                                   │ API Server 2         │    │
│                                   │ API Server 3         │    │
│                                   └──────────────────────┘    │
│                                               │               │
│                                               ▼               │
│                                   ┌──────────────────────┐    │
│                                   │ PostgreSQL Database  │    │
│                                   │ (Replicated)         │    │
│                                   └──────────────────────┘    │
│                                               │               │
│                                   ┌───────────┴──────────┐    │
│                                   │ Regular Backups      │    │
│                                   └──────────────────────┘    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

##  Component Interaction

```
Frontend Components
┌─────────────────────────────────┐
│         App.jsx                 │
│ ┌────────┬─────────┬──────────┐ │
│ │ Login  │ Home    │ History  │ │
│ │ page   │ page    │ page     │ │
│ └────────┴─────────┴──────────┘ │
│           │         │       │   │
│           ▼         ▼       ▼   │
│      Login.jsx   Home    Health │
│                         History │
│                         .jsx    │
│                                 │
│  services/api.js (all calls)    │
└─────┬───────────────────────────┘
      │
      ▼ HTTP
  Backend
  ┌─────────────────────────────┐
  │      app/main.py            │
  │                             │
  │ ┌─────┬──────┬────────┐    │
  │ │Auth │Health│ Scan   │    │
  │ │API  │ API  │ API    │    │
  │ └─────┴──────┴────────┘    │
  │          │                 │
  │          ▼                 │
  │ ┌─────────────────────┐    │
  │ │  SQLite Database    │    │
  │ │  (riskbite.db)      │    │
  │ └─────────────────────┘    │
  └─────────────────────────────┘
```

---

##  Request/Response Timeline

```
T=0ms    User clicks "Login"
│
T=10ms   ├─ Frontend validates input
│        ├─ Send POST /auth/login
│        │
T=20ms   ├─ Backend receives request
│        │
T=25ms   ├─ Query database for user
│        │
T=30ms   ├─ Hash provided password
│        │
T=35ms   ├─ Compare with stored hash
│        │
T=40ms   ├─ Generate response
│        │
T=50ms   └─ Frontend processes response
│        └─ Display user info
│
T=60ms   User sees "Logged in: user@gmail.com" 
```

---

**Architecture Generated:** February 17, 2026
**Status:** Production Ready
**Scale:** Tested for development, designed for production
