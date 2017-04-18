from yodatools.converter.Abstract import iOutputs
from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services import *
import logging
import sqlite3

class dbOutput(iOutputs):

    def save(self, session, file_path):
        tables = self.parseObjects()
        data = []
        for t in tables:
            try:
                for o in session.query(t).all():
                    data.append(o)
                    #### WRITE TO DB
            except Exception as e:
                print e

