import pandas as pd
import re

class AmharicNERLabeler:
    """
    A class to label tokens in Amharic text for Named Entity Recognition (NER).
    
    The class identifies and labels tokens as prices, locations, products, or others
    based on predefined rules and keywords.

    Attributes:
    -----------
    price_keywords : list
        Keywords associated with price entities.
    location_list : list
        Predefined list of known location keywords.
    product_keywords : list
        Predefined list of known product keywords.
    """

    def __init__(self):
        # Define keywords for different entities
        self.price_keywords = ['ዋጋ', 'ብር', 'ከ']
        self.location_list = [
            'አዲስ', 'አበባ', 'ድሬዳዋ', 'የታይላንድ', 'ቦሌ', 'ቡልጋሪ', 'ቁ2ፒያሳ', 'ቁ1መገናኛ',
            'በረራ', 'ልደታ', 'ባልቻ', 'አአ', 'ፒያሳ', 'መገናኛ', 'ጀሞ', 'ገርጂ', 'ጉርድሾላ', 'ሜክሲኮ', '22', '4ኪሎ', 'አዳማ', 'ድሬዳዋ'
        ]
        self.product_keywords = [
            'ምርት', 'የጫማ', 'ሳጥን', 'ምንጣፍ', 'ጎማ', 'ቁም', 'ማስቀመጫ', 'ፕላሰሰቲክ', 'ባልዲ', 'ኮምፒውተር', 'ስቶቭ', 'ማንኪያ', 'የችበስመጥበሻ', 'ጫማዎች', 'ጫማ', 'እስቲመር', 'መኪና',
            'መጥበሻ', 'መጥበሻዎች', 'ምርቶች', 'ባትራ', 'ካርድ', 'መፍጫ', 'ማሞቂያ',
            'መወልወያ', 'መደርደሪያ', 'መስታወት', 'እንጨት', 'ሶፋ', 'ኩርሲ'
        ]

    def tokenize(self, text):
        """Tokenize Amharic text and remove punctuation."""
        # Remove punctuation using regex
        text_without_punct = re.sub(r'[^\w\s]', '', text)
        # Tokenize the cleaned text
        return re.findall(r'\b\w+\b', text_without_punct)

    def label_tokens(self, tokens):
        """
        Label the tokens with their corresponding NER labels.

        Parameters:
        -----------
        tokens : list
            A list of tokenized strings in Amharic.

        Returns:
        --------
        list
            A list of tuples where each tuple contains a token and its corresponding label.
        """
        labels = []
        for i, token in enumerate(tokens):
            token_stripped = token.strip()  # Strip any surrounding whitespace

            # Price entity detection
            if token_stripped.endswith('ብር') or token_stripped in self.price_keywords:
                labels.append((token, 'B-PRICE' if i == 0 else 'I-PRICE'))
            elif token_stripped.isdigit() and (i + 1 < len(tokens) and tokens[i + 1].strip() == 'ብር'):
                labels.append((token, 'I-PRICE'))

            # Location entity detection
            elif token_stripped in self.location_list:
                labels.append((token, 'B-LOC'))

            # Product entity detection
            elif token_stripped in self.product_keywords:
                labels.append((token, 'B-PRODUCT'))

            # Handle punctuation or non-relevant tokens as 'O'
            elif re.match(r'^\W+$', token):
                labels.append((token, 'O'))

            # Default label
            else:
                labels.append((token, 'O'))

        return labels

    def label_dataframe(self, df, text_column):
        """
        Apply NER labeling to a DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the text data.
        text_column : str
            The column name in the DataFrame where the text data is stored.

        Returns:
        --------
        pandas.DataFrame
            A DataFrame with tokens and their corresponding NER labels.
        """
        labeled_data = []
        for _, row in df.iterrows():
            tokens = self.tokenize(row[text_column])
            labels = self.label_tokens(tokens)
            labeled_data.append(labels)
        return labeled_data

    def save_conll_format(self, labeled_data, file_path):
        """
        Save the labeled data in CoNLL format.

        Parameters:
        -----------
        labeled_data : list
            The list containing token-label pairs.
        file_path : str
            The path to the file where the CoNLL format will be saved.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            for labeled_sentence in labeled_data:
                for token, label in labeled_sentence:
                    f.write(f"{token} {label}\n")
                f.write("\n")  # Blank line between sentences/messages
