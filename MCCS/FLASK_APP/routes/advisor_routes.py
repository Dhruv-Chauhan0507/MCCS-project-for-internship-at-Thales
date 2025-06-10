# flask_app/routes/advisor_routes.py

from flask import Blueprint, jsonify
import sys
sys.path.append('..')

from ADVISOR import smartkey_advisor  # assumed SmartKeyAdvisor module

advisor_bp = Blueprint('advisor', __name__)

@advisor_bp.route('/recommend/<username>', methods=['GET'])
def recommend_rotation(username):
    try:
        recommendation = smartkey_advisor.get_recommendation(username)
        return jsonify({
            "username": username,
            "rotation_needed": recommendation["rotation_needed"],
            "reason": recommendation["reason"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
