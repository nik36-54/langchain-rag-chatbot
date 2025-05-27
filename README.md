# 🔍 LangChain RAG Chatbot – Production-Ready AI Chat Assistant

## **Overview**
This project is a production-ready **LLM-powered chatbot** built using:
- 🧠 **LangChain** for Retrieval-Augmented Generation (RAG)
- 📄 **Vector DB (Chroma)** for document chunk search
- ⚡ **FastAPI** as the backend API
- 🖥️ **Streamlit** frontend for real-time interaction
- 🚀 **Railway** for full-stack deployment

It allows users to query large PDF or text documents (up to 100MB+) and get accurate, contextual answers in milliseconds.

---

## 💡 Key Features

| Feature | Description |
|--------|-------------|
| 🧠 **RAG Pipeline** | Combines LLM with vector search for grounded, context-aware responses |
| ⚡ **Fast Response** | Sub-second answers using GPT-4 Turbo and Chroma |
| 📄 **Large Document Support** | Efficient chunking, embedding, and retrieval for PDFs/Markdowns |
| 💬 **Streamlit Interface** | Chat-like UI to interact with backend |
| 🔐 **Environment-based API Key Management** | Secure use of OpenAI API |
| 📦 **Production Deployable** | Fully deployable via Railway (frontend + backend) |

---

## 🧪 Benchmark Highlights

| Metric | Value |
|--------|-------|
| Document Size | 100MB PDF |
| Indexed Chunks | 12,000+ |
| Query Latency | ~500–800ms |
| Confidence | 0.85+ (based on vector similarity) |
| Cold Start | ~3s on free tier (Railway) |

---

## 📁 Tech Stack

- **LangChain**: RAG orchestration
- **OpenAI**: LLM + Embeddings
- **Chroma DB**: Vector similarity search
- **FastAPI**: Backend API
- **Streamlit**: Frontend interface
- **Railway**: Deployment platform

---

## 🚀 Use Cases

- Technical documentation Q&A assistant  
- Internal knowledge base chatbot  
- Legal/Policy document search bot  
- Customer support agent with contextual memory
