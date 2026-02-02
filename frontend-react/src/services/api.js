/**
 * API Service for Equipment Visualizer
 * 
 * WHAT: Functions to communicate with the Django backend
 * WHY: Centralized place for all API calls
 * HOW: Uses Axios to make HTTP requests
 * 
 * ELI5: Think of this as a "phone" that talks to the backend server
 */

import axios from 'axios';
import { API_BASE_URL } from '../config.js';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests automatically
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Authentication Services
 */

/**
 * Login user
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise} Response with token and user info
 */
export const login = async (username, password) => {
  const response = await api.post('/login/', { username, password });
  if (response.data.token) {
    localStorage.setItem('token', response.data.token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
  }
  return response.data;
};

/**
 * Register new user
 * @param {string} username - Username
 * @param {string} email - Email
 * @param {string} password - Password
 * @returns {Promise} Response with token and user info
 */
export const register = async (username, email, password) => {
  const response = await api.post('/register/', { username, email, password });
  if (response.data.token) {
    localStorage.setItem('token', response.data.token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
  }
  return response.data;
};

/**
 * Logout user
 */
export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

/**
 * Check if user is logged in
 * @returns {boolean}
 */
export const isAuthenticated = () => {
  return localStorage.getItem('token') !== null;
};

/**
 * Get current user info
 * @returns {Object|null}
 */
export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

/**
 * Dataset Services
 */

/**
 * Upload CSV file
 * @param {File} file - CSV file to upload
 * @returns {Promise} Response with dataset info
 */
export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload-csv/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

/**
 * Get upload history (last 5 datasets)
 * @returns {Promise} Array of datasets
 */
export const getUploadHistory = async () => {
  const response = await api.get('/upload-history/');
  return response.data;
};

/**
 * Get dataset summary by ID
 * @param {number} datasetId - Dataset ID
 * @returns {Promise} Dataset details with equipment records
 */
export const getDatasetSummary = async (datasetId) => {
  const response = await api.get(`/datasets/${datasetId}/summary/`);
  return response.data;
};

/**
 * Delete a dataset
 * @param {number} datasetId - Dataset ID
 * @returns {Promise}
 */
export const deleteDataset = async (datasetId) => {
  const response = await api.delete(`/datasets/${datasetId}/delete/`);
  return response.data;
};

/**
 * Download PDF report for a dataset
 * @param {number} datasetId - Dataset ID
 * @returns {Promise} Blob for PDF download
 */
export const downloadPDF = async (datasetId) => {
  const response = await api.get(`/datasets/${datasetId}/download-pdf/`, {
    responseType: 'blob',
  });
  
  // Create a download link
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `equipment_report_${datasetId}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  
  return response.data;
};

export default api;
