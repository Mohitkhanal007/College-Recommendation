# Quick Setup Guide

## Prerequisites
- Python 3.7 or higher
- Node.js 14 or higher
- npm or yarn

## Step-by-Step Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py
```

The backend API will be available at `http://localhost:5000`

### 2. Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

The frontend will open automatically at `http://localhost:3000`

### 3. Using the Application

1. Fill out the student information form with:
   - Your +2 stream
   - GPA
   - Preferred program
   - Interests
   - Location preference
   - Budget range
   - Career goal

2. OR use the chatbot to provide information naturally

3. Click "Get Recommendations" to see matching colleges

## Troubleshooting

- If backend fails to start, check if port 5000 is already in use
- If frontend fails to connect to backend, ensure backend is running first
- Make sure all dependencies are installed correctly

