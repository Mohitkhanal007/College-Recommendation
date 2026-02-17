# College Recommendation System

A web application to help students find suitable colleges in Nepal after completing +2 level.

## About

This project helps students choose the right bachelor-level college based on their academic background and preferences. The system uses AI-based content filtering to match students with colleges and provides detailed recommendations with explanations.

## Features

- **Student Profile Input**: Enter stream, GPA, preferred program, interests, career goals, location, and budget
- **Smart Recommendations**: Get personalized college suggestions with match scores
- **Detailed Explanations**: See why each college was recommended and any trade-offs
- **Visual Analytics**: 
  - Bar charts showing similarity and confidence scores
  - Pie charts for budget and location distribution
  - Interactive charts with tooltips
- **College Comparison**: Compare up to 4 colleges side-by-side
- **Statistics Dashboard**: View overall statistics about available colleges
- **Filtering & Sorting**: Filter by location/budget and sort by various criteria
- **Export Data**: Download recommendations as CSV
- **Feedback System**: Rate recommendations to help improve the system
- **Chat Interface**: Alternative way to input information

## Technology Used

- **Frontend**: React.js with Recharts for visualizations
- **Backend**: Python Flask (REST API)
- **Data**: JSON format for college information
- **Recommendation**: AI-based filtering with weighted features

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs on http://localhost:5001

### Frontend
```bash
cd frontend
npm install
npm start
```
Frontend runs on http://localhost:3000

## Project Structure

```
individual/
├── backend/          # Flask API and AI recommendation engine
├── frontend/         # React application
└── data/            # College dataset
```

## How It Works

1. **Data Input**: Student fills out profile information
2. **Preprocessing**: System validates and normalizes the input data
3. **Matching**: Calculates similarity between student profile and colleges using weighted features
4. **Scoring**: Generates confidence scores based on feature matches
5. **Ranking**: Combines similarity and confidence to rank colleges
6. **Explanation**: Provides detailed reasons for each recommendation including trade-offs
7. **Visualization**: Displays results with interactive charts and graphs

## Dataset

Contains information about colleges in Nepal including:
- College name, location, and description
- Programs offered and required streams
- Minimum GPA requirements
- Budget range (low/medium/high)
- Career focus areas
- Student interests alignment
- Contact details and facilities

## Author

Computer Science Student  
Nepal
