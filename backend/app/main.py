"""
Main FastAPI application
Entry point for RISKbite backend server
"""

import logging
import io
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


from app.models import ScanResponse, WarningResponse, HealthCheckResponse
from app.services.ocr_service import OCRService
from app.services.parser_service import ParserService
from app.services.risk_engine import RiskEngine
from app.services.explainer_service import ExplainerService
from app.services.health_parser_service import HealthParserService

# Configure logging - reduce verbosity for better performance
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# ==================== Instantiate FastAPI ====================
app = FastAPI(
    title="RISKbite Backend",
    description="AI-powered ingredient scanner with personalized health warnings",
    version="1.0.0"
)

# ==================== CORS Configuration (Optimized) ====================
# Reduce overhead by specifying exact origins instead of "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# ==================== Session Middleware (Required for OAuth) ====================
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-change-in-prod")

# ==================== Static Files Configuration ====================
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Get the backend directory path
BACKEND_DIR = Path(__file__).parent.parent
STATIC_DIR = BACKEND_DIR / "static"

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ==================== HTML Pages Cache ====================
# Cache file paths at startup to avoid filesystem checks on every request
HTML_CACHE = {
    "landing": STATIC_DIR / "html" / "landing.html",
    "login": STATIC_DIR / "html" / "login.html",
    "dashboard": STATIC_DIR / "html" / "dashboard.html",
    "scan": STATIC_DIR / "html" / "scan.html",
}

# ==================== HTML Pages Endpoints ====================
from fastapi.responses import FileResponse

@app.get("/landing")
async def serve_landing():
    """Serve landing page"""
    html_file = HTML_CACHE["landing"]
    if html_file.exists():
        return FileResponse(html_file, media_type="text/html")
    return {"message": "Landing page not found"}

@app.get("/login")
async def serve_login():
    """Serve login page"""
    html_file = HTML_CACHE["login"]
    if html_file.exists():
        return FileResponse(html_file, media_type="text/html")
    return {"message": "Login page not found"}

@app.get("/dashboard")
async def serve_dashboard():
    """Serve dashboard page"""
    html_file = HTML_CACHE["dashboard"]
    if html_file.exists():
        return FileResponse(html_file, media_type="text/html")
    return {"message": "Dashboard page not found"}

@app.get("/scan")
async def serve_scan():
    """Serve scan results page"""
    html_file = HTML_CACHE["scan"]
    if html_file.exists():
        return FileResponse(html_file, media_type="text/html")
    return {"message": "Scan page not found"}

@app.get("/scan-results")
async def serve_scan_results():
    """Serve scan results page (alias for /scan)"""
    html_file = HTML_CACHE["scan"]
    if html_file.exists():
        return FileResponse(html_file)
    return {"message": "Scan results page not found"}


# -------------------- Simple DB for users & health history --------------------
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends
import datetime


DATABASE_URL = "sqlite:///./riskbite.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class HealthHistory(Base):
    __tablename__ = "health_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    data = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    image_filename = Column(String, nullable=True)
    result = Column(Text, nullable=True)  # JSON dump of ScanResponse
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# ==================== Scan History Cleanup Function ====================
def cleanup_old_scans(db: Session, hours: int = 24):
    """
    Remove scan history older than specified hours from the database
    
    Args:
        db: Database session
        hours: Number of hours to retain scans (default: 24)
        
    Returns:
        Number of scans deleted
    """
    try:
        cutoff_time = datetime.datetime.utcnow() - datetime.timedelta(hours=hours)
        deleted = db.query(Scan).filter(Scan.created_at < cutoff_time).delete()
        db.commit()
        if deleted > 0:
            logger.info(f"Cleaned up {deleted} scans older than {hours} hours")
        return deleted
    except Exception as e:
        logger.warning(f"Error during scan cleanup: {e}")
        db.rollback()
        return 0


# Password hashing - Use argon2 with optimized parameters for faster login
# Reduced memory_cost and time_cost for ~100-300ms per operation instead of 1-3s
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,  # 64 MB (vs default 512 MB)
    argon2__time_cost=2,        # 2 iterations (vs default 3)
    argon2__parallelism=1       # 1 thread (vs default 2)
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== Startup Events ====================
@app.on_event("startup")
async def startup_event():
    """Lightweight startup - no blocking operations"""
    print("\n✅ RISKbite Backend is ready at http://localhost:8000\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down RISKbite Backend")


# -------------------- Auth / Health Pydantic models --------------------
class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class HealthRequest(BaseModel):
    # free-form health data (JSON object)
    data: dict


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



# ==================== Health Check Endpoint ====================
@app.get("/", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint - lightweight, no database hits
    
    Returns:
        Health status and API information
    """
    return HealthCheckResponse(
        status="healthy",
        message="RISKbite backend is running",
        version="1.0.0"
    )


# ==================== Main Scan Endpoint ====================
@app.post("/scan", response_model=ScanResponse)
async def scan_product(
    image: UploadFile = File(...),
    conditions: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Scan product label and generate personalized health warnings
    
    Args:
        image: Product label image file (JPG, PNG, etc.)
        conditions: JSON string of user health conditions (new preferences)
        user_id: ID of logged-in user (optional)
        db: Database session
        
    Returns:
        ScanResponse with ingredients, risk level, and warnings
        
    Example conditions:
        '["diabetes", "peanut_allergy", "gluten_sensitivity"]'
    """
    try:
        # ==================== Step 1: Validate Image ====================
        # Check file type
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPG, PNG, etc.)"
            )
        
        # Read image bytes
        image_bytes = await image.read()
        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Image file is empty")
        
        logger.info(f"Received image: {image.filename}, size: {len(image_bytes)} bytes")

        # ==================== Step 2: Parse User Conditions ====================
        user_conditions = []
        
        # Parse current/new conditions from form
        if conditions:
            try:
                user_conditions = json.loads(conditions)
                if not isinstance(user_conditions, list):
                    user_conditions = []
                logger.info(f"Current preferences: {user_conditions}")
            except json.JSONDecodeError:
                logger.warning("Invalid conditions JSON format")
                user_conditions = []
        
        # If user is logged in, fetch and merge health history
        if user_id:
            logger.info(f"Fetching health history for user_id: {user_id}")
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                # Get latest health history
                health_entry = (
                    db.query(HealthHistory)
                    .filter(HealthHistory.user_id == user_id)
                    .order_by(HealthHistory.created_at.desc())
                    .first()
                )
                if health_entry and health_entry.data:
                    try:
                        history_data = json.loads(health_entry.data)
                        # Extract conditions from history
                        if isinstance(history_data, dict):
                            # If history has a 'conditions' key
                            if "conditions" in history_data:
                                history_conditions = history_data["conditions"]
                                if isinstance(history_conditions, list):
                                    logger.info(f"Health history conditions: {history_conditions}")
                                    # Merge with current preferences (avoiding duplicates)
                                    user_conditions = list(set(user_conditions + history_conditions))
                                    logger.info(f"Merged conditions: {user_conditions}")
                    except Exception as e:
                        logger.warning(f"Error parsing health history: {e}")
            else:
                logger.warning(f"User {user_id} not found")
        
        logger.info(f"Final conditions for risk analysis: {user_conditions}")

        # ==================== Step 3: Extract Text via OCR ====================
        logger.info("Starting OCR extraction...")
        extracted_text = OCRService.extract_text_from_image(image_bytes)
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from image. Please provide a clearer product label image."
            )
        
        logger.info(f"OCR extraction successful: {len(extracted_text)} characters extracted")

        # ==================== Step 4: Parse Ingredients ====================
        logger.info("Parsing ingredients from OCR text...")
        ingredients = ParserService.parse_ingredients(extracted_text)
        
        if not ingredients:
            raise HTTPException(
                status_code=400,
                detail="No ingredients found in image. Please ensure the product label is visible."
            )
        
        logger.info(f"Parsed {len(ingredients)} ingredients: {ingredients}")

        # ==================== Step 5: Analyze Risk ====================
        logger.info("Analyzing risk for ingredients...")
        analysis_result = RiskEngine.analyze_ingredients(ingredients, user_conditions)

        # ==================== Step 6: Build Response ====================
        # Convert warnings to response format
        warnings_response = [
            WarningResponse(
                ingredient=w["ingredient"],
                reason=w["reason"],
                alternative=w["alternative"]
            )
            for w in analysis_result["warnings"]
        ]

        # Build explanations mapping for UI (use explainer service)
        explanations = {}
        for ing in analysis_result.get("ingredients", []):
            explanations[ing] = ExplainerService.explain(ing)

        response = ScanResponse(
            ingredients=analysis_result["ingredients"],
            risk_level=analysis_result["risk_level"],
            risk_score=analysis_result["risk_score"],
            warnings=warnings_response,
            explanations=explanations,
            extracted_text=extracted_text,
            summary=analysis_result["summary"]
        )

        logger.info(
            f"Scan completed successfully. "
            f"Risk Level: {response.risk_level}, "
            f"Warnings: {len(response.warnings)}"
        )

        # Persist scan result in database for user history
        try:
            scan_entry = Scan(
                user_id=int(user_id) if user_id else None,
                image_filename=getattr(image, 'filename', None),
                result=json.dumps(response.dict()),
            )
            db.add(scan_entry)
            db.commit()
            db.refresh(scan_entry)
        except Exception as db_exc:
            logger.warning(f"Could not persist scan result: {db_exc}")

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Scan failed with error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# -------------------- Authentication endpoints --------------------
from sqlalchemy.orm import Session
from fastapi import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
import os
import requests
from urllib.parse import quote_plus

# OAuth / frontend config from env
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Configure Authlib OAuth - Use hardcoded metadata to avoid blocking on startup
oauth = OAuth()
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    # Use hardcoded Google OpenID metadata - no network calls on startup!
    server_metadata = {
        "issuer": "https://accounts.google.com",
        "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_endpoint": "https://oauth2.googleapis.com/token",
        "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
        "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
    }

    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata=server_metadata,
        client_kwargs={
            "scope": "openid email profile",
            "redirect_uri": "http://localhost:8000/auth/google/callback"
        },
    )
    
    # Also explicitly set the authorize URL
    oauth.google.authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"

# Convenience constants for manual fallback token exchange
TOKEN_ENDPOINT = server_metadata.get("token_endpoint") if 'server_metadata' in locals() and server_metadata else "https://oauth2.googleapis.com/token"
USERINFO_ENDPOINT = server_metadata.get("userinfo_endpoint") if 'server_metadata' in locals() and server_metadata else "https://openidconnect.googleapis.com/v1/userinfo"



@app.post("/auth/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    # simple registration: email + password
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=request.email, hashed_password=hash_password(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"ok": True, "user_id": user.id, "email": user.email}


@app.post("/auth/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # User does not exist
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(request.password, user.hashed_password):
        # Wrong password
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"ok": True, "user_id": user.id, "email": user.email}


@app.get("/auth/google/login")
async def google_login(request: Request):
    if not (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET):
        raise HTTPException(status_code=500, detail="Google OAuth not configured on server")
    try:
        # Check if oauth.google is properly registered
        if not hasattr(oauth, 'google') or oauth.google is None:
            logger.error("OAuth Google client not registered")
            return RedirectResponse(f"{FRONTEND_URL}/login?msg=oauth_not_configured")
        
        redirect_uri = request.url_for("google_callback")
        logger.info(f"Initiating OAuth redirect to: {redirect_uri}")
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        logger.error(f"Error initiating Google OAuth redirect: {e}", exc_info=True)
        # Return detailed error in query parameter for debugging
        error_msg = str(e).replace(" ", "_").replace(":", "_").replace("\n", "_")[:100]
        return RedirectResponse(f"{FRONTEND_URL}/login?msg=oauth_redirect_error&detail={error_msg}")


@app.get("/auth/google/callback", name="google_callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    if not (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET):
        raise HTTPException(status_code=500, detail="Google OAuth not configured on server")
    token = None
    user_info = {}
    # Primary method: use Authlib to exchange code
    try:
        token = await oauth.google.authorize_access_token(request)
        try:
            user_info = await oauth.google.parse_id_token(request, token)
        except Exception:
            user_info = token.get("userinfo") or {}
    except Exception as e:
        logger.warning(f"Authlib token exchange failed, attempting manual exchange: {e}")
        # Fallback: perform manual token exchange using requests
        code = request.query_params.get("code")
        if not code:
            logger.error("No authorization code present in callback query parameters")
            return RedirectResponse(f"{FRONTEND_URL}/login?msg=oauth_token_error")
        redirect_uri = str(request.url_for("google_callback"))
        try:
            resp = requests.post(
                TOKEN_ENDPOINT,
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': redirect_uri,
                    'client_id': GOOGLE_CLIENT_ID,
                    'client_secret': GOOGLE_CLIENT_SECRET,
                },
                timeout=5,
            )
            if not resp.ok:
                logger.error(f"Manual token endpoint returned status {resp.status_code}: {resp.text}")
                return RedirectResponse(f"{FRONTEND_URL}/login?msg=oauth_token_error")
            token = resp.json()
            access_token = token.get('access_token')
            if access_token:
                ui = requests.get(USERINFO_ENDPOINT, headers={"Authorization": f"Bearer {access_token}"}, timeout=5)
                if ui.ok:
                    user_info = ui.json()
                else:
                    logger.error(f"Userinfo endpoint returned {ui.status_code}: {ui.text}")
            else:
                logger.error("No access_token present in token response")
        except Exception as e2:
            logger.error(f"Manual token exchange failed: {e2}", exc_info=True)
            return RedirectResponse(f"{FRONTEND_URL}/login?msg=oauth_token_error")

    email = (user_info.get("email") if user_info else None) or (token.get('email') if isinstance(token, dict) else None)
    if not email:
        # Unable to obtain email
        logger.error("Unable to obtain user email from Google response")
        return RedirectResponse(f"{FRONTEND_URL}/login?msg=oauth_failed")

    # Check database for user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Redirect to frontend login with message to sign up
        return RedirectResponse(f"{FRONTEND_URL}/login?msg=user_not_found&email={email}")

    # Success - redirect to frontend login route with user info so the
    # Login component can read the query params and complete client-side login.
    return RedirectResponse(f"{FRONTEND_URL}/login?auth=google&user_id={user.id}&email={email}")


# ==================== OAuth Debug Endpoints ====================
@app.get("/oauth-check")
async def oauth_check():
    """
    Debug endpoint to verify OAuth configuration
    
    Returns:
        OAuth status and configuration details
    """
    return {
        "oauth_enabled": bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET),
        "client_id_configured": bool(GOOGLE_CLIENT_ID),
        "client_secret_configured": bool(GOOGLE_CLIENT_SECRET),
        "frontend_url": FRONTEND_URL,
        "callback_url": "http://localhost:8000/auth/google/callback",
        "google_login_url": "http://localhost:8000/auth/google/login",
        "status": "✅ OAuth is properly configured" if (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET) else "❌ OAuth not configured - check .env file"
    }


@app.get("/auth-debug")
async def auth_debug():
    """
    Debug endpoint to show authentication URLs and status
    
    Returns:
        Various endpoints for testing
    """
    return {
        "endpoints": {
            "health_check": "GET /",
            "register": "POST /auth/register",
            "login": "POST /auth/login",
            "google_login": "GET /auth/google/login",
            "google_callback": "GET /auth/google/callback",
            "oauth_check": "GET /oauth-check",
            "auth_debug": "GET /auth-debug"
        },
        "environmental_config": {
            "FRONTEND_URL": FRONTEND_URL,
            "GOOGLE_CLIENT_ID": "✅ Configured" if GOOGLE_CLIENT_ID else "❌ Not configured",
            "GOOGLE_CLIENT_SECRET": "✅ Configured" if GOOGLE_CLIENT_SECRET else "❌ Not configured"
        },
        "frontend_pages": {
            "landing": "http://localhost:8000/",
            "login": "http://localhost:8000/login",
            "dashboard": "http://localhost:8000/dashboard",
            "scan": "http://localhost:8000/scan"
        },
        "test_flow": {
            "step_1": "Click Google button on /login page",
            "step_2": "You'll be redirected to: http://localhost:8000/auth/google/login",
            "step_3": "Google redirects back to: http://localhost:8000/auth/google/callback",
            "step_4": "If user exists in DB: redirected to /login?auth=google&user_id=X&email=Y",
            "step_5": "If user not found: redirected to /login?msg=user_not_found&email=Y"
        }
    }



# -------------------- Health history endpoints --------------------
class ParseHealthRequest(BaseModel):
    """Request to parse natural language health text"""
    text: str


@app.post("/parse-health")
def parse_health(request: ParseHealthRequest):
    """
    Parse natural language health information into structured format
    
    Args:
        text: Natural language description of health conditions
        
    Returns:
        Parsed health information with confidence score
        
    Example:
        Input: "I have diabetes, allergic to peanuts and shellfish, lactose intolerant"
        Output: {
            "parsed": {
                "conditions": {
                    "diabetes": True,
                    "peanut_allergy": True,
                    "shellfish_allergy": True,
                    "lactose_intolerance": True
                },
                "allergies": ["Peanut Allergy", "Shellfish Allergy", "Lactose Intolerance"],
                "dietary_preferences": [],
                "confidence": 0.95
            }
        }
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Please provide health information text"
            )

        # Parse the health text
        parsed = HealthParserService.parse_health_text(request.text)

        # Validate the parsed data
        is_valid, message = HealthParserService.validate_parsed_data(parsed)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)

        logger.info(f"Successfully parsed health text. Confidence: {parsed['confidence']:.0%}")

        return {
            "ok": True,
            "parsed": parsed
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to parse health text: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing health information: {str(e)}"
        )


@app.post("/health/{user_id}")
def save_health_history(user_id: int, payload: HealthRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hh = HealthHistory(user_id=user_id, data=json.dumps(payload.data))
    db.add(hh)
    db.commit()
    db.refresh(hh)
    return {"ok": True, "history_id": hh.id}


@app.get("/health/{user_id}")
def get_health_history(user_id: int, db: Session = Depends(get_db)):
    entry = (
        db.query(HealthHistory)
        .filter(HealthHistory.user_id == user_id)
        .order_by(HealthHistory.created_at.desc())
        .first()
    )
    if not entry:
        return {"ok": True, "history": None}
    try:
        data = json.loads(entry.data) if entry.data else None
    except Exception:
        data = entry.data
    return {"ok": True, "history": data, "created_at": entry.created_at.isoformat()}


@app.get("/scans/{user_id}")
def get_user_scans(user_id: int, limit: int = 20, db: Session = Depends(get_db)):
    """
    Return recent scans for a given user_id (most recent first)
    """
    scans = (
        db.query(Scan)
        .filter(Scan.user_id == user_id)
        .order_by(Scan.created_at.desc())
        .limit(limit)
        .all()
    )

    result_list = []
    for s in scans:
        try:
            parsed = json.loads(s.result) if s.result else {}
        except Exception:
            parsed = {"raw": s.result}

        result_list.append({
            "id": s.id,
            "user_id": s.user_id,
            "image_filename": s.image_filename,
            "created_at": s.created_at.isoformat(),
            "scan": parsed,
        })

    return {"ok": True, "scans": result_list}


# ==================== Development Entry Point ====================
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
