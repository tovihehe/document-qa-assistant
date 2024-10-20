# Document Q&A Assistant

📚 **Document Q&A Assistant** is a Streamlit application that allows users to upload PDF documents and ask questions about their content. The application utilizes Ollama for language processing and FAISS for efficient similarity searching of text embeddings.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Notes](#notes)
- [Attention Points](#attention-points)
- [Contributing](#contributing)
- [License](#license)

## Features

- Upload multiple PDF documents.
- Extract and process text from PDFs.
- Ask questions about the content using natural language.
- Incrementally update embeddings and FAISS index with new documents.

## Requirements

- Python 3.9 or higher
- Streamlit
- PyPDF2
- Torch
- Ollama
- FAISS
- Langchain

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/document-qa-assistant.git
   cd document-qa-assistant
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv\Scripts\activate # On Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
> [!NOTE]
> Ensure all required libraries are installed. Use specific versions in `requirements.txt` to avoid compatibility issues.


4. Ensure the Ollama app is installed on your device, and do the following to pull the models:
   ```bash
   # Follow Ollama's installation instructions to start the server and do the following commands to pull the models 
   ollama pull llama3
   ollama pull mxbai-embed-large 
   ```

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run local-rag.py
   ```

2. Open your web browser and go to `http://localhost:8501`.

3. Upload one or more PDF documents using the file uploader.
   
> [!CAUTION]
> Processing very large PDF files may affect performance.

> [!NOTE]
> The application supports only PDF files. Ensure documents are in this format.

5. Wait for the documents to be processed and then enter your question in the text input field.

6. Click the 'Ask' button to get a response based on the document content.

## How It Works

- The application extracts text from uploaded PDF documents using PyPDF2.
- Text is split into manageable chunks, which are then embedded into vector representations using an open-source embedding model of Ollama (mxbai-embed-large).
- A FAISS index is created and updated with these embeddings, allowing for efficient retrieval of relevant text based on user queries.
> [!NOTE]
> The FAISS index is updated incrementally. Delete `embeddings.index` and `text_chunks.txt` for a fresh start.


## Contributing

Contributions are welcome! Please create a pull request for any improvements or bug fixes. Make sure to follow the project's coding style and include tests for any new functionality.
