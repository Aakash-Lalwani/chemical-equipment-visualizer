/**
 * Main App Component - IMPROVED UI/UX
 * 
 * DESIGN CHANGES:
 * - Professional header with branding
 * - Clean tab navigation  
 * - Consistent layout structure
 * - Loading states with spinners
 * - Better spacing and visual hierarchy
 * 
 * WHY: Makes the app feel professional and easy to navigate
 */

import { useState, useEffect } from 'react';
import './styles/global.css';
import './App-new.css';
import Login from './components/Login';
import CSVUpload from './components/CSVUpload';
import Dashboard from './components/Dashboard';
import History from './components/History';
import { isAuthenticated, logout, getUploadHistory, getDatasetSummary } from './services/api';

function App() {
  // State management
  const [authenticated, setAuthenticated] = useState(false);
  const [currentView, setCurrentView] = useState('dashboard'); // Start with dashboard
  const [latestDataset, setLatestDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [username, setUsername] = useState('User');

  // Check authentication on app load
  useEffect(() => {
    const checkAuth = async () => {
      const isAuth = isAuthenticated();
      setAuthenticated(isAuth);
      
      if (isAuth) {
        // Get username from localStorage
        const storedUsername = localStorage.getItem('username') || 'User';
        setUsername(storedUsername);
        
        // Load latest dataset
        await loadLatestDataset();
      }
      
      setLoading(false);
    };
    
    checkAuth();
  }, []);

  // Load the most recent dataset
  const loadLatestDataset = async () => {
    try {
      const history = await getUploadHistory();
      if (history.length > 0) {
        const latest = await getDatasetSummary(history[0].id);
        setLatestDataset(latest);
        setCurrentView('dashboard');
      }
    } catch (err) {
      console.error('Failed to load latest dataset:', err);
    }
  };

  // Handle successful login
  const handleLoginSuccess = (loginUsername) => {
    setAuthenticated(true);
    setUsername(loginUsername || 'User');
    localStorage.setItem('username', loginUsername || 'User');
    loadLatestDataset();
  };

  // Handle logout
  const handleLogout = () => {
    logout();
    setAuthenticated(false);
    setLatestDataset(null);
    setCurrentView('dashboard');
    setUsername('User');
  };

  // Handle successful CSV upload
  const handleUploadSuccess = async (dataset) => {
    // Reload the dataset with full details
    const fullDataset = await getDatasetSummary(dataset.id);
    setLatestDataset(fullDataset);
    setCurrentView('dashboard');
  };

  // Handle dataset selection from history
  const handleDatasetSelect = (dataset) => {
    setLatestDataset(dataset);
    setCurrentView('dashboard');
  };

  // Loading state
  if (loading) {
    return (
      <div className="loading-overlay">
        <div className="spinner"></div>
        <p className="loading-text">Loading application...</p>
      </div>
    );
  }

  // Not authenticated - show login
  if (!authenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  // Authenticated - show main app
  return (
    <div className="app">
      {/* HEADER - Fixed top bar */}
      <header className="app-header">
        <div className="header-content">
          <div className="header-left">
            <div className="app-logo">
              <span className="logo-icon">⚗️</span>
              <span className="logo-text">Chemical Equipment Visualizer</span>
            </div>
          </div>
          
          <div className="header-right">
            <div className="user-info">
              <span className="user-icon">👤</span>
              <span className="user-name">{username}</span>
            </div>
            <button className="btn btn-secondary btn-sm" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* NAVIGATION - Tab bar */}
      <nav className="app-nav">
        <div className="nav-container">
          <button
            className={`nav-tab ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentView('dashboard')}
          >
            <span className="nav-icon">📊</span>
            <span>Dashboard</span>
          </button>
          
          <button
            className={`nav-tab ${currentView === 'upload' ? 'active' : ''}`}
            onClick={() => setCurrentView('upload')}
          >
            <span className="nav-icon">📤</span>
            <span>Upload Data</span>
          </button>
          
          <button
            className={`nav-tab ${currentView === 'history' ? 'active' : ''}`}
            onClick={() => setCurrentView('history')}
          >
            <span className="nav-icon">📜</span>
            <span>History</span>
          </button>
        </div>
      </nav>

      {/* MAIN CONTENT AREA */}
      <main className="app-main">
        <div className="container">
          {/* Dashboard View */}
          {currentView === 'dashboard' && (
            <Dashboard 
              latestDataset={latestDataset} 
              onRefresh={loadLatestDataset}
              onNavigateToUpload={() => setCurrentView('upload')}
            />
          )}

          {/* Upload View */}
          {currentView === 'upload' && (
            <CSVUpload onUploadSuccess={handleUploadSuccess} />
          )}

          {/* History View */}
          {currentView === 'history' && (
            <History onDatasetSelect={handleDatasetSelect} />
          )}
        </div>
      </main>

      {/* FOOTER (Optional) */}
      <footer className="app-footer">
        <div className="container">
          <p className="footer-text">
            Chemical Equipment Parameter Visualizer &copy; 2026 | FOSSE Project
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
