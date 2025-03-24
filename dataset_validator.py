import pandas as pd

def validate_dataset(file_path):
    """
    Validate if the dataset is in the correct format (CSV or JSON)
    and contains the required columns: ['question', 'answer'].
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            df = pd.read_json(file_path)
        else:
            return False, "Unsupported file format! Please upload a CSV or JSON file."

        # Check if required columns exist
        required_columns = {'question', 'answer'}
        if not required_columns.issubset(df.columns):
            return False, f"Missing required columns: {required_columns - set(df.columns)}"

        return True, "Dataset is valid!"
    
    except Exception as e:
        return False, f"Dataset validation failed: {str(e)}"

# Example Usage:
# is_valid, message = validate_dataset("uploads/user_dataset.csv")
# print(message)
