/**
 * Application Configuration
 * 
 * Centralized configuration for the frontend application.
 * Uses environment variables with fallback defaults.
 */

// Backend API Base URL
// Vite exposes env vars as import.meta.env.VITE_*
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// File upload configuration
export const MAX_FILE_SIZE_MB = 10;
export const ALLOWED_FILE_TYPES = ['.csv'];
export const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

// API endpoints
export const ENDPOINTS = {
  LOGIN: '/login/',
  REGISTER: '/register/',
  UPLOAD_CSV: '/upload-csv/',
  UPLOAD_HISTORY: '/upload-history/',
  DATASET_SUMMARY: (id) => `/datasets/${id}/summary/`,
  DATASET_DELETE: (id) => `/datasets/${id}/delete/`,
  DOWNLOAD_PDF: (id) => `/datasets/${id}/download-pdf/`,
};

// App metadata
export const APP_NAME = 'Chemical Equipment Parameter Visualizer';
export const APP_VERSION = '1.0.0';
