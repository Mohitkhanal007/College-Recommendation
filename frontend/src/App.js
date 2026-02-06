import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import './styles/index.css';
import Statistics from './components/Statistics';
import Comparison from './components/Comparison';

const API_BASE_URL = 'http://localhost:5001/api';

function App() {
  // Form state
  const [formData, setFormData] = useState({
    stream: '',
    gpa: '',
    preferred_program: '',
    location: '',
    budget_range: ''
  });

  // Chatbot state
  const [chatMessages, setChatMessages] = useState([
    {
      type: 'bot',
      text: 'Hello! I can help you find suitable colleges. Tell me about yourself, or fill out the form on the left.'
    }
  ]);
  const [chatInput, setChatInput] = useState('');

  // Results state
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [allColleges, setAllColleges] = useState([]);
  const [activeTab, setActiveTab] = useState('recommendations'); // recommendations, comparison, statistics
  const [sortBy, setSortBy] = useState('similarity');
  const [filterLocation, setFilterLocation] = useState('all');
  const [filterBudget, setFilterBudget] = useState('all');

  // Available options from dataset
  const [availablePrograms, setAvailablePrograms] = useState([]);

  // Load all colleges on mount
  useEffect(() => {
    fetch(`${API_BASE_URL}/colleges`)
      .then(res => res.json())
      .then(data => {
        setAllColleges(data);
        
        // Extract unique programs, interests, and careers
        const programs = [...new Set(data.flatMap(c => c.programs))].sort();
        
        setAvailablePrograms(programs);
      })
      .catch(err => console.error('Error loading colleges:', err));
  }, []);

  // Handle form input change
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setRecommendations([]);

    try {
      const response = await fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get recommendations');
      }

      setRecommendations(data.recommendations || []);
      setActiveTab('recommendations');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle chatbot message send
  const handleChatSend = async () => {
    if (!chatInput.trim()) return;

    const userMessage = {
      type: 'user',
      text: chatInput
    };
    setChatMessages(prev => [...prev, userMessage]);
    const currentInput = chatInput;
    setChatInput('');

    try {
      const response = await fetch(`${API_BASE_URL}/chatbot`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: currentInput,
          history: chatMessages
        })
      });

      const data = await response.json();

      const botMessage = {
        type: 'bot',
        text: data.reply || 'I understand. Please continue filling the form.'
      };
      setChatMessages(prev => [...prev, botMessage]);

      if (data.extracted_data && Object.keys(data.extracted_data).length > 0) {
        setFormData(prev => ({
          ...prev,
          ...data.extracted_data
        }));
      }
    } catch (err) {
      const errorMessage = {
        type: 'bot',
        text: 'Sorry, I encountered an error. Please try again or fill the form directly.'
      };
      setChatMessages(prev => [...prev, errorMessage]);
    }
  };

  const handleChatKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleChatSend();
    }
  };

  // Submit feedback
  const handleFeedback = async (collegeId, rating) => {
    try {
      await fetch(`${API_BASE_URL}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          college_id: collegeId,
          rating: rating,
          timestamp: new Date().toISOString()
        })
      });
      alert('Thank you for your feedback!');
    } catch (err) {
      console.error('Error submitting feedback:', err);
    }
  };

  // Export recommendations
  const exportToCSV = () => {
    if (recommendations.length === 0) {
      alert('No recommendations to export');
      return;
    }

    const headers = ['Name', 'Location', 'Programs', 'Min GPA', 'Budget', 'Similarity Score', 'Confidence Score'];
    const rows = recommendations.map(c => [
      c.name,
      c.location,
      c.programs.join('; '),
      c.min_gpa,
      c.budget_range,
      c.similarity_score,
      c.confidence_score
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'college_recommendations.csv';
    a.click();
  };

  // Get unique locations from recommendations for filter dropdown
  const availableLocations = [...new Set(recommendations.map(r => r.location).filter(Boolean))];

  // Filter and sort recommendations
  const filteredRecommendations = recommendations
    .filter(rec => {
      // Location filter - use case-insensitive comparison
      if (filterLocation !== 'all') {
        const recLocation = (rec.location || '').toLowerCase().trim();
        const filterLoc = filterLocation.toLowerCase().trim();
        if (recLocation !== filterLoc) {
          return false;
        }
      }
      // Budget filter
      if (filterBudget !== 'all' && rec.budget_range !== filterBudget) {
        return false;
      }
      return true;
    })
    .sort((a, b) => {
      if (sortBy === 'similarity') return b.similarity_score - a.similarity_score;
      if (sortBy === 'confidence') return b.confidence_score - a.confidence_score;
      if (sortBy === 'gpa') return a.min_gpa - b.min_gpa;
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      return 0;
    });

  // Prepare chart data for feature scores
  const featureChartData = filteredRecommendations.length > 0 ? filteredRecommendations.map(rec => ({
    name: rec.name.substring(0, 15) + '...',
    similarity: (rec.similarity_score * 100).toFixed(1),
    confidence: (rec.confidence_score * 100).toFixed(1)
  })) : [];

  return (
    <div className="app">
      <div className="header">
        <h1>College Recommendation System for Bachelor-Level Students in Nepal</h1>
        <p>Advanced ML-based recommendation system with comparison and analytics</p>
      </div>

      <div className="main-container">
        {/* Form Section */}
        <div className="form-section">
          <h2 className="section-title">Student Information Form</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="stream">+2 Stream *</label>
              <select
                id="stream"
                name="stream"
                value={formData.stream}
                onChange={handleInputChange}
                required
              >
                <option value="">Select stream</option>
                <option value="Science">Science</option>
                <option value="Management">Management</option>
                <option value="Commerce">Commerce</option>
                <option value="Humanities">Humanities</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="gpa">GPA (out of 4.0) *</label>
              <input
                type="number"
                id="gpa"
                name="gpa"
                min="0"
                max="4"
                step="0.01"
                value={formData.gpa}
                onChange={handleInputChange}
                required
                placeholder="e.g., 3.5"
              />
            </div>

            <div className="form-group">
              <label htmlFor="preferred_program">Preferred Bachelor Program *</label>
              <select
                id="preferred_program"
                name="preferred_program"
                value={formData.preferred_program}
                onChange={handleInputChange}
                required
              >
                <option value="">Select preferred program</option>
                {availablePrograms.map(program => (
                  <option key={program} value={program}>{program}</option>
                ))}
              </select>
              <small className="form-hint">Select from available programs or type your own</small>
            </div>



            <div className="form-group">
              <label htmlFor="location">Preferred Location *</label>
              <select
                id="location"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                required
              >
                <option value="">Select location</option>
                <option value="Any">Any Location</option>
                {[...new Set(allColleges.map(c => c.location))].sort().map(location => (
                  <option key={location} value={location}>{location}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="budget_range">Budget Range *</label>
              <select
                id="budget_range"
                name="budget_range"
                value={formData.budget_range}
                onChange={handleInputChange}
                required
              >
                <option value="">Select budget range</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>



            <button
              type="submit"
              className="submit-btn"
              disabled={loading}
            >
              {loading ? 'Getting Recommendations...' : 'Get Recommendations'}
            </button>
          </form>
        </div>

        {/* Chatbot Section */}
        <div className="chatbot-section">
          <h2 className="section-title">Chat Assistant</h2>
          <div className="chatbot-container">
            <div className="chat-messages">
              {chatMessages.map((msg, idx) => (
                <div key={idx} className={`message ${msg.type}`}>
                  {msg.text}
                </div>
              ))}
            </div>
            <div className="chat-input-container">
              <input
                type="text"
                className="chat-input"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={handleChatKeyPress}
                placeholder="Type your message here..."
              />
              <button
                className="chat-send-btn"
                onClick={handleChatSend}
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      {recommendations.length > 0 && (
        <div className="tabs">
          <button 
            className={activeTab === 'recommendations' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('recommendations')}
          >
            Recommendations
          </button>
          <button 
            className={activeTab === 'comparison' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('comparison')}
          >
            Compare Colleges
          </button>
          <button 
            className={activeTab === 'statistics' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('statistics')}
          >
            Statistics
          </button>
        </div>
      )}

      {/* Loading and Error States */}
      {loading && (
        <div className="loading">
          Analyzing your profile and finding matching colleges...
        </div>
      )}

      {error && (
        <div className="error">
          Error: {error}
        </div>
      )}

      {/* Recommendations Tab */}
      {activeTab === 'recommendations' && filteredRecommendations.length > 0 && (
        <div className="results-section">
          <div className="results-header">
            <h2 className="section-title">
              Recommended Colleges ({filteredRecommendations.length})
            </h2>
            <div className="results-controls">
              <button className="export-btn" onClick={exportToCSV}>
                Export to CSV
              </button>
              <select 
                className="sort-select"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
              >
                <option value="similarity">Sort by Similarity</option>
                <option value="confidence">Sort by Confidence</option>
                <option value="gpa">Sort by GPA</option>
                <option value="name">Sort by Name</option>
              </select>
              <select 
                className="filter-select"
                value={filterLocation}
                onChange={(e) => setFilterLocation(e.target.value)}
              >
                <option value="all">All Locations</option>
                {availableLocations.map(loc => (
                  <option key={loc} value={loc.toLowerCase()}>{loc}</option>
                ))}
              </select>
              <select 
                className="filter-select"
                value={filterBudget}
                onChange={(e) => setFilterBudget(e.target.value)}
              >
                <option value="all">All Budgets</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>

          {/* Chart Visualization */}
          {featureChartData.length > 0 && (
            <div className="chart-section">
              <h3>Recommendation Scores Visualization</h3>
              <BarChart width={800} height={300} data={featureChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="similarity" fill="#3498db" name="Similarity %" />
                <Bar dataKey="confidence" fill="#2ecc71" name="Confidence %" />
              </BarChart>
            </div>
          )}

          {filteredRecommendations.length === 0 && recommendations.length > 0 ? (
            <div className="no-results">
              <h3>No colleges match your current filters</h3>
              <p>
                Try adjusting your filters or{' '}
                <button 
                  className="reset-filters-btn"
                  onClick={() => {
                    setFilterLocation('all');
                    setFilterBudget('all');
                  }}
                >
                  Reset Filters
                </button>
              </p>
              <div className="filter-info">
                <p>Total recommendations available: {recommendations.length}</p>
                <p>Available locations in recommendations: {availableLocations.join(', ')}</p>
              </div>
            </div>
          ) : (
            <>
              {recommendations.length > filteredRecommendations.length && (
                <div className="filter-info">
                  <p>Showing {filteredRecommendations.length} of {recommendations.length} recommendations</p>
                </div>
              )}
              {filteredRecommendations.map((college, idx) => (
            <div key={college.id || idx} className="recommendation-card">
              <div className="card-header">
                <div className="college-name">{college.name}</div>
                <div className="score-badges">
                  <span className="similarity-score">
                    Match: {(college.similarity_score * 100).toFixed(1)}%
                  </span>
                  <span className="confidence-score">
                    Confidence: {(college.confidence_score * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
              <div className="college-location">📍 {college.location}</div>
              
              <div className="college-details">
                <div className="detail-item">
                  <strong>Programs:</strong>
                  <div className="program-tags">
                    {college.programs.map((prog, pidx) => (
                      <span key={pidx} className="program-tag">{prog}</span>
                    ))}
                  </div>
                </div>
                <div className="detail-item">
                  <strong>Minimum GPA:</strong> {college.min_gpa}
                </div>
                <div className="detail-item">
                  <strong>Budget Range:</strong> {college.budget_range}
                </div>
                {college.type && (
                  <div className="detail-item">
                    <strong>Type:</strong> {college.type}
                  </div>
                )}
                {college.website && (
                  <div className="detail-item">
                    <strong>Website:</strong> <a href={college.website} target="_blank" rel="noopener noreferrer">{college.website}</a>
                  </div>
                )}
              </div>

              {/* Feature Match Breakdown */}
              {college.feature_scores && (
                <div className="feature-breakdown">
                  <h4>Feature Match Breakdown:</h4>
                  <div className="feature-scores">
                    <div className="feature-item">
                      <span>Program Match:</span>
                      <span className={college.feature_scores.program_match > 0 ? 'match-yes' : 'match-no'}>
                        {college.feature_scores.program_match > 0 ? '✓' : '✗'}
                      </span>
                    </div>
                    <div className="feature-item">
                      <span>Stream Match:</span>
                      <span className={college.feature_scores.stream_match > 0 ? 'match-yes' : 'match-no'}>
                        {college.feature_scores.stream_match > 0 ? '✓' : '✗'}
                      </span>
                    </div>
                    <div className="feature-item">
                      <span>Location Match:</span>
                      <span className={college.feature_scores.location_match > 0 ? 'match-yes' : 'match-no'}>
                        {college.feature_scores.location_match > 0 ? '✓' : '✗'}
                      </span>
                    </div>
                    <div className="feature-item">
                      <span>Budget Match:</span>
                      <span className={college.feature_scores.budget_match > 0 ? 'match-yes' : 'match-no'}>
                        {college.feature_scores.budget_match > 0 ? '✓' : '✗'}
                      </span>
                    </div>
                  </div>
                </div>
              )}

              <div className="explanation">
                <strong>Why this college?</strong> {college.explanation}
              </div>

              {/* Feedback Section */}
              <div className="feedback-section">
                <p>Was this recommendation helpful?</p>
                <div className="feedback-buttons">
                  {[1, 2, 3, 4, 5].map(rating => (
                    <button
                      key={rating}
                      className="feedback-btn"
                      onClick={() => handleFeedback(college.id, rating)}
                    >
                      {rating} ⭐
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ))}
            </>
          )}
        </div>
      )}

      {/* Comparison Tab */}
      {activeTab === 'comparison' && (
        <Comparison colleges={recommendations} allColleges={allColleges} />
      )}

      {/* Statistics Tab */}
      {activeTab === 'statistics' && (
        <Statistics />
      )}
    </div>
  );
}

export default App;
