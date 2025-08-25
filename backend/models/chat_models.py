from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    session_id: Optional[str] = None

class DocumentChunk(BaseModel):
    content: str
    metadata: Dict[str, Any]
    source: str

class UploadedFile(BaseModel):
    filename: str
    size: int
    chunks: int

class UploadResponse(BaseModel):
    message: str
    files: List[UploadedFile]
    total_chunks: int

class DatabaseStats(BaseModel):
    total_documents: int
    total_chunks: int
    collections: List[str]
