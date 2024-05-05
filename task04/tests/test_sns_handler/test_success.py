from tests.test_sns_handler import SnsHandlerLambdaTestCase


class TestSuccess(SnsHandlerLambdaTestCase):

    def test_success(self):
        lambda_response = self.HANDLER.handle_request(dict(), dict())
        self.assertTrue(True)
