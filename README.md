# tap-gsheets
This is a [Singer](https://singer.io) tap that extracts data from Google Spreadshits. It produces JSON-formatted data following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

# Configuration
The tap uses the Google API underneath for accessing sheets data, so you need to
[create some credentials accordingly](https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2).

Once you have your credentials, you need to put them in the `gsheets_api` key in the configuration file so they are picked up by the tap. With another key `sheet_name` one select the spreadsheet to be extracted.

The tap supports configuration files in JSON as much as in [HOCON](https://github.com/chimpler/pyhocon) format. Use a `.json` extension for JSON format and a `.conf` extension for HOCON format.

# Example
Tapping onto a Google sheet named `Investor Loans` can be achieved with a HOCO config file such as
```hocon
{ # config.conf
  sheet_name = "Investor Loans",
  gsheets_api {
    type = "service_account",
    project_id = "pmt-spv",
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
```bash
tap-gsheets -c config.conf
# {"type": "RECORD", "stream": "Investor Loans", "record": {"id": 11, "start_date": "2018-08-22", "end_date": "2020-04-17", "investor": "Banking Corp", "amount": 20000000, "interest_rate": 0.20, "add_to_capital": "FALSE", "user_id": "some_user", "created_at": "2018-08-22 11:00:40", "updated_at": "2018-08-22 11:00:40"}}
```

# Run
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
