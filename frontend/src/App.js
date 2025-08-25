import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import DatabaseStats from './components/DatabaseStats';
import { FileText, MessageCircle, Database, Settings } from 'lucide-react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleFileUploadSuccess = () => {
    fetchStats(); // Refresh stats after successful upload
  };

  const handleClearDatabase = async () => {
    if (window.confirm('Are you sure you want to clear all documents from the database?')) {
      setIsLoading(true);
      try {
        await axios.delete(`${API_BASE_URL}/clear`);
        fetchStats();
        alert('Database cleared successfully!');
      } catch (error) {
        console.error('Error clearing database:', error);
        alert('Error clearing database. Please try again.');
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="app">
      <div className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <FileText className="title-icon" />
            Hero Vida RAG Application
          </h1>
          <p className="app-subtitle">
            Smart Document Analysis & AI-Powered Chat Interface
          </p>
        </div>
        
        {stats && (
          <div className="header-stats">
            <div className="stat-item">
              <Database size={16} />
              <span>{stats.total_documents} Documents</span>
            </div>
            <div className="stat-item">
              <FileText size={16} />
              <span>{stats.total_chunks} Chunks</span>
            </div>
          </div>
        )}
      </div>

      <div className="app-nav">
        <button
          className={`nav-button ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          <MessageCircle size={18} />
          Chat
        </button>
        <button
          className={`nav-button ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          <FileText size={18} />
          Upload Documents
        </button>
        <button
          className={`nav-button ${activeTab === 'stats' ? 'active' : ''}`}
          onClick={() => setActiveTab('stats')}
        >
          <Database size={18} />
          Database
        </button>
        <button
          className={`nav-button ${activeTab === 'settings' ? 'active' : ''}`}
          onClick={() => setActiveTab('settings')}
        >
          <Settings size={18} />
          Settings
        </button>
      </div>

      <div className="app-content">
        {activeTab === 'chat' && (
          <div className="tab-content">
            <ChatInterface apiBaseUrl={API_BASE_URL} />
          </div>
        )}

        {activeTab === 'upload' && (
          <div className="tab-content">
            <div className="upload-section">
              <h2>Upload Documents</h2>
              <p>Upload your PDF and CSV files to build the knowledge base for Hero Vida strategy analysis.</p>
              <FileUpload 
                apiBaseUrl={API_BASE_URL}
                onUploadSuccess={handleFileUploadSuccess}
              />
            </div>
          </div>
        )}

        {activeTab === 'stats' && (
          <div className="tab-content">
            <DatabaseStats 
              stats={stats}
              onRefresh={fetchStats}
              onClear={handleClearDatabase}
              isLoading={isLoading}
            />
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="tab-content">
            <div className="settings-section">
              <h2>Settings</h2>
              <div className="settings-info">
                <div className="setting-item">
                  <h3>API Configuration</h3>
                  <p>Backend URL: {API_BASE_URL}</p>
                </div>
                <div className="setting-item">
                  <h3>Supported File Types</h3>
                  <ul>
                    <li>PDF documents (.pdf)</li>
                    <li>CSV data files (.csv)</li>
                  </ul>
                </div>
                <div className="setting-item">
                  <h3>Features</h3>
                  <ul>
                    <li>Document chunking and embedding</li>
                    <li>Vector similarity search</li>
                    <li>AI-powered responses using Gemini</li>
                    <li>Source attribution</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
