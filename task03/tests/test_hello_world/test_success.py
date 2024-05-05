from tests.test_hello_world import HelloWorldLambdaTestCase


class TestSuccess(HelloWorldLambdaTestCase):

    def test_success(self):
        lambda_response = self.HANDLER.handle_request(dict(), dict())
        self.assertEqual(lambda_response['statusCode'], 200)
        self.assertEqual(lambda_response['message'], "Hello from Lambda")

