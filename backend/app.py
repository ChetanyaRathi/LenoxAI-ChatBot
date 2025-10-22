import os
import google.auth
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- LangChain & Google Vertex AI ---
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings, VertexAI
from langchain_community.vectorstores import Chroma

# --- Load environment variables ---
load_dotenv()

print("🚀 Starting Nova Resume Chatbot Backend (Local Mode)...")

# --- Google Authentication ---
try:
    credentials, project = google.auth.default()
    print("✅ Google Authentication successful.")
except google.auth.exceptions.DefaultCredentialsError:
    print("⚠️ No ADC found. Falling back to GOOGLE_API_KEY environment variable.")
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Missing GOOGLE_API_KEY. Please set it in your .env file.")
        exit()

# --- Flask setup ---
app = Flask(__name__)
CORS(app)

# --- Load Resume File ---
print("📄 Loading and chunking resume...")
try:
    loader = PyPDFLoader("Chetanya_Resume.pdf")  # Make sure resume PDF is in backend folder
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    texts = text_splitter.split_documents(documents)
    print(f"✅ Loaded {len(texts)} text chunks from resume.")
except Exception as e:
    print(f"❌ Error loading PDF: {e}")
    exit()

# --- Embeddings + Vectorstore ---
print("🔄 Creating embeddings and Chroma vectorstore...")
try:
    embeddings = VertexAIEmbeddings(model_name="text-embedding-005", location="us-central1")
    vectorstore = Chroma.from_documents(texts, embeddings)
    print("✅ Chroma vectorstore ready.")
except Exception as e:
    print(f"❌ FATAL ERROR: Failed to create embeddings/vectorstore: {e}")
    exit()

# --- Gemini Model (Chat) ---
print("🧠 Initializing Gemini model...")
try:
    llm = VertexAI(model_name="gemini-2.5-flash", temperature=0.0)
    print("✅ Gemini model ready.")
except Exception as e:
    print(f"❌ Failed to initialize Gemini model: {e}")
    exit()

# --- Routes ---
@app.route("/")
def home():
    return jsonify({"message": "Nova Resume Chatbot Backend running locally!"})

@app.route("/query", methods=["POST"])
def query_resume():
    try:
        user_input = request.json.get("input", "")

        # 1. Get most relevant context from vectorstore
        docs = vectorstore.similarity_search(user_input, k=3)
        context = "\n\n".join([d.page_content for d in docs])

        # 2. Humanized, first-person-aware prompt
        prompt = f"""
You are an expert assistant for Chetanya Rathi's resume. Answer naturally and professionally, like you are chatting with a human. 

Instructions:
- Use "he has done" or "he used" instead of "they have used".
- If the user asks for a list (e.g., "projects"), respond with only names in a concise, friendly way.
- If the user asks for details about a specific project, provide 2–3 paragraphs explaining what he did, the tools/technologies used, and the impact/results.
- For 'skills', give 2-3 paragraph describing his technical expertise, tools, and strengths, not bullets.
- For 'what is he pursuing right now' or 'education', respond accurately with the current program and expected graduation (include coursework only if explicitly asked).
- Always write in a warm, human tone, first-person-aware.
- Avoid bullets or stars unless specifically asked.

Context from resume:
{context}

User Question:
{user_input}

Answer:
"""

        # 3. Get response from Gemini LLM
        response = llm.invoke(prompt)

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
