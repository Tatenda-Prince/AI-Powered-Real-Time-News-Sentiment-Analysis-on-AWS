resource "aws_iam_role" "lambda_role" {
  name = "news_sentiment_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "news_sentiment_lambda_policy"
  description = "IAM policy for Lambda to access S3, DynamoDB, Comprehend, and SSM Parameter Store"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"]
        Resource = ["arn:aws:s3:::tatenda-news-sentiment-bucket", "arn:aws:s3:::tatenda-news-sentiment-bucket/*"]
      },
      {
        Effect   = "Allow"
        Action   = [
          "dynamodb:PutItem",
          "dynamodb:BatchWriteItem",  # ✅ Allows batch writes to DynamoDB
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = ["arn:aws:dynamodb:*:*:table/NewsSentiment"]
      },
      {
        Effect   = "Allow"
        Action   = ["comprehend:DetectSentiment", "comprehend:BatchDetectSentiment"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["ssm:GetParameter"]
        Resource = "arn:aws:ssm:*:*:parameter/newsapi_key"
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}
