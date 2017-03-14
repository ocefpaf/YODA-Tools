
from DataLoader.Model.Abstract import iInputs
from yodaLoader.YAML.yamlFunctions import YamlFunctions
from odm2api.ODM2.models import Base, setSchema

from odm2api.ODMconnection import dbconnection

class yamlInput(iInputs):
    def __init__(self):
        self.odm2session=None
        pass


    def parse(self, file_path):


        #create connection to temp sqlite db
        #session_factory = dbconnection.createConnection('sqlite', 'D:/DEV/ODM2.sqlite', 2.0)
        session_factory = dbconnection.createConnection('sqlite', ':memory:', 2.0)
        _session = session_factory.getSession()
        _engine = session_factory.engine
        setSchema(_engine)
        Base.metadata.create_all(_engine)



        yaml_load = YamlFunctions(_session, _engine)


        yaml_load.loadFromFile(file_path)
        self.odm2session=_session


    def verify(self):
        pass

    def sendODM2Session(self):
        return self.odm2session
