# Backend API for College Recommendation System

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
    # Get list of all colleges
    return jsonify(recommender.colleges)

@app.route('/api/colleges/<int:college_id>', methods=['GET'])
def get_college_by_id(college_id):
    # Get a specific college by ID
    college = next((c for c in recommender.colleges if c['id'] == college_id), None)
    if college:
        return jsonify(college)
    return jsonify({'error': 'College not found'}), 404

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    # Get college recommendations based on user profile
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
    # Compare multiple colleges side by side
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
    # Get statistics about the college dataset
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
    # Submit feedback on a recommendation
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
    # Get all feedback
    return jsonify({
        'feedback': feedback_storage,
        'count': len(feedback_storage)
    })

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    # Enhanced chatbot with better NLP and conversational abilities
    try:
        user_message = request.json.get('message', '').lower().strip()
        conversation_history = request.json.get('history', [])
        current_data = request.json.get('current_data', {})
        
        # Initialize extracted data with existing known data
        # Filter out empty values
        initial_data = {k: v for k, v in current_data.items() if v and str(v).strip()}
        
        response = {
            'reply': '',
            'extracted_data': initial_data,
            'suggestions': [],
            'confidence': 0.0
        }
        
        # Greeting detection
        # Small talk and greetings
        if any(phrase in user_message for phrase in ['how are you', 'how r u', 'how are u', 'how do you do']):
            response['reply'] = "I'm doing great, thank you for asking! 😊 I'm ready to help you find your dream college. Tell me about your academic background!"
            response['suggestions'] = [
                "I completed Science with 3.5 GPA",
                "I want to study BBA in Kathmandu",
                "Show me colleges with low budget"
            ]
            return jsonify(response)
            
        greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'namaste', 'namaskar']
        if any(greeting in user_message.split() for greeting in greetings):
            response['reply'] = "Hello! 👋 I'm your college recommendation assistant. I'm here to help you find the perfect college for your bachelor's degree in Nepal. Let's start by getting to know you better!"
            response['suggestions'] = [
                "I completed Science stream with 3.5 GPA",
                "I want to study Computer Engineering",
                "I prefer colleges in Kathmandu",
                "My budget is medium range"
            ]
            return jsonify(response)
        
        # Help/confused detection - Only if no other info is extracted
        help_keywords = ['help', 'confused', 'don\'t know', 'not sure']
        if any(keyword in user_message for keyword in help_keywords) and not any(k in user_message for k in ['science', 'management', 'gpa', 'kathmandu', 'engineering']):
            response['reply'] = "No worries! I'll guide you step by step. I need to know:\n\n1️⃣ Your +2 stream (Science/Management/Commerce/Humanities)\n2️⃣ Your GPA (out of 4.0)\n3️⃣ What program you want to study\n4️⃣ Your preferred location\n5️⃣ Your budget range (low/medium/high)\n\nJust tell me naturally, like: 'I did Science with 3.2 GPA, want to study BBA in Pokhara with low budget'"
            response['suggestions'] = [
                "I completed Science with 3.5 GPA",
                "I want to study Engineering in Kathmandu"
            ]
            return jsonify(response)
        
        # Enhanced information extraction with context
        confidence_score = 0.0
        
        # Stream detection with variations
        stream_patterns = {
            'Science': ['science', 'sci', 'pcm', 'physics', 'chemistry', 'biology'],
            'Management': ['management', 'mgmt', 'business studies', 'accountancy'],
            'Commerce': ['commerce', 'com'],
            'Humanities': ['humanities', 'arts', 'social']
        }
        
        for stream, keywords in stream_patterns.items():
            if any(kw in user_message for kw in keywords):
                response['extracted_data']['stream'] = stream
                confidence_score += 0.2
                break
        
        # GPA extraction with multiple formats
        import re
        gpa_patterns = [
            r'gpa[:\s]+([0-4]\.?\d*)',
            r'cgpa[:\s]+([0-4]\.?\d*)',
            r'grade[:\s]+([0-4]\.?\d*)',
            r'(\d\.?\d*)\s*gpa',
            r'(\d\.?\d*)\s*cgpa',
            r'scored?\s+(\d\.?\d*)',
            r'got\s+(\d\.?\d*)'
        ]
        
        for pattern in gpa_patterns:
            match = re.search(pattern, user_message)
            if match:
                try:
                    gpa = float(match.group(1))
                    if 0 <= gpa <= 4:
                        response['extracted_data']['gpa'] = gpa
                        confidence_score += 0.2
                        break
                except:
                    continue
        
        # Location detection with more cities
        locations = {
            'Kathmandu': ['kathmandu', 'ktm', 'capital'],
            'Lalitpur': ['lalitpur', 'patan'],
            'Pokhara': ['pokhara'],
            'Biratnagar': ['biratnagar'],
            'Butwal': ['butwal'],
            'Chitwan': ['chitwan', 'bharatpur'],
            'Dharan': ['dharan'],
            'Morang': ['morang']
        }
        
        for city, keywords in locations.items():
            if any(kw in user_message for kw in keywords):
                response['extracted_data']['location'] = city
                confidence_score += 0.15
                break
        
        # Budget detection with more variations
        if any(word in user_message for word in ['low', 'cheap', 'affordable', 'budget', 'economical', 'inexpensive']):
            response['extracted_data']['budget_range'] = 'low'
            confidence_score += 0.15
        elif any(word in user_message for word in ['medium', 'moderate', 'average', 'mid', 'middle']):
            response['extracted_data']['budget_range'] = 'medium'
            confidence_score += 0.15
        elif any(word in user_message for word in ['high', 'expensive', 'premium', 'costly']):
            response['extracted_data']['budget_range'] = 'high'
            confidence_score += 0.15
        
        # Enhanced program detection
        program_keywords = {
            'Computer Engineering': [r'computer\s+engineering', r'\bce\b', r'comp\s+eng'],
            'Computer Science': [r'computer\s+science', r'\bcs\b', r'bsc\s+cs', r'bsc\s+computer'],
            'Civil Engineering': [r'civil\s+engineering', r'\bcivil\b', r'ce\s+civil'],
            'Electrical Engineering': [r'electrical', r'\bee\b', r'electrical\s+engineering'],
            'Mechanical Engineering': [r'mechanical', r'mechanical\s+engineering'],
            'BBA': [r'\bbba\b', r'bachelor\s+of\s+business', r'business\s+administration'],
            'BBS': [r'\bbbs\b', r'bachelor\s+of\s+business\s+studies'],
            'MBBS': [r'\bmbbs\b', r'medicine', r'medical', r'doctor'],
            'BCA': [r'\bbca\b', r'computer\s+application'],
            'Law': [r'\blaw\b', r'\bllb\b', r'legal'],
            'Architecture': [r'architecture', r'\barch\b'],
            'Pharmacy': [r'pharmacy', r'b\.pharm']
        }
        
        for program, patterns in program_keywords.items():
            for pattern in patterns:
                if re.search(pattern, user_message):
                    response['extracted_data']['preferred_program'] = program
                    confidence_score += 0.3
                    break
        
        # Interests and career goals extraction
        if any(word in user_message for word in ['interested in', 'like', 'enjoy', 'passion']):
            interests_match = re.search(r'(?:interested in|like|enjoy|passion for)\s+(\w+(?:\s+\w+)*)', user_message)
            if interests_match:
                response['extracted_data']['interests'] = interests_match.group(1).strip()
        
        if any(word in user_message for word in ['want to be', 'become', 'career', 'goal']):
            career_match = re.search(r'(?:want to be|become|career as|goal.*?)\s+(?:a\s+)?(\w+(?:\s+\w+)*)', user_message)
            if career_match:
                response['extracted_data']['career_goals'] = career_match.group(1).strip()
        
        response['confidence'] = min(confidence_score, 1.0)
        
        # Generate intelligent contextual reply
        if not response['extracted_data']:
            response['reply'] = "I'd love to help you find the perfect college! 🎓 Could you tell me a bit about yourself? For example:\n\n'I completed Science with 3.5 GPA and want to study Computer Engineering in Kathmandu with a medium budget.'\n\nJust describe your situation naturally, and I'll understand!"
            response['suggestions'] = [
                "I did Science with 3.5 GPA",
                "I want to study Engineering",
                "I prefer Kathmandu area",
                "My budget is low to medium"
            ]
        else:
            reply_parts = ["Great! I've noted the following:"]
            emojis = {'stream': '📚', 'gpa': '📊', 'preferred_program': '🎯', 'location': '📍', 'budget_range': '💰'}
            
            for key, value in response['extracted_data'].items():
                emoji = emojis.get(key, '✓')
                friendly_key = key.replace('_', ' ').title()
                reply_parts.append(f"{emoji} {friendly_key}: {value}")
            
            # Check what's missing
            required_fields = {
                'stream': 'your +2 stream (Science/Management/Commerce/Humanities)',
                'gpa': 'your GPA (out of 4.0)',
                'preferred_program': 'the program you want to study',
                'location': 'your preferred location'
            }
            
            missing = []
            for field, description in required_fields.items():
                if field not in response['extracted_data']:
                    missing.append(description)
            
            if missing:
                reply_parts.append(f"\n\nTo give you the best recommendations, I still need to know:")
                for i, item in enumerate(missing, 1):
                    reply_parts.append(f"{i}. {item}")
                
                response['suggestions'] = [
                    f"My {missing[0].split()[1] if len(missing[0].split()) > 1 else missing[0]} is...",
                    "Can you suggest some options?",
                    "I'm not sure about this"
                ]
            else:
                reply_parts.append("\n\n✨ Perfect! I have all the information I need. You can now click 'Get Recommendations' to see colleges that match your profile!")
                response['suggestions'] = [
                    "Show me the recommendations",
                    "Can you explain how matching works?",
                    "What if I want to change something?"
                ]
            
            response['reply'] = "\n".join(reply_parts)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': 'Error processing chatbot message',
            'message': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    # Health check endpoint
    return jsonify({
        'status': 'ok',
        'message': 'College Recommendation API is running',
        'colleges_count': len(recommender.colleges)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
