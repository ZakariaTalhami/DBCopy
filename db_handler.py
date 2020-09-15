import mysql.connector


class MysqlConnection:
    """
    Mysql connection handler
    """

    _FETCH_TABLE = "Select * from {}"
    _INSERT_TABLE = "INSERT INTO {table} ({cols}) values ({values})"

    def __init__(self, host, port, username, password, database, as_dict=True):
        """

        :param host : str
            The database's host address
        :param port : str
            The database's host port number
        :param username : str
            The database's username
        :param password : str
            The database's password
        :param database : str
            The database's name
        :param as_dict : bool
            Whether to return query results as dictionary
        """
        try:
            self._cnx = mysql.connector.connect(
                user=username,
                password=password,
                host=host,
                database=database,
                port=port,
            )
            self._cursor = self._cnx.cursor(dictionary=as_dict)
        except mysql.connector.Error as err:
            print(err)
            raise err

    def fetch_table(self, table):
        """
            Fetch all rows from the given table

        :param table : str
            Table name
        :return:
            values : [dict]
                list of rows
            cols : [str]
                list of column names in the table
        """

        result = {}
        cols = []
        try:
            self._cursor.execute(self._FETCH_TABLE.format(table))
            result = [row for row in self._cursor]
            cols = [col for col in self._cursor.column_names]
        except mysql.connector.Error as err:
            print(err)
            raise err

        return result, cols

    def insert_table(self, table, rows, cols, skip=False):
        """
            Insert rows into the given table
        :param table : str
            The name of the table to store the rows
        :param rows : [dict]
            The rows to be stored
        :param cols : [str]
            The names of the columns int the table
        :param skip : bool
            Skip constraints errors
        :return:
        """
        if not rows or not len(rows):
            return

        if not cols:
            cols = rows[0].keys()
        cols_str = ", ".join(cols)

        for row in rows:
            try:
                values_str = self.create_value_string(row.values())
                query = self._INSERT_TABLE.format(
                    table=table, cols=cols_str, values=values_str
                )
                print(query)
                self._cursor.execute(query)
            except mysql.connector.IntegrityError as err:
                if not err.errno == 1062 and not skip:
                    raise err
                print("Duplicate, skipping.")
        self._cnx.commit()

    def create_value_string(self, values):
        values_list = []
        for value in values:
            value_formated = f"'{value}'" if value is not None else "NULL"
            values_list.append(value_formated)

        return ", ".join(values_list)

    def close(self):
        """
        Close the connection and cursor to the database
        """
        self._cursor.close()
        self._cnx.close()


if __name__ == "__main__":
    from pprint import pprint

    con1 = MysqlConnection(
        username="test",
        password="test",
        host="localhost",
        port="3399",
        database="testee",
    )

    con2 = MysqlConnection(
        username="test",
        password="test",
        host="localhost",
        port="3398",
        database="testee",
    )

    res_rows, res_cols = con1.fetch_table("player")
    pprint(res_rows)

    con2.insert_table("player", res_rows, res_cols)

    con1.close()
