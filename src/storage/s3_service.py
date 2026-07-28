import json
import logging
from datetime import datetime

import boto3

from src.config.aws import AWS_REGION, S3_BUCKET


class S3Service:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.client = boto3.client(
            "s3",
            region_name=AWS_REGION
        )

    def upload_json(self, data):

        now = datetime.utcnow()

        key = (
            f"raw/"
            f"{now.year}/"
            f"{now.month:02d}/"
            f"{now.day:02d}/"
            f"crypto_market_{now.strftime('%Y%m%d_%H%M%S')}.json"
        )

        self.client.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=json.dumps(data, indent=2),
            ContentType="application/json"
        )

        self.logger.info(f"Uploaded raw file to s3://{S3_BUCKET}/{key}")

        return key