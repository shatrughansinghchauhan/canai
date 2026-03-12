import os
import traceback
from pinecone import Pinecone
from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
INDEX_NAME = "candisp-index"
NAMESPACE = "candisp_documents"

print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded")

print("Connecting to Pinecone...")
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)
print("Pinecone connected")

print("Initializing Groq...")
groq_client = Groq(api_key=GROQ_API_KEY)
print("Groq ready")


def generate_embedding(text):
    return embedding_model.encode(text).tolist()


def search_vector_db(embedding):

    results = index.query(
        vector=embedding,
        top_k=5,
        include_metadata=True,
        namespace=NAMESPACE
    )

    return results


def build_context(results):

    context = ""

    matches = results.get("matches", [])

    for match in matches:

        metadata = match.get("metadata", {})

        if "text" in metadata:
            context += metadata["text"] + "\n"

    return context


def ask_llm(query, context):

    prompt = f"""
Use the context to answer the question.

Context:
{context}

Question:
{query}
"""

    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


def chat(query):

    try:

        embedding = generate_embedding(query)

        results = search_vector_db(embedding)

        context = build_context(results)

        response = ask_llm(query, context)

        return response

    except Exception as e:

        print("CHAT ERROR:", str(e))

        traceback.print_exc()

        return "Server error occurred."
