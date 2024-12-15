from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyspark import SparkConf, SparkContext
import logging
import uvicorn

# Import your preprocessor and sentiment analyzer
from preprocessor import preprocess
from sentiment_analyzer import analyze_sentiment

# Set up logging
logging.basicConfig(level=logging.INFO, filename="app.log", format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize SparkContext (only on the driver)
conf = SparkConf().setAppName("SentimentAnalysis").setMaster("local[*]")

# Global variable to hold the SparkContext
sc = None

# Initialize FastAPI
app = FastAPI()

# Define a Pydantic model for receiving multiple texts
class TextRequest(BaseModel):
    texts: list[str]

def preprocess_and_analyze_worker(text):
    """
    Worker function to preprocess and analyze sentiment.
    """
    try:
        processed_text = preprocess(text)  # Preprocess the text
        sentiment = analyze_sentiment(processed_text)  # Perform sentiment analysis
        return sentiment
    except Exception as e:
        logging.error(f"Error processing text '{text}': {e}")
        raise e

def analyze_sentiments_with_spark(texts):
    """
    Distribute preprocessing and analysis of sentiment using Spark.
    """
    try:
        global sc 

        # Initialize SparkContext if not already initialized
        if sc is None:
            try:
                sc = SparkContext(conf=conf)
                logging.info("SparkContext initialized successfully.")
            except Exception as e:
                logging.error(f"Failed to initialize SparkContext: {e}")
                raise RuntimeError("Error initializing SparkContext")

        # Broadcast the texts
        bcast_texts = sc.broadcast(texts)

        # Create RDD and map the function to process the texts
        rdd = sc.parallelize(range(len(texts)))
        sentiments = rdd.map(lambda i: preprocess_and_analyze_worker(bcast_texts.value[i])).collect()

        return sentiments
    except Exception as e:
        logging.error(f"Error processing RDD: {e}")
        raise HTTPException(status_code=500, detail="Error processing texts with Spark.")

@app.on_event("shutdown")
def shutdown_event():
    """
    Gracefully shuts down the SparkContext.
    """
    global sc
    if sc:
        logging.info("Shutting down SparkContext...")
        sc.stop()
        sc = None

@app.post("/analyze_sentiment/")
async def analyze_sentiment_endpoint(request: TextRequest):
    """
    FastAPI endpoint to analyze sentiment of input texts.
    """
    try:
        texts = request.texts
        if not texts:
            raise HTTPException(status_code=400, detail="No texts provided")

        sentiments = analyze_sentiments_with_spark(texts)
        return {"sentiments": sentiments}
    except HTTPException as he:
        logging.error(f"API HTTP Error: {he.detail}")
        raise he
    except Exception as e:
        logging.error(f"Unexpected API Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while analyzing sentiment.")

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logging.error(f"Error running the server: {e}")