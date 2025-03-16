from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load chatbot responses from the JSON file
with open("responses.json", "r") as file:
    chatbot_data = json.load(file)

@app.route("/")
def home():
    return "Welcome to the Chatbot API! Use /chatbot?message=your_message"

@app.route("/chatbot", methods=["GET"])
def chatbot():
    user_message = request.args.get("message", "").lower()
    response = chatbot_data.get(user_message, "Sorry, I don't understand that.")
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
