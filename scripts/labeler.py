import re

class Labeler:
    def __init__(self, df):
        self.df = df

    @staticmethod
    def label_message(message):
        """Label a message with entities like product, price, and location."""
        # Tokenize the message
        tokens = re.findall(r'\S+', message)
        labeled_tokens = []

        for token in tokens:
            if re.match(r'\d+(\.\d+)?(ETB|ብር|\$)', token):
                labeled_tokens.append(f"{token} I-PRICE")
            elif any(loc in token for loc in ['Addis', 'Bole', 'አዲስ', 'ሜክሲኮ']):
                labeled_tokens.append(f"{token} I-LOC")
            else:
                labeled_tokens.append(f"{token} O")
        
        return "\n".join(labeled_tokens)

    def label_data(self):
        """Apply labeling to the dataset."""
        print("Labeling data...")
        self.df['Labeled_Message'] = self.df['Message'].apply(self.label_message)

    def save_labeled_data(self, output_path):
        """Save the labeled data in CoNLL format."""
        with open(output_path, 'w', encoding='utf-8') as f:
            for _, row in self.df.iterrows():
                f.write(f"{row['Labeled_Message']}\n\n")
        print(f"Labeled data saved to {output_path}")
