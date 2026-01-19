# Quick Start Guide

Get the Academic Analyzer up and running in 5 minutes!

## 🚀 Super Quick Start (Using Docker)

### Prerequisites
- Docker and Docker Compose installed
- 8GB RAM minimum
- 20GB free disk space

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/academic-analyzer.git
cd academic-analyzer
```

2. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your configuration (use defaults for quick start)
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Wait for services to be ready** (~2 minutes)
```bash
docker-compose logs -f
```

5. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- API Health: http://localhost:5000/health

6. **Create your first account**
- Navigate to http://localhost:3000/register
- Fill in your details
- Start analyzing!

That's it! 🎉

---

## 💻 Manual Installation (Development)

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- Tesseract OCR

### Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your database credentials

# Create database
createdb academic_analyzer_dev

# Run migrations
npm run migrate

# Start server
npm run dev
```

Backend will be running on http://localhost:5000

### Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env

# Start development server
npm start
```

Frontend will be running on http://localhost:3000

### AI Services Setup

```bash
# Navigate to AI services (in a new terminal)
cd ai-services

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r ocr-service/requirements.txt
pip install -r nlp-service/requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start OCR service (Terminal 1)
cd ocr-service
uvicorn app.main:app --reload --port 8001

# Start NLP service (Terminal 2)
cd nlp-service
uvicorn app.main:app --reload --port 8002
```

---

## 🧪 Testing the Setup

### 1. Check Backend Health
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "OK",
  "timestamp": "...",
  "uptime": 123.45,
  "environment": "development"
}
```

### 2. Test User Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234",
    "firstName": "Test",
    "lastName": "User",
    "role": "student"
  }'
```

### 3. Upload Sample Answer Sheet
- Login to http://localhost:3000
- Navigate to "Upload" page
- Upload a PDF or image
- Wait for analysis results

---

## 📝 Sample Test Data

### Create Test User via API
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "Student123",
    "firstName": "John",
    "lastName": "Doe",
    "role": "student"
  }'
```

### Login and Get Token
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "Student123"
  }'
```

Save the returned `token` for subsequent requests.

---

## 🔧 Common Setup Issues

### Issue: Port already in use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Issue: Database connection failed
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql
```

### Issue: Redis connection failed
```bash
# Check if Redis is running
sudo systemctl status redis

# Start Redis
sudo systemctl start redis
```

### Issue: Docker containers not starting
```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild and start
docker-compose up -d --build
```

### Issue: Python dependencies fail to install
```bash
# Upgrade pip
pip install --upgrade pip

# Install build tools (Ubuntu)
sudo apt install python3-dev build-essential

# Try installing again
pip install -r requirements.txt
```

---

## 📚 Next Steps

1. **Read the Documentation**
   - [API Documentation](./docs/API.md)
   - [Deployment Guide](./docs/DEPLOYMENT.md)
   - [Security Guide](./docs/SECURITY.md)
   - [Architecture Overview](./docs/ARCHITECTURE.md)

2. **Explore Features**
   - Upload answer sheets
   - View analysis results
   - Track performance over time
   - Get personalized study recommendations

3. **Customize**
   - Add your own model answers
   - Configure grading rubrics
   - Customize UI theme
   - Add custom subjects

4. **Deploy to Production**
   - Follow [Deployment Guide](./docs/DEPLOYMENT.md)
   - Setup monitoring and logging
   - Configure backups
   - Enable SSL/HTTPS

---

## 🆘 Getting Help

- **Documentation:** `/docs` folder
- **Issues:** GitHub Issues
- **Email:** support@academic-analyzer.com
- **Discord:** Join our community

---

## 🔐 Security Note

**Important:** Before deploying to production:

1. Change all default passwords
2. Generate strong JWT secrets
3. Enable HTTPS/SSL
4. Configure firewalls
5. Run security audit: `npm run security:audit`
6. Review [Security Guide](./docs/SECURITY.md)

---

## 📊 System Requirements

### Minimum
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB
- OS: Ubuntu 20.04+, macOS 12+, Windows 10+

### Recommended
- CPU: 4 cores
- RAM: 8GB
- Storage: 50GB
- OS: Ubuntu 22.04 LTS

---

## 🎯 Quick Commands Reference

```bash
# Start all services (Docker)
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Backend development
cd backend && npm run dev

# Frontend development
cd frontend && npm start

# Run tests
npm test

# Database migration
npm run migrate

# Security scan
cd security && python run_security_scan.py
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Backend accessible at http://localhost:5000
- [ ] Frontend accessible at http://localhost:3000
- [ ] Database connection successful
- [ ] Redis connection successful
- [ ] OCR service running on port 8001
- [ ] NLP service running on port 8002
- [ ] Can register a new user
- [ ] Can login successfully
- [ ] Can upload a test file
- [ ] Can view analysis results

---

Happy analyzing! 🎓✨
