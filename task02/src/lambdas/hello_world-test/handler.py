import json

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('Hello_worldTest-handler')


def build_response(code: int, body: dict) -> dict:
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps(body),
        'isBase64Encoded': False
    }


class Hello_worldTest(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        _LOG.info(event)
        requestParams = event.get('requestContext', {}).get('http', {})
        method, path = requestParams.get('method'), requestParams.get('path')
        if not (method == 'GET' and path == '/hello'):
            return build_response(
                code=400,
                body={
                    'statusCode': 400,
                    'message': f'Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}'
                }
            )

        return build_response(
            code=200,
            body={
                'statusCode': 200,
                'message': 'Hello from Lambda'
            }
        )


HANDLER = Hello_worldTest()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
