# 🌿 askmydoc

> upload any pdf. ask anything. get instant answers.

**Live Demo →** [askmydoc6767.streamlit.app](https://askmydoc6767.streamlit.app)
---

## 📌 what is this?

askmydoc is a RAG (Retrieval Augmented Generation) powered chatbot that lets you have a conversation with any PDF document. upload a lecture note, textbook, or research paper — and ask questions in plain english.

built as part of a self-directed Agentic AI learning curriculum.

---

## ✨ features

- 📄 upload any PDF document
- 🤖 AI reads and processes it into a vector database
- 💬 ask questions in plain english and get instant answers
- ⌨ clickable suggestion prompts to get started quickly
- 🌿 loading indicator while the AI is thinking
- 🔒 your document stays private — nothing is stored

---

## 🛠️ tech stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Groq (llama-3.1-8b-instant) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) — runs locally |
| Vector Store | FAISS |
| PDF Reading | PyMuPDF (fitz) |
| Orchestration | LangChain |

---

## 🚀 run locally

```bash
# clone the repo
git clone https://github.com/Harini-V06/askmydoc.git
cd askmydoc

# install dependencies
pip install -r requirements.txt

# create a .env file
echo "GROQ_API_KEY=your_key_here" > .env

# run the app
streamlit run app.py
```

get a free Groq API key at [console.groq.com](https://console.groq.com)

---

## 🗂️ how it works

```
PDF uploaded
     ↓
text extracted (PyMuPDF)
     ↓
split into chunks (LangChain text splitter)
     ↓
each chunk embedded into a vector (HuggingFace)
     ↓
stored in FAISS vector database
     ↓
user asks a question
     ↓
question embedded → similar chunks retrieved
     ↓
chunks + question sent to Groq LLM
     ↓
answer returned ✦
```
---
 
## What I learned building this
 
- How RAG pipelines work end-to-end: chunking strategy matters a lot for answer quality
- FAISS similarity search and how embedding distance maps to semantic relevance  
- LangChain LCEL for composing retrieval chains
- Managing Streamlit session state for multi-turn chat
---
## Screenshots 📷
<img width="958" height="470" alt="askmydoc_0" src="https://github.com/user-attachments/assets/2428b365-dcc1-441a-8a11-d6f55f04acb2" />
<img width="956" height="472" alt="askmydoc_1" src="https://github.com/user-attachments/assets/2966f310-7272-4c0b-a23d-6b0593bedd62" />
<img width="943" height="431" alt="askmydoc_2" src="https://github.com/user-attachments/assets/d2e59e57-8d0e-47a2-94f7-9176df51eefb" />

---
