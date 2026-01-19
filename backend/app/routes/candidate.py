from flask import Blueprint, request, jsonify
from app.models.database import db, Candidate

candidate_bp = Blueprint('candidate', __name__)

@candidate_bp.route('/add', methods=['POST'])
def add_candidate():
    data = request.json
    name = data.get('name')
    party = data.get('party')
    
    if not name:
        return jsonify({'error': 'Name required'}), 400
    
    candidate = Candidate(name=name, party=party)
    db.session.add(candidate)
    db.session.commit()
    
    return jsonify({'message': 'Candidate added', 'id': candidate.id}), 201

@candidate_bp.route('/list', methods=['GET'])
def list_candidates():
    candidates = Candidate.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'party': c.party
    } for c in candidates]), 200
