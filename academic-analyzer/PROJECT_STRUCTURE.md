# Complete Project Structure

## Directory Tree
```
academic-analyzer/
├── frontend/                     # React TypeScript Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/          # Reusable components
│   │   │   ├── analysis/        # Analysis related
│   │   │   ├── dashboard/       # Dashboard components
│   │   │   └── auth/            # Authentication
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Upload.tsx
│   │   │   ├── Results.tsx
│   │   │   └── Profile.tsx
│   │   ├── services/
│   │   │   ├── api.ts           # Axios instance
│   │   │   ├── auth.service.ts
│   │   │   └── analysis.service.ts
│   │   ├── store/               # Redux store
│   │   ├── hooks/               # Custom hooks
│   │   ├── utils/               # Utilities
│   │   └── types/               # TypeScript types
│   └── package.json
│
├── backend/                      # Node.js Express Backend
│   ├── src/
│   │   ├── controllers/
│   │   │   ├── authController.js
│   │   │   ├── analysisController.js
│   │   │   ├── studentController.js
│   │   │   └── adminController.js
│   │   ├── services/
│   │   │   ├── authService.js
│   │   │   ├── analysisService.js
│   │   │   ├── uploadService.js
│   │   │   └── aiServiceClient.js
│   │   ├── models/
│   │   │   ├── index.js
│   │   │   ├── User.js
│   │   │   ├── StudentProfile.js
│   │   │   ├── Analysis.js
│   │   │   ├── Question.js
│   │   │   ├── Answer.js
│   │   │   └── RefreshToken.js
│   │   ├── middleware/
│   │   │   ├── auth.js
│   │   │   ├── validation.js
│   │   │   ├── upload.js
│   │   │   ├── errorHandler.js
│   │   │   └── securityHeaders.js
│   │   ├── routes/
│   │   │   ├── auth.js
│   │   │   ├── analysis.js
│   │   │   ├── student.js
│   │   │   └── admin.js
│   │   ├── utils/
│   │   │   ├── logger.js
│   │   │   ├── validators.js
│   │   │   └── helpers.js
│   │   ├── config/
│   │   │   ├── database.js
│   │   │   ├── redis.js
│   │   │   └── aws.js
│   │   └── server.js
│   └── package.json
│
├── ai-services/                  # Python AI Microservices
│   ├── ocr-service/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── ocr_engine.py
│   │   │   ├── preprocessor.py
│   │   │   └── models/
│   │   ├── tests/
│   │   └── requirements.txt
│   ├── nlp-service/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── analyzer.py
│   │   │   ├── semantic_similarity.py
│   │   │   ├── error_classifier.py
│   │   │   └── models/
│   │   ├── tests/
│   │   └── requirements.txt
│   ├── recommendation-service/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── recommender.py
│   │   │   └── models/
│   │   ├── tests/
│   │   └── requirements.txt
│   ├── common/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── validators.py
│   │   └── utils.py
│   └── docker-compose.yml
│
├── security/                     # Security & Penetration Testing
│   ├── scanners/
│   │   ├── __init__.py
│   │   ├── sql_injection_scanner.py
│   │   ├── xss_scanner.py
│   │   ├── auth_scanner.py
│   │   ├── file_upload_scanner.py
│   │   └── api_fuzzer.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_authentication.py
│   │   ├── test_authorization.py
│   │   ├── test_input_validation.py
│   │   └── test_file_security.py
│   ├── reports/
│   │   └── .gitkeep
│   ├── run_security_scan.py
│   └── requirements.txt
│
├── shared/                       # Shared configurations
│   ├── types/
│   │   └── common.ts
│   └── config/
│       └── constants.ts
│
├── docker/
│   ├── frontend.Dockerfile
│   ├── backend.Dockerfile
│   └── ai-services.Dockerfile
│
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── SECURITY.md
│   └── ARCHITECTURE.md
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── security-scan.yml
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## File Count Summary
- Frontend: ~50 files
- Backend: ~30 files
- AI Services: ~25 files
- Security: ~15 files
- Total: ~120+ files

## Key Technologies

### Frontend
- React 18, TypeScript, Material-UI
- Redux Toolkit, React Router
- Axios, React Query
- Recharts, React-PDF

### Backend
- Node.js, Express, PostgreSQL
- Sequelize ORM, Redis
- JWT, Bcrypt, Joi validation
- AWS S3, Winston logger

### AI Services
- Python, FastAPI, uvicorn
- Tesseract OCR, OpenCV
- spaCy, Sentence-Transformers
- scikit-learn, NumPy

### Security
- OWASP ZAP integration
- Custom penetration testing scripts
- Dependency vulnerability scanning
- Input validation & sanitization
