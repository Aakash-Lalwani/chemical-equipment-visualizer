/**
 * Main Entry Point
 * 
 * WHAT: Starting point of the React application
 * WHY: React needs an entry point to mount the app
 * HOW: Renders the App component into the root div
 */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
