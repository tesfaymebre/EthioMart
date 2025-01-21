import re
import pandas as pd

class Preprocessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None

    def load_data(self):
        """Load the dataset and drop NaN messages."""
        print("Loading data...")
        self.df = pd.read_csv(self.input_path)
        print(f"Initial dataset shape: {self.df.shape}")
        self.df.dropna(subset=['Message'], inplace=True)
        print(f"Dataset shape after dropping NaN values: {self.df.shape}")

    @staticmethod
    def remove_emojis(text):
        """Remove emojis from a text string."""
        emoji_pattern = re.compile(
            "[" 
            "\U0001F600-\U0001F64F"  
            "\U0001F300-\U0001F5FF"  
            "\U0001F680-\U0001F6FF"  
            "\U0001F700-\U0001F77F"  
            "\U0001F780-\U0001F7FF"  
            "\U0001FA00-\U0001FA6F"  
            "\U0001FA70-\U0001FAFF"  
            "\U00002702-\U000027B0"  
            "\U000024C2-\U0001F251" 
            "]+", 
            flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', text)

    @staticmethod
    def remove_english_words(text):
        """Remove English words from a text string."""
        return re.sub(r'\b[a-zA-Z]+\b', '', text)

    def clean_data(self):
        """Clean the dataset by removing emojis and English words."""
        print("Cleaning data...")
        self.df['Message'] = self.df['Message'].apply(self.remove_emojis)
        self.df['Message'] = self.df['Message'].apply(self.remove_english_words)

    def save_cleaned_data(self):
        """Save the cleaned data to a CSV file."""
        self.df.to_csv(self.output_path, index=False)
        print(f"Cleaned data saved to {self.output_path}")
