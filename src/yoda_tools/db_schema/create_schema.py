import sys
sys.path.append('../ODM2PythonAPI')

from sqlalchemy import *
from src.api.base import modelBase

class odm2CreateSchema():

    def __init__(self, debug=False):
        self._connection_format = "%s+%s://%s:%s@%s/%s"

    @classmethod
    def createDBSchema(self, engine, address, db=None, user=None, password=None):

        if engine == 'sqlite':
            connection_string = engine +':///'+address
        else:
            connection_string = self.buildConnDict(engine, address, db, user, password)

        if 'sqlite' in connection_string:
            engine = create_engine(connection_string, encoding='utf-8', echo=False)
        if 'mssql' in connection_string:
            engine = create_engine(connection_string, encoding='utf-8', echo=False, pool_recycle=3600, pool_timeout=5, pool_size=20, max_overflow=0)
        elif 'postgresql' in connection_string or 'mysql' in connection_string:
            engine = create_engine(connection_string, encoding='utf-8', echo=False, pool_recycle=3600, pool_timeout=5, pool_size=20, max_overflow=0)

        modelBase.metadata.create_all(engine)

    def buildConnDict(self, engine, address, db, user, password):
        line_dict = {}
        line_dict['engine'] = engine
        line_dict['user'] = user
        line_dict['password'] = password
        line_dict['address'] = address
        line_dict['db'] = db
        return self.__buildConnectionString(line_dict)

    def __buildConnectionString(self, conn_dict):
        driver = ""
        if conn_dict['engine'] == 'mssql':
            driver = "pyodbc"
        elif conn_dict['engine'] == 'mysql':
            driver = "pymysql"
        elif conn_dict['engine'] == 'postgresql':
            driver = "psycopg2"
        else:
            driver = "None"

        conn_string = self._connection_format % (
            conn_dict['engine'], driver, conn_dict['user'], conn_dict['password'], conn_dict['address'],
            conn_dict['db'])
        # print conn_string
        return conn_string
