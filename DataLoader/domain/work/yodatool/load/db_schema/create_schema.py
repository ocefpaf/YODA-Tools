from odm2api.base import *
from sqlalchemy import *
import sqlite3 as sqlite
import psycopg2

class odm2CreateSchema():

    def __init__(self, debug=False):
        self._connection_format = "%s+%s://%s:%s@%s/%s"

    def getconnectionstring(self,engine, address, db=None, user=None, password=None):
        if engine == 'sqlite':
            return engine +':///'+address
        else:
            return self.buildConnDict(engine, address, db, user, password)

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

    def runSQLiteScript(self,scriptfilename,dbfilename):
        connection = None
        cursor = None
        try:
            print "Opening SQLite DB..."
            connection = sqlite.connect(dbfilename)
            cursor = connection.cursor()

            print "Reading SQLite Script..."
            scriptFile = open(scriptfilename, 'r')
            script = scriptFile.read()
            scriptFile.close()

            print "Running Script..."
            cursor.executescript(script)

            connection.commit()
            print "Loading schema successfully committed\n"

        except Exception, e:
            print "Something went wrong:"
            print e
        finally:
            print "Closing DB..."
            cursor.close()
            connection.close()

    def runPostgeSQLScript(self,dbfilename, address, user, password, scriptfilename,):
        connection = None
        cursor = None
        idx = address.find(':')
        if idx > 0:
            host = address[0:idx]
            port = address[idx+1:]
        else:
            host = address
            port = "5432"
        try:
            print "Opening PostgreSQL DB..."
            connection = psycopg2.connect(database=dbfilename,
                                          host=host,
                                          port=port,
                                          user=user,
                                          password=password)
            cursor = connection.cursor()

            print "Reading PostgreSQL Script..."
            scriptFile = open(scriptfilename, 'r')
            script = scriptFile.read()
            scriptFile.close()

            print "Running Script..."
            cursor.execute(script)

            connection.commit()
            print "Loading schema successfully committed\n"

        except Exception, e:
            print "Something went wrong:"
            print e
        finally:
            print "Closing DB..."
            cursor.close()
            connection.close()
