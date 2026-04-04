from aiobotocore.session import get_session
from aioboto3 import Session
from contextlib import asynccontextmanager
import logging
from src.core.config import STORAGE_ADDRESS

logger = logging.getLogger(__name__)



class S3Client:

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
        verify_ssl: bool = False
    ) -> None:
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "verify": verify_ssl
        }
        self.bucket_name = bucket_name
        self.session = get_session()
    
    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client

    
    # async def upload_file(
    #     self,
    #     file_path: str,
    # ):  
    #     object_name = file_path.split('/')[-1]

    #     async with self.get_client() as client:
    #         with open(file_path, "rb", ) as file:
    #             await client.put_object(
    #                 Bucket=self.bucket_name,
    #                 Key=object_name,
    #                 Body=file,
    #             )


    async def upload_file_stream(
        self,
        file_obj,
        object_name: str,
        content_type: str = None
    ) -> tuple[bool, str]:
        """
        Загружает файл напрямую в S3 из потока без сохранения на диск
        """
        try:
            async with self.get_client() as client:
                put_params = {
                    "Bucket": self.bucket_name,
                    "Key": object_name,
                    "Body": file_obj,
                }
                
                if content_type:
                    put_params["ContentType"] = content_type
                
                await client.put_object(**put_params)
                
            logger.info(f"File uploaded successfully: {object_name}")
            return True, f"{STORAGE_ADDRESS}/{object_name}"
            
        except Exception as e:
            logger.error(f"Error uploading file {object_name}: {e}")
            return False, None
        
