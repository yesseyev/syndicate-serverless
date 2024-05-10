from tests.test_api_handler import ApiHandlerLambdaTestCase


class TestSuccess(ApiHandlerLambdaTestCase):

    def test_success(self):
        event = {
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/weather"
                }
            }
        }
        lambda_response = self.HANDLER.handle_request(event, dict())
        self.assertEqual(lambda_response["statusCode"], 200)
        self.assertTrue("body" in lambda_response)

