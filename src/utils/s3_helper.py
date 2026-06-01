import uuid

import base64

import aioboto3

from src.database.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_BUCKET_NAME,
    CLOUDFRONT_URL
)


class S3Helper:

    @classmethod
    async def upload_base64_image(
        cls,
        base64_image: str
    ):

        if "," in base64_image:

            base64_image = (
                base64_image.split(",")[1]
            )

        image_data = base64.b64decode(
            base64_image
        )

        file_name = (
            f"products/{uuid.uuid4()}.jpg"
        )

        session = aioboto3.Session()

        async with session.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        ) as s3_client:

            await s3_client.put_object(
                Bucket=AWS_BUCKET_NAME,
                Key=file_name,
                Body=image_data,
                ContentType="image/jpeg"
            )

        image_url = (
            f"{CLOUDFRONT_URL}/{file_name}"
        )

        return image_url
    
    
    
    @classmethod
    async def delete_image(
        cls,
        image_url: str
    ):

        try:

            file_key = image_url.split(
                f"{CLOUDFRONT_URL}/"
            )[-1]

            session = aioboto3.Session()

            async with session.client(
                "s3",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            ) as s3_client:

                await s3_client.delete_object(
                    Bucket=AWS_BUCKET_NAME,
                    Key=file_key
                )

        except Exception as error:

            print(
                f"S3 Delete Error: {error}"
            )
