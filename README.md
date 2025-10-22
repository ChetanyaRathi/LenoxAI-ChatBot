# Nova AI - Personal Resume Chatbot

Welcome to Nova! This is an interactive AI-powered chatbot built to answer any question about Chetanya Rathi's professional resume. Instead of just reading a static PDF, you can ask Nova questions in natural language.

This project uses a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, context-aware answers. The backend is powered by Python, Flask, and Google's Gemini AI, while the frontend is a dynamic chat interface built with React.


---

## 🚀 Key Features

* **Natural Language Q&A:** Ask complex questions like, "What projects has he done using Python?" or "Tell me more about his internship experience."
* **RAG Pipeline:** Uses a LangChain-powered RAG pipeline to retrieve the most relevant resume sections before generating an answer.
* **Vector Search:** Employs a ChromaDB vectorstore for fast and efficient similarity search on resume content.
* **Gemini-Powered:** Leverages Google's powerful `gemini-2.5-flash` model via the Vertex AI API for human-like and accurate responses.
* **Decoupled Architecture:** A scalable Flask REST API backend serves the AI logic to a modern React frontend.

---

## 🛠 Tech Stack

This project is built with a modern, full-stack architecture:

| Area | Technology |
| :--- | :--- |
| **Backend** | Python, Flask, LangChain |
| **AI / LLM** | Google Vertex AI (Gemini 2.5 Flash, Text Embeddings) |
| **Vector Database** | ChromaDB |
| **Frontend** | React, Vite |
| **Styling** | Tailwind CSS *(or add your styling library)* |

---

## ⚙️ Getting Started

Follow these instructions to get a local copy up and running on your machine.

### Prerequisites

* Python 3.9+
* Node.js 18+ and npm
* Git

### 1. Clone the Repository

```bash
git clone [https://github.com/ChetanyaRathi/Your-Repo-Name.git](https://github.com/ChetanyaRathi/Your-Repo-Name.git)
cd Your-Repo-Name
