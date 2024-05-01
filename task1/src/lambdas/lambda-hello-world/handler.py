from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('LambdaHelloWorld-handler')


class LambdaHelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        return {
            "statusCode": 200,
            "message": "Hello from Lambda"
        }
    

HANDLER = LambdaHelloWorld()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
