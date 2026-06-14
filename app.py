import streamlit as st
from dotenv import load_dotenv
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(page_title="askmydoc", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;1,400&family=Inter:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #eaf4f0; }
.stApp { background-color: #eaf4f0; }
.main-header { background: #d6eee8; border-radius: 16px; padding: 36px 32px 0px; text-align: center; margin-bottom: 0; }
.main-header h1 { font-family: 'Playfair Display', serif; font-size: 38px; color: #1e4d43; line-height: 1.2; margin-bottom: 10px; }
.main-header h1 em { color: #2d6a5e; font-style: italic; }
.main-header p { font-size: 13px; color: #5a8a80; font-weight: 300; margin-bottom: 24px; }
.stars { font-size: 13px; color: #a8d4ca; letter-spacing: 2px; margin-bottom: 6px; }
.steps-row { display: flex; justify-content: center; align-items: center; gap: 8px; padding-bottom: 28px; flex-wrap: wrap; }
.step-item { display: flex; flex-direction: column; align-items: center; gap: 5px; }
.step-icon { width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; }
.step-label { font-size: 10px; color: #5a8a80; letter-spacing: 0.5px; }
.step-arrow { color: #a8d4ca; font-size: 18px; padding-bottom: 14px; }
.wave { width: 100%; height: 36px; background: #eaf4f0; clip-path: ellipse(55% 100% at 50% 100%); margin-top: -1px; }
.upload-box { background: #fff; border-radius: 14px; padding: 24px 16px; border: 1.5px dashed #a8d4ca; text-align: center; margin-bottom: 12px; }
.upload-box h4 { font-size: 14px; color: #1e4d43; font-weight: 500; margin: 10px 0 4px; }
.upload-box p { font-size: 11px; color: #8ab4ac; }
.status-pill { display: inline-flex; align-items: center; gap: 6px; background: #fff; border-radius: 20px; padding: 6px 14px; border: 0.5px solid #c8ddd9; font-size: 11px; color: #2d6a5e; margin-bottom: 12px; }
.green-dot { width: 8px; height: 8px; background: #4caf84; border-radius: 50%; display: inline-block; }
.chat-box { background: #fff; border-radius: 14px; padding: 18px; border: 0.5px solid #c8ddd9; min-height: 320px; margin-bottom: 12px; }
.msg-ai { background: #eaf4f0; border-radius: 12px 12px 12px 3px; padding: 11px 14px; font-size: 13px; color: #1e4d43; max-width: 87%; line-height: 1.6; margin-bottom: 10px; }
.msg-user { background: #2d6a5e; border-radius: 12px 12px 3px 12px; padding: 11px 14px; font-size: 13px; color: #fff; max-width: 78%; margin-left: auto; line-height: 1.6; margin-bottom: 10px; }
.msg-loading { background: #eaf4f0; border-radius: 12px 12px 12px 3px; padding: 11px 14px; font-size: 13px; color: #5a8a80; max-width: 87%; line-height: 1.6; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
.msg-error { background: #fff0f0; border-radius: 12px 12px 12px 3px; padding: 11px 14px; font-size: 13px; color: #c0392b; max-width: 87%; line-height: 1.6; margin-bottom: 10px; border: 0.5px solid #f5c6c6; }
.footer-bar { display: flex; justify-content: space-between; align-items: center; padding: 14px 0 0; border-top: 0.5px solid #c8ddd9; margin-top: 16px; }
.footer-left { font-size: 11px; color: #8ab4ac; }
.footer-pills { display: flex; gap: 8px; }
.footer-pill { background: #fff; border: 0.5px solid #c8ddd9; border-radius: 16px; padding: 4px 10px; font-size: 10px; color: #5a8a80; }
div[data-testid="stFileUploader"] > div { background: transparent !important; border: none !important; }
div[data-testid="stTextInput"] input { border-radius: 24px !important; border: 0.5px solid #c8ddd9 !important; background: #fff !important; font-size: 13px !important; padding: 10px 16px !important; }
div[data-testid="stTextInput"] input:focus { border-color: #2d6a5e !important; box-shadow: none !important; }
.stButton > button { background: #2d6a5e !important; color: #fff !important; border-radius: 20px !important; border: none !important; font-size: 12px !important; font-family: 'Inter', sans-serif !important; transition: background 0.2s !important; }
.stButton > button:hover { background: #1e4d43 !important; }
.sug-btn > button { background: #eaf4f0 !important; color: #2d6a5e !important; border-radius: 20px !important; border: 0.5px solid #c8ddd9 !important; font-size: 12px !important; width: 100% !important; text-align: left !important; padding: 8px 16px !important; }
.sug-btn > button:hover { background: #d6eee8 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
  <div class="stars">✦ &nbsp; ✦ &nbsp; ✦</div>
  <h1>your pdf,<br/><em>finally</em> answers back.</h1>
  <p>upload any document · ask in plain english · get instant answers</p>
  <div class="steps-row">
    <div class="step-item"><div class="step-icon" style="background:#c8e8e0">📄</div><div class="step-label">upload pdf</div></div>
    <div class="step-arrow">→</div>
    <div class="step-item"><div class="step-icon" style="background:#b8dff0">🤖</div><div class="step-label">ai reads it</div></div>
    <div class="step-arrow">→</div>
    <div class="step-item"><div class="step-icon" style="background:#d8eac0">💬</div><div class="step-label">you ask</div></div>
    <div class="step-arrow">→</div>
    <div class="step-item"><div class="step-icon" style="background:#f0e0f0">✨</div><div class="step-label">get answers</div></div>
  </div>
  <div class="wave"></div>
</div>
""", unsafe_allow_html=True)


# ── helpers ──────────────────────────────────────────────────────────────────

def extract_text(pdf_file):
    """Extract plain text from an uploaded PDF.

    Returns:
        str: The extracted text content.

    Raises:
        ValueError: If the PDF contains no extractable text (e.g. scanned image).
        RuntimeError: If PyMuPDF fails to open or read the file.
    """
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = "".join(page.get_text() for page in doc)
        if not text.strip():
            raise ValueError(
                "This PDF appears to be a scanned image with no extractable text. "
                "Please try a text-based PDF."
            )
        return text
    except ValueError:
        raise  # re-raise our own descriptive error as-is
    except Exception as e:
        raise RuntimeError(
            f"Could not read the PDF. Make sure the file isn't corrupted. "
            f"(Detail: {e})"
        )


def build_vector_store(text):
    """Chunk text and build a FAISS vector store.

    Raises:
        RuntimeError: If embedding or indexing fails.
    """
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(text)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return FAISS.from_texts(chunks, embedding=embeddings)
    except Exception as e:
        raise RuntimeError(
            f"Failed to build the search index. Please try uploading the PDF again. "
            f"(Detail: {e})"
        )


def get_answer(vector_store, question):
    """Run the RAG chain and return an answer string.

    Raises:
        ValueError: If the question is empty.
        RuntimeError: If the LLM call or retrieval fails.
    """
    if not question or not question.strip():
        raise ValueError("Please type a question before sending.")

    try:
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)
        prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context below. Be helpful and concise.

Context: {context}

Question: {question}
""")
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain.invoke(question)

    except Exception as e:
        error_msg = str(e).lower()
        if "api key" in error_msg or "authentication" in error_msg or "401" in error_msg:
            raise RuntimeError(
                "API key error — make sure your GROQ_API_KEY is set in the .env file."
            )
        elif "rate limit" in error_msg or "429" in error_msg:
            raise RuntimeError(
                "Rate limit hit. Please wait a moment and try again."
            )
        elif "timeout" in error_msg or "connection" in error_msg:
            raise RuntimeError(
                "Connection issue. Check your internet and try again."
            )
        else:
            raise RuntimeError(
                f"Something went wrong while getting your answer. Please try again. "
                f"(Detail: {e})"
            )


# ── session state ─────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "hi! drop in your pdf and i'll read it for you 🌿"}]
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ── layout ────────────────────────────────────────────────────────────────────

col1, col2 = st.columns([1, 1.4], gap="medium")

with col1:
    st.markdown('<div class="upload-box"><div style="font-size:28px">☁️</div><h4>drop your pdf here</h4><p>lecture notes, textbooks, research papers</p></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file and not st.session_state.pdf_ready:
        with st.spinner("reading your document..."):
            try:
                text = extract_text(uploaded_file)
                st.session_state.vector_store = build_vector_store(text)
                st.session_state.pdf_ready = True
                st.session_state.messages = [
                    {"role": "ai", "content": "hi! i've read your document 🌿 ask me anything about it!"}
                ]
            except (ValueError, RuntimeError) as e:
                # Show the friendly error message in the chat panel
                st.session_state.messages = [
                    {"role": "error", "content": str(e)}
                ]
                st.session_state.pdf_ready = False

    if st.session_state.pdf_ready:
        st.markdown('<div class="status-pill"><span class="green-dot"></span> ai is ready · ask away!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-pill"><span style="width:8px;height:8px;background:#c8ddd9;border-radius:50%;display:inline-block"></span> waiting for your pdf</div>', unsafe_allow_html=True)

    st.markdown("<div style='background:#fff;border-radius:14px;padding:14px 16px;border:0.5px solid #c8ddd9;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;color:#8ab4ac;letter-spacing:0.8px;margin-bottom:10px;text-transform:uppercase;'>✦ try asking</div>", unsafe_allow_html=True)
    suggestions = ["⌨ summarise this document", "📋 what are the key points?", "❓ explain section 2 simply"]
    for sug in suggestions:
        st.markdown('<div class="sug-btn">', unsafe_allow_html=True)
        if st.button(sug, key=f"sug_{sug}"):
            st.session_state.pending_question = sug.split(" ", 1)[1]
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    chat_html = '<div class="chat-box">'
    for msg in st.session_state.messages:
        if msg["role"] == "ai":
            chat_html += f'<div class="msg-ai">{msg["content"]}</div>'
        elif msg["role"] == "user":
            chat_html += f'<div class="msg-user">{msg["content"]}</div>'
        elif msg["role"] == "error":
            chat_html += f'<div class="msg-error">⚠️ {msg["content"]}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    input_col, btn_col = st.columns([6, 1])
    with input_col:
        question = st.text_input("", placeholder="ask anything about your pdf...", label_visibility="collapsed", key="question_input")
    with btn_col:
        send = st.button("🔍")

    final_question = None
    if send and question:
        final_question = question
    elif st.session_state.pending_question:
        final_question = st.session_state.pending_question
        st.session_state.pending_question = None

    if final_question:
        if st.session_state.pdf_ready:
            st.session_state.messages.append({"role": "user", "content": final_question})
            st.rerun()
        else:
            st.warning("please upload a pdf first! 🌿")

    last = st.session_state.messages[-1] if st.session_state.messages else None
    if last and last["role"] == "user":
        st.markdown('<div class="msg-loading">🌿 reading and thinking...</div>', unsafe_allow_html=True)
        with st.spinner(""):
            try:
                answer = get_answer(st.session_state.vector_store, last["content"])
                st.session_state.messages.append({"role": "ai", "content": answer + " ✦"})
            except (ValueError, RuntimeError) as e:
                st.session_state.messages.append({"role": "error", "content": str(e)})
        st.rerun()

st.markdown("""
<div class="footer-bar">
  <div class="footer-left">✦ askmydoc — made with care</div>
  <div class="footer-pills">
    <div class="footer-pill">🔒 private</div>
    <div class="footer-pill">⚡ fast</div>
    <div class="footer-pill">🌿 free</div>
  </div>
</div>
""", unsafe_allow_html=True)
