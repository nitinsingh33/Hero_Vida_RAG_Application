import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor
import uuid
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        self.db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
        self.collection_name = "hero_vida_documents"
        self.client = None
        self.collection = None
        self.embedding_model = None
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def initialize(self):
        """Initialize ChromaDB client and collection"""
        def init_db():
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
            except:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Hero Vida strategy documents"}
                )
        
        await asyncio.get_event_loop().run_in_executor(
            self.executor, init_db
        )

    async def add_documents(self, documents: List[Dict[str, Any]], source_file: str):
        """Add document chunks to the vector store"""
        def add_docs():
            if not documents:
                return
            
            # Prepare data for ChromaDB
            ids = []
            embeddings = []
            metadatas = []
            documents_content = []
            
            for doc in documents:
                # Generate unique ID
                doc_id = str(uuid.uuid4())
                ids.append(doc_id)
                
                # Generate embedding
                embedding = self.embedding_model.encode(doc["content"]).tolist()
                embeddings.append(embedding)
                
                # Prepare metadata
                metadata = doc["metadata"].copy()
                metadata["source_file"] = source_file
                metadatas.append(metadata)
                
                # Add content
                documents_content.append(doc["content"])
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents_content
            )
        
        await asyncio.get_event_loop().run_in_executor(
            self.executor, add_docs
        )

    async def similarity_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        def search():
            if not self.collection:
                return []
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i in range(len(results["documents"][0])):
                    formatted_results.append({
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "source": results["metadatas"][0][i].get("source", "unknown"),
                        "distance": results["distances"][0][i] if results.get("distances") else 0.0
                    })
            
            return formatted_results
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, search
        )

    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        def get_db_stats():
            if not self.collection:
                return {"total_documents": 0, "total_chunks": 0, "collections": []}
            
            # Get collection count
            count = self.collection.count()
            
            # Get unique sources
            results = self.collection.get(include=["metadatas"])
            sources = set()
            if results["metadatas"]:
                for metadata in results["metadatas"]:
                    if "source" in metadata:
                        sources.add(metadata["source"])
            
            return {
                "total_documents": len(sources),
                "total_chunks": count,
                "collections": [self.collection_name],
                "sources": list(sources)
            }
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, get_db_stats
        )

    async def clear_database(self):
        """Clear all documents from the database"""
        def clear_db():
            if self.collection:
                # Get all IDs
                results = self.collection.get()
                if results["ids"]:
                    # Delete all documents
                    self.collection.delete(ids=results["ids"])
        
        await asyncio.get_event_loop().run_in_executor(
            self.executor, clear_db
        )

    async def delete_by_source(self, source_file: str):
        """Delete all documents from a specific source file"""
        def delete_source():
            if not self.collection:
                return
            
            # Query documents by source
            results = self.collection.get(
                where={"source": source_file},
                include=["ids"]
            )
            
            if results["ids"]:
                self.collection.delete(ids=results["ids"])
        
        await asyncio.get_event_loop().run_in_executor(
            self.executor, delete_source
        )
