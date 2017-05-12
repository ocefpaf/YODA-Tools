from yodatools.yodaparser import YamlFunctions
from yodatools.converter.Abstract import iInputs


class yamlInput(iInputs):

    def __init__(self, file_path, db_conn=None):
        super(yamlInput, self).__init__(file_path)
        self.odm2session = None


    def parse(self, file_path, db_conn=None):

        type = self.get_type(file_path)
        yaml_load = YamlFunctions(self._session, self._engine)

        yaml_load.loadFromFile(file_path)


        #dont close the session, you wont be able to access it :-)
        #_session.close()

    def verify(self):
        pass

    def get_type(self, filename):
        s= YamlFunctions.extractYaml(self, filename)
        type = s["YODA"]["Profile"]
        if "specimen" in type.lower():
            pass
        else:
            raise Exception("TimeSeries Not yet implemented")


    def sendODM2Session(self):
        return self._session
