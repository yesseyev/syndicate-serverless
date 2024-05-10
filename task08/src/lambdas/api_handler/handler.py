import json
import httpx

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda


_LOG = get_logger('ApiHandler-handler')
_BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_forecast(latitude: float, longitude: float) -> str:
	url = f"{_BASE_URL}?latitude={latitude}&longitude={longitude}"
	response = httpx.get(url)
	response.raise_for_status()

	return response.text


def build_response(code: int, body: str | dict) -> dict:
	return {
		'statusCode': code,
		'headers': {
			'Content-Type': 'application/json',
		},
		'body': body if isinstance(body, str) else json.dumps(body),
		'isBase64Encoded': False
	}


class ApiHandler(AbstractLambda):

	def validate_request(self, event) -> dict:
		pass

	def handle_request(self, event, context):
		""" Get weather data using Open Meteo API """
		request_params = event.get('requestContext', {}).get('http', {})
		method, path = request_params.get('method'), request_params.get('path')
		if not (method == 'GET' and path == '/weather'):
			return build_response(
				code=400,
				body={
					'statusCode': 400,
					'message': f'Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}'
				}
			)

		try:
			latitude, longitude = 51.169392, 71.449074
			weather_data = get_weather_forecast(latitude, longitude)
			return build_response(code=200, body=weather_data)

		except Exception as exc:
			return build_response(code=400, body="Error " + str(exc))


HANDLER = ApiHandler()


def lambda_handler(event, context):
	return HANDLER.lambda_handler(event=event, context=context)
