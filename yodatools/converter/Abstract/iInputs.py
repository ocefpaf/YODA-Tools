from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.models import Base, setSchema

class iInputs(object):
    def parse(self, file_path):
        raise NotImplementedError()

    def verify(self):
        raise NotImplementedError()

    def sendODM2Session(self):
        raise NotImplementedError()

    def create_memory_db(self):
        # create connection to temp sqlite db
        self.session_factory = dbconnection.createConnection('sqlite', ':memory:', 2.0)
        self._session = self.session_factory.getSession()
        self._engine = self.session_factory.engine
        setSchema(self._engine)
        Base.metadata.create_all(self._engine)