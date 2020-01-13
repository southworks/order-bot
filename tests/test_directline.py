import os
import json
from unittest import TestCase

from tests.directline_client import DirectLineClient


class PyBotTest(TestCase):
    def setUp(self):
        direct_line_config = os.environ.get(
            "DIRECT_LINE_CONFIG", "../DirectLineConfig.json"
        )
        with open(direct_line_config) as direct_line_file:
            self.direct_line_config = json.load(direct_line_file)
        self.direct_line_secret = self.direct_line_config["properties"]["properties"][
            "sites"
        ][0]["key"]
        self.assertIsNotNone(self.direct_line_secret)

    def test_deployed_bot_answer(self):
        client = DirectLineClient(self.direct_line_secret)
        user_message = "Hi"
        response_message = "The items in the list are:\n5 Chocolate\n3 Yerba\n2 Candy\n"

        send_result = client.send_message(user_message)
        self.assertIsNotNone(send_result)
        self.assertEqual(200, send_result.status_code)

        response, text = client.get_message()
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response_message, text)
        print("SUCCESS!")
