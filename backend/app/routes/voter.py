from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.models.database import db, Voter
from app.utils.face_utils import encode_face
import os
from datetime import datetime

voter_bp = Blueprint('voter', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@voter_bp.route('/register', methods=['POST'])
def register_voter():
    data = request.form
    name = data.get('name')
    dob = data.get('dob')
    citizenship_number = data.get('citizenship_number')
    
    if not all([name, dob, citizenship_number]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    existing = Voter.query.filter_by(citizenship_number=citizenship_number).first()
    if existing:
        return jsonify({'error': 'Citizenship number already registered'}), 400
    
    citizenship_img = request.files.get('citizenship_image')
    face_img = request.files.get('face_image')
    
    if not citizenship_img or not face_img:
        return jsonify({'error': 'Both images required'}), 400
    
    upload_folder = os.getenv('UPLOAD_FOLDER', '../uploads')
    citizenship_path = os.path.join(upload_folder, 'citizenship', secure_filename(f"{citizenship_number}_{citizenship_img.filename}"))
    face_path = os.path.join(upload_folder, 'faces', secure_filename(f"{citizenship_number}_{face_img.filename}"))
    
    os.makedirs(os.path.dirname(citizenship_path), exist_ok=True)
    os.makedirs(os.path.dirname(face_path), exist_ok=True)
    
    citizenship_img.save(citizenship_path)
    face_img.save(face_path)
    
    face_encoding = encode_face(face_path)
    if face_encoding is None:
        return jsonify({'error': 'No face detected in image'}), 400
    
    voter = Voter(
        name=name,
        dob=datetime.strptime(dob, '%Y-%m-%d').date(),
        citizenship_number=citizenship_number,
        citizenship_image_path=citizenship_path,
        face_encoding=face_encoding.tobytes(),
        verification_status='PENDING'
    )
    
    db.session.add(voter)
    db.session.commit()
    
    return jsonify({'message': 'Registration successful', 'voter_id': voter.id}), 201

@voter_bp.route('/status/<citizenship_number>', methods=['GET'])
def get_voter_status(citizenship_number):
    voter = Voter.query.filter_by(citizenship_number=citizenship_number).first()
    if not voter:
        return jsonify({'error': 'Voter not found'}), 404
    
    return jsonify({
        'name': voter.name,
        'citizenship_number': voter.citizenship_number,
        'verification_status': voter.verification_status,
        'registered_at': voter.created_at.isoformat()
    }), 200
