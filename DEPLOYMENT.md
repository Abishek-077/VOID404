# 🚀 Deployment Guide

## Local Development

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python init_db.py
python run.py
```

## Production Deployment

### Option 1: Traditional Server (Ubuntu)

```bash
# Install system dependencies
sudo apt update
sudo apt install python3-pip python3-venv tesseract-ocr cmake nginx

# Clone and setup
git clone <repo-url>
cd Smart-Election-System/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn

# Configure environment
cp .env.example .env
nano .env  # Set production values

# Initialize database
python init_db.py

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Option 2: Docker

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/election
    volumes:
      - ./uploads:/app/uploads
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: election
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html

volumes:
  postgres_data:
```

Run: `docker-compose up -d`

### Option 3: Cloud Platforms

#### AWS Elastic Beanstalk

```bash
pip install awsebcli
eb init -p python-3.10 election-system
eb create election-env
eb deploy
```

#### Heroku

```bash
# Add Procfile
echo "web: gunicorn run:app" > Procfile

# Deploy
heroku create nepal-election
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

#### DigitalOcean App Platform

1. Connect GitHub repo
2. Select Python app
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `gunicorn -w 4 run:app`
5. Add PostgreSQL database

## Environment Variables (Production)

```env
DATABASE_URL=postgresql://user:pass@host:5432/election
SECRET_KEY=<generate-strong-key>
UPLOAD_FOLDER=/var/uploads
MAX_CONTENT_LENGTH=16777216
FLASK_ENV=production
```

## Nginx Configuration

```nginx
server {
    listen 80;
    server_name election.example.com;

    location / {
        root /var/www/frontend;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /uploads {
        alias /var/uploads;
    }
}
```

## SSL/HTTPS (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d election.example.com
```

## Database Backup

```bash
# PostgreSQL
pg_dump election > backup_$(date +%Y%m%d).sql

# SQLite
cp election.db backup_$(date +%Y%m%d).db
```

## Monitoring

**Health Check Endpoint:**
```python
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

**Logging:**
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Security Checklist

- [ ] Change SECRET_KEY
- [ ] Use HTTPS
- [ ] Enable CORS only for trusted domains
- [ ] Set strong database password
- [ ] Limit file upload size
- [ ] Validate all inputs
- [ ] Use environment variables
- [ ] Regular backups
- [ ] Monitor logs
- [ ] Rate limiting

## Performance Optimization

```python
# Use connection pooling
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20

# Enable caching
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

## Scaling

**Horizontal Scaling:**
- Load balancer (Nginx/HAProxy)
- Multiple Gunicorn instances
- Shared database
- Shared file storage (S3/NFS)

**Database Optimization:**
- Add indexes on citizenship_number, voter_id
- Use read replicas
- Connection pooling

---

**Production URL:** `https://election.example.com`
