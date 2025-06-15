"""Configuration settings for the RAG chatbot."""

import os

# Vector Database Configuration
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "event_documents"

# Embedding Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Text Processing Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# LLM Configuration
OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "mistral"

# Streamlit Configuration
PAGE_TITLE = "Event Q&A Chatbot"
PAGE_ICON = "Chat"
