# 🗳️ Nepal Smart Election System

Modern web-based election system with facial recognition, OCR verification, and secure voting for Nepal.

## 🚀 Features

- **Voter Registration** with Citizenship Card & Face Photo
- **AI-Powered Verification** (OCR + Face Matching)
- **Secure Voting** (One vote per verified voter)
- **Live Results Dashboard** with auto-refresh
- **Database Storage** (SQLite/PostgreSQL)

## 📁 Project Structure

```
backend/
├── app/
│   ├── models/
│   │   └── database.py          # SQLAlchemy models
│   ├── routes/
│   │   ├── voter.py             # Registration endpoints
│   │   ├── verify.py            # Verification logic
│   │   ├── vote.py              # Voting endpoints
│   │   └── candidate.py         # Candidate management
│   ├── utils/
│   │   ├── ocr.py               # Tesseract OCR
│   │   ├── face_utils.py        # Face recognition
│   │   └── validation.py        # Data validation
│   └── __init__.py              # Flask app factory
├── run.py                       # Entry point
└── requirements.txt

frontend/
├── register.html                # Voter registration UI
├── vote.html                    # Voting interface
└── results.html                 # Live results dashboard

uploads/
├── citizenship/                 # Citizenship card images
└── faces/                       # Face photos
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Tesseract OCR: `sudo apt install tesseract-ocr` (Linux) or `brew install tesseract` (Mac)
- CMake: `sudo apt install cmake` (for dlib/face_recognition)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run server
python run.py
```

Server runs at: `http://localhost:5000`

### Frontend Setup

Simply open HTML files in browser or use a local server:

```bash
cd frontend
python -m http.server 8000
```

Access at: `http://localhost:8000`

## 📡 API Endpoints

### Voter Registration
```http
POST /api/voter/register
Content-Type: multipart/form-data

Fields:
- name: string
- dob: YYYY-MM-DD
- citizenship_number: string (format: 1234-5678-9012)
- citizenship_image: file
- face_image: file

Response: { "message": "Registration successful", "voter_id": 1 }
```

### Check Voter Status
```http
GET /api/voter/status/<citizenship_number>

Response: {
  "name": "John Doe",
  "citizenship_number": "1234-5678-9012",
  "verification_status": "PENDING|VERIFIED|REJECTED",
  "registered_at": "2024-01-01T00:00:00"
}
```

### Verify Voter (OCR + Face Match)
```http
POST /api/verify/verify/<voter_id>

Response: {
  "status": "VERIFIED|REJECTED",
  "checks": {
    "citizenship_format_valid": true,
    "name_match": true,
    "citizenship_number_match": true,
    "face_match": true
  },
  "ocr_data": { ... },
  "confidence": "4/4"
}
```

### Cast Vote
```http
POST /api/vote/cast
Content-Type: application/json

Body: {
  "citizenship_number": "1234-5678-9012",
  "candidate_id": 1
}

Response: { "message": "Vote recorded successfully" }
```

### Get Results
```http
GET /api/vote/results

Response: [
  { "candidate": "Candidate A", "party": "Party X", "votes": 42 },
  { "candidate": "Candidate B", "party": "Party Y", "votes": 38 }
]
```

### Add Candidate
```http
POST /api/candidate/add
Content-Type: application/json

Body: {
  "name": "Candidate Name",
  "party": "Party Name"
}

Response: { "message": "Candidate added", "id": 1 }
```

### List Candidates
```http
GET /api/candidate/list

Response: [
  { "id": 1, "name": "Candidate A", "party": "Party X" }
]
```

## 🧪 Testing Workflow

1. **Add Candidates**
```bash
curl -X POST http://localhost:5000/api/candidate/add \
  -H "Content-Type: application/json" \
  -d '{"name":"Ram Sharma","party":"Nepal Congress"}'
```

2. **Register Voter** (use `register.html`)

3. **Verify Voter**
```bash
curl -X POST http://localhost:5000/api/verify/verify/1
```

4. **Cast Vote** (use `vote.html`)

5. **View Results** (use `results.html`)

## 🔒 Security Features

- Unique citizenship number constraint
- Face encoding stored as binary
- One vote per voter (DB constraint)
- CORS enabled for frontend
- File upload validation

## 🎯 Verification Logic

Voter is **VERIFIED** if ≥3 checks pass:
1. ✅ Citizenship number format valid
2. ✅ Name matches (fuzzy matching ≥80%)
3. ✅ Citizenship number matches OCR
4. ✅ Face matches ID photo (tolerance 0.6)

## 📊 Database Schema

**voters**
- id, name, dob, citizenship_number (unique)
- citizenship_image_path, face_encoding (binary)
- verification_status, created_at

**votes**
- id, voter_id (unique FK), candidate_id (FK)
- voted_at

**candidates**
- id, name, party, symbol_image

## 🐛 Troubleshooting

**Face recognition install fails:**
```bash
pip install cmake
pip install dlib
pip install face-recognition
```

**Tesseract not found:**
```bash
# Linux
sudo apt install tesseract-ocr

# Mac
brew install tesseract

# Windows
Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

**Database locked:**
```bash
rm backend/election.db
python backend/run.py  # Recreates DB
```

## 📝 License

MIT License

## 🤝 Contributing

Fork, modify, and submit PRs!

---

**Built for Nepal Elections 🇳🇵**
