# Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Environment Configuration](#environment-configuration)
7. [Database Migration](#database-migration)
8. [Monitoring & Logging](#monitoring--logging)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Node.js** 18+ and npm 9+
- **Python** 3.9+
- **PostgreSQL** 14+
- **Redis** 6+
- **Tesseract OCR** 4.1+
- **Docker** & Docker Compose (for containerized deployment)

### System Requirements
- **CPU:** 2+ cores
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 20GB minimum
- **OS:** Ubuntu 20.04+, macOS 12+, or Windows 10+ with WSL2

---

## Local Development

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/academic-analyzer.git
cd academic-analyzer
```

### 2. Install Dependencies

#### Backend
```bash
cd backend
npm install
```

#### Frontend
```bash
cd ../frontend
npm install
```

#### AI Services
```bash
cd ../ai-services
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r ocr-service/requirements.txt
pip install -r nlp-service/requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Setup Environment Variables
```bash
# Copy example env files
cp .env.example .env
cd backend && cp .env.example .env
cd ../frontend && cp .env.example .env
```

Edit each `.env` file with your configuration.

### 4. Setup Database
```bash
# Install PostgreSQL (Ubuntu)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE academic_analyzer_dev;
CREATE USER academic_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE academic_analyzer_dev TO academic_user;
\q

# Run migrations
cd backend
npm run migrate
npm run seed  # Optional: seed with sample data
```

### 5. Setup Redis
```bash
# Ubuntu
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

# macOS
brew install redis
brew services start redis
```

### 6. Install Tesseract OCR
```bash
# Ubuntu
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev

# macOS
brew install tesseract

# Windows
# Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
```

### 7. Start Services

Terminal 1 - Backend:
```bash
cd backend
npm run dev
```

Terminal 2 - Frontend:
```bash
cd frontend
npm start
```

Terminal 3 - OCR Service:
```bash
cd ai-services/ocr-service
source ../../venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

Terminal 4 - NLP Service:
```bash
cd ai-services/nlp-service
source ../../venv/bin/activate
uvicorn app.main:app --reload --port 8002
```

### 8. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Docs: http://localhost:5000/api/docs
- OCR Service: http://localhost:8001
- NLP Service: http://localhost:8002

---

## Production Deployment

### Pre-deployment Checklist
- [ ] All tests passing
- [ ] Security audit completed
- [ ] Environment variables configured
- [ ] SSL certificates obtained
- [ ] Backup strategy in place
- [ ] Monitoring setup
- [ ] Domain configured
- [ ] CDN configured (optional)

### 1. Server Setup (Ubuntu 22.04)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Redis
sudo apt install redis-server -y

# Install Nginx
sudo apt install nginx -y

# Install Python
sudo apt install python3.9 python3.9-venv python3-pip -y

# Install Tesseract
sudo apt install tesseract-ocr libtesseract-dev -y

# Install PM2 for process management
sudo npm install -g pm2
```

### 2. Application Setup

```bash
# Create app directory
sudo mkdir -p /var/www/academic-analyzer
sudo chown -R $USER:$USER /var/www/academic-analyzer

# Clone repository
cd /var/www/academic-analyzer
git clone https://github.com/yourusername/academic-analyzer.git .

# Install dependencies
cd backend && npm ci --production
cd ../frontend && npm ci && npm run build

cd ../ai-services
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure PM2

Create `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [
    {
      name: 'backend',
      script: 'src/server.js',
      cwd: '/var/www/academic-analyzer/backend',
      instances: 2,
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
        PORT: 5000
      }
    },
    {
      name: 'ocr-service',
      script: 'venv/bin/uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8001 --workers 2',
      cwd: '/var/www/academic-analyzer/ai-services/ocr-service'
    },
    {
      name: 'nlp-service',
      script: 'venv/bin/uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8002 --workers 2',
      cwd: '/var/www/academic-analyzer/ai-services/nlp-service'
    }
  ]
};
```

Start services:
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### 4. Configure Nginx

Create `/etc/nginx/sites-available/academic-analyzer`:
```nginx
# Frontend
server {
    listen 80;
    server_name academic-analyzer.com www.academic-analyzer.com;
    
    root /var/www/academic-analyzer/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;
}

# Backend API
server {
    listen 80;
    server_name api.academic-analyzer.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/academic-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d academic-analyzer.com -d www.academic-analyzer.com
sudo certbot --nginx -d api.academic-analyzer.com

# Auto-renewal
sudo certbot renew --dry-run
```

### 6. Configure Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## Docker Deployment

### 1. Build and Run

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### 2. Production Docker Compose

Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    restart: always
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: ../docker/backend.Dockerfile
    restart: always
    environment:
      NODE_ENV: production
    depends_on:
      - postgres
      - redis

  ai-services:
    build:
      context: ./ai-services
      dockerfile: ../docker/ai-services.Dockerfile
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/frontend.Dockerfile
      args:
        - REACT_APP_API_URL=${API_URL}
    restart: always

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
```

Run production:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Cloud Deployment

### AWS Deployment

#### 1. Prerequisites
- AWS Account
- AWS CLI installed
- EB CLI installed

#### 2. RDS Setup
```bash
# Create PostgreSQL instance via AWS Console or CLI
aws rds create-db-instance \
  --db-instance-identifier academic-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YourPassword \
  --allocated-storage 20
```

#### 3. ElastiCache Setup
```bash
# Create Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id academic-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1
```

#### 4. S3 for File Storage
```bash
# Create bucket
aws s3 mb s3://academic-analyzer-files

# Set bucket policy for uploads
```

#### 5. Deploy Backend (Elastic Beanstalk)
```bash
cd backend
eb init -p node.js academic-analyzer-backend
eb create academic-analyzer-env
eb deploy
```

#### 6. Deploy Frontend (S3 + CloudFront)
```bash
cd frontend
npm run build
aws s3 sync build/ s3://academic-analyzer-frontend
# Configure CloudFront distribution
```

### DigitalOcean Deployment

#### 1. Create Droplet
```bash
# Via doctl CLI
doctl compute droplet create academic-analyzer \
  --image ubuntu-22-04-x64 \
  --size s-2vcpu-4gb \
  --region nyc3
```

#### 2. Setup Managed Database
- Create managed PostgreSQL database
- Create managed Redis cluster

#### 3. Deploy Application
- Follow production deployment steps
- Use App Platform for simplified deployment

---

## Environment Configuration

### Production Environment Variables

```env
# Application
NODE_ENV=production
PORT=5000

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://host:6379

# JWT
JWT_SECRET=strong-random-secret-here
JWT_EXPIRE=1h
JWT_REFRESH_EXPIRE=7d

# AWS
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_S3_BUCKET=academic-analyzer-files

# Security
BCRYPT_ROUNDS=12
SESSION_SECRET=another-strong-secret

# Services
AI_SERVICE_URL=http://ai-services:8000
FRONTEND_URL=https://academic-analyzer.com

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=your-sendgrid-api-key
```

---

## Database Migration

### Create Migration
```bash
cd backend
npx sequelize-cli migration:generate --name add-new-column
```

### Run Migrations
```bash
# Development
npm run migrate

# Production
NODE_ENV=production npm run migrate

# Rollback
npm run migrate:undo
```

---

## Monitoring & Logging

### Setup PM2 Monitoring
```bash
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
```

### Application Monitoring
- Use PM2 Plus: https://pm2.io
- Setup New Relic or DataDog
- Configure CloudWatch (AWS)

### Log Aggregation
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk
- Papertrail

---

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
lsof -i :5000
# Kill process
kill -9 <PID>
```

#### Database Connection Failed
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U username -d database -h localhost
```

#### Redis Connection Failed
```bash
# Check Redis status
sudo systemctl status redis-server

# Test connection
redis-cli ping
```

#### PM2 Process Crashed
```bash
# View logs
pm2 logs

# Restart service
pm2 restart backend

# Flush logs
pm2 flush
```

---

## Backup & Recovery

### Database Backup
```bash
# Backup
pg_dump -U username -d database > backup.sql

# Restore
psql -U username -d database < backup.sql

# Automated backup script
*/0 0 * * * pg_dump -U user database | gzip > /backups/db-$(date +\%Y\%m\%d).sql.gz
```

### File Backup
```bash
# Backup uploads
tar -czf uploads-backup.tar.gz uploads/

# S3 sync
aws s3 sync uploads/ s3://backups/uploads/
```

---

## Health Checks

### Backend Health
```bash
curl http://localhost:5000/health
```

### Database Health
```bash
psql -U user -d database -c "SELECT 1"
```

### Redis Health
```bash
redis-cli ping
```

---

## Scaling

### Horizontal Scaling
- Use PM2 cluster mode
- Setup load balancer (Nginx, HAProxy)
- Deploy multiple app instances

### Vertical Scaling
- Upgrade server resources
- Optimize database queries
- Enable caching

### Database Scaling
- Read replicas
- Connection pooling
- Query optimization
- Indexing

---

For more help, contact: support@academic-analyzer.com
