import json
import boto3
import os
import requests

ssm = boto3.client('ssm')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Retrieve API Key from SSM Parameter Store
        response = ssm.get_parameter(Name='newsapi_key', WithDecryption=True)
        api_key = response['Parameter']['Value']

        # Fetch news from NewsAPI
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        news_response = requests.get(url)
        news_data = news_response.json()

        # Store news in S3
        bucket_name = os.environ['BUCKET_NAME']
        file_name = f"news_{event['timestamp']}.json"
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(news_data))

        return {"statusCode": 200, "message": "News fetched and stored in S3"}
    except Exception as e:
        return {"statusCode": 500, "error": str(e)}

