"""Document processing utilities for PDF text extraction and chunking."""

import PyPDF2
from typing import List, Dict
import re

class DocumentProcessor:
    """Handles PDF text extraction and document chunking."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                # print("-------------->",page_text)
                if page_text.strip():
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text
            
            return self._clean_text(text)
        
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere
        text = re.sub(r'[^\w\s\-.,!?;:()\[\]"]', '', text)
        return text.strip()
    
    def chunk_text(self, text: str) -> List[Dict[str, any]]:
        """Split text into overlapping chunks for better retrieval."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            # Create metadata for each chunk
            chunk_metadata = {
                'chunk_id': len(chunks),
                'start_word': i,
                'end_word': min(i + self.chunk_size, len(words)),
                'word_count': len(chunk_words)
            }
            
            chunks.append({
                'text': chunk_text,
                'metadata': chunk_metadata
            })
        
        return chunks
