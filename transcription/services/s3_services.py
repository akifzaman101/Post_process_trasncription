import boto3
from django.conf import settings
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
            file_chunks.close()
        except Exception as e:
            raise Exception(f"Error uploading file to S3: {e}")
        
    def list_files(self, path):
        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=path
            )
            return response.get("Contents", [])
        except Exception as e:
            raise Exception(f"Error listing files: {e}")

    def download_file(self, key, local_path):
        try:
            self.client.download_file(self.bucket, key, local_path)
        except Exception as e:
            raise Exception(f"Error downloading file: {e}")

    def upload_file(self, local_path, key):
        try:
            self.client.upload_file(local_path, self.bucket, key)
        except Exception as e:
            raise Exception(f"Error uploading merged file: {e}")

    
