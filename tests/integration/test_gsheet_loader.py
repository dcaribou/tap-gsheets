import unittest

from tap_gsheets.gsheet_loader import GSheetsLoader
import json
import os


test_config = {
    "type": "service_account",
    "project_id":  os.getenv('PROJECT_ID'),
    "private_key_id": os.getenv('PRIVATE_KEY_ID'),
    "private_key": os.getenv('PRIVATE_KEY'),
    "client_email": os.getenv('CLIENT_EMAIL'),
    "client_id": os.getenv('CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv('CERT_URL')
}


class TestSum(unittest.TestCase):

    def test_authentication(self):
        """
        Test that we are able to authenitcate provided some valid configs
        are passed
        """
        GSheetsLoader(test_config).client.session.close()

    def test_get_schema(self):
        """
        Test that the tap is able to infer a simple schema from a sample sheet
        """
        loader = GSheetsLoader(test_config)
        expected_schema = {
            "properties": {
                "ID": {"type": "integer"},
                "Name": {"type": "string"},
                "RegisteredAt": {"type": "string"}
            },
            "type": "object"
        }

        self.assertEqual(
            expected_schema,
            loader.get_schema('Tap Gsheets Integration Tests')
        )

        loader.client.session.close()

    def test_get_data(self):
        """
        Test that the tap outputs the expected sheet contents
        """
        loader = GSheetsLoader(test_config)
        expected_contents = [
            {'ID': 30, 'Name': 'Napoleón Bonaparte', 'RegisteredAt': '2019-03-04'},
            {'ID': 50, 'Name': 'San Juan Bautista', 'RegisteredAt': '2019-04-02'}
        ]

        self.assertEqual(
            expected_contents,
            loader.get_records_as_json('Tap Gsheets Integration Tests')
        )

        loader.client.session.close()


if __name__ == '__main__':
    unittest.main()
