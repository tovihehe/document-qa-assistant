import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Add this to bypass the OpenMP error

import streamlit as st
import PyPDF2
import re
import torch
import ollama
import faiss
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Function to convert PDF to text and return it
def convert_pdf_to_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    text = ''
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        if page.extract_text():
            text += page.extract_text() + " "
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

# Function to process content and split it into chunks
def split_text_into_chunks(content, max_chunk_size=500):
    splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_size, chunk_overlap=0)
    chunks = splitter.split_text(content)
    return chunks

# Function to embed text and return embeddings using Ollama
def embed_text(text_chunks):
    embeddings = []
    for chunk in text_chunks:
        response = ollama.embeddings(model='mxbai-embed-large', prompt=chunk)
        embeddings.append(response["embedding"])
    return torch.tensor(embeddings)

# Function to save or update the FAISS index and text chunks
def update_faiss_index(embeddings_tensor, text_chunks):
    if os.path.exists("embeddings.index"):
        # Load existing index
        index = faiss.read_index("embeddings.index")
        
        # Add new embeddings to the existing index
        index.add(embeddings_tensor.numpy())  
    else:
        # Create new index if it doesn't exist
        index = faiss.IndexFlatL2(embeddings_tensor.shape[1])
        index.add(embeddings_tensor.numpy())  # Add embeddings to index

    # Write the updated index to the file
    faiss.write_index(index, "embeddings.index")

    # Update the text chunks file
    with open("text_chunks.txt", "a", encoding="utf-8") as file:
        file.writelines([chunk + "\n" for chunk in text_chunks])  # Append new chunks

    return index

# Load FAISS index (no need to pass embedding_dim)
def load_faiss_index():
    if os.path.exists("embeddings.index"):
        index = faiss.read_index("embeddings.index")
    else:
        raise FileNotFoundError("FAISS index file not found")
    return index

# Get relevant context using FAISS
def get_relevant_context_faiss(user_input, index, text_chunks, top_k=3):
    user_input_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=user_input)["embedding"]
    user_input_embedding = torch.tensor(user_input_embedding).unsqueeze(0).numpy()
    
    distances, indices = index.search(user_input_embedding, top_k)
    relevant_chunks = [text_chunks[idx] for idx in indices[0]]
    return relevant_chunks

# Function to interact with Ollama model
def ollama_chat(user_input, system_message, faiss_index, text_chunks, ollama_model, conversation_history):
    relevant_context = get_relevant_context_faiss(user_input, faiss_index, text_chunks, top_k=3)
    context_str = "\n".join(relevant_context) if relevant_context else ""
    
    user_input_with_context = context_str + "\n\n" + user_input if relevant_context else user_input
    conversation_history.append({"role": "user", "content": user_input_with_context})
    
    messages = [{"role": "system", "content": system_message}] + conversation_history
    response = client.chat.completions.create(model=ollama_model, messages=messages)
    
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

# Streamlit app
def main():
    st.set_page_config(page_title="Document Q&A Assistant", layout="wide")
    
    st.title("📚 Document Q&A Assistant")
    st.markdown("Upload your documents and ask questions about their content.")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Document Upload")
        pdf_file = st.file_uploader("Upload PDFs", type=["pdf"], help="Select one or more PDF files", key="pdf_file")
        
        if pdf_file:
            with st.spinner("Extracting text from PDFs..."):
                text = convert_pdf_to_text(pdf_file)
            with st.spinner("Chunking text..."):
                text_chunks = split_text_into_chunks(text)
            with st.spinner("Embedding text..."):
                embeddings_tensor = embed_text(text_chunks)
            with st.spinner("Saving embeddings..."):
                faiss_index = update_faiss_index(embeddings_tensor, text_chunks)
            st.success("PDF content processed and embedded successfully!")
    
    with col2:
        st.subheader("Ask Questions")
        user_input = st.text_input("What would you like to know about the documents?", 
                                   placeholder="Enter your question here...")
        
        if st.button("Ask", type="primary"):
            if user_input:
                if os.path.exists("embeddings.index"):
                    faiss_index = load_faiss_index()
                    conversation_history = []
                    system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text"
                    # Open the text chunks file
                    with open("text_chunks.txt", "r", encoding="utf-8") as file:
                        text_chunks = file.readlines()

                    with st.spinner("Analyzing documents and generating response..."):
                        response = ollama_chat(user_input, system_message, faiss_index, text_chunks, "llama3", conversation_history)
                    
                    st.markdown("### 🤖 Assistant's Response:")
                    st.markdown(response)
                else:
                    st.warning("Please upload a document first.")
            else:
                st.warning("Please enter a question.")
    
    st.markdown("---")
    st.markdown("### How to use this app:")
    st.markdown("""
    1. Upload one or more PDF documents using the file uploader.
    2. Wait for the documents to be processed.
    3. Enter your question in the text input field.
    4. Click the 'Ask' button to get a response based on the document content.
    """)

if __name__ == "__main__":
    # Configuration for the Ollama API client
    global client
    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='llama3'
    )
    main()