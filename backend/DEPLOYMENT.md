# RISKbite Deployment Guide

## Local Development

### Prerequisites
```bash
# 1. Python 3.8+
python --version

# 2. Tesseract OCR
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr

# 3. Node.js 16+ (for frontend)
node --version
npm --version
```

### Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python run_server.py
# or
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Setup Frontend
```bash
# In root directory
npm install
npm run dev
```

---

## Docker Deployment (Optional)

### Build Docker Image
```bash
# Create Dockerfile in backend directory
cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

# Install Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app/ app/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get

# Run app
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Build image
docker build -t riskbite-backend:latest backend/

# Run container
docker run -p 8000:8000 \
  -e CORS_ORIGINS="http://localhost:5173" \
  riskbite-backend:latest
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - API_ENV=production
      - CORS_ORIGINS=http://localhost:5173
      - LOG_LEVEL=INFO
    volumes:
      - ./backend:/app

  frontend:
    build: .
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
```

Run with: `docker-compose up`

---

## Cloud Deployment Options

### Option 1: Heroku (Easiest)

```bash
# 1. Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Create app
heroku create riskbite-app

# 4. Add buildpacks (for Tesseract)
heroku buildpacks:add https://github.com/heroku-community/heroku-buildpack-python
heroku buildpacks:add https://github.com/jontewks/heroku-buildpack-tesseract

# 5. Deploy
git push heroku main

# 6. View logs
heroku logs --tail
```

### Option 2: AWS (EC2)

```bash
# 1. Launch EC2 instance (Ubuntu 20.04)

# 2. Connect and install
ssh -i key.pem ubuntu@instance-ip

# 3. Update system
sudo apt-get update && sudo apt-get upgrade -y

# 4. Install dependencies
sudo apt-get install -y python3.9 python3.9-venv python3-pip
sudo apt-get install -y tesseract-ocr imagemagick
sudo apt-get install -y nodejs npm

# 5. Clone repository
git clone https://github.com/yourusername/riskbite.git
cd riskbite

# 6. Setup backend
cd backend
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 7. Setup systemd service
sudo cat > /etc/systemd/system/riskbite-backend.service << 'EOF'
[Unit]
Description=RISKbite Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/riskbite/backend
Environment="PATH=/home/ubuntu/riskbite/backend/venv/bin"
ExecStart=/home/ubuntu/riskbite/backend/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start riskbite-backend
sudo systemctl enable riskbite-backend

# 8. Setup frontend (using nginx)
sudo apt-get install -y nginx

# Build frontend
npm install
npm run build

# Configure nginx
sudo cat > /etc/nginx/sites-available/riskbite << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /home/ubuntu/riskbite/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
    }
}
EOF

sudo systemctl restart nginx
```

### Option 3: Railway (Simple)

```bash
# 1. Push to GitHub

# 2. Connect Railway to repo
# https://railway.app

# 3. Add environment variables:
# - PYTESSERACT_LOCATION (if needed)
# - CORS_ORIGINS

# 4. Deploy automatically on push
```

### Option 4: Vercel + Railway

```bash
# Frontend: Vercel
npm install -g vercel
vercel

# Backend: Railway (see above)

# Update frontend .env
VITE_API_URL=https://your-backend.railway.app
```

---

## Environment Setup (.env)

```bash
# Development
API_ENV=development
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=DEBUG

# Production
API_ENV=production
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://your-frontend.com,https://www.your-frontend.com
LOG_LEVEL=INFO
MAX_IMAGE_SIZE_MB=10

# Tesseract (if custom path)
TESSERACT_PATH=/usr/bin/tesseract  # Linux/Mac
# TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe  # Windows
```

---

## Production Checklist

### Backend
- [ ] Install Tesseract OCR
- [ ] Set environment variables
- [ ] Configure CORS correctly
- [ ] Enable rate limiting
- [ ] Setup error logging
- [ ] Monitor API performance
- [ ] Implement caching (Redis)
- [ ] Setup database backups
- [ ] Configure SSL/TLS
- [ ] Setup monitoring (Sentry)
- [ ] Add request validation
- [ ] Document API
- [ ] Setup CI/CD pipeline
- [ ] Load testing

### Frontend
- [ ] Build optimization
- [ ] Asset compression
- [ ] CDN setup
- [ ] CSS/JS minification
- [ ] Image optimization
- [ ] SEO optimization
- [ ] Accessibility audit
- [ ] Performance monitoring
- [ ] Error tracking
- [ ] Analytics setup

### Infrastructure
- [ ] Domain setup
- [ ] SSL certificate
- [ ] Database (if needed)
- [ ] Backup strategy
- [ ] DDoS protection
- [ ] Monitoring alerts
- [ ] Log aggregation
- [ ] Auto-scaling config

---

## Monitoring & Logging

### Backend Logging
```python
# Already configured in main.py
import logging
logger = logging.getLogger(__name__)
logger.info("Event message")
logger.error("Error message")
```

### Monitor Performance
```bash
# Check response times
curl -w "@format.txt" http://localhost:8000/

# Monitor resource usage
top
# or
htop

# Check logs
tail -f logs/app.log
```

### Error Tracking (Sentry)
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/project-id",
    environment="production"
)
```

---

## Scaling for Production

### 1. Caching
```python
# Cache ingredient lookups
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_ingredient_info(ingredient: str):
    return INGREDIENTS_DB.get(ingredient)
```

### 2. Database
```python
# Switch from in-memory to SQLite/PostgreSQL
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@localhost/riskbite')
```

### 3. Background Tasks
```python
# For long-running OCR
from celery import Celery

celery_app = Celery('riskbite')

@celery_app.task
def scan_product_async(image_path, conditions):
    # Long-running task
    return result
```

### 4. Load Balancing
```nginx
upstream backend {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

---

## Performance Optimization

### Backend
```bash
# Use Gunicorn for production
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# With async workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker --worker-class=uvicorn.workers.UvicornH11Worker app.main:app
```

### Frontend
```bash
# Build optimization
npm run build

# Check bundle size
npm run build -- --analyze

# Lighthouse audit
lighthouse https://your-frontend.com
```

### Database (if used)
```sql
-- Add indexes
CREATE INDEX idx_ingredient_name ON ingredients(name);
CREATE INDEX idx_ingredient_risk ON ingredients(risk_level);

-- Analyze performance
EXPLAIN ANALYZE SELECT * FROM ingredients WHERE risk_level = 'high';
```

---

## Troubleshooting Deployments

### Issue: Tesseract not found in production
```bash
# Solution: Install in container/server
# Docker: Already included
# EC2: sudo apt-get install tesseract-ocr
# Heroku: Use buildpack (see above)
```

### Issue: CORS errors
```python
# Check CORS_ORIGINS environment variable
# Frontend URL must be in list
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Slow OCR
```bash
# Solution: Upgrade server CPU
# Or: Use async workers
# Or: Pre-process images
# Or: Use GPU acceleration
```

### Issue: Memory usage high
```bash
# Limit image size
MAX_IMAGE_SIZE_MB = 10

# Implement caching
# Use Redis for session storage
```

---

## Maintenance

### Regular Tasks
```bash
# Check logs daily
tail -f logs/app.log

# Monitor performance hourly
# Review error rates
# Check database size

# Weekly
- Backup database
- Review analytics
- Check for updates

# Monthly
- Security audit
- Performance review
- User feedback analysis
```

### Updates
```bash
# Update Python packages
pip install --upgrade -r requirements.txt

# Update Node packages
npm update

# Security patches
# Apply immediately
```

---

## Support

For deployment issues:
1. Check logs: `tail -f logs/app.log`
2. Check health endpoint: `curl https://your-api.com/`
3. Check environment variables
4. Review firewall rules
5. Check database connectivity

---

That's it! Your RISKbite is production-ready! 🚀
