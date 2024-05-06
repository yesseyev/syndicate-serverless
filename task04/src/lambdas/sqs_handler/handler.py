from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('SqsHandler-handler')


class SqsHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        if 'Records' not in event:
            return "No message"

        message = str(event['Records'][0]['body'])
        _LOG.info(message)

        return {
            "statusCode": 200,
            "message": message
        }


HANDLER = SqsHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
