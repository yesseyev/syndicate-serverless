import json
import os
from datetime import datetime
from uuid import uuid4 as generate_id

import boto3
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('UuidGenerator-handler')


class UuidGenerator(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Create s3 object with 10 UUIDs named as timestamp
        """
        lambda_name = os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'NO_NAME')
        s3_bucket_name = lambda_name.replace('uuid_generator', 'uuid-storage')

        s3_client = boto3.client('s3')
        payload_data = {"ids": [str(generate_id()) for _ in range(10)]}
        s3_file_key = datetime.now().isoformat()

        s3_client.put_object(
            Body=json.dumps(payload_data),
            Bucket=s3_bucket_name,
            Key=s3_file_key
        )


HANDLER = UuidGenerator()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
