from yodatools.converter.Abstract import iInputs
from yodatools.yodaparser import YamlFunctions


class yamlInput(iInputs):

    def __init__(self):
        super(yamlInput, self).__init__()
        self.odm2session = None

    def parse(self, file_path):
        yaml_load = YamlFunctions(self._session, self._engine)
        # FIXME: yoda_type is assigned but never used.
        # yoda_type = self.get_type(yaml_load, file_path )
        yaml_load.loadFromFile(file_path)

        # Don't close the session, you wont be able to access it :-)
        # _session.close()

    def verify(self):
        pass

    def get_type(self, yaml_load, file_path):
        # FIXME: yoda_type and s are assigned but never used.
        # s = yaml_load.extractYaml(file_path)
        # yoda_type = s['YODA'][0]['Profile']
        if 'specimen' in type.lower():
            pass
        else:
            raise Exception('TimeSeries Not yet implemented')

    def sendODM2Session(self):
        return self._session
