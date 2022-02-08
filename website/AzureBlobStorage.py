# upload_blob_images_parallel.py
# Python program to bulk upload jpg image files as blobs to azure storage
# Uses ThreadPool for faster parallel uploads!
# Uses latest python SDK() for Azure blob storage
# Requires python 3.6 or above
import os
from multiprocessing.pool import ThreadPool
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
from sqlalchemy.sql.functions import current_user, now
from flask_login import current_user
from .models import Student, Documents
from .import db
from sqlalchemy.sql import func
from datetime import date

today = date.today()

# IMPORTANT: Replace connection string with your storage account connection string
# Usually starts with DefaultEndpointsProtocol=https;...
MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=updocst;AccountKey=YopaE7MD6BkWhZcO5D0TTxM0EhZBbsG4pizVZ8pv0fDVqdZ+FJqMpNUsMjXJgEujhkWai3yqjdoWxi/EphudmA==;EndpointSuffix=core.windows.net"

# Replace with blob container
MY_IMAGE_CONTAINER = "updocblob"

user=current_user
if user!=None:
    studentid= user.get_id()

class AzureBlobFileUploader:

    def __init__(self):
        print("Intializing AzureBlobFileUploader")

        # Initialize the connection to Azure storage account
        self.blob_service_client = BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)

    def run(self, all_file_names):
        # Upload 10 files at a time!
        with ThreadPool(processes=int(10)) as pool:
            return pool.map(self.upload_image, all_file_names)

    def upload_image(self, file_name):
        # Create blob with same name as local file name
        blob_client = self.blob_service_client.get_blob_client(container=MY_IMAGE_CONTAINER,
                                                               blob=file_name)
        # Get full path to the file
        upload_file_path = os.path.join(file_name)

        # Create blob on storage
        # Overwrite if it already exists!
        image_content_setting = ContentSettings(content_type='image/jpeg')
        print(f"uploading file - {file_name}")
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=image_content_setting)
            docurl=blob_client.url
            document=Documents(id=studentid,document_uploaded=docurl,filename=file_name,uploaded_on=today)
            db.session.add(document)
            db.session.commit()
        return file_name



# Initialize class and upload files
azure_blob_file_uploader = AzureBlobFileUploader()
azure_blob_file_uploader.upload_all_images_in_folder()
