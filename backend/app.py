"""
Enhanced Backend REST API for College Recommendation System
Includes comparison, statistics, and feedback features
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from ml_recommender import CollegeRecommender

app = Flask(__name__)
CORS(app)  # Allow frontend to make requests

# Initialize recommender
colleges_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'colleges.json')
recommender = CollegeRecommender(colleges_file)

# Store feedback (in production, use a database)
feedback_storage = []

@app.route('/api/colleges', methods=['GET'])
def get_all_colleges():
    """
    Get list of all colleges (for reference)
    """
    return jsonify(recommender.colleges)

@app.route('/api/colleges/<int:college_id>', methods=['GET'])
def get_college_by_id(college_id):
    """
    Get a specific college by ID
    """
    college = next((c for c in recommender.colleges if c['id'] == college_id), None)
    if college:
        return jsonify(college)
    return jsonify({'error': 'College not found'}), 404

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """
    Get college recommendations based on user profile
    Expects JSON with: stream, gpa, preferred_program, interests, location, budget_range, career_goal
    """
    try:
        user_profile = request.json
        
        # Validate required fields
        required_fields = ['stream', 'gpa', 'preferred_program', 'location', 'budget_range']
        missing_fields = [field for field in required_fields if not user_profile.get(field)]
        
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing': missing_fields
            }), 400
        
        # Get recommendations
        top_n = int(user_profile.get('top_n', 5))
        recommendations = recommender.recommend(user_profile, top_n=top_n)
        
        return jsonify({
            'recommendations': recommendations,
            'count': len(recommendations),
            'user_profile': user_profile
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Error processing request',
            'message': str(e)
        }), 500

@app.route('/api/compare', methods=['POST'])
def compare_colleges():
    """
    Compare multiple colleges side by side
    Expects JSON with: college_ids (list of college IDs)
    """
    try:
        data = request.json
        college_ids = data.get('college_ids', [])
        
        if not college_ids or len(college_ids) < 2:
            return jsonify({
                'error': 'Please provide at least 2 college IDs to compare'
            }), 400
        
        comparison = recommender.compare_colleges(college_ids)
        return jsonify(comparison)
    
    except Exception as e:
        return jsonify({
            'error': 'Error comparing colleges',
            'message': str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get statistics about the college dataset
    """
    try:
        stats = recommender.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'error': 'Error getting statistics',
            'message': str(e)
        }), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit feedback on a recommendation
    Expects JSON with: college_id, rating (1-5), comment (optional)
    """
    try:
        data = request.json
        feedback = {
            'college_id': data.get('college_id'),
            'rating': data.get('rating'),
            'comment': data.get('comment', ''),
            'timestamp': data.get('timestamp')
        }
        
        feedback_storage.append(feedback)
        
        return jsonify({
            'message': 'Feedback submitted successfully',
            'feedback': feedback
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Error submitting feedback',
            'message': str(e)
        }), 500

@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    """
    Get all feedback (for admin/analytics)
    """
    return jsonify({
        'feedback': feedback_storage,
        'count': len(feedback_storage)
    })

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """
    Enhanced rule-based chatbot to extract user information
    """
    try:
        user_message = request.json.get('message', '').lower()
        conversation_history = request.json.get('history', [])
        
        # Simple keyword matching to extract information
        response = {
            'reply': '',
            'extracted_data': {},
            'suggestions': []
        }
        
        # Check for stream
        if any(word in user_message for word in ['science', 'management', 'commerce', 'humanities']):
            if 'science' in user_message:
                response['extracted_data']['stream'] = 'Science'
            elif 'management' in user_message or 'commerce' in user_message:
                response['extracted_data']['stream'] = 'Management'
            elif 'humanities' in user_message:
                response['extracted_data']['stream'] = 'Humanities'
        
        # Check for GPA
        if 'gpa' in user_message or 'grade' in user_message or 'cgpa' in user_message:
            words = user_message.split()
            for i, word in enumerate(words):
                try:
                    gpa = float(word)
                    if 0 <= gpa <= 4:
                        response['extracted_data']['gpa'] = gpa
                        break
                except:
                    continue
        
        # Check for location
        locations = ['kathmandu', 'lalitpur', 'pokhara', 'biratnagar', 'butwal', 'any']
        for loc in locations:
            if loc in user_message:
                response['extracted_data']['location'] = loc.capitalize()
                break
        
        # Check for budget
        if any(word in user_message for word in ['low', 'cheap', 'affordable', 'budget']):
            response['extracted_data']['budget_range'] = 'low'
        elif any(word in user_message for word in ['medium', 'moderate', 'average']):
            response['extracted_data']['budget_range'] = 'medium'
        elif any(word in user_message for word in ['high', 'expensive', 'premium']):
            response['extracted_data']['budget_range'] = 'high'
        
        # Check for program
        programs = ['engineering', 'computer', 'bba', 'bbs', 'medicine', 'law', 'science', 'business']
        for prog in programs:
            if prog in user_message:
                if prog == 'engineering':
                    response['extracted_data']['preferred_program'] = 'Computer Engineering'
                elif prog == 'computer':
                    response['extracted_data']['preferred_program'] = 'Computer Science'
                elif prog == 'bba' or prog == 'business':
                    response['extracted_data']['preferred_program'] = 'BBA'
                elif prog == 'medicine':
                    response['extracted_data']['preferred_program'] = 'MBBS'
                else:
                    response['extracted_data']['preferred_program'] = prog.capitalize()
                break
        

        
        # Generate contextual reply
        if not response['extracted_data']:
            response['reply'] = "I can help you find colleges! Please tell me about your +2 stream, GPA, preferred program, location, and budget. For example: 'I completed Science with 3.5 GPA, want to study Computer Engineering in Kathmandu with medium budget.'"
            response['suggestions'] = [
                "What's your +2 stream?",
                "What's your GPA?",
                "Which program interests you?",
                "Where do you want to study?"
            ]
        else:
            extracted = response['extracted_data']
            reply_parts = ["Great! I noted:"]
            if 'stream' in extracted:
                reply_parts.append(f"Stream: {extracted['stream']}")
            if 'gpa' in extracted:
                reply_parts.append(f"GPA: {extracted['gpa']}")
            if 'location' in extracted:
                reply_parts.append(f"Location: {extracted['location']}")
            if 'preferred_program' in extracted:
                reply_parts.append(f"Program: {extracted['preferred_program']}")
            if 'budget_range' in extracted:
                reply_parts.append(f"Budget: {extracted['budget_range']}")
            
            missing = []
            if 'stream' not in extracted:
                missing.append("your +2 stream")
            if 'gpa' not in extracted:
                missing.append("your GPA")
            if 'preferred_program' not in extracted:
                missing.append("preferred program")
            if 'location' not in extracted:
                missing.append("location preference")
            
            if missing:
                reply_parts.append(f"Please also tell me about {', '.join(missing)}.")
            else:
                reply_parts.append("You can now fill the form and get recommendations!")
            
            response['reply'] = " ".join(reply_parts)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': 'Error processing chatbot message',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'ok',
        'message': 'College Recommendation API is running',
        'colleges_count': len(recommender.colleges)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
