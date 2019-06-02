import gspread
from gspread.utils import numericise_all
from genson import SchemaBuilder
from singer.schema import Schema
from oauth2client.service_account import ServiceAccountCredentials
import logging

logging.getLogger('oauth2client').setLevel(logging.ERROR)

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
        self.data = None
        self.schema = None

    def get_data(self, sheet_name):
        if self.data is None:
            sheet1 = self.client.open(sheet_name).sheet1
            self.data = sheet1.get_all_records()

    def get_records_as_json(self, sheet_name):
        self.get_data(sheet_name)
        return self.data

    def get_schema(self, sheet_name):
        self.get_data(sheet_name)

        # add object to schema builder so he can infer schema
        builder = SchemaBuilder()
        for record in self.data:
            builder.add_object(record)

        # create a singer Schema from Json Schema
        singer_schema = Schema.from_dict(builder.to_schema())
        self.schema = singer_schema.to_dict()

        return self.schema
