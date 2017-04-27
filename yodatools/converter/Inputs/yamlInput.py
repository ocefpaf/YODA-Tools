from yodatools.yodaparser import YamlFunctions
from yodatools.converter.Abstract import iInputs


class yamlInput(iInputs):
    # def __init__(self, file_path, db_conn = None):
    #     super(yamlInput, self).__init__()
    #     self.odm2session=None
    #     pass

    # def create_memory_db(self):
    #     self.session_factory =
    def parse(self, file_path, db_conn = None):
        self.create_memory_db()
        yaml_load = YamlFunctions(self._session, self._engine)

        yaml_load.loadFromFile(file_path)

        self.odm2session = self._session
        #dont close the session, you wont be able to access it :-)
        #_session.close()

    def verify(self):
        pass

    def sendODM2Session(self):
        return self._session
