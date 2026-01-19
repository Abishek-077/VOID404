# 🎓 AI-Powered Academic Answer Sheet Analyzer

A comprehensive web application that helps students improve their exam performance through AI-powered analysis, personalized feedback, and study recommendations.

## 🏗️ Architecture Overview

```
academic-analyzer/
├── frontend/              # React + TypeScript frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── hooks/        # Custom React hooks
│   │   ├── utils/        # Utility functions
│   │   └── types/        # TypeScript types
│   └── public/
├── backend/              # Node.js + Express backend
│   ├── src/
│   │   ├── controllers/  # Route controllers
│   │   ├── services/     # Business logic
│   │   ├── models/       # Database models
│   │   ├── middleware/   # Express middleware
│   │   ├── routes/       # API routes
│   │   └── utils/        # Helper functions
│   └── tests/
├── ai-services/          # Python AI/ML microservices
│   ├── ocr-service/      # OCR processing
│   ├── nlp-service/      # Answer analysis
│   ├── recommendation/   # Study recommendations
│   └── common/           # Shared utilities
├── security/             # Security & penetration testing
│   ├── scanners/         # Vulnerability scanners
│   ├── reports/          # Security reports
│   └── tests/            # Security tests
└── shared/               # Shared types and configs
    ├── types/
    └── config/
```

## 🚀 Features

### Core Features
- **OCR Processing**: Extracts text from handwritten/typed answer sheets
- **AI Analysis**: Evaluates answer quality using NLP and semantic similarity
- **Error Detection**: Identifies conceptual, computational, and structural errors
- **Personalized Feedback**: Provides actionable improvement suggestions
- **Score Prediction**: Predicts current and potential scores
- **Study Recommendations**: Suggests relevant learning resources
- **Performance Tracking**: Tracks improvement over time
- **Peer Benchmarking**: Compares performance with peer averages

### Security Features
- **Input Validation**: Sanitizes all user inputs
- **File Upload Security**: Validates file types, sizes, and content
- **Rate Limiting**: Prevents abuse and DDoS attacks
- **Authentication**: JWT-based secure authentication
- **Data Encryption**: Encrypts sensitive data at rest and in transit
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Content Security Policy implementation
- **CSRF Protection**: Token-based CSRF prevention

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI)
- **State Management**: Redux Toolkit
- **API Client**: Axios
- **Charts**: Recharts
- **File Upload**: React Dropzone
- **PDF Viewer**: React-PDF

### Backend
- **Runtime**: Node.js 18+
- **Framework**: Express.js
- **Database**: PostgreSQL with Sequelize ORM
- **Cache**: Redis
- **File Storage**: AWS S3 / MinIO
- **Authentication**: JWT + bcrypt
- **Validation**: Joi

### AI Services
- **Language**: Python 3.9+
- **OCR**: Tesseract, TrOCR
- **NLP**: spaCy, Sentence-Transformers
- **ML**: scikit-learn, TensorFlow
- **Image Processing**: OpenCV, Pillow
- **API Framework**: FastAPI

### Security
- **Vulnerability Scanning**: OWASP ZAP, Nmap
- **Dependency Scanning**: Snyk, npm audit
- **Penetration Testing**: Custom Python scripts
- **Monitoring**: ELK Stack (Elasticsearch, Logstash, Kibana)

## 📋 Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- Docker and Docker Compose (optional)
- Tesseract OCR

## 🔧 Installation

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/academic-analyzer.git
cd academic-analyzer

# Start all services
docker-compose up -d

# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
# AI Services: http://localhost:8000
```

### Manual Installation

#### 1. Backend Setup
```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your configuration
npm run migrate
npm run seed
npm run dev
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your configuration
npm start
```

#### 3. AI Services Setup
```bash
cd ai-services
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload --port 8000
```

## 🔐 Environment Variables

### Backend (.env)
```env
NODE_ENV=development
PORT=5000
DATABASE_URL=postgresql://user:password@localhost:5432/academic_analyzer
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRE=7d
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=academic-analyzer-files
AI_SERVICE_URL=http://localhost:8000
MAX_FILE_SIZE=10485760  # 10MB
RATE_LIMIT_WINDOW=900000  # 15 minutes
RATE_LIMIT_MAX=100
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

### AI Services (.env)
```env
MODEL_PATH=./models
DEVICE=cpu  # or cuda
MAX_WORKERS=4
LOG_LEVEL=INFO
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh JWT token
- `POST /api/auth/logout` - Logout user

### Analysis Endpoints
- `POST /api/analysis/upload` - Upload answer sheet
- `GET /api/analysis/:id` - Get analysis results
- `GET /api/analysis/user/:userId` - Get user's analysis history
- `DELETE /api/analysis/:id` - Delete analysis

### Student Endpoints
- `GET /api/students/profile` - Get student profile
- `PUT /api/students/profile` - Update profile
- `GET /api/students/performance` - Get performance metrics
- `GET /api/students/recommendations` - Get study recommendations

### Admin Endpoints
- `GET /api/admin/users` - List all users
- `GET /api/admin/analytics` - System analytics
- `POST /api/admin/model-answers` - Add model answers
- `PUT /api/admin/model-answers/:id` - Update model answer

## 🧪 Testing

```bash
# Backend tests
cd backend
npm test
npm run test:coverage

# Frontend tests
cd frontend
npm test
npm run test:coverage

# AI Services tests
cd ai-services
pytest
pytest --cov=.

# Security tests
cd security
python run_security_scan.py
```

## 🛡️ Security Best Practices

1. **Never commit sensitive data** (.env files, keys, passwords)
2. **Use parameterized queries** to prevent SQL injection
3. **Validate all inputs** on both client and server
4. **Implement rate limiting** on all endpoints
5. **Use HTTPS** in production
6. **Keep dependencies updated** regularly
7. **Implement proper CORS** policies
8. **Use Content Security Policy** headers
9. **Sanitize file uploads** thoroughly
10. **Log security events** for monitoring

## 📊 Performance Optimization

- **Database indexing** on frequently queried fields
- **Redis caching** for frequently accessed data
- **CDN** for static assets
- **Image optimization** for faster loading
- **Code splitting** in React
- **Lazy loading** for routes and components
- **Database connection pooling**
- **Gzip compression** for API responses

## 🚀 Deployment

### Production Checklist
- [ ] Set `NODE_ENV=production`
- [ ] Use production database
- [ ] Enable HTTPS/SSL
- [ ] Set secure session cookies
- [ ] Configure CORS properly
- [ ] Set up monitoring (PM2, CloudWatch)
- [ ] Configure log rotation
- [ ] Set up automated backups
- [ ] Enable CDN for static assets
- [ ] Run security audit
- [ ] Set up CI/CD pipeline

### Deployment Platforms
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Backend**: AWS EC2, Heroku, DigitalOcean
- **Database**: AWS RDS, DigitalOcean Managed DB
- **AI Services**: AWS Lambda, Google Cloud Run

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- OpenAI for AI capabilities
- Tesseract OCR team
- All open-source contributors

## 📧 Support

For support, email support@academic-analyzer.com or open an issue on GitHub.

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.
