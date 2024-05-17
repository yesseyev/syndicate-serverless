import json

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')

import requests


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """ Get weather data using Open Meteo API """
        print('Event', event)
        if 'rawPath' in event:
            print(f'rawPath: {event["rawPath"]}')

        url = 'https://api.open-meteo.com/v1/forecast?latitude=52.27&longitude=6.87417&current=' \
              'temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m'
        response = requests.get(url)

        return response.json()


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
