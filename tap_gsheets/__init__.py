#!/usr/bin/env python3

import singer
from singer import utils
from tap_gsheets.gsheet_loader import GSheetsLoader

REQUIRED_CONFIG_KEYS = [
    "sheet_name",
    "gsheets_api"
]
LOGGER = singer.get_logger()


def sync(config):
    """
    Authenticates a connection with the Google API, retrieves a spreadsheet and
    outputs its values in a JSON format
    """

    gsheets_loader = GSheetsLoader(config['gsheets_api'])
    sheet_name = config['sheet_name']

    singer.write_records(
        sheet_name,
        gsheets_loader.get_records_as_json(sheet_name)
    )


@utils.handle_top_exception(LOGGER)
def main():

    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    sync(args.config)

if __name__ == "__main__":
    main()
