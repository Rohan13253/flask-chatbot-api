from flask import Flask, request, jsonify
import json
from rapidfuzz import process  # For fuzzy matching

app = Flask(__name__)

# Load chatbot responses from responses.json
with open("responses.json", "r") as file:
    chatbot_data = json.load(file)

@app.route("/chatbot", methods=["GET"])
def chatbot():
    user_message = request.args.get("message", "").lower()

    # Find the closest matching key using fuzzy matching
    best_match, score, _ = process.extractOne(user_message, chatbot_data.keys())

    if score > 70:  # Set a similarity threshold (adjustable)
        response = chatbot_data[best_match]
    else:
        response = "Sorry, I don't understand that."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
