"""Vector database operations using ChromaDB."""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import numpy as np

class VectorStore:
    """Manages vector embeddings and similarity search using ChromaDB."""
    
    def __init__(self, db_path: str, collection_name: str, embedding_model: str):
        self.db_path = db_path
        self.collection_name = collection_name
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Get existing collection or create new one."""
        try:
            collection = self.client.get_collection(name=self.collection_name)
        except:
            collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Event document embeddings"}
            )
        return collection
    
    def add_documents(self, chunks: List[Dict[str, any]]) -> None:
        """Add document chunks to vector database."""
        texts = [chunk['text'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts, convert_to_tensor=False)
        
        # Create unique IDs for each chunk
        ids = [f"chunk_{i}" for i in range(len(texts))]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, any]]:
        """Search for similar documents based on query."""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query], convert_to_tensor=False)
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def clear_collection(self) -> None:
        """Clear all documents from collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self._get_or_create_collection()
        except:
            pass
