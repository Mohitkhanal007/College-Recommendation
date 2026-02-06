import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell } from 'recharts';

const Statistics = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5001/api/statistics')
      .then(res => res.json())
      .then(data => {
        setStats(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching statistics:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading">Loading statistics...</div>;
  if (!stats) return <div className="error">Failed to load statistics</div>;

  const locationData = Object.entries(stats.by_location || {}).map(([name, value]) => ({
    name,
    value
  }));

  const budgetData = Object.entries(stats.by_budget || {}).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value
  }));

  const streamData = Object.entries(stats.by_stream || {}).map(([name, value]) => ({
    name,
    value
  }));

  const COLORS = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c'];

  return (
    <div className="statistics-section">
      <h2 className="section-title">Dataset Statistics</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Colleges</h3>
          <p className="stat-number">{stats.total_colleges}</p>
        </div>
        <div className="stat-card">
          <h3>Total Programs</h3>
          <p className="stat-number">{stats.programs_count}</p>
        </div>
        <div className="stat-card">
          <h3>Average Min GPA</h3>
          <p className="stat-number">{stats.average_min_gpa}</p>
        </div>
      </div>

      <div className="charts-container">
        <div className="chart-box">
          <h3>Colleges by Location</h3>
          <BarChart width={400} height={300} data={locationData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#3498db" />
          </BarChart>
        </div>

        <div className="chart-box">
          <h3>Colleges by Budget Range</h3>
          <PieChart width={400} height={300}>
            <Pie
              data={budgetData}
              cx={200}
              cy={150}
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {budgetData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </div>

        <div className="chart-box">
          <h3>Colleges by Stream</h3>
          <BarChart width={400} height={300} data={streamData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#2ecc71" />
          </BarChart>
        </div>
      </div>
    </div>
  );
};

export default Statistics;

