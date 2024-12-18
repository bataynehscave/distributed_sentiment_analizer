# Sentiment Analysis with FastAPI and Spark

This project provides a FastAPI-based web service to analyze the sentiment of input texts using Apache Spark for distributed processing.

## Features

- FastAPI for handling API requests
- Apache Spark for distributed data processing
- Logging for monitoring and debugging
- Graceful shutdown of SparkContext

## Requirements

- Python 3.8 or higher
- Apache Spark

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. **Install dependencies:**

```bash
pip install -r requirements.txt 
```

3. **Set up Apache Spark:**

Download and install Apache Spark from the official website.

## Usage
1. **Run the FastAPI server:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 
```

2. **Analyze sentiment:**

Send a POST request to /analyze_sentiment/ with a JSON body containing a list of texts.

Example request:
json
{
  "texts": ["I love programming!", "I hate bugs."]
}
Example response:

json
{
  "sentiments": ["positive", "negative"]
}

3. **Access API documentation:**

Open your browser and go to http://0.0.0.0:8000/docs to view and interact with the automatically generated API documentation.


POST /analyze_sentiment/
Analyzes the sentiment of a list of input texts.

### Request Body:
texts (list of strings): The texts to analyze.

### Response:
sentiments (list of strings): The analyzed sentiments for each text.
Logging
Logs are written to app.log file with timestamps and log levels.

## Shutdown
The SparkContext is gracefully shut down when the server stops.

## Configuration
You can customize the application settings by modifying the config.yaml file.

## License
This project is licensed under the MIT License.