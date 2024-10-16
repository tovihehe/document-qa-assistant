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

4. Ensure the Ollama app is installed on your device, and do the following to pull the models:
   ```bash
   # Follow Ollama's installation instructions to start the server.
   ```

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501`.

3. Upload one or more PDF documents using the file uploader.

4. Wait for the documents to be processed and then enter your question in the text input field.

5. Click the 'Ask' button to get a response based on the document content.

## How It Works

- The application extracts text from uploaded PDF documents using PyPDF2.
- Text is split into manageable chunks, which are then embedded into vector representations using an open-source embedding model of Ollama.
- A FAISS index is created and updated with these embeddings, allowing for efficient retrieval of relevant text based on user queries.

## Notes

- **Dependencies**: Ensure all required libraries are installed. Use specific versions in `requirements.txt` to avoid compatibility issues.
- **Environment Variables**: The application sets `KMP_DUPLICATE_LIB_OK = TRUE` to prevent OpenMP errors.
- **Local Ollama API**: The Ollama API must be running locally for the application to function correctly.
- **PDF Processing**: The application supports only PDF files. Ensure documents are in this format.
- **FAISS Index**: The FAISS index is updated incrementally. Delete `embeddings.index` and `text_chunks.txt` for a fresh start.
- **Text Chunk Size**: Maximum chunk size for text splitting is set to 500 characters.
- **Conversation History**: Maintains a history of user interactions for context in responses.

## Attention Points

- **Performance**: Processing very large PDF files may affect performance.
- **Security**: Be cautious with sensitive information in uploaded documents.
- **User Input Validation**: Consider implementing input validation for better user experience.
- **Error Handling**: Handle exceptions gracefully, especially for file operations and API calls.
- **Documentation**: Keep the README and inline code documentation updated.
- **Testing**: Regularly test the application with various PDFs for consistent behavior.
- **Feedback Loop**: Encourage user feedback to guide future improvements.
- **Future Improvements**: Potential features include support for more file formats and enhanced UI/UX.

## Contributing

Contributions are welcome! Please create a pull request for any improvements or bug fixes. Make sure to follow the project's coding style and include tests for any new functionality.
