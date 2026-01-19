from flask import Blueprint, request, jsonify
from app.models.database import db, Voter
from app.utils.ocr import extract_citizenship_data
from app.utils.face_utils import extract_face_from_id, compare_faces
from app.utils.validation import compare_names, validate_citizenship_format
import numpy as np

verify_bp = Blueprint('verify', __name__)

@verify_bp.route('/verify/<int:voter_id>', methods=['POST'])
def verify_voter(voter_id):
    voter = Voter.query.get(voter_id)
    if not voter:
        return jsonify({'error': 'Voter not found'}), 404
    
    ocr_data, raw_text = extract_citizenship_data(voter.citizenship_image_path)
    
    checks = {
        'citizenship_format_valid': validate_citizenship_format(voter.citizenship_number),
        'name_match': False,
        'citizenship_number_match': False,
        'face_match': False
    }
    
    if ocr_data['name']:
        checks['name_match'] = compare_names(voter.name, ocr_data['name'])
    
    if ocr_data['citizenship_number']:
        checks['citizenship_number_match'] = (voter.citizenship_number == ocr_data['citizenship_number'])
    
    id_face_encoding = extract_face_from_id(voter.citizenship_image_path)
    voter_face_encoding = np.frombuffer(voter.face_encoding, dtype=np.float64)
    
    if id_face_encoding is not None:
        checks['face_match'] = compare_faces(id_face_encoding, voter_face_encoding)
    
    passed_checks = sum(checks.values())
    total_checks = len(checks)
    
    if passed_checks >= 3:
        voter.verification_status = 'VERIFIED'
        status = 'VERIFIED'
    else:
        voter.verification_status = 'REJECTED'
        status = 'REJECTED'
    
    db.session.commit()
    
    return jsonify({
        'status': status,
        'checks': checks,
        'ocr_data': ocr_data,
        'confidence': f"{passed_checks}/{total_checks}"
    }), 200
