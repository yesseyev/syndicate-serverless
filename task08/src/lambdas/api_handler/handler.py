import asyncio
import json
from open_meteo import OpenMeteo

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda


_LOG = get_logger('ApiHandler-handler')


async def get_weather_forecast(latitude: float, longitude: float) -> dict:
	async with OpenMeteo() as open_meteo:
		forecast = await open_meteo.forecast(
			latitude=latitude,
			longitude=longitude,
			current_weather=True
		)

	return forecast.dict()


def build_response(code: int, body: str | dict) -> dict:
	print("BODY", json.dumps(body, default=str))
	return {
		'statusCode': code,
		'headers': {
			'Content-Type': 'application/json',
		},
		'body': body if isinstance(body, str) else json.dumps(body, default=str),
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
			loop = asyncio.get_event_loop()
			weather_data = loop.run_until_complete(get_weather_forecast(latitude, longitude))
			return build_response(code=200, body=weather_data)

		except Exception as exc:
			print(exc)
			return build_response(code=400, body="Error " + str(exc))


HANDLER = ApiHandler()


def lambda_handler(event, context):
	return HANDLER.lambda_handler(event=event, context=context)
