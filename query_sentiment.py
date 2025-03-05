import json
import boto3
import os
import time
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
table_name = os.environ["DYNAMODB_TABLE"]
table = dynamodb.Table(table_name)

def decimal_to_json(obj):
    """Convert DynamoDB Decimal types to JSON-safe types"""
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)  # Convert to int if whole number, else float
    if isinstance(obj, list):
        return [decimal_to_json(i) for i in obj]
    if isinstance(obj, dict):
        return {k: decimal_to_json(v) for k, v in obj.items()}
    return obj

def lambda_handler(event, context):
    try:
        # Extract query parameters
        sentiment_filter = event.get("sentiment", None)
        keyword = event.get("keyword", None)

        # Calculate timestamp for the past 7 days
        current_time = int(time.time())  # Current UNIX timestamp
        past_week_timestamp = current_time - (7 * 24 * 60 * 60)  # 7 days ago

        # Build filter expression
        filter_expression = Attr("timestamp").gt(past_week_timestamp)

        if sentiment_filter:
            filter_expression &= Attr("sentiment").eq(sentiment_filter)

        if keyword:
            filter_expression &= Attr("title").contains(keyword)

        # Perform scan with filter
        response = table.scan(
            FilterExpression=filter_expression
        )

        # Convert to JSON-safe format
        items = decimal_to_json(response.get("Items", []))

        return {
            "statusCode": 200,
            "body": json.dumps(items)  
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }

