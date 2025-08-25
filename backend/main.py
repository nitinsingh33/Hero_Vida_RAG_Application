from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import uvicorn
from typing import List, Optional
import tempfile
import shutil

from services.document_processor import DocumentProcessor
from services.vector_store import VectorStore
from services.gemini_service import GeminiService
from models.chat_models import ChatRequest, ChatResponse, UploadResponse

load_dotenv()

app = FastAPI(title="Hero Vida RAG Application", version="1.0.0")

# CORS middleware
allowed_origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "https://*.vercel.app",
    "https://*.netlify.app",
    "https://*.surge.sh",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
document_processor = DocumentProcessor()
vector_store = VectorStore()
gemini_service = GeminiService()

@app.on_event("startup")
async def startup_event():
    """Initialize the vector database on startup"""
    await vector_store.initialize()

@app.get("/")
async def root():
    return {"message": "Hero Vida RAG API is running!"}

@app.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and process documents (PDF, CSV)"""
    try:
        uploaded_files = []
        total_chunks = 0
        
        for file in files:
            # Validate file type
            if not file.filename.lower().endswith(('.pdf', '.csv')):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file.filename}. Only PDF and CSV files are allowed."
                )
            
            # Check file size
            file_size = 0
            content = await file.read()
            file_size = len(content)
            
            max_size = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB default
            if file_size > max_size:
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} is too large. Maximum size: {max_size/1024/1024:.1f}MB"
                )
            
            # Save temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            try:
                # Process document
                chunks = await document_processor.process_document(tmp_file_path, file.filename)
                
                # Store in vector database
                await vector_store.add_documents(chunks, file.filename)
                
                uploaded_files.append({
                    "filename": file.filename,
                    "size": file_size,
                    "chunks": len(chunks)
                })
                total_chunks += len(chunks)
                
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)
        
        return UploadResponse(
            message=f"Successfully processed {len(uploaded_files)} files",
            files=uploaded_files,
            total_chunks=total_chunks
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint for RAG queries"""
    try:
        # Retrieve relevant documents
        relevant_docs = await vector_store.similarity_search(request.query, k=5)
        
        if not relevant_docs:
            return ChatResponse(
                response="I don't have any relevant information in the uploaded documents to answer your question. Please upload some documents first.",
                sources=[]
            )
        
        # Generate response using Gemini
        response_text = await gemini_service.generate_response(request.query, relevant_docs)
        
        # Extract unique sources
        sources = list(set([doc["source"] for doc in relevant_docs]))
        
        return ChatResponse(
            response=response_text,
            sources=sources
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Hero Vida RAG API"}

@app.get("/stats")
async def get_stats():
    """Get database statistics"""
    try:
        stats = await vector_store.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@app.delete("/clear")
async def clear_database():
    """Clear all documents from the vector database"""
    try:
        await vector_store.clear_database()
        return {"message": "Database cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing database: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
