from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


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
        # todo implement business logic
        return 200
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
