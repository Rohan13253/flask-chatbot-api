from flask import Flask, request, jsonify
import os  # For reading the PORT environment variable

app = Flask(__name__)

# Load chatbot responses from JSON file
with open("chatbot_data.json", "r") as file:
    chatbot_data = json.load(file)

# ✅ Home route to prevent 404 errors
@app.route("/")
def home():
    return "Welcome to the Chatbot API! Use /chatbot?message=your_message"

# ✅ Chatbot API
@app.route("/chatbot", methods=["GET"])
def chatbot():
    user_message = request.args.get("message", "").lower()
    response = chatbot_responses.get(user_message, "Sorry, I don't understand that.")
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Read Render's assigned port
    app.run(host="0.0.0.0", port=port)
