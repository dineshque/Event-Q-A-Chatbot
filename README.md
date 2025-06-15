# AI-Powered Event Q&A Chatbot using RAG Architecture

A production-ready chatbot that enables natural language queries on event documents using Retrieval-Augmented Generation (RAG). Built with Streamlit, Sentence Transformers, ChromaDB, and local LLM inference via Ollama.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Features

- **PDF Document Processing**: Extract and chunk text from event PDFs automatically
- **Semantic Search**: Vector-based similarity search using Sentence Transformers
- **Local LLM Integration**: No external API dependencies - runs entirely offline
- **Interactive Chat Interface**: Streamlit-powered web UI with chat history
- **Source Attribution**: View relevant document chunks for each response
- **Real-time Processing**: Fast document indexing and query responses

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **Document Processing** | PyPDF2, Custom text chunking |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **Vector Database** | ChromaDB |
| **LLM** | Ollama (Mistral model) |
| **Language** | Python 3.8+ |

## 📋 Prerequisites

- Python 3.8 or higher
- Ollama installed and running
- At least 8GB RAM (recommended for local LLM)

## 🔧 Installation

### 1. Clone the Repository
git clone https://github.com/DineshKumawat/ Event Q&A Chatbot using RAG.git
cd  Event Q&A Chatbot using RAG


### 2. Create Virtual Environment

python -m venv venv

Windows
venv\Scripts\activate


### 3. Install Dependencies

pip install -r requirements.txt


### 4. Install and Setup Ollama

#### Windows:
1. Download from [https://ollama.ai](https://ollama.ai)
2. Install the executable
3. Open Command Prompt and run:


ollama pull mistral
ollama serve



## 🚀 Usage

### 1. Start Ollama Server

ollama serve
> **Note**: Keep this terminal open while using the application.

### 2. Run the Application
streamlit run app.py






























