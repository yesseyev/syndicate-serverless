import asyncio
import json

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

from open_meteo import OpenMeteo
from open_meteo.models import HourlyParameters

_LOG = get_logger('ApiHandler-handler')


async def get_weather_forecast(latitude: float, longitude: float) -> dict:
	async with OpenMeteo() as open_meteo:
		forecast = await open_meteo.forecast(
			latitude=latitude,
			longitude=longitude,
			current_weather=True,
			hourly=[
				HourlyParameters.TEMPERATURE_2M,
				HourlyParameters.RELATIVE_HUMIDITY_2M,
			],
		)

	return json.loads(forecast.json())


class ApiHandler(AbstractLambda):

	def validate_request(self, event) -> dict:
		pass

	def handle_request(self, event, context):
		""" Get weather data using Open Meteo API """
		print('Event', event)
		latitude, longitude = 51.169392, 71.449074
		loop = asyncio.get_event_loop()
		weather_data = loop.run_until_complete(get_weather_forecast(latitude, longitude))
		return weather_data


HANDLER = ApiHandler()


def lambda_handler(event, context):
	return HANDLER.lambda_handler(event=event, context=context)
