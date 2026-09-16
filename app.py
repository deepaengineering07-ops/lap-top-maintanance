import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured in the .env file.")

client = genai.Client(api_key=API_KEY)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()

    if not user_message:
        return jsonify({"reply": "Please enter a laptop-maintenance question."}), 400

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"{SYSTEM_PROMPT}\n\nUser question:\n{user_message}"
        )

        reply = response.text or "I could not generate a response."
        return jsonify({"reply": reply})

    except Exception:
        return jsonify({
            "reply": "Sorry, I could not connect to the AI service right now. Please try again."
        }), 500


if __name__ == "__main__":
    app.run()
