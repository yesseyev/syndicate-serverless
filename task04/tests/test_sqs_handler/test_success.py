from tests.test_sqs_handler import SqsHandlerLambdaTestCase


class TestSuccess(SqsHandlerLambdaTestCase):

    def test_success(self):
        lambda_response = self.HANDLER.handle_request(dict(), dict())
        self.assertTrue(True)

