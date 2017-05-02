from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.models import Base, setSchema

class iInputs(object):
    def __init__(self, file_path, db_conn = None):
        self.create_memory_db()
        if db_conn:
            self.connect_to_db(db_conn)

    def parse(self, file_path, db_conn= None):
        raise NotImplementedError()

    def verify(self):
        raise NotImplementedError()

    def sendODM2Session(self):
        raise NotImplementedError()

    def connect_to_db(self, db_conn):
        self.session_factory = dbconnection.createConnectionFromString(db_conn)
        self._session = self.session_factory.getSession()
        self._engine = self.session_factory.engine
        setSchema(self._engine)

    def create_memory_db(self):
        # create connection to temp sqlite db
        # self.session_factory = dbconnection.createConnection('sqlite', ':memory:', 2.0)
        self.session_factory = dbconnection.createConnection('sqlite', 'myfile.sqlite', 2.0)
        self._session = self.session_factory.getSession()
        self._engine = self.session_factory.engine
        setSchema(self._engine)
        Base.metadata.create_all(self._engine)



