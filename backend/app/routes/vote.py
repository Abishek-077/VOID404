from flask import Blueprint, request, jsonify
from app.models.database import db, Voter, Vote, Candidate

vote_bp = Blueprint('vote', __name__)

@vote_bp.route('/cast', methods=['POST'])
def cast_vote():
    data = request.json
    citizenship_number = data.get('citizenship_number')
    candidate_id = data.get('candidate_id')
    
    if not all([citizenship_number, candidate_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    voter = Voter.query.filter_by(citizenship_number=citizenship_number).first()
    if not voter:
        return jsonify({'error': 'Voter not found'}), 404
    
    if voter.verification_status != 'VERIFIED':
        return jsonify({'error': 'Voter not verified'}), 403
    
    existing_vote = Vote.query.filter_by(voter_id=voter.id).first()
    if existing_vote:
        return jsonify({'error': 'Already voted'}), 403
    
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({'error': 'Invalid candidate'}), 404
    
    vote = Vote(voter_id=voter.id, candidate_id=candidate_id)
    db.session.add(vote)
    db.session.commit()
    
    return jsonify({'message': 'Vote recorded successfully'}), 201

@vote_bp.route('/results', methods=['GET'])
def get_results():
    results = db.session.query(
        Candidate.name,
        Candidate.party,
        db.func.count(Vote.id).label('vote_count')
    ).join(Vote, Candidate.id == Vote.candidate_id, isouter=True)\
     .group_by(Candidate.id)\
     .all()
    
    return jsonify([{
        'candidate': r.name,
        'party': r.party,
        'votes': r.vote_count
    } for r in results]), 200
