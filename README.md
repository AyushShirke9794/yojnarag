# YojanaRAG

## Explainable Multilingual Government Scheme Question Answering and Eligibility Assistance Using RAG

YojanaRAG is an AI & Data Science mini-project that helps users explore government scheme information through a multilingual question-answering interface.

### Features

- Questions in English, Hindi, and Marathi
- PDF-based document processing
- Multilingual sentence embeddings
- FAISS semantic retrieval
- BM25 keyword retrieval
- Reciprocal Rank Fusion for hybrid search
- Cross-encoder reranking
- Gemini-based grounded answer generation
- Source page references
- Offline evidence fallback when generation is unavailable
- Government scheme information and eligibility assistance
- Streamlit web interface

### Architecture

Government PDF
    |
    v
Text Extraction
    |
    v
Text Chunking
    |
    v
Multilingual Embeddings
    |
    +--> FAISS Semantic Retrieval
    |
    +--> BM25 Keyword Retrieval
              |
              v
       Hybrid Retrieval (RRF)
              |
              v
       Cross-Encoder Reranking
              |
              v
       Gemini Grounded Answer
              |
              v
       Streamlit User Interface

The eligibility assistance component reads structured scheme information and uses a separate rule-evaluation engine. It does not issue official eligibility approvals.

### Technology Stack

Python, Streamlit, FAISS, BM25, Sentence Transformers, Cross-Encoder, Google Gemini API, Pydantic, Pytest.

### Dataset and Source Limitations

The currently indexed knowledge base contains PM-KISAN operational guidelines dated 29 March 2020.

This source is classified as historical. Current eligibility requirements and required documents have not been independently verified.

The system is a technical and educational prototype. It must not be used as an authoritative source for current government benefits or eligibility decisions.

### Installation

Create a Python virtual environment and activate it.

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file containing:

```text
GEMINI_API_KEY=your_api_key_here
```

Never commit the actual API key to Git.

### Run the Application

```powershell
python -m streamlit run app.py
```

Open http://localhost:8501

### Run Automated Tests

```powershell
python -m pytest tests -v
```

### Testing Status

Eight foundational automated tests passed during local development.

The tests cover database loading, historical-source safety, basic rule evaluation, and required project artifacts. They do not establish complete retrieval accuracy or multilingual answer quality.

### Future Improvements

- Expand the number of government schemes
- Verify current official eligibility rules
- Add more comprehensive multilingual evaluation
- Deploy the application online

### Disclaimer

YojanaRAG is a student mini-project. Always consult the relevant official government portal for current scheme rules and application decisions.
