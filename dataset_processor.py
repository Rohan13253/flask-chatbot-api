import pandas as pd
import json
import os

UPLOAD_FOLDER = "uploads/"

def process_dataset(file_path):
    """
    Load the dataset and convert it into a structured format for training.
    Returns a dictionary with 'intents' for chatbot training.
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            df = pd.read_json(file_path)
        else:
            return None, "Unsupported file format!"

        # Convert into chatbot training format
        chatbot_data = {"intents": []}
        for _, row in df.iterrows():
            chatbot_data["intents"].append({
                "question": row["question"],
                "answer": row["answer"]
            })

        # Save processed data
        processed_file_path = os.path.join(UPLOAD_FOLDER, "processed_data.json")
        with open(processed_file_path, "w") as f:
            json.dump(chatbot_data, f, indent=4)

        return processed_file_path, "Dataset processed successfully!"

    except Exception as e:
        return None, f"Error processing dataset: {str(e)}"

# Example Usage:
# processed_file, message = process_dataset("uploads/user_dataset.csv")
# print(message)
