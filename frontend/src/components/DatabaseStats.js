import React from 'react';
import { Database, FileText, RefreshCw, Trash2, AlertTriangle } from 'lucide-react';
import './DatabaseStats.css';

const DatabaseStats = ({ stats, onRefresh, onClear, isLoading }) => {
  if (!stats) {
    return (
      <div className="stats-container">
        <div className="stats-header">
          <h2>Database Statistics</h2>
          <button 
            className="refresh-button"
            onClick={onRefresh}
            disabled={isLoading}
          >
            <RefreshCw className={`refresh-icon ${isLoading ? 'spinning' : ''}`} />
            Refresh
          </button>
        </div>
        <div className="loading-stats">
          <p>Loading statistics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="stats-container">
      <div className="stats-header">
        <h2>Database Statistics</h2>
        <div className="header-buttons">
          <button 
            className="refresh-button"
            onClick={onRefresh}
            disabled={isLoading}
          >
            <RefreshCw className={`refresh-icon ${isLoading ? 'spinning' : ''}`} />
            Refresh
          </button>
          <button 
            className="clear-button"
            onClick={onClear}
            disabled={isLoading || stats.total_documents === 0}
          >
            <Trash2 className="clear-icon" />
            Clear All
          </button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon documents">
            <FileText />
          </div>
          <div className="stat-info">
            <div className="stat-value">{stats.total_documents}</div>
            <div className="stat-label">Documents</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon chunks">
            <Database />
          </div>
          <div className="stat-info">
            <div className="stat-value">{stats.total_chunks}</div>
            <div className="stat-label">Text Chunks</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon collections">
            <Database />
          </div>
          <div className="stat-info">
            <div className="stat-value">{stats.collections?.length || 0}</div>
            <div className="stat-label">Collections</div>
          </div>
        </div>
      </div>

      {stats.sources && stats.sources.length > 0 && (
        <div className="sources-section">
          <h3>Uploaded Documents</h3>
          <div className="sources-list">
            {stats.sources.map((source, index) => (
              <div key={index} className="source-item">
                <FileText className="source-icon" />
                <span className="source-name">{source}</span>
                <span className="source-type">
                  {source.toLowerCase().endsWith('.pdf') ? 'PDF' :
                   source.toLowerCase().endsWith('.csv') ? 'CSV' : 'Unknown'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {stats.collections && stats.collections.length > 0 && (
        <div className="collections-section">
          <h3>Vector Collections</h3>
          <div className="collections-list">
            {stats.collections.map((collection, index) => (
              <div key={index} className="collection-item">
                <Database className="collection-icon" />
                <span className="collection-name">{collection}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {stats.total_documents === 0 && (
        <div className="empty-state">
          <AlertTriangle className="empty-icon" />
          <h3>No Documents Found</h3>
          <p>Upload some PDF or CSV files to get started with your RAG application.</p>
        </div>
      )}

      <div className="database-info">
        <h3>Database Information</h3>
        <div className="info-grid">
          <div className="info-item">
            <strong>Vector Database:</strong>
            <span>ChromaDB</span>
          </div>
          <div className="info-item">
            <strong>Embedding Model:</strong>
            <span>all-MiniLM-L6-v2</span>
          </div>
          <div className="info-item">
            <strong>Text Processing:</strong>
            <span>Recursive Character Splitter</span>
          </div>
          <div className="info-item">
            <strong>AI Model:</strong>
            <span>Google Gemini Pro</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DatabaseStats;
