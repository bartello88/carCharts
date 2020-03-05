import psycopg2
import pyodbc
import os
import yaml
import utils.backoff
import utils.config


def connect(connection_config, max_retries=1):
    """connects to Postgresql database, number of connection retries can be set, uses tupperware as config input"""
    if hasattr(connection_config, '_asdict'):
        connection_config = connection_config._asdict()

    def try_connect():
        try:
            return psycopg2.connect(**connection_config)
        except psycopg2.DatabaseError as e:
            raise utils.backoff.RetryableException from e

    return utils.backoff.exponential_backoff(try_connect, max_retries, 1)


def connect_to_db(dbname, configuration=None):
    """distincts database type between postgresql and mssql"""
    if configuration is None:
        if os.path.exists("../db_connection_config.yml"):
            configuration = _load_config_file("../db_connection_config.yml")
        elif os.path.exists("./db_connection_config.yml"):
            configuration = _load_config_file("./db_connection_config.yml")
        else:
            raise NotImplementedError("Configuration file is missing.")
    else:
        if os.path.exists(configuration):
            configuration = _load_config_file(configuration)
        else:
            raise NotImplementedError("Configuration file is missing.")

    db_config = configuration.get(dbname)
    if db_config.get("type") == "postgres":
        return _create_postgres_db_connection(db_config)
    elif db_config.get("type") == "mssql":
        return _create_mssql_db_connection(db_config)
    else:
        raise NotImplementedError("Db connection not implemented.")


def select_single_row(connection, query, params):
    cursor = connection.cursor()
    cursor.execute(query, params)
    return cursor.fetchone()


def select_single(connection, query, params):
    row = select_single_row(connection, query, params)
    if row is None:
        return None
    return row[0]


def select_all(connection, query, params):
    cursor = connection.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()


def _load_config_file(path_to_config_file=None):
    with open(path_to_config_file) as configfile:
        config = yaml.load(configfile, Loader=yaml.SafeLoader)
    return config


def _create_postgres_db_connection(config):
    return PostgresDbConnection(host=config.get("host"),
                                port=config.get("port"),
                                user=config.get("user"),
                                password=config.get("password"),
                                database=config.get("database"),
                                schema=config.get("schema")
                                )


def _create_mssql_db_connection(config):
    return MssqlDbConnection(host=config.get("host"),
                             user=config.get("user"),
                             password=config.get("password"),
                             database=config.get("database")
                             )


class DbConnection(object):
    host = None
    port = None
    user = None
    password = None
    database = None
    schema = None
    conn = None

    def __init__(self, host=None, port=0, user=None, password=None,
                 database=None, schema=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.schema = schema

    def _connect(self):
        pass

    def execute_query(self, query=None, params=None):
        """
        Executes query passed as parameter. May be aditionally parametrized
        :param query:  Query to run
        :param params: Optional parameters
        :return: <TUPLE> ( <TUPLE> result_rows , <LIST> column_names ) or TRUE for update/insert.
                RAISES SQLExecutionException
        """
        if self.conn is None:
            self._connect()
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if "INSERT " not in query.upper() and "UPDATE " not in query.upper():
                # fetch list of columnnames from output
                columnnames = list(map(lambda x: x[0], cursor.description))
            else:
                self.conn.commit()
                return True
            result = cursor.fetchall()
            return result, columnnames
        except Exception as e:
            # print(traceback.format_exc())
            raise Exception("error executing query: {0}".format(e))

    def __enter__(self):
        if self._connect():
            # print("Established connection to {0}.".format(self.database))
            return self
        else:
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            self.conn.close()


class PostgresDbConnection(DbConnection):

    def __init__(self, host=None, port=0, user=None, password=None,
                 database=None, schema=None):
        super(PostgresDbConnection, self).__init__(host=host, port=port, user=user, password=password,
                                                   database=database, schema=schema)

    def _connect(self):

        connection_config = utils.config.load_dict(
            {"host": self.host, "port": self.port, "user": self.user, "password": self.password,
             "database": self.database})

        try:
            self.conn = connect(connection_config, max_retries=2)
            return True
        except Exception as e:
            raise Exception(e)


class MssqlDbConnection(DbConnection):

    def __init__(self, host=None, user=None, password=None, database=None):
        super(MssqlDbConnection, self).__init__(host=host, password=password, user=user, database=database)

    def _connect(self):
        try:
            self.conn = pyodbc.connect(DRIVER='{SQL Server}', host=self.host, database=self.database, user=self.user,
                                       password=self.password)
            return True
        except Exception as e:
            raise Exception(e)
