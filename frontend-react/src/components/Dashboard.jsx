/**
 * Dashboard Component - PHASE 2 IMPROVED
 * 
 * UX IMPROVEMENTS:
 * ✅ Professional summary cards with icons
 * ✅ Responsive grid layout (mobile-friendly)
 * ✅ Meaningful chart titles and legends
 * ✅ Loading states while fetching
 * ✅ Empty state with clear call-to-action
 * ✅ Better color scheme consistency
 * 
 * DESIGN TOKENS:
 * Colors now imported from ../styles/tokens.js for consistency
 * with desktop app (desktop-pyqt/ui/style_tokens.py)
 */

import { useEffect, useState } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip as ChartTooltip, Legend } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import { getUploadHistory } from '../services/api';
import Tooltip from './Tooltip';
import { setupKeyboardShortcuts } from '../utils/keyboardShortcuts';
import { colors } from '../styles/tokens';  // NEW: Import design tokens

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

function Dashboard({ latestDataset, onRefresh, onNavigateToUpload }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadHistory();
  }, [latestDataset]);

  // Keyboard shortcuts
  useEffect(() => {
    const cleanup = setupKeyboardShortcuts({
      onRefresh: () => {
        if (onRefresh) onRefresh();
      },
    });
    return cleanup;
  }, [onRefresh]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const data = await getUploadHistory();
      setHistory(data);
    } catch (err) {
      console.error('Failed to load history:', err);
    } finally {
      setLoading(false);
    }
  };

  // Empty State - No Data Uploaded Yet
  if (!latestDataset) {
    return (
      <div className="card" role="region" aria-label="Dashboard">
        <div className="empty-state">
          <div className="empty-icon" aria-hidden="true">📭</div>
          <h3 className="empty-title">No Data Yet</h3>
          <p className="empty-description">
            Upload your first CSV file to see beautiful visualizations and insights about your equipment data.
          </p>
          {onNavigateToUpload && (
            <button 
              className="btn btn-primary btn-lg"
              onClick={onNavigateToUpload}
            >
              📤 Upload CSV File
            </button>
          )}
        </div>
      </div>
    );
  }

  // Prepare chart data with professional colors
  const chartData = latestDataset.chart_data || { labels: [], values: [] };
  
  const barChartData = {
    labels: chartData.labels,
    datasets: [
      {
        label: 'Number of Equipment',
        data: chartData.values,
        backgroundColor: '#3b82f6', // Primary blue
        borderColor: '#2563eb',
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  };

  const pieChartData = {
    labels: chartData.labels,
    datasets: [
      {
        data: chartData.values,
        backgroundColor: [
          '#3b82f6', // Primary blue
          '#10b981', // Success green
          '#8b5cf6', // Purple
          '#f59e0b', // Amber
          '#ef4444', // Danger red
          '#ec4899', // Pink
        ],
        borderColor: '#ffffff',
        borderWidth: 2,
      },
    ],
  };

  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          font: { size: 12, weight: '600' },
          padding: 12,
        }
      },
      title: {
        display: true,
        text: 'Equipment Type Distribution (Bar Chart)',
        font: { size: 16, weight: '700' },
        padding: { bottom: 16 }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { font: { size: 11 } },
        title: {
          display: true,
          text: 'Count',
          font: { size: 12, weight: '600' }
        }
      },
      x: {
        ticks: { font: { size: 11 } },
        title: {
          display: true,
          text: 'Equipment Type',
          font: { size: 12, weight: '600' }
        }
      }
    }
  };

  const pieChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'right',
        labels: {
          font: { size: 12, weight: '600' },
          padding: 12,
        }
      },
      title: {
        display: true,
        text: 'Equipment Type Distribution (Pie Chart)',
        font: { size: 16, weight: '700' },
        padding: { bottom: 16 }
      }
    }
  };

  return (
    <div>
      {/* Summary Cards */}
      <div className="grid-4" style={{ marginBottom: 'var(--spacing-xl)' }} role="region" aria-label="Equipment Statistics">
        <div className="card" style={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          border: 'none'
        }} role="article" aria-label="Total Equipment Count">
          <div style={{ fontSize: '32px', marginBottom: 'var(--spacing-sm)' }} aria-hidden="true">⚙️</div>
          <div style={{ 
            fontSize: 'var(--font-size-sm)', 
            opacity: 0.9,
            marginBottom: 'var(--spacing-xs)'
          }}>
            <Tooltip text="Total number of equipment items in the dataset">
              Total Equipment
            </Tooltip>
          </div>
          <div style={{ 
            fontSize: 'var(--font-size-2xl)', 
            fontWeight: '700' 
          }}>
            {latestDataset.total_equipment}
          </div>
        </div>
        
        <div className="card" style={{ 
          background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
          color: 'white',
          border: 'none'
        }} role="article" aria-label="Average Flowrate">
          <div style={{ fontSize: '32px', marginBottom: 'var(--spacing-sm)' }} aria-hidden="true">💧</div>
          <div style={{ 
            fontSize: 'var(--font-size-sm)', 
            opacity: 0.9,
            marginBottom: 'var(--spacing-xs)'
          }}>
            <Tooltip text="Average volume of fluid passing through equipment per unit time (L/min)">
              Avg Flowrate
            </Tooltip>
          </div>
          <div style={{ 
            fontSize: 'var(--font-size-2xl)', 
            fontWeight: '700' 
          }}>
            {latestDataset.avg_flowrate}
          </div>
        </div>
        
        <div className="card" style={{ 
          background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
          color: 'white',
          border: 'none'
        }} role="article" aria-label="Average Pressure">
          <div style={{ fontSize: '32px', marginBottom: 'var(--spacing-sm)' }} aria-hidden="true">📊</div>
          <div style={{ 
            fontSize: 'var(--font-size-sm)', 
            opacity: 0.9,
            marginBottom: 'var(--spacing-xs)'
          }}>
            <Tooltip text="Average force per unit area applied by equipment (PSI or bar)">
              Avg Pressure
            </Tooltip>
          </div>
          <div style={{ 
            fontSize: 'var(--font-size-2xl)', 
            fontWeight: '700' 
          }}>
            {latestDataset.avg_pressure}
          </div>
        </div>
        
        <div className="card" style={{ 
          background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
          color: 'white',
          border: 'none'
        }} role="article" aria-label="Average Temperature">
          <div style={{ fontSize: '32px', marginBottom: 'var(--spacing-sm)' }} aria-hidden="true">🌡️</div>
          <div style={{ 
            fontSize: 'var(--font-size-sm)', 
            opacity: 0.9,
            marginBottom: 'var(--spacing-xs)'
          }}>
            <Tooltip text="Average operating temperature of equipment (°C or °F)">
              Avg Temperature
            </Tooltip>
          </div>
          <div style={{ 
            fontSize: 'var(--font-size-2xl)', 
            fontWeight: '700' 
          }}>
            {latestDataset.avg_temperature}
          </div>
        </div>
      </div>

      {/* Charts Section */}
      {chartData.labels.length > 0 && (
        <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
          <div className="card-header">
            <h2 className="card-title">📈 Data Visualizations</h2>
          </div>
          
          <div className="grid-2" style={{ gap: 'var(--spacing-xl)' }}>
            <div>
              <div style={{ height: '350px' }}>
                <Bar data={barChartData} options={barChartOptions} />
              </div>
            </div>
            
            <div>
              <div style={{ height: '350px' }}>
                <Pie data={pieChartData} options={pieChartOptions} />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Equipment Data Table */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">🗂️ Equipment Records</h2>
          <span className="badge badge-primary">
            {latestDataset.equipment_records?.length || 0} records
          </span>
        </div>
        
        <div style={{ overflowX: 'auto' }}>
          <table style={{ 
            width: '100%', 
            borderCollapse: 'collapse',
            fontSize: 'var(--font-size-sm)'
          }}>
            <thead>
              <tr style={{ 
                backgroundColor: 'var(--color-bg)', 
                borderBottom: '2px solid var(--color-border)'
              }}>
                <th style={{ 
                  padding: 'var(--spacing-md)', 
                  textAlign: 'left',
                  fontWeight: '600',
                  color: 'var(--color-text)'
                }}>
                  Equipment Name
                </th>
                <th style={{ 
                  padding: 'var(--spacing-md)', 
                  textAlign: 'left',
                  fontWeight: '600',
                  color: 'var(--color-text)'
                }}>
                  Type
                </th>
                <th style={{ 
                  padding: 'var(--spacing-md)', 
                  textAlign: 'right',
                  fontWeight: '600',
                  color: 'var(--color-text)'
                }}>
                  Flowrate
                </th>
                <th style={{ 
                  padding: 'var(--spacing-md)', 
                  textAlign: 'right',
                  fontWeight: '600',
                  color: 'var(--color-text)'
                }}>
                  Pressure
                </th>
                <th style={{ 
                  padding: 'var(--spacing-md)', 
                  textAlign: 'right',
                  fontWeight: '600',
                  color: 'var(--color-text)'
                }}>
                  Temperature
                </th>
              </tr>
            </thead>
            <tbody>
              {latestDataset.equipment_records?.map((record, index) => (
                <tr key={record.id} style={{ 
                  borderBottom: '1px solid var(--color-border)',
                  backgroundColor: index % 2 === 0 ? 'white' : 'var(--color-bg)'
                }}>
                  <td style={{ 
                    padding: 'var(--spacing-md)',
                    fontWeight: '500'
                  }}>
                    {record.equipment_name}
                  </td>
                  <td style={{ padding: 'var(--spacing-md)' }}>
                    <span className="badge badge-secondary">
                      {record.equipment_type}
                    </span>
                  </td>
                  <td style={{ 
                    padding: 'var(--spacing-md)',
                    textAlign: 'right',
                    fontFamily: 'monospace'
                  }}>
                    {record.flowrate}
                  </td>
                  <td style={{ 
                    padding: 'var(--spacing-md)',
                    textAlign: 'right',
                    fontFamily: 'monospace'
                  }}>
                    {record.pressure}
                  </td>
                  <td style={{ 
                    padding: 'var(--spacing-md)',
                    textAlign: 'right',
                    fontFamily: 'monospace'
                  }}>
                    {record.temperature}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
