from flask import Flask, request, jsonify
import json
from rapidfuzz import process, fuzz
from api_helpers import get_weather, search_wikipedia, get_current_time

app = Flask(__name__)

# Load chatbot responses from JSON
with open("responses.json", "r") as file:
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

    # Handle weather queries
    if "weather" in user_message or "forecast" in user_message:
        city = user_message.split("in")[-1].strip() if "in" in user_message else ""
        response = get_weather(city)

    # Handle Wikipedia queries
    elif "who is" in user_message or "what is" in user_message:
        response = search_wikipedia(user_message)

    # Handle time requests
    elif "time" in user_message:
        response = get_current_time()

    # Default chatbot responses (fuzzy matching)
    else:
        response = get_best_match(user_message)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
