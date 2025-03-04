import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
from datetime import datetime, timedelta
import mimetypes
import shutil

class R2Manager:
    def __init__(self):
        self.region = 'auto'
        self.endpoint = 'https://264f6d64d30e423773358f553ad62463.r2.cloudflarestorage.com'
        self.access_key_id = '90fb7b22ab6188f6533d89687db014a4'
        self.secret_access_key = 'f95bc846590a0a44456ec8a75312e5081a6bae8dd79198c055683371727f9d65'
        self.bucket_name = 'cloudydrive'
        self.prefix = 'cloudy4win/'

        self.s3 = boto3.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region
        )

    def upload_file(self, filename, filepath):
        """Uploads a file to R2."""
        try:
            object_key = self.prefix + filename
            with open(filepath, 'rb') as data:
                 self.s3.upload_fileobj(data, self.bucket_name, object_key)
            print(f"Uploaded {filename} to {self.bucket_name}/{object_key}")
            return True
        except FileNotFoundError:
            print(f"The file {filepath} was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return False

    def delete_file(self, filename):
        """Deletes a file from R2."""
        try:
            object_key = self.prefix + filename
            self.s3.delete_object(Bucket=self.bucket_name, Key=object_key)
            print(f"Deleted {filename} from {self.bucket_name}/{object_key}")
            return True
        except ClientError as e:
            print(f"Error deleting file: {e}")
            return False

    def download_file(self, filename):
        """Downloads a file from R2."""
        try:
            object_key = self.prefix + filename
            local_filename = filename
            self.s3.download_file(self.bucket_name, object_key, local_filename)
            print(f"Downloaded {filename} from {self.bucket_name}/{object_key} to {local_filename}")
            return True
        except ClientError as e:
            print(f"Error downloading file: {e}")
            return False

    def list_files(self):
        """Lists files in the R2 bucket with the given prefix."""
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=self.prefix)
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append(obj['Key'].replace(self.prefix, ""))
            return files
        except ClientError as e:
            print(f"Error listing files: {e}")
            return []

    def get_presigned_url(self, filename, expiration=3600):
        """Generate a presigned URL to share the file"""
        try:
          object_key = self.prefix + filename
          response = self.s3.generate_presigned_url('get_object',
                                                          Params={'Bucket': self.bucket_name,
                                                                  'Key': object_key},
                                                          ExpiresIn=expiration)
          return response
        except ClientError as e:
            print(f"Error generating presigned url: {e}")
            return None
        
    def get_file_details(self, filename):
        """Get the file size and type from R2."""
        try:
            object_key = self.prefix + filename
            response = self.s3.head_object(Bucket=self.bucket_name, Key=object_key)

            file_size = response['ContentLength']
            # Get content type from response or detect from file extension
            file_type = response.get('ContentType')
            if not file_type:
                # Map common file extensions to MIME types
                extension = filename.lower().split('.')[-1] if '.' in filename else ''
                mime_types = {
                    'txt': 'text/plain',
                    'pdf': 'application/pdf',
                    'png': 'image/png',
                    'jpg': 'image/jpeg',
                    'jpeg': 'image/jpeg',
                    'gif': 'image/gif',
                    'mp4': 'video/mp4',
                    'mov': 'video/quicktime',
                    'avi': 'video/x-msvideo',
                    'doc': 'application/msword',
                    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'xls': 'application/vnd.ms-excel',
                    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'zip': 'application/zip'
                }
                file_type = mime_types.get(extension, 'application/octet-stream')

            # Format file size to human readable
            if file_size < 1024:
                size_str = f"{file_size} B"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.2f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"

            return size_str, file_type
        
        except ClientError as e:
            print(f"Error getting file details for {filename}: {e}")
            return "N/A", "N/A"

    def rename_file(self, old_filename, new_filename):
        """Rename a file in R2."""
        try:
            old_object_key = self.prefix + old_filename
            new_object_key = self.prefix + new_filename

            # Copy the object with the new key
            self.s3.copy_object(
                Bucket=self.bucket_name,
                CopySource={'Bucket': self.bucket_name, 'Key': old_object_key},
                Key=new_object_key
            )

            # Delete the old object
            self.s3.delete_object(Bucket=self.bucket_name, Key=old_object_key)

            print(f"Renamed {old_filename} to {new_filename} in {self.bucket_name}")
            return True
        except ClientError as e:
            print(f"Error renaming file: {e}")
            return False
