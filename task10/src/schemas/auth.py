import re

from dataclasses import dataclass


def validate_email(email):
	# Regular expression for email validation
	pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
	if not re.match(pattern, email):
		raise ValueError('Bad email')


def validate_password(password):
	# Regular expression for password validation
	pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[^\w\s]).{12,}$'
	if not re.match(pattern, password):
		raise ValueError('Bad password')


@dataclass
class SignUpData:
	email: str
	password: str
	first_name: str
	last_name: str

	def __post_init__(self):
		validate_email(self.email)
		validate_password(self.password)


@dataclass
class SignInData:
	email: str
	password: str

	def __post_init__(self):
		validate_email(self.email)
		validate_password(self.password)
