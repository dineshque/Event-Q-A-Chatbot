"""Main RAG chatbot class that orchestrates all components."""

from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_interface import OllamaLLM
from typing import List, Dict, Optional
import config

class RAGChatbot:
    """Main chatbot class implementing RAG architecture."""
    
    def __init__(self):
        self.document_processor = DocumentProcessor(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        
        self.vector_store = VectorStore(
            db_path=config.CHROMA_DB_PATH,
            collection_name=config.COLLECTION_NAME,
            embedding_model=config.EMBEDDING_MODEL
        )
        
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.DEFAULT_MODEL
        )
        
        self.is_initialized = False
    
    def process_document(self, pdf_file) -> Dict[str, any]:
        """Process uploaded PDF and store in vector database."""
        try:
            # Extract text from PDF
            text = self.document_processor.extract_text_from_pdf(pdf_file)
            
            # Chunk the text
            chunks = self.document_processor.chunk_text(text)
            
            # Clear existing data and add new chunks
            self.vector_store.clear_collection()
            self.vector_store.add_documents(chunks)
            
            self.is_initialized = True
            
            return {
                'success': True,
                'message': f'Successfully processed document with {len(chunks)} chunks.',
                'chunks_count': len(chunks),
                'total_words': len(text.split())
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error processing document: {str(e)}',
                'chunks_count': 0,
                'total_words': 0
            }
    
    def answer_question(self, question: str, top_k: int = 5) -> Dict[str, any]:
        """Answer question using RAG approach."""
        if not self.is_initialized:
            return {
                'success': False,
                'answer': 'Please upload and process a document first.',
                'sources': []
            }
        
        if not self.llm.is_available():
            return {
                'success': False,
                'answer': 'LLM service (Ollama) is not available. Please ensure Ollama is running.',
                'sources': []
            }
        
        try:
            # Retrieve relevant chunks
            relevant_chunks = self.vector_store.search_similar(question, top_k=top_k)
            
            if not relevant_chunks:
                return {
                    'success': False,
                    'answer': 'No relevant information found in the document.',
                    'sources': []
                }
            
            # Generate response using LLM
            answer = self.llm.generate_response(question, relevant_chunks)
            
            # Prepare source information
            sources = [
                {
                    'chunk_id': chunk['metadata']['chunk_id'],
                    'text_preview': chunk['text'][:200] + '...' if len(chunk['text']) > 200 else chunk['text'],
                    'relevance_score': 1 - chunk['distance'] if chunk['distance'] else None
                }
                for chunk in relevant_chunks
            ]
            
            return {
                'success': True,
                'answer': answer,
                'sources': sources
            }
        
        except Exception as e:
            return {
                'success': False,
                'answer': f'Error generating answer: {str(e)}',
                'sources': []
            }
