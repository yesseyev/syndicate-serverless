from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('SnsHandler-handler')


class SnsHandler(AbstractLambda):
    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        if 'Records' not in event:
            return "No message"

        message = event['Records'][0]['Sns']['Message']
        _LOG.info(message)

        return {
            "statusCode": 200,
            "message": message
        }


HANDLER = SnsHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
