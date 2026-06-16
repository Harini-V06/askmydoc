# askmydoc 🌿

A RAG-powered PDF chatbot — upload any document and ask questions in plain English.

**🌐 Live Demo → [askmydoc6767.streamlit.app](https://askmydoc6767.streamlit.app/)**

---

## What it does

Upload a PDF (lecture notes, research paper, textbook) and ask questions about it in natural language. The app retrieves the most relevant chunks from your document and generates a grounded answer — no hallucinations about content that isn't there.

---

## Architecture

```
PDF Upload
  → Text Extraction     PyMuPDF (fitz)
  → Chunking            RecursiveCharacterTextSplitter (1000 tokens, 200 overlap)
  → Embedding           HuggingFace all-MiniLM-L6-v2
  → Vector Store        FAISS (in-memory)
  → Retrieval           Top-3 most relevant chunks
  → Generation          Groq · LLaMA 3.1 8B Instant
  → Answer
```

Built with LangChain LCEL — retrieval and generation are composed as a declarative chain rather than imperative function calls.

---

## Tech Stack

| Component | Tool |
|---|---|
| UI | Streamlit |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector Store | FAISS |
| LLM | Groq (LLaMA 3.1 8B Instant) |
| Orchestration | LangChain LCEL |
| PDF Parsing | PyMuPDF |

---

## Setup

```bash
git clone https://github.com/Harini-V06/askmydoc
cd askmydoc
pip install -r requirements.txt
```

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_key_here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

Run the app:

```bash
streamlit run app.py
```

---

## What I'd improve next

- Persistent vector store so re-uploads aren't needed each session
- Conversation memory for follow-up questions
- Multi-document support
- Retrieval quality metrics (precision@k)
---
## Screenshots 📷
<img width="958" height="470" alt="askmydoc_0" src="https://github.com/user-attachments/assets/2428b365-dcc1-441a-8a11-d6f55f04acb2" />
<img width="956" height="472" alt="askmydoc_1" src="https://github.com/user-attachments/assets/2966f310-7272-4c0b-a23d-6b0593bedd62" />
<img width="943" height="431" alt="askmydoc_2" src="https://github.com/user-attachments/assets/d2e59e57-8d0e-47a2-94f7-9176df51eefb" />

---
