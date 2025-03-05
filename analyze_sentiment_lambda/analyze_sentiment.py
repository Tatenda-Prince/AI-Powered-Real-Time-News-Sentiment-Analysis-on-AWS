import json
import boto3
import os
import time
import re

# Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
comprehend = boto3.client('comprehend')

# Load environment variables
table_name = os.environ['DYNAMODB_TABLE']
bucket_name = os.environ['BUCKET_NAME']
table = dynamodb.Table(table_name)

def clean_text(text):
    """Normalize text for better sentiment analysis."""
    text = text.lower().strip()
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove punctuation/numbers
    return text

def lambda_handler(event, context):
    try:
        if "file_key" not in event:
            raise ValueError("Missing required key: 'file_key' in event payload")

        file_key = event["file_key"]

        # Fetch file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        news_data = json.loads(response['Body'].read().decode('utf-8'))

        articles = news_data.get("articles", [])
        texts = []
        valid_articles = []
        
        MIN_TITLE_LENGTH = 5  # Minimum words required for analysis

        for article in articles:
            url = article.get("url")
            title = article.get("title", "").strip()
            clean_title = clean_text(title)

            if url and title and len(title.split()) >= MIN_TITLE_LENGTH:
                texts.append(clean_title)
                valid_articles.append({"url": url, "title": title})

        if not texts:
            return {"statusCode": 400, "message": "No valid articles for sentiment analysis."}

        sentiment_results = []
        BATCH_SIZE = 25

        for i in range(0, len(texts), BATCH_SIZE):
            batch_texts = texts[i : i + BATCH_SIZE]

            try:
                comprehend_response = comprehend.batch_detect_sentiment(
                    TextList=batch_texts,
                    LanguageCode="en"
                )

                print("Comprehend Full Response:", json.dumps(comprehend_response, indent=2))

                sentiments = comprehend_response.get("ResultList", [])
                errors = comprehend_response.get("ErrorList", [])

                for j, sentiment_data in enumerate(sentiments):
                    sentiment_scores = sentiment_data["SentimentScore"]

                    # Adjusted Thresholds
                    if sentiment_scores["Positive"] >= 0.3:
                        sentiment = "POSITIVE"
                    elif sentiment_scores["Negative"] >= 0.3:
                        sentiment = "NEGATIVE"
                    elif sentiment_scores["Mixed"] >= 0.3:
                        sentiment = "MIXED"
                    else:
                        sentiment = "NEUTRAL"

                    article = valid_articles[i + j]
                    timestamp = int(time.time())

                    print(f"Title: {article['title']}")
                    print(f"Sentiment Scores: {sentiment_scores}")
                    print(f"Assigned Sentiment: {sentiment}")

                    item = {
                        "id": article["url"],
                        "timestamp": timestamp,
                        "title": article["title"],
                        "sentiment": sentiment
                    }
                    sentiment_results.append(item)

                if errors:
                    print(f"Comprehend Errors: {errors}")

            except Exception as e:
                print(f"Comprehend batch error: {str(e)}")

        # Store results in DynamoDB
        with table.batch_writer() as batch:
            for item in sentiment_results:
                batch.put_item(Item=item)

        return {
            "statusCode": 200,
            "message": "Sentiment analysis completed",
            "results": sentiment_results
        }

    except Exception as e:
        print(f"Error in Lambda function: {str(e)}")
        return {"statusCode": 500, "error": str(e)}

