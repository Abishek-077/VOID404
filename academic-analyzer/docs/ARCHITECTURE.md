# System Architecture

## Overview

The Academic Answer Sheet Analyzer is a microservices-based web application that uses AI to analyze student answer sheets, provide feedback, and suggest improvements.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  Web Browser (React SPA)    │    Mobile App (Future)            │
└──────────────────┬───────────────────────────────────────────────┘
                   │
                   │ HTTPS/WSS
                   │
┌──────────────────▼───────────────────────────────────────────────┐
│                      LOAD BALANCER / CDN                          │
│                     (Nginx / CloudFlare)                          │
└──────────────────┬───────────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼─────────┐  ┌────────▼────────┐
│   Frontend      │  │   Backend API   │
│   (Static)      │  │   (Node.js)     │
│   React Build   │  │   Express.js    │
└─────────────────┘  └────────┬────────┘
                              │
                   ┌──────────┼──────────┐
                   │          │          │
              ┌────▼───┐  ┌───▼────┐  ┌─▼──────────┐
              │ Redis  │  │ PostDB │  │ AI Services│
              │ Cache  │  │        │  │  (Python)  │
              └────────┘  └────────┘  └─┬──────────┘
                                        │
                                ┌───────┼────────┐
                                │       │        │
                           ┌────▼──┐ ┌─▼───┐ ┌──▼────┐
                           │  OCR  │ │ NLP │ │ Recom │
                           │Service│ │Svc  │ │ Svc   │
                           └───────┘ └─────┘ └───────┘
                           
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                           │
├─────────────────────────────────────────────────────────────────┤
│   AWS S3    │   SendGrid   │   Analytics   │   Monitoring      │
│  (Storage)  │   (Email)    │  (Mixpanel)   │  (DataDog)        │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
```
Technology: React 18 + TypeScript
UI Framework: Material-UI (MUI)
State Management: Redux Toolkit
Routing: React Router v6
HTTP Client: Axios
Charts: Recharts
Build Tool: Create React App (CRA)
```

### Backend
```
Runtime: Node.js 18 LTS
Framework: Express.js
Database ORM: Sequelize
Authentication: JWT + bcrypt
Validation: Joi
File Upload: Multer
Cache: Redis (ioredis)
Logging: Winston
Process Manager: PM2
```

### AI Services
```
Language: Python 3.9+
Framework: FastAPI
OCR: Tesseract, TrOCR
NLP: spaCy, Sentence-Transformers
ML: scikit-learn, TensorFlow
Image Processing: OpenCV, Pillow
```

### Database
```
Primary: PostgreSQL 14
Cache: Redis 6
File Storage: AWS S3 / MinIO
```

### Security
```
Authentication: JWT (Access + Refresh tokens)
Password Hashing: bcrypt (12 rounds)
Input Validation: Joi + express-validator
SQL Injection Prevention: Sequelize ORM
XSS Protection: Helmet, sanitize-html
CSRF Protection: csurf
Rate Limiting: express-rate-limit
```

---

## Component Architecture

### 1. Frontend Architecture

```
src/
├── components/           # Reusable UI components
│   ├── common/          # Button, Card, Modal, etc.
│   ├── analysis/        # Analysis-specific components
│   ├── dashboard/       # Dashboard widgets
│   └── auth/            # Login, Register forms
│
├── pages/               # Route-level components
│   ├── Login.tsx
│   ├── Dashboard.tsx
│   ├── Upload.tsx
│   ├── Results.tsx
│   └── Profile.tsx
│
├── store/               # Redux store
│   ├── slices/
│   │   ├── authSlice.ts
│   │   ├── analysisSlice.ts
│   │   └── uiSlice.ts
│   └── store.ts
│
├── services/            # API integration
│   ├── api.ts          # Axios instance
│   ├── auth.service.ts
│   └── analysis.service.ts
│
├── hooks/               # Custom React hooks
│   ├── useAuth.ts
│   ├── useAnalysis.ts
│   └── useDebounce.ts
│
├── utils/               # Helper functions
│   ├── validators.ts
│   ├── formatters.ts
│   └── constants.ts
│
└── types/               # TypeScript types
    ├── auth.types.ts
    └── analysis.types.ts
```

**Design Patterns:**
- Container/Presentational pattern
- Custom hooks for logic reuse
- Redux Toolkit for state management
- Atomic design principles

### 2. Backend Architecture

```
src/
├── controllers/         # Route handlers
│   ├── authController.js
│   ├── analysisController.js
│   ├── studentController.js
│   └── adminController.js
│
├── services/            # Business logic
│   ├── authService.js
│   ├── analysisService.js
│   ├── uploadService.js
│   └── aiServiceClient.js
│
├── models/              # Database models
│   ├── User.js
│   ├── StudentProfile.js
│   ├── Analysis.js
│   ├── Question.js
│   └── Answer.js
│
├── middleware/          # Express middleware
│   ├── auth.js         # JWT verification
│   ├── validation.js   # Input validation
│   ├── upload.js       # File upload handling
│   └── errorHandler.js # Global error handling
│
├── routes/              # API routes
│   ├── auth.js
│   ├── analysis.js
│   ├── student.js
│   └── admin.js
│
├── utils/               # Utilities
│   ├── logger.js
│   ├── validators.js
│   └── helpers.js
│
└── config/              # Configuration
    ├── database.js
    ├── redis.js
    └── aws.js
```

**Design Patterns:**
- MVC (Model-View-Controller)
- Service layer pattern
- Repository pattern
- Dependency injection

### 3. AI Services Architecture

```
ai-services/
├── ocr-service/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── ocr_engine.py        # OCR processing
│   │   ├── preprocessor.py      # Image preprocessing
│   │   └── models/              # ML models
│   └── requirements.txt
│
├── nlp-service/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── analyzer.py          # Answer analysis
│   │   ├── semantic_similarity.py
│   │   ├── error_classifier.py
│   │   └── models/              # NLP models
│   └── requirements.txt
│
└── recommendation-service/
    ├── app/
    │   ├── main.py              # FastAPI app
    │   ├── recommender.py       # Study recommendations
    │   └── models/
    └── requirements.txt
```

**Design Patterns:**
- Microservices architecture
- API Gateway pattern
- Circuit Breaker (for resilience)
- Queue-based processing

---

## Data Flow

### 1. User Registration Flow

```
┌──────┐      ┌─────────┐      ┌──────────┐      ┌──────────┐
│Client│─────>│ Backend │─────>│ Database │<─────│ Validate │
└──────┘      └─────────┘      └──────────┘      └──────────┘
    │              │                  │
    │              │                  │
    │         ┌────▼────┐             │
    │         │  Hash   │             │
    │         │Password │             │
    │         └────┬────┘             │
    │              │                  │
    │              ▼                  │
    │         ┌────────┐              │
    │◄────────│  JWT   │              │
    │         │ Token  │              │
    │         └────────┘              │
    │                                 │
    │◄────────────────────────────────┘
```

### 2. Answer Sheet Analysis Flow

```
┌──────┐  1. Upload  ┌─────────┐  2. Store  ┌─────┐
│Client│────────────>│ Backend │──────────>│ S3  │
└──────┘             └─────────┘            └─────┘
    │                     │
    │                     │ 3. Extract Text
    │                     ▼
    │                ┌─────────┐
    │                │   OCR   │
    │                │ Service │
    │                └────┬────┘
    │                     │
    │                     │ 4. Analyze
    │                     ▼
    │                ┌─────────┐
    │                │   NLP   │
    │                │ Service │
    │                └────┬────┘
    │                     │
    │                     │ 5. Generate Report
    │                     ▼
    │                ┌─────────┐
    │                │Recommend│
    │                │ Service │
    │                └────┬────┘
    │                     │
    │                     │ 6. Save Results
    │                     ▼
    │                ┌──────────┐
    │                │ Database │
    │                └──────────┘
    │                     │
    │                     │ 7. Cache
    │                     ▼
    │                ┌─────────┐
    │                │  Redis  │
    │                └────┬────┘
    │                     │
    │       8. Results    │
    │◄────────────────────┘
```

### 3. Caching Strategy

```
┌──────────────────────────────────────────┐
│           Request Flow with Cache         │
└──────────────────────────────────────────┘

Request
   │
   ▼
┌────────────┐     Hit     ┌──────────┐
│   Redis    │<───────────>│  Return  │
│   Cache    │             │  Cached  │
└─────┬──────┘             └──────────┘
      │ Miss
      ▼
┌────────────┐
│  Database  │
│   Query    │
└─────┬──────┘
      │
      ▼
┌────────────┐
│   Store    │
│  in Cache  │
└─────┬──────┘
      │
      ▼
   Return
```

**Cache Keys:**
- `user:{userId}` - User profile (TTL: 1 hour)
- `analysis:{analysisId}` - Analysis results (TTL: 24 hours)
- `performance:{userId}:{period}` - Performance metrics (TTL: 15 minutes)
- `session:{sessionId}` - Session data (TTL: 7 days)

---

## Database Schema

### Core Tables

```sql
-- Users table
users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role ENUM('student', 'teacher', 'admin'),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)

-- Student profiles
student_profiles (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    grade VARCHAR(20),
    school VARCHAR(255),
    subjects JSONB,
    created_at TIMESTAMP
)

-- Analyses
analyses (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    subject VARCHAR(100),
    exam_type VARCHAR(50),
    file_url VARCHAR(500),
    status VARCHAR(50),
    results JSONB,
    created_at TIMESTAMP
)

-- Questions
questions (
    id UUID PRIMARY KEY,
    analysis_id UUID REFERENCES analyses(id),
    question_number INTEGER,
    question_text TEXT,
    max_marks INTEGER
)

-- Answers
answers (
    id UUID PRIMARY KEY,
    question_id UUID REFERENCES questions(id),
    answer_text TEXT,
    score FLOAT,
    feedback JSONB
)
```

**Indexes:**
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_analyses_user ON analyses(user_id);
CREATE INDEX idx_analyses_created ON analyses(created_at DESC);
CREATE INDEX idx_questions_analysis ON questions(analysis_id);
```

---

## Security Architecture

### Authentication Flow

```
┌──────┐                ┌─────────┐
│Client│                │ Backend │
└───┬──┘                └────┬────┘
    │                        │
    │  1. Login Credentials  │
    │───────────────────────>│
    │                        │
    │                   ┌────▼─────┐
    │                   │ Validate │
    │                   │Credentials│
    │                   └────┬─────┘
    │                        │
    │                   ┌────▼─────┐
    │                   │ Generate │
    │                   │   JWT    │
    │                   └────┬─────┘
    │                        │
    │  2. Access + Refresh   │
    │<───────────────────────┤
    │      Tokens            │
    │                        │
    │  3. API Request        │
    │     + Access Token     │
    │───────────────────────>│
    │                        │
    │                   ┌────▼─────┐
    │                   │ Verify   │
    │                   │   JWT    │
    │                   └────┬─────┘
    │                        │
    │  4. Response           │
    │<───────────────────────┤
```

### Security Layers

1. **Network Layer**
   - HTTPS/TLS 1.3
   - Firewall rules
   - DDoS protection

2. **Application Layer**
   - Input validation
   - Output encoding
   - CORS configuration
   - Security headers (Helmet)

3. **Authentication Layer**
   - JWT tokens
   - Refresh token rotation
   - Password hashing (bcrypt)
   - Account lockout

4. **Authorization Layer**
   - Role-based access control (RBAC)
   - Resource-level permissions
   - API rate limiting

5. **Data Layer**
   - Encrypted at rest
   - Encrypted in transit
   - SQL injection prevention
   - XSS protection

---

## Scalability Considerations

### Horizontal Scaling

```
                    ┌─────────────┐
                    │Load Balancer│
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼────┐      ┌─────▼────┐
   │Backend 1│       │Backend 2 │      │Backend 3 │
   └────┬────┘       └─────┬────┘      └─────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │  PostgreSQL │
                    │   (Master)  │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      ┌─────▼────┐   ┌─────▼────┐  ┌─────▼────┐
      │Replica 1 │   │Replica 2 │  │Replica 3 │
      └──────────┘   └──────────┘  └──────────┘
```

### Performance Optimization

1. **Database**
   - Connection pooling
   - Query optimization
   - Proper indexing
   - Read replicas

2. **Caching**
   - Redis for session data
   - CDN for static assets
   - API response caching

3. **AI Services**
   - Model optimization
   - Batch processing
   - GPU acceleration

4. **Frontend**
   - Code splitting
   - Lazy loading
   - Image optimization
   - Service workers

---

## Monitoring & Observability

### Metrics to Track

- **System Metrics:** CPU, Memory, Disk, Network
- **Application Metrics:** Request rate, Response time, Error rate
- **Business Metrics:** User registrations, Analyses completed, Average scores
- **AI Metrics:** OCR accuracy, NLP processing time, Model confidence

### Logging Strategy

```
Application Logs
    ├── Error logs (Critical issues)
    ├── Access logs (API requests)
    ├── Security logs (Auth attempts, suspicious activity)
    └── Business logs (Analysis completions, user actions)
```

### Alerting Rules

- CPU > 80% for 5 minutes
- Memory > 90% for 5 minutes
- Error rate > 5% for 10 minutes
- Database connections > 90% of pool
- API response time > 2 seconds

---

## Disaster Recovery

### Backup Strategy

```
Daily:
├── Database full backup (3AM)
├── Incremental backup (Every 6 hours)
└── File storage sync to S3

Weekly:
└── Complete system snapshot

Monthly:
└── Archive to Glacier
```

### Recovery Time Objectives (RTO)

- Database: < 1 hour
- Application: < 30 minutes
- Files: < 2 hours

### Recovery Point Objectives (RPO)

- Database: < 15 minutes
- Files: < 1 hour

---

## Future Enhancements

1. **Real-time Collaboration**
   - WebSocket integration
   - Live feedback

2. **Mobile Applications**
   - React Native apps
   - Progressive Web App (PWA)

3. **Advanced AI Features**
   - Handwriting recognition improvements
   - Multi-language support
   - Personalized learning paths

4. **Integration**
   - LMS integration (Moodle, Canvas)
   - Google Classroom
   - Microsoft Teams

5. **Analytics Dashboard**
   - Teacher analytics
   - Class performance tracking
   - Predictive analytics

---

For implementation details, see:
- [API Documentation](./API.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Security Guide](./SECURITY.md)
