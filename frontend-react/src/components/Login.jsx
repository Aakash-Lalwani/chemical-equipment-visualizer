/**
 * Login Component - PHASE 2 IMPROVED
 * 
 * UX IMPROVEMENTS:
 * ✅ Clean card layout with proper spacing
 * ✅ Password visibility toggle (show/hide)
 * ✅ Better loading states with spinner
 * ✅ Welcoming design with icon
 * ✅ Clear error messages with icons
 * ✅ Professional color scheme
 */

import { useState } from 'react';
import { login, register } from '../services/api';

function Login({ onLoginSuccess }) {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isRegistering) {
        await register(username, email, password);
      } else {
        await login(username, password);
      }
      
      // Pass username to parent for display
      onLoginSuccess(username);
    } catch (err) {
      setError(
        err.response?.data?.error || 
        'An error occurred. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setIsRegistering(!isRegistering);
    setError('');
    setEmail('');
    setPassword('');
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: 'var(--spacing-lg)'
    }}>
      <div className="card" style={{ 
        maxWidth: '440px', 
        width: '100%',
        boxShadow: 'var(--shadow-lg)'
      }}>
        {/* Welcome Header */}
        <div style={{ textAlign: 'center', marginBottom: 'var(--spacing-xl)' }}>
          <div style={{ 
            fontSize: '48px', 
            marginBottom: 'var(--spacing-sm)' 
          }}>
            ⚗️
          </div>
          <h2 style={{ 
            fontSize: 'var(--font-size-xl)', 
            fontWeight: '700',
            color: 'var(--color-text)',
            marginBottom: 'var(--spacing-xs)'
          }}>
            {isRegistering ? 'Create Account' : 'Welcome Back'}
          </h2>
          <p style={{ 
            color: 'var(--color-text-secondary)',
            fontSize: 'var(--font-size-sm)'
          }}>
            {isRegistering 
              ? 'Join us to visualize your equipment data' 
              : 'Sign in to continue to your dashboard'}
          </p>
        </div>
        
        {/* Error Alert */}
        {error && (
          <div className="alert alert-error" style={{ marginBottom: 'var(--spacing-md)' }}>
            <span style={{ marginRight: 'var(--spacing-xs)' }}>⚠️</span>
            {error}
          </div>
        )}

        {/* Login/Register Form */}
        <form onSubmit={handleSubmit}>
          {/* Username Field */}
          <div style={{ marginBottom: 'var(--spacing-md)' }}>
            <label className="label">
              👤 Username
            </label>
            <input
              type="text"
              className="input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder="Enter your username"
              disabled={loading}
            />
          </div>

          {/* Email Field (Register only) */}
          {isRegistering && (
            <div style={{ marginBottom: 'var(--spacing-md)' }}>
              <label className="label">
                📧 Email (Optional)
              </label>
              <input
                type="email"
                className="input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your.email@example.com"
                disabled={loading}
              />
            </div>
          )}

          {/* Password Field with Toggle */}
          <div style={{ marginBottom: 'var(--spacing-lg)' }}>
            <label className="label">
              🔒 Password
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPassword ? 'text' : 'password'}
                className="input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Enter your password"
                disabled={loading}
                style={{ paddingRight: '40px' }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: 'absolute',
                  right: '12px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '18px',
                  padding: '4px'
                }}
                disabled={loading}
              >
                {showPassword ? '🙈' : '👁️'}
              </button>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="btn btn-primary btn-lg"
            style={{ width: '100%' }}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner" style={{ 
                  width: '16px', 
                  height: '16px', 
                  marginRight: 'var(--spacing-sm)' 
                }}></span>
                {isRegistering ? 'Creating Account...' : 'Signing In...'}
              </>
            ) : (
              isRegistering ? '✨ Create Account' : '🚀 Sign In'
            )}
          </button>
        </form>

        {/* Toggle Mode */}
        <div style={{ 
          textAlign: 'center', 
          marginTop: 'var(--spacing-lg)',
          paddingTop: 'var(--spacing-lg)',
          borderTop: '1px solid var(--color-border)'
        }}>
          <p style={{ 
            color: 'var(--color-text-secondary)',
            fontSize: 'var(--font-size-sm)'
          }}>
            {isRegistering ? 'Already have an account?' : "Don't have an account?"}{' '}
            <button
              type="button"
              onClick={toggleMode}
              disabled={loading}
              style={{
                background: 'none',
                border: 'none',
                color: 'var(--color-primary)',
                cursor: 'pointer',
                fontWeight: '600',
                textDecoration: 'underline',
                fontSize: 'var(--font-size-sm)'
              }}
            >
              {isRegistering ? 'Sign In' : 'Create Account'}
            </button>
          </p>
        </div>

        {/* Demo Account Info */}
        {!isRegistering && (
          <div className="alert alert-warning" style={{ 
            marginTop: 'var(--spacing-md)',
            fontSize: 'var(--font-size-sm)'
          }}>
            <div style={{ fontWeight: '600', marginBottom: 'var(--spacing-xs)' }}>
              🎯 Demo Account
            </div>
            <div style={{ fontFamily: 'monospace' }}>
              Username: <strong>admin</strong><br />
              Password: <strong>admin123</strong>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Login;
