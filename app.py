from flask import Flask, request, jsonify
import json
from rapidfuzz import process, fuzz

app = Flask(__name__)

# Load chatbot responses from JSON
with open("data/responses.json", "r") as file:
    chatbot_data = json.load(file)

def get_best_match(user_message):
    """Finds the best matching response using fuzzy matching."""
    choices = list(chatbot_data.keys())  # List of predefined messages
    best_match, score, _ = process.extractOne(user_message, choices, scorer=fuzz.ratio)
    
    if score >= 80:  # Set threshold for similarity
        return chatbot_data[best_match]
    return "Sorry, I can't understand that."

@app.route("/chatbot", methods=["GET"])
def chatbot():
    user_message = request.args.get("message", "").lower()
    response = get_best_match(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
