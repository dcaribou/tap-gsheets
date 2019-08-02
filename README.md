# tap-gsheets
This is a [Singer](https://singer.io) tap that extracts data from Google Spreadsheets. It produces JSON-formatted data following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

# Configuration
The tap uses the Google API underneath for accessing sheets data, so you need to
[create some credentials accordingly](https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2).

Once you have your credentials, you need to put them in the `gsheets_api` key in the configuration file so they are picked up by the tap. With another key `sheet_name` for indicating the sheet to be extrated.

The tap supports configuration files in JSON as much as in [HOCON](https://github.com/chimpler/pyhocon) format. Use a `.json` extension for JSON format and a `.conf` extension for HOCON format.

# Example
Tapping onto a Google sheet named `Investor Loans` can be achieved with a HOCON config file such as
```hocon
{ # config.conf
  sheet_name = "Investor Loans",
  gsheets_api {
    type = "service_account",
    project_id = "some-gc-project",
    private_key_id = ${PRIVATE_KEY_ID},
    private_key = ${PRIVATE_KEY},
    client_email = ${CLIENT_EMAIL},
    client_id = ${CLIENT_ID},
    auth_uri =  "https://accounts.google.com/o/oauth2/auth",
    token_uri = "https://oauth2.googleapis.com/token",
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs",
    client_x509_cert_url = ${CERT_URL}
  }
}
```
Which will output something like
```console
$ tap-gsheets -c config.conf
{"type": "RECORD", "stream": "Investor Loans", "record": {"id": 11, "start_date": "2018-08-22", "end_date": "2020-04-17", "investor": "Banking Corp", "amount": 20000000, "interest_rate": 0.20, "add_to_capital": "FALSE", "user_id": "some_user", "created_at": "2018-08-22 11:00:40", "updated_at": "2018-08-22 11:00:40"}}
```

## Additional config
Import your service account config from the file Google provides:
```hocon
{ # config.conf
  gsheets_api {
    include "gcloud-team-name-001122334455.json"
  }
}
```

Change the table name format to singular form and convert column names to the valid database format:
```hocon
{ # config.conf
  underscore_columns = True,
  singular_table_name = True,
}
```

Process several sheets and worksheets in that sheets at a time:
```hocon
{ # config.conf
  sheets = [
    {
      name = "Investor Loans",
      worksheets = [
        PageA,
        PageB,
        PageC
      ]
    },
    {
      # ...
    }
  ]
}
```

# Overriding configuration
The configurations in the file can be overriden with the command line parameter `--overrides`,
which takes configuration overrides in a JSON string and applies them over the passed
config file.
```bash
tap-gsheets -c config.conf --overrides '{"sheet_name":"2019 Baseball Games"}'
```

# Install
To install the `tap-gsheets` utility as a system command, create and activate a
Python3 virtual environment
```bash
$ cd tap-gsheets
$ python3 -m venv ~/.virtualenvs/tap-gsheets
$ source ~/.virtualenvs/tap-gsheets/bin/activate
```
and install the package
```bash
$ pip install -e .
```

# Integration Tests
The [integration tests spec](tests/integration/test_gsheet_loader.py) tests the project against a [sample Google sheet](https://docs.google.com/a/pagantis.com/spreadsheets/d/e/2PACX-1vRcyNFmNV4EXv_J7CyiIWjQOirwrZCXKQ5DKDMfr-lxV2iqgHMWdX14EKFXyS_tZZ4Xyn9jlpmZagzY/pubhtml).
They can be executed running `python tests/integration/test_gsheet_loader.py`.
