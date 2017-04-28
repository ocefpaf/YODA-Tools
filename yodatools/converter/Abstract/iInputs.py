from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.models import Base, setSchema

class iInputs(object):
    # def __init__(self, file_path, db_conn = None):
    #     self.create_memory_db()
    #     if db_conn:
    #         self.connect_to_db(db_conn)

    def parse(self, file_path, db_conn= None):
        raise NotImplementedError()

    def verify(self):
        raise NotImplementedError()

    def sendODM2Session(self):
        raise NotImplementedError()

    def create_db_conn(self, conn_string=None):
        if conn_string:
            self.session_factory = dbconnection.createConnectionFromString(conn_string)
        else:
            # create connection to temp sqlite db
            self.session_factory = dbconnection.createConnection('sqlite', ':memory:', 2.0)
        # self.session_factory = dbconnection.createConnection('sqlite', 'ODM2_ts_specimen.sqlite', 2.0)
        self._session = self.session_factory.getSession()
        self._engine = self.session_factory.engine
        setSchema(self._engine)
        Base.metadata.create_all(self._engine)

    def get_or_create(self, sess, obj):
        valuedict = obj.__dict__

        #does it already exist?
        instance = sess.query(type(obj)).filter_by().first()
        if instance:
            #if yes, return
            return instance
        else:
            # if no, add to db

            instance = obj
            # sess.merge(instance)
            sess.add(instance)
            sess.flush()
            return instance

