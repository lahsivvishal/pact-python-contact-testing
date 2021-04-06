import os
import requests
import pytest
from pact import Consumer, Provider, Format
import unittest
import json


pact = Consumer('Consumer').has_pact_with(Provider('Provider'), port=1234,host_name='localhost')
pact.start_service()

CURR_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
PACT_DIR = os.path.join(CURR_FILE_PATH, '')
PACT_FILE = os.path.join(PACT_DIR, 'pact.json')

#defining class
class GetUsers(unittest.TestCase):
    def test_get_board(self):
        with open(os.path.join(PACT_DIR, PACT_FILE), 'rb') as path_file:
            pact_file_json = json.load(path_file)

            (pact
                .given('Request to send message')
                .upon_receiving('a request for response or send message')
                .with_request(method = 'GET', path = '/api/users?page=2')
                .will_respond_with(status = 200, body = pact_file_json))

            with pact:
                result = requests.get('https://reqres.in/api/users?page=2')
                print(result)

            self.assertEqual(pact_file_json, result.json())
            pact.verify()


ge = GetUsers()
print(ge.test_get_board())
