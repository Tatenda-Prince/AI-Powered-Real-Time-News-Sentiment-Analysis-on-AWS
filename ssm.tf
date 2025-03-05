resource "aws_ssm_parameter" "newsapi_key" {
  name  = "newsapi_key"
  type  = "SecureString"
  value = "YOUR_NEWSAPI_KEY"
}
