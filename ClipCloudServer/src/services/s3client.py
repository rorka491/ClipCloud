import aioboto3
from src.core.config import STORAGE_ADDRESS
from botocore.config import Config



class S3Client:
    storage_address = STORAGE_ADDRESS
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
        verify_ssl: bool = False 
    ) -> None:
        self.bucket_name = bucket_name

        self._session = aioboto3.Session()
        self._client_kwargs = {
            "service_name": "s3",
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "verify": verify_ssl,
            "config": Config(signature_version="s3v4"),
        }

    def _client(self):
        return self._session.client(**self._client_kwargs)


    async def upload(self, key: str, data: bytes, content_type: str):
        async with self._client() as s3:
            await s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=data,
                ContentType=content_type,
            )
        return f'{self.storage_address}/{key}'

