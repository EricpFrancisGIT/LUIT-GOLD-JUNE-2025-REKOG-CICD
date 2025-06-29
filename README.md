# 📸 Serverless Image Tagging Pipeline with AWS Rekognition & GitHub Actions

Welcome to the **Pixel Learning Co. AI Image Labeling Pipeline** — a fully automated, serverless system for tagging and classifying educational image content using **Amazon Rekognition**, **S3**, **DynamoDB**, and **GitHub Actions**. This solution streamlines content management by eliminating manual tagging and enabling seamless content review workflows for staging and production environments.

---

## 📘 Project Overview

**Pixel Learning Co.**, a digital-first education startup, leverages this pipeline to:

- 🔍 **Automate Image Classification**: AI-driven object and scene detection on image changes.
- 🧪 **Streamline QA and Review**: Results routed to branch-specific DynamoDB tables.
- 🗂️ **Improve Content Organization**: Auto-tagging enhances search, filtering, and indexing.
- ☁️ **Reduce Infrastructure Overhead**: Uses AWS-managed services with zero custom model training.

---

## 🚀 Features

- **Amazon Rekognition** for AI-powered image labeling.
- **S3** as the staging ground for Rekognition input.
- **DynamoDB** for structured results storage.
- **GitHub Actions** to automate everything on PRs and merges.
- **Branch-Aware Workflows**: Staging (`beta_results`) and Production (`prod_results`) isolation.

---

## 🛠️ Architecture

```text
GitHub Repo (image added)
        |
GitHub Actions Workflow
        |
     Python Script
        |
     ┌───────────────┐
     │     S3        │
     └───────────────┘
        |
     ┌───────────────┐
     │ Rekognition   │
     └───────────────┘
        |
     ┌───────────────┐
     │  DynamoDB     │
     └───────────────┘
     
🧰 Requirements
AWS Resources

Ensure the following resources are available in your AWS environment:

    S3 Bucket: For storing uploaded images.

    Amazon Rekognition: No additional setup required.

    DynamoDB Tables:

        beta_results — for pull requests.

        prod_results — for merges to main.

🔐 GitHub Repository Secrets

| Name                    | Description                               |
| ----------------------- | ----------------------------------------- |
| `AWS_ACCESS_KEY_ID`     | IAM user's access key                     |
| `AWS_SECRET_ACCESS_KEY` | IAM user's secret access key              |
| `AWS_REGION`            | AWS Region (e.g., `us-east-1`)            |
| `S3_BUCKET`             | Your S3 bucket name                       |
| `DYNAMODB_TABLE_BETA`   | Beta results table (e.g., `beta_results`) |
| `DYNAMODB_TABLE_PROD`   | Prod results table (e.g., `prod_results`) |

🧪 How to Test

    Add an Image: Commit a .jpg or .png file to the images/ directory.

    Submit a PR: Open a pull request against main. This triggers the beta pipeline.

    Merge the PR: On merge, the prod pipeline is triggered.

    Verify Results:

        Go to AWS DynamoDB.

        Check the appropriate table (beta_results or prod_results).

        You should see an entry like:
{
  "filename": "rekognition-input/sample.jpg",
  "labels": [
    {"Name": "Laptop", "Confidence": 98.32},
    {"Name": "Desk", "Confidence": 95.11}
  ],
  "timestamp": "2025-06-01T14:55:32Z",
  "branch": "feature/content-tagging"
}

🧱 Setup Instructions
1. Provision AWS Resources

    Create an S3 bucket (e.g., pixel-image-input).

    Create two DynamoDB tables:

        beta_results with primary key: filename (String)

        prod_results with primary key: filename (String)

    Ensure Rekognition permissions are granted to your IAM user or role.

2. Configure IAM Permissions

The IAM user should have the following permissions:
{
  "Effect": "Allow",
  "Action": [
    "rekognition:DetectLabels",
    "s3:PutObject",
    "s3:GetObject",
    "dynamodb:PutItem"
  ],
  "Resource": "*"
}

3. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and Variables → Actions and add:

    AWS_ACCESS_KEY_ID

    AWS_SECRET_ACCESS_KEY

    AWS_REGION

    S3_BUCKET

    DYNAMODB_TABLE_BETA

    DYNAMODB_TABLE_PROD

📎 License

MIT © 2025 Pixel Learning Co.
🤝 Contributions

Contributions and issues are welcome! Please fork the repo and open a PR.
📬 Contact

For questions or demo requests, reach out to: eric.francis1103@gmail.com