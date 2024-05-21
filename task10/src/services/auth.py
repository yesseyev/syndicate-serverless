from clients.cognito_client import CognitoClient
from commons.log_helper import get_logger
from schemas.auth import SignInData, SignUpData


_LOG = get_logger('AuthService')


class AuthService:
	def __init__(self, user_pool_name: str, client_name: str):
		self._client = CognitoClient(user_pool_name, client_name)

	def sign_up(self, body):
		try:
			ev = SignUpData(**body)
		except (TypeError, ValueError):
			_LOG.error("Error while registration form validation", exc_info=True)
			return 400, "There was an error in the request"

		try:
			self._client.add_user(
				email=ev.email,
				password=ev.password,
				first_name=ev.firstName,
				last_name=ev.lastName,
			)
		except Exception:
			_LOG.error("Error while cognito sign up", exc_info=True)
			return 400, "There was an error in the request"

		return 200, "Sign-up process is successful"

	def sign_in(self, body):
		try:
			ev = SignInData(**body)
		except (TypeError, ValueError):
			_LOG.error("Error while login data", exc_info=True)
			return 400, "There was an error in the request"

		try:
			auth_data = self._client.get_access_token(
				email=ev.email,
				password=ev.password
			)
		except Exception:
			_LOG.error("Error while cognito sign in", exc_info=True)
			return 400, "There was an error in the request"

		return 200, auth_data
