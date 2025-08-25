import os
import pandas as pd
import PyPDF2
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
import asyncio
from concurrent.futures import ThreadPoolExecutor

class DocumentProcessor:
    def __init__(self):
        self.chunk_size = int(os.getenv("CHUNK_SIZE", 1000))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 200))
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def process_document(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Process a document and return chunks with metadata"""
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext == '.pdf':
            return await self._process_pdf(file_path, filename)
        elif file_ext == '.csv':
            return await self._process_csv(file_path, filename)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    async def _process_pdf(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Process PDF file and extract text chunks"""
        def extract_pdf_text():
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text.strip():  # Only add non-empty pages
                        text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            return text
        
        # Extract text in executor to avoid blocking
        text = await asyncio.get_event_loop().run_in_executor(
            self.executor, extract_pdf_text
        )
        
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF file")
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create document chunks with metadata
        document_chunks = []
        for i, chunk in enumerate(chunks):
            if chunk.strip():  # Only include non-empty chunks
                document_chunks.append({
                    "content": chunk.strip(),
                    "metadata": {
                        "source": filename,
                        "chunk_id": i,
                        "type": "pdf",
                        "chunk_size": len(chunk)
                    },
                    "source": filename
                })
        
        return document_chunks

    async def _process_csv(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Process CSV file and create text chunks from rows"""
        def read_csv():
            try:
                # Try different encodings
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                        return df
                    except UnicodeDecodeError:
                        continue
                # If all encodings fail, try with error handling
                return pd.read_csv(file_path, encoding='utf-8', errors='ignore')
            except Exception as e:
                raise ValueError(f"Error reading CSV file: {str(e)}")
        
        # Read CSV in executor
        df = await asyncio.get_event_loop().run_in_executor(
            self.executor, read_csv
        )
        
        if df.empty:
            raise ValueError("CSV file is empty or could not be read")
        
        # Convert DataFrame to text chunks
        document_chunks = []
        
        # Add column headers as first chunk
        headers_text = f"CSV File: {filename}\nColumns: {', '.join(df.columns.tolist())}\n\n"
        headers_text += "Column Details:\n"
        for col in df.columns:
            headers_text += f"- {col}: {df[col].dtype}\n"
        
        document_chunks.append({
            "content": headers_text,
            "metadata": {
                "source": filename,
                "chunk_id": 0,
                "type": "csv_headers",
                "chunk_size": len(headers_text)
            },
            "source": filename
        })
        
        # Process rows in batches to create meaningful chunks
        batch_size = 50  # Adjust based on your needs
        for batch_start in range(0, len(df), batch_size):
            batch_end = min(batch_start + batch_size, len(df))
            batch_df = df.iloc[batch_start:batch_end]
            
            # Convert batch to readable text
            batch_text = f"Rows {batch_start + 1} to {batch_end} from {filename}:\n\n"
            
            for idx, row in batch_df.iterrows():
                row_text = f"Row {idx + 1}:\n"
                for col, value in row.items():
                    if pd.notna(value):  # Only include non-null values
                        row_text += f"  {col}: {value}\n"
                row_text += "\n"
                batch_text += row_text
            
            # Split large batches if needed
            if len(batch_text) > self.chunk_size * 2:
                chunks = self.text_splitter.split_text(batch_text)
                for i, chunk in enumerate(chunks):
                    if chunk.strip():
                        document_chunks.append({
                            "content": chunk.strip(),
                            "metadata": {
                                "source": filename,
                                "chunk_id": len(document_chunks),
                                "type": "csv_data",
                                "batch_start": batch_start,
                                "batch_end": batch_end,
                                "sub_chunk": i,
                                "chunk_size": len(chunk)
                            },
                            "source": filename
                        })
            else:
                document_chunks.append({
                    "content": batch_text.strip(),
                    "metadata": {
                        "source": filename,
                        "chunk_id": len(document_chunks),
                        "type": "csv_data",
                        "batch_start": batch_start,
                        "batch_end": batch_end,
                        "chunk_size": len(batch_text)
                    },
                    "source": filename
                })
        
        return document_chunks
