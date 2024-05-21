import json
import os


from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
from services.auth import AuthService
from services.reservation import ReservationService
_LOG = get_logger('ApiHandler-handler')


def build_response(code: int, body: dict) -> dict:
    return {
        'statusCode': code,
        'body': json.dumps(body)
    }


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        ...

    def handle_request(self, event, context):
        _LOG.info(f'Event: {event}')
        lambda_name = os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'NO_NAME')

        # Init auth service
        user_pool_name, client_name = lambda_name.replace('api_handler', 'simple-booking-userpool'), "app_users"
        _LOG.info(f'Using user pool: {user_pool_name} and app client: {client_name}')
        auth_service = AuthService(user_pool_name, client_name=client_name)

        # Init reservation service
        reservations_tbl_name = lambda_name.replace('api_handler', 'Reservations')
        tables_tbl_name = lambda_name.replace('api_handler', 'Tables')
        _LOG.info(f'Using tables: {reservations_tbl_name} and {tables_tbl_name}')
        reservation_service = ReservationService(reservations_tbl_name, tables_tbl_name)

        # Define routes
        routes = {
            ('POST', '/signup'): auth_service.sign_up,
            ('POST', '/signin'): auth_service.sign_in,
            ('POST', '/tables'): reservation_service.add_table,
            ('GET', '/tables'): reservation_service.get_tables,
            ('GET', '/tables/{tableId}'): reservation_service.get_table,
            ('POST', '/reservations'): reservation_service.add_reservation,
            ('GET', '/reservations'): reservation_service.get_reservations,
        }
        route = event['httpMethod'], event['resource']

        if route in routes:
            if route[0] == "POST":
                body = json.loads(event['body'])
                return build_response(*routes[route](body))
            elif route[0] == "GET":
                return build_response(*routes[route](event['path']))

        _LOG.info('Unsupported request type for my task10 app')
        return build_response(400, {'Error message': f'Bad request. Unable to locate route: {route} '})


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
