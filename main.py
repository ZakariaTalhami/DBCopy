import argparse
from settings_parser import SettingsParser, TablesParser
from pprint import pprint
import time
from datetime import timedelta

DEFAULT_SETTINGS_FILE = 'settings.json'

# time reporting
SETTINGS_READ_TIME = 0
DB_CONNECT_TIME = 0
COPY_TIME = 0


def report_time():
    print(f'The script performed:')
    print(f'\tRead settings: {timedelta(seconds=SETTINGS_READ_TIME)}')
    print(f'\tConnect to databases: {timedelta(seconds=DB_CONNECT_TIME)}')
    print(f'\tCopy tables: {timedelta(seconds=COPY_TIME)}')
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "-conf",
        help="Requires the json for tables",
        type=argparse.FileType('r'),
        dest="config",
        default=DEFAULT_SETTINGS_FILE
    )
    parser.add_argument(
        "-t",
        "-tableConf",
        required=True,
        help="Requires the json for tables",
        type=argparse.FileType('r'),
        dest="tables"
    )
    parser.add_argument("--skip_constraints", "-sc", action='store_true', dest="skip_constraint")
    args = parser.parse_args()

    skip_constraint = args.skip_constraint

    # load settings
    start = time.time()
    settings = SettingsParser(args.config, is_json=True)
    tables_conf = TablesParser(args.tables, is_json=True)
    SETTINGS_READ_TIME = time.time() - start

    # connect to dbs
    source_db = settings.source_db
    dest_db = settings.dest_db

    start = time.time()
    source_db.connect()
    dest_db.connect()
    DB_CONNECT_TIME = time.time() - start

    if not source_db.conn or not dest_db.conn:
        print("Failed to connect to database!")
        exit(1)

    # pull tables
    pprint(tables_conf.tables)

    start = time.time()
    for table in tables_conf.tables:
        # Load all rows from source table
        res_rows, res_cols = source_db.conn.fetch_table(table)

        # Insert all rows into destination table
        dest_db.conn.insert_table(table, res_rows, res_cols, skip=skip_constraint)

    # close connections
    settings.close()
    COPY_TIME = time.time() - start

    report_time()
    exit(0)
