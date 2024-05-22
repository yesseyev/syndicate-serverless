import boto3


class CognitoClient:
	def __init__(self, user_pool_name: str, client_name: str):
		self._user_pool_name = user_pool_name
		self._cog = boto3.client('cognito-idp')
		self.user_pool_id = self.__get_user_pool_id_by_name(user_pool_name)
		self.client_id = self.__get_client_id_by_name(self.user_pool_id, client_name)

	def __get_user_pool_id_by_name(self, user_pool_name):
		response = self._cog.list_user_pools(MaxResults=60)

		for user_pool in response['UserPools']:
			if user_pool['Name'] == user_pool_name:
				return user_pool['Id']

		return None

	def __get_client_id_by_name(self, user_pool_id, client_name):
		response = self._cog.list_user_pool_clients(
			UserPoolId=user_pool_id,
			MaxResults=10
		)

		for app_client in response['UserPoolClients']:
			if app_client['ClientName'] == client_name:
				return app_client['ClientId']

		return None

	def add_user(self, email: str, password: str, first_name: str, last_name: str):
		self._cog.admin_create_user(
			UserPoolId=self.user_pool_id,
			Username=email,
			UserAttributes=[
				{
					'Name': 'email',
					'Value': email
				},
				{
					'Name': 'given_name',
					'Value': first_name
				},
				{
					'Name': 'family_name',
					'Value': last_name
				},
			],
			TemporaryPassword=password,
			MessageAction='SUPPRESS'
		)
		resp = self._cog.admin_set_user_password(
			UserPoolId=self.user_pool_id,
			Username=email,
			Password=password,
			Permanent=True
		)
		print(f"Received response: {resp}")

	def get_access_token(self, email, password):
		response = self._cog.initiate_auth(
			ClientId=self.client_id,
			AuthFlow='USER_PASSWORD_AUTH',
			AuthParameters={
				'USERNAME': email,
				'PASSWORD': password
			}
		)

		# access_token = response['AuthenticationResult']['AccessToken']
		id_token = response['AuthenticationResult']['IdToken']

		return {"accessToken": id_token}
