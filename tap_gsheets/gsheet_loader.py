import gspread
from gspread.utils import numericise_all
from genson import SchemaBuilder, TypedSchemaStrategy
from singer.schema import Schema
from oauth2client.service_account import ServiceAccountCredentials
import logging
import datetime

logging.getLogger('oauth2client').setLevel(logging.ERROR)
date_format = None

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
        self.data = {}
        self.headers = {}
        self.schema = {}
        self.sheet_name = None
        self.spreadsheet = None

    def get_data(self, sheet_name, worksheet_name, start_from_row):
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
            self.data[worksheet_name] = sheet.get_all_records(head=start_from_row)
            self.headers[worksheet_name] = sheet.row_values(start_from_row)

    def get_records_as_json(self, sheet_name, worksheet_name, start_from_row):
        self.get_data(sheet_name, worksheet_name, start_from_row)
        return self.data[worksheet_name]

    def get_schema(self, sheet_name, worksheet_name, start_from_row):
        self.get_data(sheet_name, worksheet_name, start_from_row)

        # add object to schema builder so he can infer schema
        builder = CustomSchemaBuilder()
        if len(self.data[worksheet_name]) == 0:
            # build sample record to be used for schema inference if the
            # spreadsheet is empty
            sample_record = {key: "some string" for key in self.headers[worksheet_name]}
            builder.add_object(sample_record)
        else:
            for record in self.data[worksheet_name]:
                builder.add_object(record)

        # create a singer Schema from Json Schema
        singer_schema = Schema.from_dict(builder.to_schema())
        self.schema[worksheet_name] = singer_schema.to_dict()

        return self.schema[worksheet_name]


class CustomDateTime(TypedSchemaStrategy):
    """
    strategy for date-time formatted strings
    """
    JS_TYPE = 'string'
    PYTHON_TYPE = (str, type(u''))

    # create a new instance variable
    def __init__(self, node_class):
        super().__init__(node_class)
        self.format = "date-time"
        self.timestamp = None

    @classmethod
    def match_object(self, obj):
        super().match_object(obj)
        try:
            date_time_obj = datetime.datetime.strptime(obj, "{}".format(date_format))
            if isinstance(date_time_obj, datetime.datetime):
                return True
            else:
                return False
        except (TypeError, ValueError) as exception:
            #print(exception)
            return False

    def to_schema(self):
        schema = super().to_schema()
        schema['type'] = self.JS_TYPE
        schema['format'] = self.format
        return schema

class CustomSchemaBuilder(SchemaBuilder):
    """ detects & labels date-time formatted strings """
    EXTRA_STRATEGIES = (CustomDateTime,)
