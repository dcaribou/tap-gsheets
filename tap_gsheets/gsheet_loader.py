import gspread
import warnings
import functools
from genson import SchemaBuilder
from singer.schema import Schema
from oauth2client.service_account import ServiceAccountCredentials
import logging

logging.getLogger('oauth2client').setLevel(logging.ERROR)

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func


class GSheetsLoader:
    """Wrapper for authenticating and retrieving data from Google Sheets"""

    def __init__(self, config):
        super(GSheetsLoader, self).__init__()
        self.config = config
        # TODO: Move the scope to a config file
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(config, scope)
        client = gspread.authorize(creds)
        self.client = client
        self.data = {}
        self.headers = {}
        self.schema = {}
        self.sheet_name = None
        self.spreadsheet = None

    def get_data(self, sheet_name, worksheet_name=None):
        # reset cache in case of switching to another sheet
        if self.sheet_name is None or self.sheet_name != sheet_name:
            del self.data
            self.data = {}
            self.schema = {}
            self.headers = {}
            self.sheet_name = sheet_name
            self.spreadsheet = self.client.open(sheet_name)

        # backwards compatibility
        if worksheet_name is None:
            worksheet_name = self.spreadsheet.sheet1.title

        if worksheet_name not in self.data:
            sheet = self.spreadsheet.worksheet(worksheet_name)
            self.data[worksheet_name] = sheet.get_all_records()
            self.headers[worksheet_name] = sheet.row_values(1)

        return self.data[worksheet_name]

    @deprecated
    def get_records_as_json(self, sheet_name, worksheet_name=None):
        return self.get_data(sheet_name, worksheet_name)

    def get_schema(self, sheet_name, worksheet_name=None):
        data = self.get_data(sheet_name, worksheet_name)

        # add object to schema builder so he can infer schema
        builder = SchemaBuilder()
        if len(data) == 0:
            # build sample record to be used for schema inference if the
            # spreadsheet is empty
            sample_record = {key: "some string" for key in self.headers[worksheet_name]}
            builder.add_object(sample_record)
        else:
            for record in data:
                builder.add_object(record)

        # create a singer Schema from Json Schema
        singer_schema = Schema.from_dict(builder.to_schema())
        self.schema[worksheet_name] = singer_schema.to_dict()

        return self.schema[worksheet_name]
