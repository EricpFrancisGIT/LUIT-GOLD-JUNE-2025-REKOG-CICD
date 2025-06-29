import boto3
import os
from datetime import datetime

AWS_REGION = os.environ.get('AWS-REGION',"us-east-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", 'PROD_TABLE')')
S3_BUCKET_NAME = 'pixel-rekog-cicd'

s3 = boto3.client('s3', region_name=AWS_REGION)
rekognition = boto3.client('rekognition', region_name=AWS_REGION)
dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)

### CONSTANTS#####
DEST_BUCKET = "pixel-rekog-cicd/"
IMAGE_LOCATION = "Pictures"

def image_analysis():
    for filename in os.listdir(IMAGE_LOCATION):
        if not (filename.endswith(".jpg") or filename.endswith(".png")):
            continue

        local_path = os.path.join(IMAGE_LOCATION, filename)
        s3_key = DEST_BUCKET + filename

        s3.upload_file(local_path, S3_BUCKET_NAME, s3_key)
        print(f"Uploaded {filename} to S3 bucket {S3_BUCKET_NAME} at {s3_key} successfully.")

        response = rekognition.detect_labels(
            Image={"S3Object": {"Bucket": S3_BUCKET_NAME, "Name": s3_key}},
            MaxLabels=10,
            MinConfidence=75
        )

        Labels = [{"Name": Label["Name"], "Confidence": round(Label["Confidence"], 3)} for Label in response["Labels"]]
        print(f"These labels were detected in {filename}:")
        for Label in Labels:
            print(f"  {Label['Name']} ({Label['Confidence']}%)")
        
        dynamodb.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                "filename": {"S": s3_key},
                "labels": {"S": str(Labels)},
                "branch": {"S": os.getenv("GITHUB_REF_NAME", "main")},
                "timestamp": {"S": datetime.now().isoformat() + "Z"}
           }
        )

        print(f"Labels for {filename} stored in DynamoDB table {DYNAMODB_TABLE}\n")

if __name__ == "__main__":
    image_analysis()            
