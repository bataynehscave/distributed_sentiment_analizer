import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure necessary resources are downloaded
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

def preprocess(text):
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove mentions (@username)
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtags (#hashtag)
    text = re.sub(r'#\w+', '', text)
    
    # Remove non-alphanumeric characters (excluding spaces)
    text = re.sub(r'[^A-Za-z0-9\s]+', '', text)
    
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Convert to lowercase
    tokens = [word.lower() for word in tokens]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Join tokens back into a single string
    cleaned_text = ' '.join(tokens)
    
    return cleaned_text


