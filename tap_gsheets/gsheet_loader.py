import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

class GSheetsLoader:
    """Wrapper for authenticating and retrieving data from Google Sheets"""

    def __init__(self, config):
        super(GSheetsLoader, self).__init__()
        self.config = config
        # TODO: Move the scope to a config file
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(config, scope)
        client = gspread.authorize(creds)
        self.client = client

    def get_records_as_json(self, sheet_name):
        sheet1 = self.client.open(sheet_name).sheet1
        return sheet1.get_all_records()
