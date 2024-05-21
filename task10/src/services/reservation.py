from clients.dynamo_db_client import DynamoDbClient


class ReservationService:
	def __init__(self, reservations_tbl_name: str, tables_tbl_name: str):
		self._tables_tbl = DynamoDbClient(tables_tbl_name, id_key="id")
		self._reservations_tbl = DynamoDbClient(reservations_tbl_name, id_key="id")

	def add_table(self):
		self._tables_tbl.add()
		...

