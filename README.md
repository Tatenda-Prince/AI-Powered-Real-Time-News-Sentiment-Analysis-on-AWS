# SentimentStream-AI-Powered-Real-Time-News-Sentiment-Analysis-on-AWS

## Technical Architecture



## Project Overview

SentimentStream is a cloud-native, AI-powered system that fetches real-time news, analyzes sentiment using AWS Comprehend, and stores insights in Amazon DynamoDB. It enables businesses to track sentiment trends efficiently, making data-driven decisions based on news insights.The project is fully automated with Terraform, following best practices in Infrastructure as Code (IaC), ensuring easy deployment and scalability.

## Project Objective

This project solves the challenge of real-time news sentiment tracking by automating:

1.News Fetching – Retrieve real-time news articles from NewsAPI.

3.Sentiment Analysis – Use AWS Comprehend to classify articles as Positive, Negative, Neutral, or Mixed.

4.Data Storage & Querying – Store results in DynamoDB for quick sentiment insights.

Why It Matters? Businesses need real-time insights on market trends, competitor analysis, and crisis detection. SentimentStream helps them stay ahead by providing AI-driven sentiment intelligence.

## Features

1.Fully Serverless Architecture – Uses AWS Lambda, S3, DynamoDB, and Comprehend.

2.Real-Time News Fetching – Automatically retrieves news from NewsAPI.

3.AI-Powered Sentiment Analysis – Uses AWS Comprehend for accurate sentiment classification.

4.Fast Sentiment Queries – Stores results in DynamoDB for instant lookups.

5.Scalable & Cost-Efficient – Serverless and pay-as-you-go AWS model.

6.Terraform-Powered Deployment – Easily provision AWS infrastructure with Infrastructure as Code (IaC).

## Technologies Used

1.AWS Lambda – Serverless compute for news fetching, querying sentiments & sentiment analysis

1.Amazon S3 – Stores raw news articles.

3.AWS Comprehend – AI-based sentiment analysis.

4.Amazon DynamoDB – NoSQL database for fast sentiment lookups.

4.Terraform – Infrastructure as Code for automated AWS provisioning.


## Use Case

A financial investing firm uses the AI-Powered News Sentiment Analysis System to monitor sentiment trends in real time.  By analysing news stories about stock markets, industries, and firms, the firm learns about public perception and market mood.  If news opinion towards a given company shifts unfavourable, the corporation can immediately modify its investing strategy to reduce risk.  In contrast, positive mood trends may indicate possible prospects for growth.  This automated technology enables traders and analysts to make data-driven investment decisions, decreasing human work and improving strategic decision-making.


## Prerequisites

1.https://newsapi.org/: register and get your API

2.AWS Account with configured Access key and Secret access key.

3.Terraform & AWS CLI installed (if using Terraform for infrastructure)


## Step 1: Clone the Repository

1.1.Clone this repository to your local machine.

```language
git clone 
```











