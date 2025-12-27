import React, { useState } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import './App.css';
import ReactMarkdown from 'react-markdown';

ChartJS.register(ArcElement, Tooltip, Legend);
const API_URL = process.env.REACT_APP_API_URL || '';
function App() {
  const [artist, setArtist] = useState('');
  const [track, setTrack] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showPrompt, setShowPrompt] = useState(false);
  const [showLyrics, setShowLyrics] = useState(false);
  const [prompt, setPrompt] = useState('');

  const handleAnalyze = async () => {
    if (!artist || !track) {
      setError('Please enter both artist and track');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // === Stage 1: Fetch Lyrics ===
      setLoadingStage('fetching');
      
      const lyricsResponse = await fetch(`${API_URL}/api/lyrics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ artist, track })
      });

      const lyricsData = await lyricsResponse.json();

      if (!lyricsResponse.ok) {
        setError(lyricsData.error || 'Failed to fetch lyrics');
        return;
      }

      // === Stage 2: Analyze Lyrics ===
      setLoadingStage('analyzing');

      const analysisResponse = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ artist, lyrics: lyricsData.lyrics })
      });

      const analysisData = await analysisResponse.json();
      

      if (!analysisResponse.ok) {
        setError(analysisData.error || 'Analysis failed');
        return;
      }
      try {
        const promptResponse = await fetch(`${API_URL}/api/prompt`);
        const promptData = await promptResponse.json();
        setPrompt(promptData.prompt);
      } catch (err) {
        console.log('Could not load prompt');
      }
      // Combine results
      setResult({
        lyrics: lyricsData,
        analysis: analysisData
      });

    } catch (err) {
      setError('Failed to connect to server. Is Flask running?');
    } finally {
      setLoading(false);
      setLoadingStage('');
    }
  };

  const getPieData = () => {
    if (!result) return null;
    
    const breakdown = result.analysis.quantitative_breakdown;
    
    return {
      labels: [
        'Permissible',
        'Tawheed Violation',
        'Oppression',
        'Distortion',
        'Indecency',
        'Rights Violation'
      ],
      datasets: [{
        data: [
          breakdown.permissible_content_percent,
          breakdown.violation_of_tawheed_percent,
          breakdown.promotion_of_oppression_percent,
          breakdown.distortion_of_revelation_percent,
          breakdown.promotion_of_indecency_percent,
          breakdown.violation_of_rights_percent
        ],
        backgroundColor: [
          '#98D8AA', // Pastel green
          '#FF6B6B', // Pastel red
          '#FFB347', // Pastel orange
          '#C3AED6', // Pastel purple
          '#FFB6C1', // Pastel pink
          '#FDFD96'  // Pastel yellow
        ],
        borderColor: '#2d2d2d',
        borderWidth: 2
      }]
    };
  };

  const pieOptions = {
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#E8D5B7',
          font: { family: 'monospace', size: 10 },
          padding: 10
        }
      }
    }
  };

  return (
    <div className="App">
      <div className="scanlines"></div>
      
      <div className="container">
        {/* Header with Logo */}
        <div className="header">
          <div className="logo">
            <img src="/canilisten.svg" alt="Can I Listen?" />
          </div>
          <h1 className="title">CAN I LISTEN?</h1>
          <p className="subtitle">Islamic Lyric Analyzer v1.0</p>
          <div className="marquee">
            <span>DISCLAIMER : This is a project made as a hobby and is in no way authoritative or final and has no scholarly backing.</span>
          </div>
        </div>

        {/* Input Section */}
        <div className="box">
          <div className="box-title">[ ENTER SONG INFO ]</div>
          <div className="input-group">
            <label>&gt; ARTIST_NAME:</label>
            <input
              type="text"
              value={artist}
              onChange={(e) => setArtist(e.target.value)}
              placeholder="type here..."
            />
          </div>
          <div className="input-group">
            <label>&gt; TRACK_NAME:</label>
            <input
              type="text"
              value={track}
              onChange={(e) => setTrack(e.target.value)}
              placeholder="type here..."
            />
          </div>
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? '[ PROCESSING... ]' : '[ ANALYZE ]'}
          </button>
        </div>

        {/* Loading Bar */}
        {loading && (
          <div className="box loading-box">
            <div className="loading-stage">
              <span className={loadingStage === 'fetching' ? 'active' : 'done'}>
                {loadingStage === 'fetching' ? '▶' : '✓'} FETCHING LYRICS
              </span>
              <span className={loadingStage === 'analyzing' ? 'active' : ''}>
                {loadingStage === 'analyzing' ? '▶' : '○'} ANALYZING WITH AI
              </span>
            </div>
            <div className="loading-bar">
              <div className={`loading-fill ${loadingStage}`}></div>
            </div>
            <div className="loading-dots">
              <span>.</span><span>.</span><span>.</span>
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="box error-box">
            <div className="box-title">[ ERROR ]</div>
            <p>!! {error} !!</p>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="box result-box">
            <div className="box-title">[ RESULTS ]</div>
            
            <div className="result-header">
              <p>ARTIST: {result.lyrics.artist}</p>
              <p>TRACK: {result.lyrics.title}</p>
              <p>SOURCE: {result.lyrics.source}</p>
            </div>

            <div className="divider">═══════════════════════════════</div>

            <div className="score-box">
              <div className="score-label">PERMISSIBILITY SCORE</div>
              <div className="score-value">{result.analysis.acceptance_score}/100</div>
              <div className="score-bar">
                <div 
                  className="score-fill" 
                  style={{width: `${result.analysis.acceptance_score}%`}}
                ></div>
              </div>
            </div>

            <div className="divider">═══════════════════════════════</div>

            <div className="chart-box">
              <div className="section-title">&lt; BREAKDOWN &gt;</div>
              <div className="pie-wrapper">
                <Pie data={getPieData()} options={pieOptions} />
              </div>
            </div>

            <div className="divider">═══════════════════════════════</div>

            <div className="text-box">
              <div className="section-title">&lt; ANALYSIS &gt;</div>
              <p>{result.analysis.lyrical_analysis}</p>
            </div>

            <div className="divider">═══════════════════════════════</div>

            <div className="text-box">
              <div className="section-title">&lt; VERDICT &gt;</div>
              <p>{result.analysis.artist_verdict}</p>
            </div>
            

            <div className="divider">═══════════════════════════════</div>

            <div className="collapsible">
              <button 
                className="collapse-btn"
                onClick={() => setShowLyrics(!showLyrics)}
              >
                {showLyrics ? '▼' : '▶'} VIEW LYRICS
              </button>
              {showLyrics && (
                <div className="collapse-content">
                  <ReactMarkdown>{result.lyrics.lyrics}</ReactMarkdown>
                </div>
              )}
            </div>

            <div className="collapsible">
              <button 
                className="collapse-btn"
                onClick={() => setShowPrompt(!showPrompt)}
              >
                {showPrompt ? '▼' : '▶'} VIEW ANALYSIS PROMPT
              </button>
              {showPrompt && (
                <div className="collapse-content">
                  <ReactMarkdown>{prompt}</ReactMarkdown>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="footer">
          <div className="divider">═══════════════════════════════</div>
          <p>Developed by <a href="https://github.com/SalarMohammadUzair" target="_blank" rel="noreferrer">smbleh</a></p>
          <p className="contact">For critique, please email at <a href="mailto:smbleh@proton.me">smbleh@proton.me</a></p>
          <p className="copy">© 2025 In service of the khilafat</p>
        </div>
      </div>
    </div>
  );
}

export default App;