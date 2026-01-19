from flask import Flask
from flask_cors import CORS
from app.models.database import db
from app.routes.voter import voter_bp
from app.routes.verify import verify_bp
from app.routes.vote import vote_bp
from app.routes.candidate import candidate_bp
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///election.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    
    db.init_app(app)
    CORS(app)
    
    app.register_blueprint(voter_bp, url_prefix='/api/voter')
    app.register_blueprint(verify_bp, url_prefix='/api/verify')
    app.register_blueprint(vote_bp, url_prefix='/api/vote')
    app.register_blueprint(candidate_bp, url_prefix='/api/candidate')
    
    with app.app_context():
        db.create_all()
    
    return app
