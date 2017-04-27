from yodatools.converter.Abstract import iOutputs
from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services import *
import logging
import sqlite3

class dbOutput(iOutputs):

    def __init__(self, file_path, connection_string = None):
        if connection_string:
            self.connect_to_db(connection_string)

    def connect_to_db(self, connection_string):
        self.session_factory_out = dbconnection.createConnectionFromString(connection_string)
        self._session_out = self.session_factory_out.getSession()
        self._engine = self.session_factory_out.engine
        return self._session_out

    def save(self, session, file_path, connection_string):
        tables = self.parseObjects(session)
        session_out = self.connect_to_db(connection_string)
        #data = []

        for t in tables:
            try:
                for o in session.query(t).all():
                    #data.append(o)
                    session_out.add(o)

            except Exception as e:
                print e

