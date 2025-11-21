from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# ---------- Load heritage data ----------
DATA_FILE = "heritage_data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        HERITAGE_DATA = json.load(f)
else:
    HERITAGE_DATA = {}


def find_place_in_data(user_message: str):
    msg = user_message.lower()
    for key, value in HERITAGE_DATA.items():
        if key in msg:
            return key, value
    return None, None


def generate_answer(user_message: str) -> str:
    lower_msg = user_message.lower()

    if any(w in lower_msg for w in ["hi", "hello", "hey", "namaste"]):
        return (
            "Hi! I am your Heritage Guide Bot 🏛️.\n"
            "Ask me about places like Curzon Gate, Victoria Memorial, Hazarduari Palace, etc."
        )

    key, place = find_place_in_data(user_message)
    if place:
        lines = []
        lines.append(f"📍 {place['name']} — {place['city']}, {place['state']}\n")
        lines.append(f"📝 Description: {place['description']}\n")
        lines.append(f"📚 History: {place['history']}\n")

        for fact in place.get("fun_facts", []):
            lines.append("✨ " + fact)

        nearby = place.get("nearby_places", [])
        if nearby:
            lines.append("\n📌 Nearby places: " + ", ".join(nearby))

        tips = place.get("visit_tips", [])
        if tips:
            lines.append("\n💡 Visit tips:")
            for tip in tips:
                lines.append("• " + tip)

        return "\n".join(lines)

    return (
        "I don't have information about that place yet 😔.\n"
        "Try asking: 'Tell me about Curzon Gate' or 'What is Victoria Memorial?'"
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_reply = generate_answer(user_message)
    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
