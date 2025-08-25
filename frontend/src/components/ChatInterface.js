import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Send, Bot, User, FileText, Loader2 } from 'lucide-react';
import './ChatInterface.css';

const ChatInterface = ({ apiBaseUrl }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hello! I'm your Hero Vida strategy assistant. I can help you analyze and answer questions about your uploaded documents. What would you like to know?",
      sources: []
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      sources: []
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${apiBaseUrl}/chat`, {
        query: inputValue
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.response,
        sources: response.data.sources || []
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: `Sorry, I encountered an error: ${error.response?.data?.detail || error.message}. Please try again.`,
        sources: [],
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: 1,
        type: 'bot',
        content: "Chat cleared! I'm ready to help you with questions about your Hero Vida documents.",
        sources: []
      }
    ]);
  };

  const suggestedQuestions = [
    "What are the key strategic priorities for Hero Vida?",
    "Can you summarize the main business challenges mentioned?",
    "What market opportunities are identified in the documents?",
    "What are the financial highlights or projections?",
    "How does Hero Vida plan to compete in the EV market?"
  ];

  const handleSuggestionClick = (question) => {
    setInputValue(question);
    inputRef.current?.focus();
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-title">
          <Bot className="chat-icon" />
          <span>Hero Vida Strategy Assistant</span>
        </div>
        <button 
          className="clear-button"
          onClick={handleClearChat}
          disabled={isLoading}
        >
          Clear Chat
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            <div className="message-avatar">
              {message.type === 'user' ? (
                <User className="avatar-icon" />
              ) : (
                <Bot className="avatar-icon" />
              )}
            </div>
            
            <div className="message-content">
              <div className={`message-bubble ${message.isError ? 'error' : ''}`}>
                {message.type === 'bot' ? (
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                ) : (
                  <p>{message.content}</p>
                )}
              </div>
              
              {message.sources && message.sources.length > 0 && (
                <div className="message-sources">
                  <div className="sources-label">
                    <FileText size={14} />
                    <span>Sources:</span>
                  </div>
                  <div className="sources-list">
                    {message.sources.map((source, index) => (
                      <span key={index} className="source-tag">
                        {source}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot">
            <div className="message-avatar">
              <Bot className="avatar-icon" />
            </div>
            <div className="message-content">
              <div className="message-bubble loading">
                <Loader2 className="loading-icon" />
                <span>Analyzing documents and generating response...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {messages.length === 1 && (
        <div className="suggestions">
          <h4>Try asking:</h4>
          <div className="suggestion-chips">
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                className="suggestion-chip"
                onClick={() => handleSuggestionClick(question)}
                disabled={isLoading}
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="chat-input">
        <div className="input-container">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything about your Hero Vida documents..."
            disabled={isLoading}
            rows={1}
            className="message-input"
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            <Send className="send-icon" />
          </button>
        </div>
        <div className="input-hint">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
