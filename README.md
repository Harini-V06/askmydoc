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
