import sqlite3

DB_FILE = "chatbot.db"

def create_table():
    """
    Create a database table to store chatbot configurations.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chatbot_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            chatbot_name TEXT,
            dataset_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def save_chatbot_config(user_id, chatbot_name, dataset_file):
    """
    Save chatbot configuration in the database.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO chatbot_config (user_id, chatbot_name, dataset_file) VALUES (?, ?, ?)",
                   (user_id, chatbot_name, dataset_file))
    
    conn.commit()
    conn.close()

# Example Usage:
# create_table()
# save_chatbot_config("user123", "MyChatbot", "uploads/user_dataset.csv")
