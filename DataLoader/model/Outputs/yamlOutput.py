
from DataLoader.model.Abstract import iOutputs
from yodaloader.YAML.yamlFunctions import YamlFunctions


class yamlOutput(iOutputs):

    def save(self, session, file_path):
        tables = self.parseObjects()
        print file_path


    def accept(self):
        raise NotImplementedError()

