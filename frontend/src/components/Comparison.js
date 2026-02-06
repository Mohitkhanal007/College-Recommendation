import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const Comparison = ({ colleges, allColleges }) => {
  const [selectedIds, setSelectedIds] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCompare = async () => {
    if (selectedIds.length < 2) {
      alert('Please select at least 2 colleges to compare');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5001/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ college_ids: selectedIds })
      });
      const data = await response.json();
      setComparisonData(data);
    } catch (err) {
      console.error('Error comparing colleges:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleSelection = (id) => {
    setSelectedIds(prev => 
      prev.includes(id) 
        ? prev.filter(i => i !== id)
        : [...prev, id].slice(0, 4) // Max 4 colleges
    );
  };

  const selectedColleges = allColleges.filter(c => selectedIds.includes(c.id));

  const chartData = selectedColleges.map(college => ({
    name: college.name.substring(0, 20) + '...',
    'Min GPA': college.min_gpa,
    'Programs Count': college.programs.length
  }));

  return (
    <div className="comparison-section">
      <h2 className="section-title">Compare Colleges</h2>
      
      <div className="comparison-selector">
        <p>Select up to 4 colleges to compare:</p>
        <div className="college-checkboxes">
          {allColleges.map(college => (
            <label key={college.id} className="checkbox-label">
              <input
                type="checkbox"
                checked={selectedIds.includes(college.id)}
                onChange={() => toggleSelection(college.id)}
                disabled={!selectedIds.includes(college.id) && selectedIds.length >= 4}
              />
              {college.name}
            </label>
          ))}
        </div>
        <button className="compare-btn" onClick={handleCompare} disabled={selectedIds.length < 2 || loading}>
          {loading ? 'Comparing...' : 'Compare Selected Colleges'}
        </button>
      </div>

      {comparisonData && selectedColleges.length > 0 && (
        <div className="comparison-results">
          <div className="comparison-table">
            <table>
              <thead>
                <tr>
                  <th>Feature</th>
                  {selectedColleges.map(college => (
                    <th key={college.id}>{college.name}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Location</td>
                  {selectedColleges.map(college => (
                    <td key={college.id}>{college.location}</td>
                  ))}
                </tr>
                <tr>
                  <td>Min GPA</td>
                  {selectedColleges.map(college => (
                    <td key={college.id}>{college.min_gpa}</td>
                  ))}
                </tr>
                <tr>
                  <td>Budget Range</td>
                  {selectedColleges.map(college => (
                    <td key={college.id}>{college.budget_range}</td>
                  ))}
                </tr>
                <tr>
                  <td>Programs</td>
                  {selectedColleges.map(college => (
                    <td key={college.id}>{college.programs.join(', ')}</td>
                  ))}
                </tr>
                <tr>
                  <td>Type</td>
                  {selectedColleges.map(college => (
                    <td key={college.id}>{college.type || 'N/A'}</td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>

          <div className="comparison-chart">
            <h3>Visual Comparison</h3>
            <BarChart width={600} height={300} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="Min GPA" fill="#3498db" />
              <Bar dataKey="Programs Count" fill="#2ecc71" />
            </BarChart>
          </div>
        </div>
      )}
    </div>
  );
};

export default Comparison;

