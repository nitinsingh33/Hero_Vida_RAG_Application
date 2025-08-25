import os
import google.generativeai as genai
from typing import List, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

class GeminiService:
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.executor = ThreadPoolExecutor(max_workers=2)

    async def generate_response(self, query: str, relevant_docs: List[Dict[str, Any]]) -> str:
        """Generate response using Gemini with RAG context"""
        def generate():
            # Prepare context from relevant documents
            context = self._prepare_context(relevant_docs)
            
            # Create the prompt
            prompt = self._create_rag_prompt(query, context)
            
            try:
                # Generate response
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                # Fallback response if generation fails
                return f"I apologize, but I encountered an error while generating a response: {str(e)}. However, I found some relevant information in the documents that might help answer your question:\n\n{context[:500]}..."
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, generate
        )

    def _prepare_context(self, relevant_docs: List[Dict[str, Any]]) -> str:
        """Prepare context from relevant documents"""
        if not relevant_docs:
            return "No relevant documents found."
        
        context_parts = []
        for i, doc in enumerate(relevant_docs, 1):
            source = doc.get("source", "Unknown")
            content = doc.get("content", "")
            distance = doc.get("distance", 0.0)
            
            # Add document with source information
            context_parts.append(f"Document {i} (Source: {source}):\n{content}")
        
        return "\n\n---\n\n".join(context_parts)

    def _create_rag_prompt(self, query: str, context: str) -> str:
        """Create a RAG prompt for Gemini"""
        prompt = f"""You are a helpful AI assistant specialized in Hero Vida strategy and business information. You have access to internal documents and data about Hero Vida.

Your task is to answer the user's question based on the provided context from the company's documents. Follow these guidelines:

1. Answer based primarily on the provided context
2. Be specific and detailed when the context supports it
3. If the context doesn't fully answer the question, say so and provide what information is available
4. Always cite which document(s) your answer comes from
5. Keep your response focused on Hero Vida strategy and business matters
6. Use professional business language appropriate for strategic discussions

CONTEXT FROM DOCUMENTS:
{context}

USER QUESTION: {query}

Please provide a comprehensive answer based on the context above. If you reference specific information, mention which document it came from."""

        return prompt

    async def generate_summary(self, documents: List[Dict[str, Any]]) -> str:
        """Generate a summary of uploaded documents"""
        def generate():
            if not documents:
                return "No documents to summarize."
            
            # Prepare content for summarization
            content_parts = []
            sources = set()
            
            for doc in documents[:10]:  # Limit to first 10 docs for summary
                content_parts.append(doc.get("content", "")[:500])  # Limit content length
                sources.add(doc.get("source", "Unknown"))
            
            combined_content = "\n\n".join(content_parts)
            
            prompt = f"""Please provide a concise summary of the following Hero Vida business documents:

DOCUMENTS:
{combined_content}

SOURCES: {', '.join(sources)}

Provide a summary that includes:
1. Main topics covered
2. Key strategic points
3. Important business information
4. Overall themes

Keep the summary concise but informative (2-3 paragraphs)."""
            
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Error generating summary: {str(e)}"
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, generate
        )
