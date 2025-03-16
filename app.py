from flask import Flask, request, jsonify
import json
from rapidfuzz import process  

app = Flask(__name__)

# Load chatbot responses from responses.json
try:
    with open("responses.json", "r") as file:
        chatbot_data = json.load(file)
    print("Chatbot Data Loaded:", chatbot_data)  # Debugging print
except Exception as e:
    print("Error loading JSON:", e)

@app.route("/chatbot", methods=["GET"])
def chatbot():
    user_message = request.args.get("message", "").lower()
    
    print("User Message:", user_message)  # Debugging print

    # Check if exact match exists
    if user_message in chatbot_data:
        response = chatbot_data[user_message]
    else:
        # Find the closest match using fuzzy matching
        best_match, score, _ = process.extractOne(user_message, chatbot_data.keys())
        print(f"Best Match: {best_match}, Score: {score}")  # Debugging print
        
        if score > 70:  # If similarity is high enough, return response
            response = chatbot_data[best_match]
        else:
            response = "Sorry, I don't understand that."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
