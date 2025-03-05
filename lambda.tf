resource "aws_lambda_function" "fetch_news_lambda" {
  function_name = "fetch_news"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "fetch_news.lambda_handler"

  filename         = "fetch_news.zip"
  source_code_hash = filebase64sha256("fetch_news.zip")

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.news_bucket.bucket
    }
  }
}

resource "aws_lambda_function" "analyze_sentiment_lambda" {
  function_name = "analyze_sentiment"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "analyze_sentiment.lambda_handler"

  filename         = "analyze_sentiment.zip"
  source_code_hash = filebase64sha256("analyze_sentiment.zip")

  environment {
    variables = {
      BUCKET_NAME    = aws_s3_bucket.news_bucket.bucket
      DYNAMODB_TABLE = aws_dynamodb_table.news_sentiment_table.name  # ✅ Fix the reference
    }
  }
}

resource "aws_lambda_function" "query_sentiment_lambda" {
  function_name = "query_sentiment"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "query_sentiment.lambda_handler"

  filename         = "query_sentiment.zip"
  source_code_hash = filebase64sha256("query_sentiment.zip")

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.news_sentiment_table.name
    }
  }
}

