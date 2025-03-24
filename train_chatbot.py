import json
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

UPLOAD_FOLDER = "uploads/"
MODEL_FOLDER = "models/"

def train_chatbot():
    """
    Train a chatbot model using processed dataset and save it.
    """
    try:
        processed_file = os.path.join(UPLOAD_FOLDER, "processed_data.json")

        # Load processed dataset
        with open(processed_file, "r") as f:
            chatbot_data = json.load(f)

        # Extract questions and answers
        questions = [item["question"] for item in chatbot_data["intents"]]
        answers = [item["answer"] for item in chatbot_data["intents"]]

        # Convert text data to numerical format
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(questions)

        # Train a Naive Bayes model
        model = MultinomialNB()
        model.fit(X, answers)

        # Save model and vectorizer
        os.makedirs(MODEL_FOLDER, exist_ok=True)
        with open(os.path.join(MODEL_FOLDER, "chatbot_model.pkl"), "wb") as f:
            pickle.dump(model, f)
        with open(os.path.join(MODEL_FOLDER, "vectorizer.pkl"), "wb") as f:
            pickle.dump(vectorizer, f)

        return "Chatbot trained and model saved successfully!"

    except Exception as e:
        return f"Error training chatbot: {str(e)}"

# Example Usage:
# message = train_chatbot()
# print(message)
