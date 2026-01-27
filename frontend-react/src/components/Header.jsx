/**
 * Header Component
 * 
 * WHAT: Top navigation bar with user info and logout
 * WHY: Provides app branding and user controls
 * HOW: Displays user name and logout button
 */

import { getCurrentUser } from '../services/api';

function Header({ onLogout }) {
  const user = getCurrentUser();

  return (
    <header className="header">
      <div className="header-content">
        <h1>Chemical Equipment Visualizer</h1>
        <div className="header-actions">
          <span className="user-info">
            Welcome, {user?.username || 'User'}
          </span>
          <button className="btn btn-secondary" onClick={onLogout}>
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;
