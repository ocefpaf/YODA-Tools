from odm2api.ODM2.models import Base, setSchema
from odm2api.ODMconnection import dbconnection


class iInputs(object):
    def __init__(self):
        self.create_memory_db()

    def parse(self, file_path):
        raise NotImplementedError()

    def verify(self):
        raise NotImplementedError()

    def sendODM2Session(self):
        raise NotImplementedError()

    def create_memory_db(self):

        # create connection to temp sqlite db
        self.session_factory = dbconnection.createConnection('sqlite', ':memory:', 2.0)  # noqa
        # self.session_factory = dbconnection.createConnection('sqlite', 'ODM2_ts_specimen.sqlite', 2.0)  # noqa
        self._session = self.session_factory.getSession()
        self._engine = self.session_factory.engine
        setSchema(self._engine)
        Base.metadata.create_all(self._engine)
