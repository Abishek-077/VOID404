# 🚀 Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies

```bash
# Install Tesseract OCR
sudo apt install tesseract-ocr cmake  # Linux
# brew install tesseract cmake        # Mac

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
# Copy environment file
cp .env.example .env

# Initialize database with sample candidates
python init_db.py
```

### 3. Start Server

```bash
python run.py
```

Server runs at: **http://localhost:5000**

### 4. Open Frontend

Open in browser:
- Registration: `frontend/register.html`
- Voting: `frontend/vote.html`
- Results: `frontend/results.html`

## 🧪 Test Flow

1. **Add candidates** (already done by init_db.py)
2. **Register voter** → Open `register.html`
   - Fill form with citizenship number format: `1234-5678-9012`
   - Upload citizenship card image
   - Upload face photo
3. **Verify voter** → Run:
   ```bash
   curl -X POST http://localhost:5000/api/verify/verify/1
   ```
4. **Cast vote** → Open `vote.html`
   - Enter citizenship number
   - Select candidate
   - Submit
5. **View results** → Open `results.html`

## 📋 Sample Test Data

**Citizenship Number Format:** `1234-5678-9012`

**Sample Candidates (auto-added):**
- Ram Bahadur Thapa (Nepal Congress)
- Sita Kumari Sharma (CPN-UML)
- Krishna Prasad Oli (Maoist Centre)
- NOTA (None of the Above)

## 🔧 Troubleshooting

**Port 5000 in use:**
```bash
# Change port in backend/run.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Face recognition fails:**
```bash
pip install cmake dlib
pip install face-recognition
```

**Database errors:**
```bash
rm election.db
python init_db.py
```

## 📡 API Endpoints

- `POST /api/voter/register` - Register voter
- `GET /api/voter/status/<citizenship>` - Check status
- `POST /api/verify/verify/<voter_id>` - Verify voter
- `POST /api/vote/cast` - Cast vote
- `GET /api/vote/results` - Get results
- `POST /api/candidate/add` - Add candidate
- `GET /api/candidate/list` - List candidates

## 🎯 Next Steps

1. Improve OCR accuracy for Nepal citizenship cards
2. Add admin panel for verification approval
3. Implement voter authentication
4. Add vote encryption
5. Deploy to production server

---

**Need help?** Check `backend/README.md` for detailed documentation.
