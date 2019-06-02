#!/usr/bin/env python3

import singer
from tap_gsheets.gsheet_loader import GSheetsLoader
from pyhocon import ConfigFactory
from inflection import parameterize, tableize
import argparse

def sync(config):
    """
    Authenticates a connection with the Google API, retrieves a spreadsheet and
    outputs its values in a JSON format
    """

    gsheets_loader = GSheetsLoader(config['gsheets_api'])
    sheet_name = config['sheet_name']
    snake_cased = tableize(parameterize(sheet_name))

    singer.write_schema(
        stream_name=snake_cased,
        schema=gsheets_loader.get_schema(sheet_name),
        key_properties=['id']
    )

    singer.write_records(
        stream_name=snake_cased,
        records=gsheets_loader.get_records_as_json(sheet_name)
    )


def main():

    # parse arguments. get config file path.
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='config file', required=True)
    args = parser.parse_args()

    # the configuration file can be provided in json as much as in hocon
    # ConfigFactory will pick up the format from the file extension
    config = ConfigFactory.parse_file(args.c)

    # we like to keep the config as a dict from here on
    config = config.as_plain_ordered_dict()

    # go on processing
    sync(config)


if __name__ == "__main__":
    main()
