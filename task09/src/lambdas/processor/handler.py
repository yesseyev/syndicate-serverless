from decimal import Decimal
import json
import os
from uuid import uuid4 as generate_id

import boto3
import requests

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda


_LOG = get_logger('Processor-handler')


def get_forecast():
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.27&longitude=6.87417&current=temperature_2m," \
          "wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    response = requests.get(url)
    return response.json()


class Processor(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # Prepare table
        lambda_name = os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'NO_NAME')
        dyn_table = lambda_name.replace('processor', 'Weather')
        _LOG.info(f'Using table: {dyn_table}')

        dyn_resource = boto3.resource('dynamodb')
        table = dyn_resource.Table(dyn_table)
        api_response = get_forecast()
        payload = {
            "id": str(generate_id()),
            "forecast": {
                "elevation": api_response['elevation'],
                "generationtime_ms": api_response['generationtime_ms'],
                "hourly": {
                    "temperature_2m": api_response['hourly']['temperature_2m'],
                    "time": api_response['hourly']['time']
                },
                "hourly_units": {
                    "temperature_2m": api_response['hourly_units']['temperature_2m'],
                    "time": api_response['hourly_units']['time']
                },
                "latitude": api_response['latitude'],
                "longitude": api_response['longitude'],
                "timezone": api_response['timezone'],
                "timezone_abbreviation": api_response['timezone_abbreviation'],
                "utc_offset_seconds": api_response['utc_offset_seconds']
            }
        }
        item = json.loads(json.dumps(payload), parse_float=Decimal)

        table.put_item(Item=item)

        return item


HANDLER = Processor()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
