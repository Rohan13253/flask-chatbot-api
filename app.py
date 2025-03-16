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
    return None

@app.route("/")
def home():
    return "Welcome to the AI Chatbot API! Use /chatbot?message=your_message"

@app.route("/chatbot", methods=["GET"])
def chatbot():
    user_message = request.args.get("message", "").lower()
    
    # Check for weather queries
    if "weather" in user_message or "forecast" in user_message:
        city = user_message.split("in")[-1].strip()  # Extract city name
        if city:
            response = get_weather(city)
        else:
            response = "Please specify a city. Example: 'What's the weather in Mumbai?'"

    # Check for Wikipedia search
    elif "who is" in user_message or "tell me about" in user_message:
        query = user_message.replace("who is ", "").replace("tell me about ", "").strip()
        response = search_wikipedia(query)

    # Check for current time request
    elif "time" in user_message or "date" in user_message:
        response = get_current_time()

    # Use fuzzy matching for general chatbot responses
    else:
        response = get_best_match(user_message)
        if response is None:
            response = "Sorry, I don't understand that. Try asking about weather, time, or a famous person!"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
