from tests.test_hello_world_test import HelloWorldTestLambdaTestCase


class TestSuccess(HelloWorldTestLambdaTestCase):

    def test_success(self):
        lambda_response = self.HANDLER.handle_request(dict(), dict())
        self.assertEqual(lambda_response['statusCode'], 200)
        self.assertEqual(lambda_response['message'], "Hello from Lambda")
