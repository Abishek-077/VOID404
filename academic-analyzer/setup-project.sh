#!/bin/bash

# Academic Analyzer - Complete Project Generator
# This script creates all necessary files and directories

set -e

echo "🚀 Generating Academic Analyzer Project Structure..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_DIR="/home/claude/academic-analyzer"

# Create all directories
echo -e "${BLUE}Creating directory structure...${NC}"

mkdir -p "$BASE_DIR"/{frontend,backend,ai-services,security,shared,docs,docker,.github/workflows}

# Frontend directories
mkdir -p "$BASE_DIR"/frontend/{public,src/{components/{common,analysis,dashboard,auth},pages,services,store,hooks,utils,types,assets}}

# Backend directories  
mkdir -p "$BASE_DIR"/backend/{src/{controllers,services,models,middleware,routes,utils,config},tests,logs}

# AI Services directories
mkdir -p "$BASE_DIR"/ai-services/{ocr-service/{app,tests},nlp-service/{app,tests},recommendation-service/{app,tests},common}

# Security directories
mkdir -p "$BASE_DIR"/security/{scanners,tests,reports}

# Shared directories
mkdir -p "$BASE_DIR"/shared/{types,config}

echo -e "${GREEN}✅ Directory structure created${NC}"

# Create .gitignore
cat > "$BASE_DIR"/.gitignore << 'EOF'
# Dependencies
node_modules/
__pycache__/
*.pyc
venv/
env/
.env
.env.local
.env.*.local

# Build outputs
dist/
build/
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test coverage
coverage/
.nyc_output/
*.cover
.coverage

# Uploads
uploads/
temp/

# Database
*.db
*.sqlite

# Security
reports/
*.pem
*.key
!.github

EOF

# Create docker-compose.yml
cat > "$BASE_DIR"/docker-compose.yml << 'EOF'
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:14-alpine
    container_name: academic-db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: academic_analyzer_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - academic-network

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: academic-redis
    ports:
      - "6379:6379"
    networks:
      - academic-network

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: ../docker/backend.Dockerfile
    container_name: academic-backend
    environment:
      - NODE_ENV=development
      - PORT=5000
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/academic_analyzer_dev
      - REDIS_URL=redis://redis:6379
      - AI_SERVICE_URL=http://ai-services:8000
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
      - /app/node_modules
    depends_on:
      - postgres
      - redis
    networks:
      - academic-network

  # AI Services
  ai-services:
    build:
      context: ./ai-services
      dockerfile: ../docker/ai-services.Dockerfile
    container_name: academic-ai
    ports:
      - "8000:8000"
    volumes:
      - ./ai-services:/app
    networks:
      - academic-network

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/frontend.Dockerfile
    container_name: academic-frontend
    environment:
      - REACT_APP_API_URL=http://localhost:5000/api
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    networks:
      - academic-network

networks:
  academic-network:
    driver: bridge

volumes:
  postgres_data:
EOF

# Create .env.example
cat > "$BASE_DIR"/.env.example << 'EOF'
# Application
NODE_ENV=development
PORT=5000

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=academic_analyzer_dev
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/academic_analyzer_dev

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRE=7d
JWT_REFRESH_EXPIRE=30d

# AWS S3 (Optional - for file storage)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET=academic-analyzer-files

# AI Services
AI_SERVICE_URL=http://localhost:8000

# File Upload
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=pdf,jpg,jpeg,png

# Rate Limiting
RATE_LIMIT_WINDOW=900000
RATE_LIMIT_MAX=100

# Email (Optional - for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=noreply@academic-analyzer.com

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Security
BCRYPT_ROUNDS=10
SESSION_SECRET=your-session-secret-change-this

# Logging
LOG_LEVEL=info
EOF

echo -e "${GREEN}✅ Configuration files created${NC}"
echo -e "${BLUE}Project structure generated successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. cd academic-analyzer"
echo "2. cp .env.example .env"
echo "3. Edit .env with your configuration"
echo "4. docker-compose up -d"
echo ""
echo "Or for manual setup:"
echo "1. cd backend && npm install"
echo "2. cd ../frontend && npm install"  
echo "3. cd ../ai-services && pip install -r requirements.txt"
echo "4. Setup PostgreSQL and Redis"
echo "5. npm run dev (in backend)"
echo "6. npm start (in frontend)"
echo "7. uvicorn main:app --reload (in ai-services)"

chmod +x "$BASE_DIR"/setup-project.sh
echo -e "${GREEN}✅ Setup script is executable${NC}"
EOF
chmod +x /home/claude/academic-analyzer/setup-project.sh
/home/claude/academic-analyzer/setup-project.sh