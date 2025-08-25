# Hero Vida RAG Application

A powerful Retrieval-Augmented Generation (RAG) application built specifically for Hero Vida strategy analysis. This application allows you to upload PDF and CSV documents, process them into a vector database, and interact with the data through an AI-powered chat interface using Google's Gemini API.

## 🚀 Features

- **Document Upload & Processing**: Upload PDF and CSV files with drag-and-drop interface
- **Vector Database**: ChromaDB for efficient similarity search and retrieval
- **AI-Powered Chat**: ChatGPT-like interface powered by Google Gemini
- **Real-time Analytics**: Database statistics and document management
- **Source Attribution**: Track which documents answers come from
- **Modern UI**: Clean, responsive React interface with Tailwind-inspired design

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │   Google Gemini │
│                 │◄──►│                  │◄──►│      API        │
│ - File Upload   │    │ - Document Proc. │    │                 │
│ - Chat Interface│    │ - Vector Search  │    └─────────────────┘
│ - Dashboard     │    │ - API Endpoints  │
└─────────────────┘    └──────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    ChromaDB     │
                       │ Vector Database │
                       │                 │
                       └─────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **ChromaDB**: Vector database for embeddings
- **Google Gemini**: Large language model for responses
- **Sentence Transformers**: Text embedding generation
- **PyPDF2**: PDF document processing
- **Pandas**: CSV data processing

### Frontend
- **React 18**: Modern React with hooks
- **Axios**: HTTP client for API calls
- **React Markdown**: Markdown rendering for AI responses
- **Lucide React**: Beautiful icons
- **React Dropzone**: File upload with drag-and-drop

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Google Gemini API Key**

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hero-vida-rag-app
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env

# Edit .env file and add your Gemini API key
# GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

### 4. Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your backend `.env` file

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
hero-vida-rag-app/
├── backend/
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat_models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   ├── vector_store.py
│   │   └── gemini_service.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js
│   │   │   ├── ChatInterface.js
│   │   │   ├── DatabaseStats.js
│   │   │   └── *.css files
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
├── data/ (for sample files)
└── README.md
```

## 💡 How to Use

### Step 1: Upload Documents
1. Click on the "Upload Documents" tab
2. Drag and drop or select PDF/CSV files
3. Files are automatically processed and stored in the vector database

### Step 2: Chat with Your Data
1. Go to the "Chat" tab
2. Ask questions about your uploaded documents
3. Get AI-powered responses with source attribution

### Step 3: Monitor Database
1. Check the "Database" tab for statistics
2. View uploaded documents and collection info
3. Clear database if needed

## 📊 Sample Questions to Try

- "What are the key strategic priorities for Hero Vida?"
- "Can you summarize the main business challenges mentioned?"
- "What market opportunities are identified in the documents?"
- "What are the financial highlights or projections?"
- "How does Hero Vida plan to compete in the EV market?"

## 🔧 Configuration

### Backend Environment Variables (.env)

```env
GOOGLE_API_KEY=your_gemini_api_key_here
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
CHROMA_DB_PATH=./chroma_db
MAX_FILE_SIZE=10485760
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### Frontend Environment Variables (optional)

Create `.env` in frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Make sure you've installed all dependencies
   - Check that you're in the correct directory
   - Try deleting node_modules and npm install again

2. **API Key errors**
   - Verify your Gemini API key is correct
   - Check that the .env file is in the backend directory
   - Restart the backend server after adding the API key

3. **CORS errors**
   - Ensure the frontend URL is correctly set in backend .env
   - Check that both servers are running on correct ports

4. **File upload errors**
   - Check file size limits (default 10MB)
   - Ensure files are PDF or CSV format
   - Verify write permissions for the application

### Debug Mode

Run backend with debug logging:
```bash
# Set log level to debug
python main.py --log-level debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review API documentation at http://localhost:8000/docs
- Create an issue in the repository

## 🔮 Future Enhancements

- [ ] Support for more document formats (Word, Excel, etc.)
- [ ] Advanced search and filtering
- [ ] User authentication and sessions
- [ ] Document versioning
- [ ] Export chat conversations
- [ ] Integration with more LLM providers
- [ ] Advanced analytics and insights

---

Built with ❤️ for Hero Vida strategy analysis
