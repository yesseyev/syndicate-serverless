from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4 as generate_id

import boto3
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


@dataclass
class InputSchema:
    principalId: int
    content: dict


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        IncomeEvent:
            principalId: int
            content: dict

        SaveData:
            id: uuid
            principalId: int
            createdAt: str
            body: dict (same as incoming `content`)

        Output:
            statusCode: 201,
            event: SaveData

        """
        try:
            ev = InputSchema(**event)
        except TypeError:
            return {
                "statusCode": 400,
                "message": "Invalid input event passed"
            }

        payload = {
            "id": str(generate_id()),
            "created_at": datetime.now().isoformat(),
            "principalId": ev.principalId,
            "body": ev.content
        }

        # add payload to DynamoDB
        dyn_resource = boto3.resource("dynamodb")
        table = dyn_resource.Table("Events")
        table.put_item(Item=payload)

        return {
            "statusCode": 201,
            "event": payload
        }


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
