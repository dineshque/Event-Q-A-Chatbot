"""Streamlit web application for the RAG chatbot."""

import streamlit as st
from rag_chatbot import RAGChatbot
import config

# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide"
)

# Initialize chatbot
@st.cache_resource
def initialize_chatbot():
    return RAGChatbot()

def main():
    st.title(" Event Q&A Chatbot")
    st.markdown("Upload an event PDF and ask questions about speakers, sessions, agenda, and more!")
    
    # Initialize chatbot
    chatbot = initialize_chatbot()
    
    # Sidebar for document upload
    with st.sidebar:
        st.header(" Document Upload")
        uploaded_file = st.file_uploader(
            "Upload Event PDF",
            type=['pdf'],
            help="Upload a PDF containing event information"
        )
        
        if uploaded_file is not None:
            if st.button("Process Document", type="primary"):
                with st.spinner("Processing document..."):
                    result = chatbot.process_document(uploaded_file)
                
                if result['success']:
                    st.success(result['message'])
                    st.info(f" **Statistics:**\n- Chunks created: {result['chunks_count']}\n- Total words: {result['total_words']}")
                else:
                    st.error(result['message'])
        
        # LLM Status
        st.header("🔧 System Status")
        if chatbot.llm.is_available():
            st.success(" Ollama LLM Available")
        else:
            st.error(" Ollama LLM Unavailable")
            st.info("Please ensure Ollama is running with Mistral model")
    
    # Main chat interface
    st.header(" Ask Questions")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                if message["sources"]:
                    with st.expander(" Sources"):
                        for i, source in enumerate(message["sources"]):
                            st.markdown(f"**Source {i+1}:**")
                            st.text(source["text_preview"])
                            if source["relevance_score"]:
                                st.caption(f"Relevance: {source['relevance_score']:.3f}")
                            st.divider()
    
    # Chat input
    if prompt := st.chat_input("Ask about the event..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chatbot.answer_question(prompt)
            
            if response['success']:
                st.markdown(response['answer'])
                
                # Show sources
                if response['sources']:
                    with st.expander(" Sources"):
                        for i, source in enumerate(response['sources']):
                            st.markdown(f"**Source {i+1}:**")
                            st.text(source["text_preview"])
                            if source["relevance_score"]:
                                st.caption(f"Relevance: {source['relevance_score']:.3f}")
                            st.divider()
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response['answer'],
                    "sources": response['sources']
                })
            else:
                st.error(response['answer'])
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response['answer']
                })
    
    # Example queries
    st.header(" Example Questions")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **About Speakers:**
        - Who are the keynote speakers?
        - What is [Speaker Name]'s background?
        - Which speakers are from [Company/Organization]?
        """)
    
    with col2:
        st.markdown("""
        **About Sessions:**
        - What sessions are on [Topic]?
        - When is the [Session Name] session?
        - What are the workshop topics?
        """)

if __name__ == "__main__":
    main()
