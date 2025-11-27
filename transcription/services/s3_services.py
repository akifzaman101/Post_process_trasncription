import boto3
from django.conf import settings
from botocore.exceptions import BotoCoreError, ClientError




class S3Service:
    def __init__(self):
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME
        self.region = settings.AWS_REGION
        self.client = boto3.client(
            "s3",
            region_name=self.region,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def upload_chunks(self, file_chunks, path):
        try:
            self.client.upload_fileobj(file_chunks, self.bucket, path)
        except Exception as e:
            raise Exception(f"Error uploading file to S3: {e}")

    
