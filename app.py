from flask import Flask, request, jsonify
import json
from rapidfuzz import process, fuzz
from api_helpers import get_weather  # Import the weather function
import wikipediaapi

app = Flask(__name__)

# Load chatbot responses from JSON
with open("responses.json", "r") as file:
    chatbot_data = json.load(file)

# 🔍 Function to find the best matching response
def get_best_match(user_message):
    """Finds the best response using fuzzy matching."""
    choices = list(chatbot_data.keys())  # Predefined chatbot responses
    best_match, score, _ = process.extractOne(user_message, choices, scorer=fuzz.ratio)

    if score >= 80:  # Threshold for similarity
        return chatbot_data[best_match]
    return "Sorry, I don't understand that."

@app.route("/chatbot", methods=["GET"])
def chatbot():
    user_message = request.args.get("message", "").lower()

    if "time" in user_message or "date" in user_message:
        response = get_time_date(user_message)
    else:
        response = "I'm not sure about that. Try asking about the time or date!"

    return jsonify({"response": response})

def search_wikipedia(user_message):
    """Fetches a short summary from Wikipedia."""
    wiki = wikipediaapi.Wikipedia("en")
    topic = user_message.replace("who is", "").replace("what is", "").strip()

    if not topic:
        return "Please specify a topic. Example: 'Who is Albert Einstein?'"

    page = wiki.page(topic)
    if page.exists():
        return page.summary[:300] + "..."  # Return first 300 characters
    else:
        return f"Sorry, I couldn't find anything about {topic} on Wikipedia."

# 🗣️ Chatbot API
@app.route("/chatbot", methods=["GET"])
def chatbot():
    user_message = request.args.get("message", "").lower()

    # 🌤️ Check if the user is asking about weather
    if "weather" in user_message or "forecast" in user_message:
        city = user_message.split("in")[-1].strip()  # Extract city name
        if city:
            response = get_weather(city)  # Fetch weather from API
        else:
            response = "Please specify a city. Example: 'What's the weather in Mumbai?'"
    else:
        response = get_best_match(user_message)  # Use fuzzy matching for chatbot responses

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
