from yodatools.yodaparser import YamlFunctions
from yodatools.converter.Abstract import iInputs


class yamlInput(iInputs):

    def __init__(self):
        super(yamlInput, self).__init__()
        self.odm2session = None


    def parse(self, file_path):


        yaml_load = YamlFunctions(self._session, self._engine)
        type = self.get_type(yaml_load, file_path )
        yaml_load.loadFromFile(file_path)


        #dont close the session, you wont be able to access it :-)
        #_session.close()

    def verify(self):
        pass

    def get_type(self, yaml_load, file_path):
        s= yaml_load.extractYaml(file_path)
        type = s["YODA"][0]["Profile"]
        if "specimen" in type.lower():
            pass
        else:
            raise Exception("TimeSeries Not yet implemented")


    def sendODM2Session(self):
        return self._session
