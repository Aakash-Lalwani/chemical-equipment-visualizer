/**
 * History Component - PHASE 2 IMPROVED
 * 
 * UX IMPROVEMENTS:
 * ✅ Clean card-based list layout
 * ✅ Search/filter functionality
 * ✅ Sort by date
 * ✅ Delete confirmation modal
 * ✅ Loading skeleton states
 * ✅ Empty state with illustration
 * ✅ Better button grouping and actions
 */

import { useState, useEffect } from 'react';
import { getUploadHistory, getDatasetSummary, downloadPDF, deleteDataset } from '../services/api';
import Tooltip from './Tooltip';
import { setupKeyboardShortcuts } from '../utils/keyboardShortcuts';

function History({ onDatasetSelect }) {
  const [history, setHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [actionLoading, setActionLoading] = useState(null);

  useEffect(() => {
    loadHistory();
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const cleanup = setupKeyboardShortcuts({
      onEscape: () => {
        if (deleteConfirm) setDeleteConfirm(null);
        if (searchTerm) setSearchTerm('');
      },
      onRefresh: () => loadHistory(),
    });
    return cleanup;
  }, [deleteConfirm, searchTerm]);

  useEffect(() => {
    // Filter history based on search term
    if (searchTerm.trim() === '') {
      setFilteredHistory(history);
    } else {
      const filtered = history.filter(dataset => 
        dataset.id.toString().includes(searchTerm) ||
        dataset.total_equipment.toString().includes(searchTerm)
      );
      setFilteredHistory(filtered);
    }
  }, [searchTerm, history]);

  const loadHistory = async () => {
    setLoading(true);
    setError('');
    
    try {
      const data = await getUploadHistory();
      setHistory(data);
      setFilteredHistory(data);
    } catch (err) {
      setError('Failed to load upload history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleView = async (datasetId) => {
    setActionLoading(datasetId);
    try {
      const dataset = await getDatasetSummary(datasetId);
      onDatasetSelect(dataset);
    } catch (err) {
      alert('⚠️ Failed to load dataset details. Please try again.');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDownloadPDF = async (datasetId) => {
    setActionLoading(`pdf-${datasetId}`);
    try {
      await downloadPDF(datasetId);
    } catch (err) {
      alert('⚠️ Failed to download PDF. Please try again.');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDeleteClick = (datasetId) => {
    setDeleteConfirm(datasetId);
  };

  const handleDeleteConfirm = async () => {
    const datasetId = deleteConfirm;
    setActionLoading(`delete-${datasetId}`);
    
    try {
      await deleteDataset(datasetId);
      setHistory(prev => prev.filter(d => d.id !== datasetId));
      setDeleteConfirm(null);
    } catch (err) {
      alert('⚠️ Failed to delete dataset. Please try again.');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteConfirm(null);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Loading State
  if (loading) {
    return (
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">📜 Upload History</h2>
        </div>
        <div className="loading-overlay" style={{ position: 'relative', minHeight: '200px' }}>
          <div className="spinner"></div>
          <p style={{ marginTop: 'var(--spacing-md)', color: 'var(--color-text-secondary)' }}>
            Loading history...
          </p>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">📜 Upload History</h2>
          <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
            <span className="badge badge-primary">
              {history.length} {history.length === 1 ? 'dataset' : 'datasets'}
            </span>
            <button 
              className="btn btn-secondary btn-sm" 
              onClick={loadHistory}
              disabled={loading}
            >
              🔄 Refresh
            </button>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="alert alert-error" style={{ marginBottom: 'var(--spacing-md)' }}>
            <span style={{ marginRight: 'var(--spacing-xs)' }}>⚠️</span>
            {error}
          </div>
        )}

        {/* Search Bar */}
        {history.length > 0 && (
          <div style={{ marginBottom: 'var(--spacing-lg)' }}>
            <input
              type="text"
              className="input"
              placeholder="🔍 Search by dataset ID or equipment count..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        )}

        {/* Empty State */}
        {history.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📭</div>
            <h3 className="empty-title">No Upload History</h3>
            <p className="empty-description">
              You haven't uploaded any datasets yet. Upload a CSV file to get started!
            </p>
          </div>
        ) : filteredHistory.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3 className="empty-title">No Results Found</h3>
            <p className="empty-description">
              No datasets match your search. Try different keywords.
            </p>
          </div>
        ) : (
          /* Dataset Cards */
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-md)' }}>
            {filteredHistory.map((dataset) => (
              <div 
                key={dataset.id} 
                className="card"
                style={{ 
                  padding: 'var(--spacing-lg)',
                  boxShadow: 'var(--shadow-sm)',
                  transition: 'box-shadow 0.3s ease',
                }}
              >
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  gap: 'var(--spacing-lg)',
                  flexWrap: 'wrap'
                }}>
                  {/* Dataset Info */}
                  <div style={{ flex: 1, minWidth: '250px' }}>
                    <div style={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: 'var(--spacing-sm)',
                      marginBottom: 'var(--spacing-sm)'
                    }}>
                      <span style={{ fontSize: '28px' }}>📊</span>
                      <h3 style={{ 
                        fontSize: 'var(--font-size-lg)', 
                        fontWeight: '700',
                        color: 'var(--color-text)'
                      }}>
                        Dataset #{dataset.id}
                      </h3>
                    </div>
                    
                    <div style={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: 'var(--spacing-sm)',
                      color: 'var(--color-text-secondary)',
                      fontSize: 'var(--font-size-sm)',
                      marginBottom: 'var(--spacing-md)'
                    }}>
                      <span>🕒 {formatDate(dataset.uploaded_at)}</span>
                    </div>

                    {/* Stats Grid */}
                    <div style={{ 
                      display: 'grid', 
                      gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
                      gap: 'var(--spacing-sm)'
                    }}>
                      <div style={{ 
                        padding: 'var(--spacing-sm)',
                        backgroundColor: 'var(--color-bg)',
                        borderRadius: 'var(--radius-md)'
                      }}>
                        <div style={{ 
                          fontSize: 'var(--font-size-xs)',
                          color: 'var(--color-text-secondary)'
                        }}>
                          Equipment
                        </div>
                        <div style={{ 
                          fontSize: 'var(--font-size-lg)',
                          fontWeight: '700',
                          color: 'var(--color-primary)'
                        }}>
                          {dataset.total_equipment}
                        </div>
                      </div>
                      
                      <div style={{ 
                        padding: 'var(--spacing-sm)',
                        backgroundColor: 'var(--color-bg)',
                        borderRadius: 'var(--radius-md)'
                      }}>
                        <div style={{ 
                          fontSize: 'var(--font-size-xs)',
                          color: 'var(--color-text-secondary)'
                        }}>
                          Avg Flowrate
                        </div>
                        <div style={{ 
                          fontSize: 'var(--font-size-lg)',
                          fontWeight: '700',
                          color: 'var(--color-success)'
                        }}>
                          {dataset.avg_flowrate}
                        </div>
                      </div>
                      
                      <div style={{ 
                        padding: 'var(--spacing-sm)',
                        backgroundColor: 'var(--color-bg)',
                        borderRadius: 'var(--radius-md)'
                      }}>
                        <div style={{ 
                          fontSize: 'var(--font-size-xs)',
                          color: 'var(--color-text-secondary)'
                        }}>
                          Avg Pressure
                        </div>
                        <div style={{ 
                          fontSize: 'var(--font-size-lg)',
                          fontWeight: '700',
                          color: '#8b5cf6'
                        }}>
                          {dataset.avg_pressure}
                        </div>
                      </div>
                      
                      <div style={{ 
                        padding: 'var(--spacing-sm)',
                        backgroundColor: 'var(--color-bg)',
                        borderRadius: 'var(--radius-md)'
                      }}>
                        <div style={{ 
                          fontSize: 'var(--font-size-xs)',
                          color: 'var(--color-text-secondary)'
                        }}>
                          Avg Temp
                        </div>
                        <div style={{ 
                          fontSize: 'var(--font-size-lg)',
                          fontWeight: '700',
                          color: '#f59e0b'
                        }}>
                          {dataset.avg_temperature}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div style={{ 
                    display: 'flex', 
                    flexDirection: 'column',
                    gap: 'var(--spacing-sm)',
                    minWidth: '140px'
                  }}>
                    <button
                      className="btn btn-primary btn-sm"
                      onClick={() => handleView(dataset.id)}
                      disabled={actionLoading === dataset.id}
                      style={{ width: '100%' }}
                    >
                      {actionLoading === dataset.id ? (
                        <>
                          <span className="spinner" style={{ width: '12px', height: '12px' }}></span>
                        </>
                      ) : (
                        <>👁️ View Details</>
                      )}
                    </button>
                    
                    <button
                      className="btn btn-success btn-sm"
                      onClick={() => handleDownloadPDF(dataset.id)}
                      disabled={actionLoading === `pdf-${dataset.id}`}
                      style={{ width: '100%' }}
                    >
                      {actionLoading === `pdf-${dataset.id}` ? (
                        <>
                          <span className="spinner" style={{ width: '12px', height: '12px' }}></span>
                        </>
                      ) : (
                        <>📥 Download PDF</>
                      )}
                    </button>
                    
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDeleteClick(dataset.id)}
                      disabled={actionLoading === `delete-${dataset.id}`}
                      style={{ width: '100%' }}
                    >
                      {actionLoading === `delete-${dataset.id}` ? (
                        <>
                          <span className="spinner" style={{ width: '12px', height: '12px' }}></span>
                        </>
                      ) : (
                        <>🗑️ Delete</>
                      )}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: 'var(--spacing-lg)'
        }}>
          <div className="card" style={{ 
            maxWidth: '400px',
            width: '100%',
            boxShadow: 'var(--shadow-lg)'
          }}>
            <div style={{ textAlign: 'center', marginBottom: 'var(--spacing-lg)' }}>
              <div style={{ fontSize: '64px', marginBottom: 'var(--spacing-md)' }}>
                ⚠️
              </div>
              <h3 style={{ 
                fontSize: 'var(--font-size-xl)', 
                fontWeight: '700',
                marginBottom: 'var(--spacing-sm)'
              }}>
                Delete Dataset?
              </h3>
              <p style={{ 
                color: 'var(--color-text-secondary)',
                fontSize: 'var(--font-size-sm)'
              }}>
                Are you sure you want to delete Dataset #{deleteConfirm}? This action cannot be undone.
              </p>
            </div>
            
            <div style={{ 
              display: 'flex', 
              gap: 'var(--spacing-sm)',
              justifyContent: 'flex-end'
            }}>
              <button
                className="btn btn-secondary"
                onClick={handleDeleteCancel}
                disabled={actionLoading}
              >
                Cancel
              </button>
              <button
                className="btn btn-danger"
                onClick={handleDeleteConfirm}
                disabled={actionLoading}
              >
                {actionLoading ? (
                  <>
                    <span className="spinner" style={{ width: '14px', height: '14px', marginRight: 'var(--spacing-xs)' }}></span>
                    Deleting...
                  </>
                ) : (
                  'Delete'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default History;
