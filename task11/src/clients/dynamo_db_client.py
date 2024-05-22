import boto3


class DynamoDbClient:
	def __init__(self, table_name: str, id_key: str = 'id'):
		dyn_resource = boto3.resource('dynamodb')
		self._table_name = table_name
		self._table = dyn_resource.Table(table_name)
		self._id_key = id_key

	def add_item(self, item) -> None:
		response = self._table.put_item(Item=item)
		print(f"[{self._table_name}] Response: {response}")

	def get_item(self, uid) -> dict:
		return self._table.get_item(Key={
			self._id_key: int(uid)
		})["Item"]

	def find_all(self) -> list[dict]:
		return self._table.scan()["Items"]

	def find_with_filters(self, filter_expr) -> list[dict]:
		return self._table.scan(FilterExpression=filter_expr)["Items"]
