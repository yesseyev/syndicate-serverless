from dataclasses import asdict
from decimal import Decimal

from clients.dynamo_db_client import DynamoDbClient
from commons.log_helper import get_logger
from schemas.reservation import ReservationData, TableData

_LOG = get_logger('ReservationService')


def convert_decimals_to_int(i):
	if isinstance(i, list):
		return [convert_decimals_to_int(i) for i in i]
	elif isinstance(i, dict):
		return {k: convert_decimals_to_int(v) for k, v in i.items()}
	elif isinstance(i, Decimal):
		return int(i)
	else:
		return i


class ReservationService:
	def __init__(self, reservations_tbl_name: str, tables_tbl_name: str):
		self._tables_tbl = DynamoDbClient(tables_tbl_name, id_key="id")
		self._reservations_tbl = DynamoDbClient(reservations_tbl_name, id_key="id")

	def add_table(self, body):
		try:
			ev = TableData(**body)
		except (TypeError, ValueError):
			_LOG.error("Error with TableData validation", exc_info=True)
			return 400, "There was an error in the request"

		self._tables_tbl.add_item(item=asdict(ev))

		return 200, {"id": ev.id}

	def get_tables(self, _):
		try:
			items = self._tables_tbl.find_all()
		except Exception:
			_LOG.error("Error while `Tables` scan", exc_info=True)
			return 400, "There was an error in the request"

		items = convert_decimals_to_int(items)
		items = sorted(items, key=lambda item: item['id'])
		result = {'tables': items}
		_LOG.info(f'Tables fetched: {result}')

		return 200, result

	def get_table(self, request_path):
		try:
			uid = int(request_path.split('/')[-1])
		except (AttributeError, ValueError):
			_LOG.error("Error with Table ID validation", exc_info=True)
			return 400, "There was an error in the request"

		try:
			item = self._tables_tbl.get_item(uid)
		except Exception:
			_LOG.error("Error with `Tables` `get_item` method", exc_info=True)
			return 400, "There was an error in the request"

		result = convert_decimals_to_int(item)

		return 200, result
