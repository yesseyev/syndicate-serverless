from tests.test_hello_world_test import HelloWorldTestLambdaTestCase


class TestSuccess(HelloWorldTestLambdaTestCase):

    def test_success(self):
        event = {
            'version': '2.0', 'routeKey': '$default', 'rawPath': '/hello', 'rawQueryString': '',
            'headers': {
                'x-amzn-tls-cipher-suite': 'TLS_AES_128_GCM_SHA256', 'x-amzn-tls-version': 'TLSv1.3',
                'x-amzn-trace-id': 'Root=1-663503ff-34fbf8d41789d0f443ba17c2',
                'x-forwarded-proto': 'https', 'postman-token': '4fca0149-fe78-418c-9906-c688003438d6',
                'host': 'zaguh7lznhgtlsbi62av7533oa0rqbli.lambda-url.eu-central-1.on.aws',
                'x-forwarded-port': '443', 'x-forwarded-for': '77.245.106.188',
                'accept-encoding': 'gzip, deflate, br', 'accept': '*/*',
                'user-agent': 'PostmanRuntime/7.38.0'
            },
            'requestContext': {
                'accountId': 'anonymous', 'apiId': 'zaguh7lznhgtlsbi62av7533oa0rqbli',
                'domainName': 'zaguh7lznhgtlsbi62av7533oa0rqbli.lambda-url.eu-central-1.on.aws',
                'domainPrefix': 'zaguh7lznhgtlsbi62av7533oa0rqbli',
                'http': {
                    'method': 'GET', 'path': '/hello', 'protocol': 'HTTP/1.1',
                    'sourceIp': '77.245.106.188', 'userAgent': 'PostmanRuntime/7.38.0'
                },
                'requestId': '8e4b5e25-0b7d-424e-90f9-0612818e3007', 'routeKey': '$default',
                'stage': '$default', 'time': '03/May/2024:15:34:23 +0000',
                'timeEpoch': 1714750463305
            },
            'isBase64Encoded': False
        }
        valid_lambda_response = self.HANDLER.handle_request(event, dict())
        self.assertEqual(valid_lambda_response['statusCode'], 200)
        self.assertEqual(valid_lambda_response['message'], "Hello from Lambda")

        invalid_lambda_response = self.HANDLER.handle_request(dict(), dict())
        self.assertEqual(invalid_lambda_response['statusCode'], 400)
        self.assertTrue('Bad request syntax or unsupported method' in invalid_lambda_response['message'])
