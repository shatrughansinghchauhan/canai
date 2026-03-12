import os
from flask import Flask, request, jsonify, send_from_directory
from rag_chat import chat

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)


@app.route("/")
def serve_ui():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)


@app.route("/chat", methods=["POST"])
def chat_api():
    try:

        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({"error": "Query missing"}), 400

        query = data["query"]

        answer = chat(query)

        return jsonify({"answer": answer})

    except Exception as e:
        print("API ERROR:", str(e))
        return jsonify({"error": "Server error"}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
