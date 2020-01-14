import os
import json
from unittest import TestCase

from .directline_client import DirectLineClient


class PyBotTest(TestCase):
    def setUp(self):
        direct_line_config = os.environ.get(
            "DIRECT_LINE_CONFIG", "DirectLineConfig.json"
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
        items_e = ['1 Coca Cola', '3 Agua Mineral', '500Gr Frutos Secos', '5 Alfajor de Arroz', '500Gr Banana', '500Gr Manzana', '500Gr Yerba Organica']

        send_result = client.send_message(user_message)
        self.assertIsNotNone(send_result)
        self.assertEqual(200, send_result.status_code)

        response, text = client.get_message()
        items_a = get_items(text)
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        for item_a, item_e in zip(items_e, items_a):
            self.assertEqual(item_a, item_e)


def get_items(text):
    item_list = []
    for i in range(1, len(text)):
        item_list.append(text[i]['text'])
    return item_list