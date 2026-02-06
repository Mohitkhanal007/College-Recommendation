# College Recommendation System for Bachelor-Level Students in Nepal Using Machine Learning

## Project Overview

This project is an advanced web-based college recommendation system designed to help students in Nepal who have completed their +2 level education to find suitable bachelor-level colleges. The system uses enhanced machine learning techniques with weighted feature matching, confidence scoring, and comprehensive analytics to provide personalized college recommendations.

## Problem Statement

After completing +2 education in Nepal, students face significant challenges in choosing the right bachelor-level college. They often have to manually search through multiple websites and college brochures without any personalized guidance. This project aims to solve this problem by providing an intelligent, automated recommendation system that matches students with colleges based on their academic background, preferences, and career goals.

## Objectives

1. To develop an advanced machine learning-based recommendation system for college selection
2. To help students find colleges that match their academic profile and preferences
3. To provide detailed explanations and feature breakdowns for each recommendation
4. To enable college comparison and statistical analysis
5. To create a user-friendly interface with both form-based and chatbot-based input methods
6. To implement feedback mechanisms for continuous improvement

## Technology Stack

- **Frontend**: React.js with Recharts for data visualization
- **Backend**: Python Flask (REST API)
- **Machine Learning**: Enhanced content-based filtering with weighted features and cosine similarity
- **Data Format**: JSON
- **Visualization**: Recharts library for interactive charts

## Machine Learning Approach

The system uses an **enhanced content-based filtering** approach with the following advanced features:

### 1. Weighted Feature Vectors
- Different features are assigned different weights based on importance:
  - Program match: 2.0 (most important)
  - Stream requirement: 1.5
  - Career alignment: 1.3
  - Location preference: 1.2
  - Budget range: 1.1
  - Interests: 1.0
  - GPA: 0.8

### 2. Weighted Cosine Similarity
- Uses weighted cosine similarity instead of standard cosine similarity
- Formula: `similarity = (weighted_A · weighted_B) / (||weighted_A|| × ||weighted_B||)`
- Ensures important features contribute more to the final score

### 3. Confidence Scoring
- Calculates confidence score based on:
  - Base similarity score
  - Critical feature matches (program, stream, location)
  - Provides reliability indicator for each recommendation

### 4. Feature Match Analysis
- Detailed breakdown of which features matched:
  - Program match
  - Stream match
  - Location match
  - Budget match
  - Career goal match
  - Interest matches
  - GPA eligibility

### 5. Combined Scoring
- Final score = similarity × confidence
- Ensures recommendations are both relevant and reliable

## Project Structure

```
individual/
├── backend/
│   ├── app.py                 # Enhanced Flask REST API
│   ├── ml_recommender.py      # Advanced ML recommendation module
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js             # Main React component with all features
│   │   ├── index.js
│   │   ├── components/
│   │   │   ├── Statistics.js  # Statistics dashboard component
│   │   │   └── Comparison.js  # College comparison component
│   │   └── styles/
│   │       └── index.css      # Enhanced styling
│   └── package.json
├── data/
│   └── colleges.json          # Expanded college dataset (20 colleges)
└── README.md
```

## Dataset

The project includes an expanded dataset of **20 colleges** in Nepal with comprehensive information:
- College name and description
- Location
- Programs offered
- Required streams
- Minimum GPA requirement
- Budget range (low/medium/high)
- Career focus areas
- Student interests
- Additional fields: website, contact, facilities, established year, type (Government/Private)

## Features

### Core Features

1. **Student Profile Input**: Users can provide:
   - +2 stream (Science, Management, Commerce, Humanities)
   - GPA (out of 4.0)
   - Preferred bachelor program
   - Interests (comma-separated)
   - Preferred location
   - Budget range
   - Career goal

2. **Advanced Recommendation System**: Returns top N colleges with:
   - Similarity score (weighted)
   - Confidence score
   - Combined score
   - Detailed feature match breakdown
   - Comprehensive explanations

### Advanced Features

3. **College Comparison**:
   - Compare up to 4 colleges side by side
   - Visual comparison charts
   - Feature-by-feature comparison table
   - Common features identification

4. **Data Visualization**:
   - Bar charts for recommendation scores
   - Pie charts for budget distribution
   - Bar charts for location and stream distribution
   - Interactive charts using Recharts library

5. **Statistics Dashboard**:
   - Total colleges count
   - Total programs count
   - Average minimum GPA
   - Distribution by location
   - Distribution by budget range
   - Distribution by stream

6. **Filtering and Sorting**:
   - Filter by location
   - Filter by budget range
   - Sort by similarity score
   - Sort by confidence score
   - Sort by GPA requirement
   - Sort by name

7. **Enhanced Chatbot**:
   - Context-aware conversations
   - Better natural language understanding
   - Suggestion prompts
   - Auto-fill form from conversation

8. **User Feedback System**:
   - Rate recommendations (1-5 stars)
   - Feedback storage for analytics
   - Helps improve future recommendations

9. **Export Functionality**:
   - Export recommendations to CSV
   - Includes all relevant college information
   - Easy to share and analyze

10. **Enhanced UI/UX**:
    - Modern gradient designs
    - Smooth animations and transitions
    - Responsive design for mobile devices
    - Tab-based navigation
    - Interactive elements

## API Endpoints

### GET `/api/colleges`
Get list of all colleges

### GET `/api/colleges/<id>`
Get a specific college by ID

### POST `/api/recommend`
Get college recommendations based on user profile

### POST `/api/compare`
Compare multiple colleges

### GET `/api/statistics`
Get statistics about the dataset

### POST `/api/feedback`
Submit feedback on a recommendation

### GET `/api/feedback`
Get all feedback (for analytics)

### POST `/api/chatbot`
Enhanced chatbot endpoint with context awareness

### GET `/api/health`
Health check endpoint

## Installation and Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:
   ```bash
   python app.py
   ```
   The API will run on `http://localhost:5001`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```
   The frontend will run on `http://localhost:3000`

## Usage

1. Open the web application in your browser
2. Fill out the student information form OR use the chatbot to provide information
3. Click "Get Recommendations"
4. Review the recommended colleges with detailed scores and explanations
5. Use filters and sorting to refine results
6. Compare colleges side by side
7. View statistics and analytics
8. Export results to CSV
9. Provide feedback on recommendations

## Advanced ML Features Explained

### Feature Weighting
The system uses different weights for different features because not all features are equally important. For example, matching the preferred program is more critical than matching interests, so program matches get a higher weight (2.0) compared to interest matches (1.0).

### Confidence Scoring
Confidence score indicates how reliable a recommendation is. A high confidence score means the recommendation is based on strong feature matches, while a low confidence score suggests the match might be weaker.

### Combined Scoring
The final recommendation ranking uses a combined score that multiplies similarity and confidence. This ensures that recommendations are both relevant (high similarity) and reliable (high confidence).

## Limitations and Future Work

### Current Limitations:
- Dataset size (20 colleges) - can be expanded
- Rule-based chatbot (not using advanced NLP)
- No user authentication or saved profiles
- Feedback not used to improve recommendations yet

### Future Improvements:
- Expand dataset to include more colleges (50+)
- Implement collaborative filtering alongside content-based
- Add machine learning model training on user feedback
- Implement more sophisticated NLP for chatbot
- Add college reviews and ratings from students
- Implement user accounts with saved preferences
- Add recommendation history
- Implement A/B testing for recommendation algorithms
- Add more visualization options
- Implement recommendation explanation using SHAP values

## Academic Contribution

This project demonstrates:
1. **Advanced ML Techniques**: Weighted feature vectors, confidence scoring, feature analysis
2. **Full-Stack Development**: React frontend, Flask backend, RESTful API design
3. **Data Visualization**: Interactive charts and analytics
4. **User Experience Design**: Intuitive interface with multiple interaction methods
5. **Software Engineering**: Modular code structure, component-based architecture

## Conclusion

This project demonstrates a comprehensive application of machine learning for solving a real-world problem faced by students in Nepal. The enhanced content-based filtering approach with weighted features and confidence scoring provides transparent, explainable, and reliable recommendations. The system successfully matches students with colleges based on multiple criteria, provides detailed analysis, enables comparison, and offers comprehensive analytics - making it suitable for final semester academic evaluation.

## Author

Final Year Computer Science Student
[Your University Name]
Nepal

## References

- Cosine Similarity: https://en.wikipedia.org/wiki/Cosine_similarity
- Content-Based Filtering: Introduction to Information Retrieval (Textbook)
- Weighted Similarity Metrics: Information Retrieval and Web Search
- Flask Documentation: https://flask.palletsprojects.com/
- React Documentation: https://react.dev/
- Recharts Documentation: https://recharts.org/
