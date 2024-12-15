import tensorflow as tf
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
from tensorflow.keras import layers, models

# Load the fine-tuned sentiment analysis model and tokenizer
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

# Example function to analyze sentiment
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True, max_length=512)
    outputs = model(inputs)  # Forward pass
    logits = outputs.logits  # Raw model outputs (logits)
    
    # Convert logits to probabilities and return sentiment (positive or negative)
    probabilities = tf.nn.softmax(logits, axis=-1)
    sentiment = tf.argmax(probabilities, axis=-1).numpy()
    
    # 1 means positive sentiment, 0 means negative sentiment
    return "Positive" if sentiment[0] == 1 else "Negative"


