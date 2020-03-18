import unittest
import requests_mock
import json

from .. import client as saarctf_client

TEST_DATA = '''
{
    "teams": [
        {
            "id": 1,
            "name": "NOP",
            "ip": "10.32.1.2"
        },
        {
            "id": 2,
            "name": "saarsec",
            "ip": "10.32.2.2"
        }
    ],
    "flag_ids": {
        "service_1": {
            "10.32.1.2": {
                "15": ["username1", "username1.2"],
                "16": ["username2", "username2.2"]
            },
            "10.32.2.2": {
                "15": ["username3", "username3.2"],
                "16": ["username4", "username4.2"]
            }
        }
    }
}
'''

def mock(f):
    def wrapped_f(*args, **kwargs):
        with requests_mock.mock() as m:
            m.get('https://scoreboard.ctf.saarland/attack.json', text=TEST_DATA)
            f(*args, **kwargs)
    return wrapped_f

class ClientTests(unittest.TestCase):
    @mock
    def test_mock(self):
        self.assertEqual(saarctf_client._get_status(), json.loads(TEST_DATA))

    @mock
    def test_get_teams(self):
        self.assertEqual(saarctf_client.get_teams(), [
            {
                "id": 1,
                "name": "NOP",
                "ip": "10.32.1.2"
            },
            {
                "id": 2,
                "name": "saarsec",
                "ip": "10.32.2.2"
            }
        ])

    @mock
    def test_get_ips(self):
        self.assertEqual(saarctf_client.get_ips(), [
            "10.32.1.2",
            "10.32.2.2",
        ])

    @mock
    def test_is_online(self):
        self.assertTrue(saarctf_client.is_online('10.32.1.2'))
        self.assertFalse(saarctf_client.is_online('10.32.3.2'))

    @mock
    def test_assert_online(self):
        try:
            saarctf_client.assert_online('10.32.1.2')
        except AssertionError:
            fail()

        try:
            saarctf_client.assert_online('10.32.3.2')
            fail()
        except AssertionError:
            pass

    @mock
    def test_get_services(self):
        self.assertEqual(saarctf_client.get_services(), ['service_1'])

    @mock
    def test_get_flag_ids(self):
        self.assertEqual(
            saarctf_client.get_flag_ids('service_1', '10.32.1.2'),
            {
                '15': ['username1', 'username1.2'],
                '16': ['username2', 'username2.2'],
            }
        )

        self.assertEqual(
            saarctf_client.get_flag_ids('service_1', '10.32.2.2'),
            {
                '15': ['username3', 'username3.2'],
                '16': ['username4', 'username4.2'],
            }
        )
