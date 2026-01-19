from app import create_app
from app.models.database import db, Candidate

app = create_app()

with app.app_context():
    db.create_all()
    
    # Add sample candidates
    if Candidate.query.count() == 0:
        candidates = [
            Candidate(name='Ram Bahadur Thapa', party='Nepal Congress'),
            Candidate(name='Sita Kumari Sharma', party='CPN-UML'),
            Candidate(name='Krishna Prasad Oli', party='Maoist Centre'),
            Candidate(name='NOTA', party='None of the Above')
        ]
        
        for candidate in candidates:
            db.session.add(candidate)
        
        db.session.commit()
        print("✅ Database initialized with sample candidates")
    else:
        print("ℹ️ Database already contains data")
