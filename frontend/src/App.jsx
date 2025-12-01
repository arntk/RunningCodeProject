import { useState, useEffect } from 'react'
import './App.css'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [data, setData] = useState([
    { name: '00:00', hr: 70, speed: 0 },
    { name: '00:05', hr: 85, speed: 5 },
    { name: '00:10', hr: 110, speed: 8 },
    { name: '00:15', hr: 130, speed: 9 },
    { name: '00:20', hr: 145, speed: 9.5 },
    { name: '00:25', hr: 150, speed: 9 },
    { name: '00:30', hr: 140, speed: 6 },
  ]);

  return (
    <div className="app-container">
      <header className="header">
        <h1>AeroFit AI</h1>
        <p>Real-time Workout Monitoring</p>
      </header>

      <main className="dashboard">
        <div className="card">
          <h2>Heart Rate & Speed</h2>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="hr" stroke="#ff0000" name="Heart Rate (bpm)" />
                <Line yAxisId="right" type="monotone" dataKey="speed" stroke="#8884d8" name="Speed (km/h)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <h2>AI Analysis</h2>
          <div className="ai-feedback">
            <p>Status: <strong>Analyzing...</strong></p>
            <p>Intensity: <span className="tag">Just Right</span></p>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
