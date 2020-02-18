import json
from db_handler import MysqlConnection
import mysql.connector


class DatabaseConf:

    def __init__(self, database):
        if not database:
            raise ValueError("Bad database configuration parsed")
        self._database = database
        self._conn = None

    @property
    def host(self):
        return self._database.get('host')

    @property
    def db(self):
        return self._database.get('name')

    @property
    def username(self):
        return self._database.get('username')

    @property
    def password(self):
        return self._database.get('password')

    @property
    def port(self):
        return self._database.get('port')

    @property
    def conn(self):
        return self._conn

    def connect(self):
        cnx = None
        try:
            cnx = MysqlConnection(
                username=self.username,
                password=self.password,
                database=self.db,
                host=self.host,
                port=self.port
            )

            self._conn = cnx

        except mysql.connector.Error:
            print(f'Failed to connect to database: {self.db}@{self.host}:{self.port} with "{self.username}" username')
        return cnx

    def disconnect(self):
        if self._conn:
            self._conn.close()


class ConfigParser:
    def __init__(self, file, is_json=False, close=True):
        open_file = file
        if type(file) == str:
            # try/except
            open_file = open(file, 'r')

        self._file = open_file
        self._lines = open_file.readlines()
        self._str = "".join(self._lines).replace("\n", '')
        self._json = None
        if is_json:
            self._json = json.loads(self._str)
        self._extract()

        if close:
            self.close()

    def _extract(self):
        raise NotImplementedError("Extract is not implemented in parent class")

    def close(self):
        self._file.close()


class SettingsParser(ConfigParser):

    def _extract(self):
        self._from_db = DatabaseConf(self._json.get("from_db"))
        self._to_db = DatabaseConf(self._json.get("to_db"))

    @property
    def source_db(self):
        return self._from_db

    @property
    def dest_db(self):
        return self._to_db

    def close(self):
        super(SettingsParser, self).close()
        self.source_db.disconnect()
        self.dest_db.disconnect()


class TablesParser(ConfigParser):

    def _extract(self):
        self._tables = self._json.get('tables')

    @property
    def tables(self):
        return self._tables
