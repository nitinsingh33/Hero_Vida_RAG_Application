import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { Upload, File, Check, X, AlertCircle } from 'lucide-react';
import './FileUpload.css';

const FileUpload = ({ apiBaseUrl, onUploadSuccess }) => {
  const [uploadStatus, setUploadStatus] = useState('idle'); // idle, uploading, success, error
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    setUploadStatus('uploading');
    setError(null);

    try {
      const formData = new FormData();
      acceptedFiles.forEach((file) => {
        formData.append('files', file);
      });

      const response = await axios.post(`${apiBaseUrl}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          // Optional: Add progress tracking
        },
      });

      setUploadResult(response.data);
      setUploadStatus('success');
      
      if (onUploadSuccess) {
        onUploadSuccess(response.data);
      }
      
      // Reset status after 3 seconds
      setTimeout(() => {
        setUploadStatus('idle');
        setUploadResult(null);
      }, 3000);

    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed');
      setUploadStatus('error');
      
      // Reset status after 5 seconds
      setTimeout(() => {
        setUploadStatus('idle');
        setError(null);
      }, 5000);
    }
  }, [apiBaseUrl, onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/csv': ['.csv'],
    },
    multiple: true,
    disabled: uploadStatus === 'uploading',
  });

  const getStatusIcon = () => {
    switch (uploadStatus) {
      case 'uploading':
        return <div className="spinner" />;
      case 'success':
        return <Check className="status-icon success" />;
      case 'error':
        return <X className="status-icon error" />;
      default:
        return <Upload className="upload-icon" />;
    }
  };

  const getStatusMessage = () => {
    switch (uploadStatus) {
      case 'uploading':
        return 'Processing files...';
      case 'success':
        return uploadResult ? `Successfully processed ${uploadResult.files.length} files (${uploadResult.total_chunks} chunks)` : 'Upload successful!';
      case 'error':
        return error || 'Upload failed';
      default:
        return isDragActive ? 'Drop the files here...' : 'Drag & drop PDF or CSV files here, or click to select';
    }
  };

  return (
    <div className="file-upload-container">
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'drag-active' : ''} ${uploadStatus}`}
      >
        <input {...getInputProps()} />
        
        <div className="upload-content">
          {getStatusIcon()}
          
          <div className="upload-text">
            <p className="primary-text">{getStatusMessage()}</p>
            
            {uploadStatus === 'idle' && (
              <p className="secondary-text">
                Supported formats: PDF, CSV • Max size: 30MB per file
              </p>
            )}
            
            {uploadStatus === 'error' && error && (
              <div className="error-details">
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}
          </div>
        </div>
        
        {acceptedFiles.length > 0 && uploadStatus === 'uploading' && (
          <div className="file-list">
            <h4>Processing Files:</h4>
            {acceptedFiles.map((file, index) => (
              <div key={index} className="file-item">
                <File size={16} />
                <span>{file.name}</span>
                <span className="file-size">({Math.round(file.size / 1024)} KB)</span>
              </div>
            ))}
          </div>
        )}
        
        {uploadResult && uploadStatus === 'success' && (
          <div className="upload-results">
            <h4>Upload Results:</h4>
            {uploadResult.files.map((file, index) => (
              <div key={index} className="result-item">
                <File size={16} />
                <span>{file.filename}</span>
                <span className="chunk-count">{file.chunks} chunks</span>
              </div>
            ))}
          </div>
        )}
      </div>
      
      <div className="upload-info">
        <h3>How it works:</h3>
        <ol>
          <li><strong>Upload:</strong> Select or drag PDF/CSV files containing Hero Vida strategy documents</li>
          <li><strong>Process:</strong> Files are automatically parsed and split into searchable chunks</li>
          <li><strong>Embed:</strong> Text chunks are converted to vector embeddings for similarity search</li>
          <li><strong>Chat:</strong> Ask questions and get AI-powered answers based on your documents</li>
        </ol>
      </div>
    </div>
  );
};

export default FileUpload;
