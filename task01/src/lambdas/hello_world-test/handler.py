from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('Hello_worldTest-handler')


class Hello_worldTest(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        return {
            "statusCode": 200,
            "message": "Hello from Lambda"
        }
    

HANDLER = Hello_worldTest()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
